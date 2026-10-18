"""Local stdio JSON-RPC MCP server exposing the six study tools.

Implements the minimal MCP surface over the standard library: `initialize`,
`tools/list`, and `tools/call`. One JSON object per line on stdin/stdout. No
network listener is opened.
"""

from __future__ import annotations

import json
import sys
from typing import Any, TextIO

from study_core.bootstrap import build_runtime
from study_core.settings import Settings

from study_mcp.handlers import TOOL_NAMES, ToolRouter

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "studyai-study-core"
SERVER_VERSION = "0.1.0"

# Minimal JSON Schemas advertised for each tool.
_TOOL_SCHEMAS: dict[str, dict[str, Any]] = {
    "start_session": {
        "type": "object",
        "required": ["learner_id", "mode", "request_id"],
        "additionalProperties": False,
        "properties": {
            "learner_id": {"type": "string"},
            "mode": {"type": "string", "enum": ["grill", "review"]},
            "objective_filter": {"type": "array", "items": {"type": "string"}},
            "request_id": {"type": "string"},
        },
    },
    "next_question": {
        "type": "object",
        "required": ["session_id", "request_id"],
        "additionalProperties": False,
        "properties": {
            "session_id": {"type": "string"},
            "request_id": {"type": "string"},
        },
    },
    "grade_and_record": {
        "type": "object",
        "required": ["session_id", "question_id", "confidence", "elapsed_seconds", "event_id"],
        "additionalProperties": False,
        "properties": {
            "session_id": {"type": "string"},
            "question_id": {"type": "string"},
            "selected_option_ids": {"type": "array", "items": {"type": "string"}},
            "confidence": {"type": "integer", "minimum": 0, "maximum": 100},
            "elapsed_seconds": {"type": "number", "minimum": 0},
            "event_id": {"type": "string"},
        },
    },
    "get_due_reviews": {
        "type": "object",
        "required": ["learner_id"],
        "additionalProperties": False,
        "properties": {
            "learner_id": {"type": "string"},
            "objective_filter": {"type": "array", "items": {"type": "string"}},
        },
    },
    "get_progress": {
        "type": "object",
        "required": ["learner_id"],
        "additionalProperties": False,
        "properties": {"learner_id": {"type": "string"}},
    },
    "search_local_material": {
        "type": "object",
        "required": ["query"],
        "additionalProperties": False,
        "properties": {
            "query": {"type": "string"},
            "objective_filter": {"type": "array", "items": {"type": "string"}},
            "limit": {"type": "integer", "minimum": 1},
            "offset": {"type": "integer", "minimum": 0},
        },
    },
}


def _tools_list() -> dict[str, Any]:
    return {
        "tools": [
            {
                "name": name,
                "description": f"studyAI {name} use case.",
                "inputSchema": _TOOL_SCHEMAS[name],
            }
            for name in TOOL_NAMES
        ]
    }


def handle_request(router: ToolRouter, request: dict[str, Any]) -> dict[str, Any] | None:
    """Handle one JSON-RPC request and return a response (or None for notifications)."""
    method = request.get("method")
    request_id = request.get("id")
    if method == "initialize":
        result: dict[str, Any] = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        }
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": _tools_list()}
    if method == "tools/call":
        params = request.get("params") or {}
        tool = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        outcome = router.call(tool, arguments)
        payload = json.dumps(outcome, sort_keys=True)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{"type": "text", "text": payload}],
                "isError": "error" in outcome,
            },
        }
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


def serve(router: ToolRouter, stdin: TextIO, stdout: TextIO) -> None:
    """Run the stdio request loop until EOF."""
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = handle_request(router, request)
        if response is not None:
            stdout.write(json.dumps(response) + "\n")
            stdout.flush()


def main() -> int:
    """CLI entry point for the local stdio MCP server."""
    settings = Settings.from_env()
    from content.aip_c01 import BLUEPRINT_VERSION

    runtime = build_runtime(settings, blueprint_version=BLUEPRINT_VERSION)
    router = ToolRouter(runtime.service)
    serve(router, sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
