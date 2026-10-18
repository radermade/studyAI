"""Tests for the MCP tool router, allowlist, and error mapping."""

from __future__ import annotations

from study_core.service import StudyService
from study_mcp.handlers import TOOL_NAMES, ToolRouter
from study_mcp.server import handle_request


def test_tool_allowlist_is_exactly_six() -> None:
    assert set(TOOL_NAMES) == {
        "start_session",
        "next_question",
        "grade_and_record",
        "get_due_reviews",
        "get_progress",
        "search_local_material",
    }


def test_unknown_tool_is_validation_error(service: StudyService) -> None:
    router = ToolRouter(service)
    out = router.call("drop_table", {})
    assert out["error"]["category"] == "validation"


def test_no_raw_sql_or_shell_tool_exposed(service: StudyService) -> None:
    router = ToolRouter(service)
    for forbidden in ("execute_sql", "run_shell", "read_file", "aws_call"):
        out = router.call(forbidden, {})
        assert "error" in out


def test_start_session_through_router(service: StudyService) -> None:
    router = ToolRouter(service)
    out = router.call(
        "start_session",
        {"learner_id": "L1", "mode": "grill", "request_id": "r1"},
    )
    assert "result" in out
    assert out["result"]["state"] == "active"


def test_invalid_payload_maps_to_validation(service: StudyService) -> None:
    router = ToolRouter(service)
    out = router.call("start_session", {"learner_id": "L1"})  # missing fields
    assert out["error"]["category"] == "validation"


def test_full_grill_cycle_through_router(service: StudyService) -> None:
    router = ToolRouter(service)
    start = router.call("start_session", {"learner_id": "L1", "mode": "grill", "request_id": "r1"})
    session_id = start["result"]["session_id"]
    served = router.call("next_question", {"session_id": session_id, "request_id": "nq1"})
    question_id = served["result"]["question_id"]
    assert "correct_option_ids" not in served["result"]
    graded = router.call(
        "grade_and_record",
        {
            "session_id": session_id,
            "question_id": question_id,
            "selected_option_ids": ["a"],
            "confidence": 70,
            "elapsed_seconds": 15.0,
            "event_id": "e1",
        },
    )
    assert graded["result"]["outcome"] == "correct"


def test_initialize_and_tools_list(service: StudyService) -> None:
    router = ToolRouter(service)
    init = handle_request(router, {"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert init is not None
    assert init["result"]["serverInfo"]["name"] == "studyai-study-core"
    listed = handle_request(router, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    assert listed is not None
    names = {tool["name"] for tool in listed["result"]["tools"]}
    assert names == set(TOOL_NAMES)
