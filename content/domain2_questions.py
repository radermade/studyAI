"""Authored Domain 2 (AIP-C01) scenario questions with answers and explanations.

Original scenario-style questions grounded in the AWS exam guide. No proprietary
exam content is reproduced.
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    {
        "question_id": "d2-agent-db-api-report-state",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An agentic solution must query an internal order database, call "
            "external shipping APIs, generate PDF reports, recover from transient "
            "tool failures, and remember prior turns across a long conversation. "
            "Which TWO AWS building blocks most directly deliver this with the "
            "least custom orchestration code? Select TWO."
        ),
        "scenario_constraint": "Tool invocation plus durable conversation state with minimal custom code.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            (
                "a",
                "Amazon Bedrock Agents with action groups for the database, APIs, and report tasks.",
            ),
            ("b", "A DynamoDB table keyed by session ID for conversation and task state."),
            ("c", "Amazon Comprehend to classify the user's intent on every turn."),
            ("d", "Amazon Kinesis Data Streams to buffer each conversational message."),
            ("e", "Amazon Rekognition to inspect the generated PDF reports."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Bedrock Agents with action groups expose the database, shipping, and "
            "report tools to a reasoning loop, and DynamoDB gives low-latency "
            "durable session state keyed by conversation. Comprehend, Kinesis, "
            "and Rekognition solve unrelated problems here."
        ),
        "rationales": {
            "a": (
                True,
                "Action groups wire the agent to the DB, APIs, and report tools under one reasoning loop.",
            ),
            "b": (
                True,
                "DynamoDB keyed by session ID holds durable per-conversation state cheaply.",
            ),
            "c": (
                False,
                "Intent classification is not the stated need and adds an extra model hop.",
            ),
            "d": (False, "A streaming buffer does not provide addressable conversation state."),
            "e": (False, "Image analysis has no role in text-driven report generation."),
        },
    },
    {
        "question_id": "d2-tool-schema-validation",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A tool-using agent occasionally calls an internal API with malformed "
            "arguments, causing downstream 500s. Which TWO controls block bad "
            "calls before they leave the agent? Select TWO."
        ),
        "scenario_constraint": "Stop malformed tool calls at the agent boundary.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Add a sentence to the system prompt asking the model to be careful."),
            ("b", "Define a typed tool schema and validate arguments before each invocation."),
            ("c", "Retry the tool call until one eventually succeeds."),
            ("d", "Log the failures and let the downstream API reject bad input."),
            ("e", "Reject calls whose arguments fail a boundary validation check."),
        ],
        "correct_option_ids": ["b", "e"],
        "explanation": (
            "A typed tool schema plus a boundary validation check reject bad "
            "calls before they reach downstream systems. Prompt pleading is not "
            "enforced, blind retries amplify the fault, and downstream rejection "
            "means the bad call already escaped."
        ),
        "rationales": {
            "a": (False, "A prompt request is advisory, not an enforced validation gate."),
            "b": (True, "Schema validation is the enforced boundary that rejects malformed calls."),
            "c": (False, "Retrying malformed arguments repeats the error rather than fixing it."),
            "d": (
                False,
                "Downstream rejection fires after the bad call has already left the agent.",
            ),
            "e": (True, "A boundary validation check stops invalid arguments before dispatch."),
        },
    },
    {
        "question_id": "d2-react-loop-step-limit",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A ReAct-style Bedrock agent sometimes loops between two tools and "
            "never returns an answer, running up cost. Which TWO safeguards "
            "guarantee the loop terminates within budget? Select TWO."
        ),
        "scenario_constraint": "Guarantee the reasoning loop terminates within a bounded budget.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Lower the model temperature so it stops repeating itself."),
            ("b", "Remove one of the two tools so it cannot alternate."),
            ("c", "Enforce a maximum step/iteration budget that ends the loop."),
            ("d", "Increase the context window so more history fits."),
            ("e", "Add a per-request wall-clock timeout that aborts long runs."),
        ],
        "correct_option_ids": ["c", "e"],
        "explanation": (
            "A hard step budget and a wall-clock timeout each guarantee "
            "termination and bound cost regardless of model behavior. Temperature "
            "is probabilistic, dropping a needed tool breaks the task, and a "
            "larger context window does nothing to stop a loop."
        ),
        "rationales": {
            "a": (False, "Temperature only shifts probabilities; it cannot guarantee termination."),
            "b": (False, "Removing a required tool breaks legitimate workflows that need it."),
            "c": (True, "A bounded step budget deterministically ends the loop and caps cost."),
            "d": (False, "A bigger context window lets the loop run longer, not stop."),
            "e": (True, "A wall-clock timeout bounds total runtime and forces termination."),
        },
    },
    {
        "question_id": "d2-least-privilege-action-group",
        "objective_ids": ["AIP-2.1", "AIP-3.1"],
        "prompt": (
            "An agent invokes several AWS actions through action groups. Security "
            "review requires that a compromised agent cannot exceed its intended "
            "scope. Which design BEST enforces containment?"
        ),
        "scenario_constraint": "Limit blast radius if the agent is compromised.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Grant the agent's execution role a scoped IAM policy limited to the exact actions and resources.",
            ),
            ("b", "Give the agent a broad administrator role and audit CloudTrail afterward."),
            ("c", "Embed long-lived access keys in the Lambda handling the action group."),
            ("d", "Rely on the system prompt to tell the agent which actions are allowed."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A least-privilege IAM policy on the execution role is the enforced "
            "boundary that caps what the agent can ever do. Broad roles plus "
            "after-the-fact audit, embedded keys, and prompt-level rules do not "
            "actually constrain a misbehaving agent."
        ),
        "rationales": {
            "a": (True, "A scoped execution-role policy is the enforced ceiling on agent actions."),
            "b": (False, "Auditing after the fact does not prevent an over-broad action."),
            "c": (False, "Long-lived embedded keys widen exposure and bypass role scoping."),
            "d": (False, "Prompt text is advisory and cannot stop an action IAM allows."),
        },
    },
    {
        "question_id": "d2-human-in-the-loop-approval",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An agent can issue customer refunds via a tool. The business "
            "requires that refunds above $500 get human approval before they "
            "execute, while smaller refunds proceed automatically. Which design "
            "meets this with the LEAST operational overhead?"
        ),
        "scenario_constraint": "Gate only high-value actions on human approval without blocking the rest.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Have a human review every single refund the agent proposes."),
            (
                "b",
                "Insert a human-in-the-loop approval step that triggers only when the refund exceeds the threshold.",
            ),
            ("c", "Let the agent self-approve but email a summary to a manager daily."),
            ("d", "Lower the model temperature so it refunds more conservatively."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "A conditional human-in-the-loop gate on the high-value branch "
            "preserves automation for small refunds while enforcing review where "
            "it matters. Reviewing everything is wasteful, daily summaries are "
            "after-the-fact, and temperature does not enforce a dollar threshold."
        ),
        "rationales": {
            "a": (False, "Reviewing every refund removes the automation benefit entirely."),
            "b": (True, "A threshold-triggered approval gate blocks only the risky actions."),
            "c": (
                False,
                "A daily summary cannot stop an incorrect large refund before it executes.",
            ),
            "d": (False, "Temperature does not implement a deterministic approval threshold."),
        },
    },
    {
        "question_id": "d2-mcp-tool-exposure",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "Your team wants one agent to reuse the same catalog of internal "
            "tools that several other applications already expose over a "
            "standardized protocol, without re-implementing adapters per client. "
            "Which approach fits BEST?"
        ),
        "scenario_constraint": "Reuse a shared, standardized tool catalog across multiple clients.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Hard-code each tool's HTTP call directly inside the agent."),
            ("b", "Copy the tool code into every application that needs it."),
            (
                "c",
                "Expose the tools through a Model Context Protocol server the agent connects to as a client.",
            ),
            ("d", "Store the tool definitions as prompt text and let the model call them."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "An MCP server publishes tools over a standard protocol so any "
            "MCP-aware client, including the agent, consumes them uniformly. "
            "Hard-coding and copying duplicate adapters, and prompt-only "
            "definitions have no execution layer."
        ),
        "rationales": {
            "a": (False, "Hard-coded calls defeat reuse and must be rewritten per client."),
            "b": (False, "Copying tool code creates duplicated, drift-prone adapters."),
            "c": (True, "An MCP server standardizes tool exposure across all MCP clients."),
            "d": (False, "Prompt text describes tools but provides no shared execution path."),
        },
    },
    {
        "question_id": "d2-agentcore-memory",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "You are building on Amazon Bedrock AgentCore and need managed short- "
            "and long-term memory for an agent so it recalls prior sessions "
            "without you operating a custom store. Which AgentCore capability "
            "addresses this directly?"
        ),
        "scenario_constraint": "Managed cross-session memory without self-operated storage.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AgentCore Code Interpreter."),
            ("b", "AgentCore Gateway."),
            ("c", "AgentCore Observability."),
            ("d", "AgentCore Memory."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "AgentCore Memory is the managed capability for retaining agent "
            "context across turns and sessions. Code Interpreter runs code, "
            "Gateway exposes tools/APIs, and Observability handles tracing."
        ),
        "rationales": {
            "a": (False, "Code Interpreter executes code, not conversation memory."),
            "b": (False, "Gateway brokers tools and APIs, not memory storage."),
            "c": (False, "Observability provides traces and metrics, not memory."),
            "d": (True, "Memory is the AgentCore service for managed agent recall."),
        },
    },
    {
        "question_id": "d2-agentcore-gateway-vs-runtime",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An AgentCore-based agent must call a dozen existing REST APIs as "
            "tools, with auth and schema translation handled for it. Which "
            "AgentCore component is designed for turning those APIs into agent "
            "tools?"
        ),
        "scenario_constraint": "Convert existing REST APIs into governed agent tools.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AgentCore Runtime."),
            ("b", "AgentCore Identity."),
            ("c", "AgentCore Gateway."),
            ("d", "AgentCore Memory."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "AgentCore Gateway turns APIs and services into agent-callable tools "
            "with auth and schema handling. Runtime hosts the agent, Identity "
            "manages access, and Memory stores context."
        ),
        "rationales": {
            "a": (False, "Runtime is the managed execution environment, not the tool broker."),
            "b": (False, "Identity governs access and credentials, not API-to-tool conversion."),
            "c": (True, "Gateway converts APIs into governed agent tools."),
            "d": (False, "Memory stores context and has no tool-brokering role."),
        },
    },
    {
        "question_id": "d2-session-state-dynamodb",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A custom agent runs across stateless Lambda invocations and must "
            "resume each user's multi-turn conversation exactly where it left off "
            "at low read latency. Which TWO stores are appropriate for durable "
            "per-session state? Select TWO."
        ),
        "scenario_constraint": "Low-latency durable per-session state across stateless compute.",
        "difficulty": "easy",
        "question_format": "multiple_response",
        "options": [
            ("a", "A DynamoDB table partitioned by session ID."),
            ("b", "A managed agent memory service (such as AgentCore Memory)."),
            ("c", "A module-level Python dictionary in the Lambda."),
            ("d", "An Amazon S3 object rewritten on every turn."),
            ("e", "The model's context window only."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "DynamoDB keyed by session ID and a managed agent memory service both "
            "provide durable state that survives cold starts. In-memory dicts "
            "vanish, per-turn S3 rewrites are slow and race-prone, and the "
            "context window is lost between invocations."
        ),
        "rationales": {
            "a": (True, "DynamoDB by session ID is durable and low-latency."),
            "b": (True, "A managed memory service persists durable per-session context."),
            "c": (False, "Module memory is per-container and lost on cold starts."),
            "d": (False, "Rewriting an S3 object per turn is slow and conflict-prone."),
            "e": (False, "The context window does not persist across stateless invocations."),
        },
    },
    {
        "question_id": "d2-multi-agent-orchestration",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A workflow needs a planner agent to delegate subtasks to a research "
            "agent and a coding agent, then merge their outputs. The team wants a "
            "framework purpose-built for coordinating multiple collaborating "
            "agents on AWS. Which choice fits BEST?"
        ),
        "scenario_constraint": "Coordinate multiple specialized agents under one orchestrator.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A single prompt that lists all three roles for one model."),
            ("b", "AWS Agent Squad for multi-agent orchestration."),
            ("c", "Amazon SQS fan-out with no coordinating logic."),
            ("d", "Amazon Athena to query the agents' outputs."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "AWS Agent Squad is built to route and coordinate multiple "
            "specialized agents. A single mega-prompt loses role isolation, SQS "
            "fan-out lacks orchestration logic, and Athena is an analytics query "
            "engine."
        ),
        "rationales": {
            "a": (False, "One prompt collapses the roles and loses delegation control."),
            "b": (True, "Agent Squad orchestrates collaboration among multiple agents."),
            "c": (False, "Raw SQS fan-out has no planner or merge coordination."),
            "d": (False, "Athena queries data; it does not orchestrate agents."),
        },
    },
    {
        "question_id": "d2-strands-agents-choice",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A Python team wants a lightweight, code-first open-source SDK to "
            "define a single agent's model, tools, and prompt, deployable to AWS, "
            "without adopting a heavy orchestration platform. Which option best "
            "matches?"
        ),
        "scenario_constraint": "Lightweight code-first single-agent SDK on AWS.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AWS Strands Agents SDK."),
            ("b", "Amazon Bedrock Guardrails."),
            ("c", "AWS Step Functions Standard workflows."),
            ("d", "Amazon SageMaker Ground Truth."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Strands Agents is a code-first SDK for defining an agent's model, "
            "tools, and prompt loop. Guardrails filter content, Step Functions is "
            "a workflow engine, and Ground Truth is for labeling."
        ),
        "rationales": {
            "a": (True, "Strands is the lightweight code-first agent SDK described."),
            "b": (False, "Guardrails enforce safety policy, not agent definition."),
            "c": (False, "Step Functions orchestrates workflows, not agent reasoning loops."),
            "d": (False, "Ground Truth is a data-labeling service."),
        },
    },
    {
        "question_id": "d2-function-calling-vs-freeform",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A model should return parameters an application can execute "
            "deterministically against a weather tool, rather than prose the app "
            "must parse. Which model capability enforces a machine-readable call?"
        ),
        "scenario_constraint": "Produce structured, directly-executable tool arguments.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Streaming token output."),
            ("b", "A higher temperature setting."),
            ("c", "A larger max-tokens limit."),
            ("d", "Function calling with a declared tool schema."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Function calling with a declared schema makes the model emit "
            "structured arguments the app can execute without brittle parsing. "
            "Streaming, temperature, and max-tokens affect delivery or length, "
            "not structure."
        ),
        "rationales": {
            "a": (False, "Streaming changes delivery timing, not output structure."),
            "b": (False, "Higher temperature increases variability, hurting structure."),
            "c": (False, "A larger token limit allows longer output, not structured calls."),
            "d": (True, "Function calling yields schema-conformant executable arguments."),
        },
    },
    {
        "question_id": "d2-agent-cost-time-limits",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An autonomous agent occasionally fans out dozens of tool calls on a "
            "single request, spiking cost and latency unpredictably. You must cap "
            "per-request resource use. Which TWO controls directly bound it? "
            "Select TWO."
        ),
        "scenario_constraint": "Cap per-request cost and wall-clock time deterministically.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "A maximum number of tool calls (steps) per request."),
            ("b", "A per-request wall-clock timeout that aborts long runs."),
            ("c", "Switching the model to a larger context window."),
            ("d", "Raising the account's Bedrock on-demand quota."),
            ("e", "Increasing the agent's temperature for faster answers."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "A step cap and a wall-clock timeout are the direct, deterministic "
            "bounds on per-request work. A bigger context window, a higher quota, "
            "and temperature changes do not limit fan-out or runtime."
        ),
        "rationales": {
            "a": (True, "A step cap bounds the number of billable tool invocations."),
            "b": (True, "A wall-clock timeout bounds total latency per request."),
            "c": (False, "A larger context window does not limit tool fan-out."),
            "d": (False, "Raising quotas permits more usage rather than capping it."),
            "e": (False, "Temperature affects randomness, not resource consumption."),
        },
    },
    {
        "question_id": "d2-agent-idempotent-tool",
        "objective_ids": ["AIP-2.1", "AIP-2.4"],
        "prompt": (
            "An agent retries a 'create invoice' tool after a timeout and "
            "sometimes creates duplicate invoices. You must make retries safe. "
            "What is the MOST reliable fix?"
        ),
        "scenario_constraint": "Make a mutating tool safe to retry.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Instruct the agent in the prompt not to retry."),
            (
                "b",
                "Have the agent pass a client-generated idempotency key the tool deduplicates on.",
            ),
            ("c", "Increase the tool's timeout so retries are rarer."),
            ("d", "Delete duplicate invoices in a nightly cleanup job."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "A caller-supplied idempotency key lets the tool collapse repeated "
            "requests to one invoice regardless of retries. Prompt instructions "
            "are not enforced, longer timeouts only reduce frequency, and nightly "
            "cleanup is a lossy afterthought."
        ),
        "rationales": {
            "a": (False, "A prompt instruction cannot reliably prevent retries."),
            "b": (True, "An idempotency key makes repeated creates resolve to one record."),
            "c": (False, "A longer timeout reduces but does not eliminate duplicates."),
            "d": (False, "Nightly cleanup is reactive and risks removing valid records."),
        },
    },
    {
        "question_id": "d2-agent-tool-timeout-isolation",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "One slow external tool occasionally hangs for minutes, stalling the "
            "whole agent run. You want the agent to give up on that tool quickly "
            "and continue reasoning. Which control fits BEST?"
        ),
        "scenario_constraint": "Prevent one slow tool from blocking the whole run.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A global retry that re-runs the entire agent from the start."),
            ("b", "Removing all timeouts so the tool can finish."),
            ("c", "A per-tool timeout that fails the call fast and lets the agent proceed."),
            ("d", "Caching the tool's last response forever."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "A per-tool timeout isolates the slow dependency and returns control "
            "to the reasoning loop quickly. Restarting the whole run wastes work, "
            "removing timeouts worsens hangs, and permanent caching returns stale "
            "data."
        ),
        "rationales": {
            "a": (False, "Restarting the whole run discards progress and repeats the hang."),
            "b": (False, "Removing timeouts guarantees the stall continues."),
            "c": (True, "A per-tool timeout contains the hang and keeps the agent moving."),
            "d": (False, "Caching forever serves stale data and ignores fresh needs."),
        },
    },
    {
        "question_id": "d2-agentcore-identity",
        "objective_ids": ["AIP-2.1", "AIP-3.1"],
        "prompt": (
            "An AgentCore agent must act on behalf of the signed-in end user when "
            "it calls downstream services, carrying that user's identity rather "
            "than a single shared role. Which AgentCore capability provides this?"
        ),
        "scenario_constraint": "Propagate per-user identity through agent tool calls.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AgentCore Observability."),
            ("b", "AgentCore Code Interpreter."),
            ("c", "AgentCore Memory."),
            ("d", "AgentCore Identity."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "AgentCore Identity handles authenticated, per-user access when the "
            "agent calls downstream resources. Observability traces, Code "
            "Interpreter runs code, and Memory stores context."
        ),
        "rationales": {
            "a": (False, "Observability provides telemetry, not identity propagation."),
            "b": (False, "Code Interpreter executes code, not auth."),
            "c": (False, "Memory stores context and does not handle identity."),
            "d": (True, "Identity carries per-user access through agent actions."),
        },
    },
    {
        "question_id": "d2-code-interpreter-use",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An agent must run user-provided Python to compute statistics on an "
            "uploaded CSV, in a sandbox you do not have to operate. Which "
            "AgentCore capability is designed for this?"
        ),
        "scenario_constraint": "Safely execute generated code in a managed sandbox.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AgentCore Code Interpreter."),
            ("b", "AgentCore Gateway."),
            ("c", "AgentCore Memory."),
            ("d", "AgentCore Identity."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "AgentCore Code Interpreter runs generated code in a managed sandbox. "
            "Gateway exposes tools, Memory stores context, and Identity handles "
            "access."
        ),
        "rationales": {
            "a": (True, "Code Interpreter is the managed sandbox for running code."),
            "b": (False, "Gateway brokers tool/API access, not code execution."),
            "c": (False, "Memory persists context and runs no code."),
            "d": (False, "Identity governs access, not execution."),
        },
    },
    {
        "question_id": "d2-agent-observability-trace",
        "objective_ids": ["AIP-2.1", "AIP-2.5"],
        "prompt": (
            "Users report that an agent 'sometimes does the wrong thing,' but you "
            "cannot see which tools it chose or why. You want end-to-end "
            "visibility into each reasoning step and tool call. Which AgentCore "
            "capability addresses this?"
        ),
        "scenario_constraint": "Gain step-level visibility into agent decisions.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AgentCore Observability."),
            ("b", "AgentCore Runtime."),
            ("c", "AgentCore Memory."),
            ("d", "AgentCore Gateway."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "AgentCore Observability surfaces traces and metrics for each "
            "reasoning step and tool call. Runtime hosts execution, Memory stores "
            "context, and Gateway brokers tools."
        ),
        "rationales": {
            "a": (True, "Observability exposes per-step traces and tool decisions."),
            "b": (False, "Runtime executes the agent but is not the tracing layer."),
            "c": (False, "Memory holds context, not execution traces."),
            "d": (False, "Gateway brokers tools and does not provide tracing."),
        },
    },
    {
        "question_id": "d2-agent-grounding-vs-hallucinated-tool",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An agent occasionally invents a tool name that does not exist and "
            "fails. You want the agent to only ever call tools that are actually "
            "registered. What is the BEST control?"
        ),
        "scenario_constraint": "Restrict calls to the registered tool catalog only.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase max tokens so the model has room to pick correctly."),
            (
                "b",
                "Validate each proposed tool name against the registered tool catalog and reject unknown ones.",
            ),
            ("c", "Ask the model in the prompt to only use real tools."),
            ("d", "Lower temperature to zero to remove all errors."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Validating the proposed tool name against the registry and rejecting "
            "unknowns deterministically prevents calls to nonexistent tools. More "
            "tokens, prompt pleas, and zero temperature reduce but never "
            "guarantee the behavior."
        ),
        "rationales": {
            "a": (False, "More tokens do not constrain which tools are callable."),
            "b": (True, "Registry validation is the enforced gate against invented tools."),
            "c": (False, "A prompt request is advisory, not enforced."),
            "d": (False, "Zero temperature lowers variance but can still emit a bad name."),
        },
    },
    {
        "question_id": "d2-agent-vs-single-prompt",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A request requires looking up live inventory, checking a shipping "
            "API, and only then answering. A single zero-shot prompt keeps "
            "fabricating numbers. Which design change MOST improves correctness?"
        ),
        "scenario_constraint": "Ground answers in live data instead of fabrication.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Raise the max-tokens limit so answers are longer."),
            ("b", "Add more examples of fabricated answers to the prompt."),
            ("c", "Give the model tools/action groups so it fetches live data before answering."),
            ("d", "Switch to a smaller, cheaper model."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Equipping the model with tools lets it retrieve live inventory and "
            "shipping data instead of guessing. Longer outputs, bad examples, and "
            "a smaller model do not add grounding."
        ),
        "rationales": {
            "a": (False, "Longer answers do not make fabricated numbers correct."),
            "b": (False, "Showing fabricated examples reinforces the wrong behavior."),
            "c": (True, "Tool access grounds the answer in real-time data."),
            "d": (False, "A smaller model does not gain access to live data."),
        },
    },
    {
        "question_id": "d2-agent-parallel-tools",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An agent must gather three independent data points from three "
            "unrelated APIs before composing an answer, and latency is critical. "
            "Which execution strategy is BEST?"
        ),
        "scenario_constraint": "Minimize latency across independent tool calls.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Call them strictly in sequence to keep logic simple."),
            ("b", "Call the same tool three times and hope for different answers."),
            ("c", "Skip two tools and extrapolate the missing values."),
            ("d", "Invoke the three independent tools in parallel and join the results."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Because the three calls are independent, running them in parallel "
            "cuts total latency to roughly the slowest call. Sequencing is "
            "slower, repeating one tool is wrong, and extrapolating drops "
            "required data."
        ),
        "rationales": {
            "a": (False, "Sequential calls add their latencies unnecessarily."),
            "b": (False, "Repeating one tool does not fetch the other data points."),
            "c": (False, "Extrapolating omits required real values."),
            "d": (True, "Parallelizing independent calls minimizes end-to-end latency."),
        },
    },
    {
        "question_id": "d2-agent-memory-vs-context",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A support agent must remember a customer's preferences across "
            "sessions that may be days apart, but each session's prompt should "
            "stay small for cost reasons. Which approach fits BEST?"
        ),
        "scenario_constraint": "Persist long-term memory without bloating every prompt.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Paste the entire conversation history into every prompt."),
            ("b", "Keep everything in the model's context window between sessions."),
            (
                "c",
                "Store durable preferences in a memory store and retrieve only relevant items per session.",
            ),
            ("d", "Discard preferences after each session and re-ask the user."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "A durable memory store with selective retrieval keeps per-session "
            "prompts small while preserving long-term recall. Pasting all history "
            "inflates cost, the context window does not persist across sessions, "
            "and re-asking harms experience."
        ),
        "rationales": {
            "a": (False, "Pasting full history inflates every prompt and its cost."),
            "b": (False, "Context windows do not persist across separate sessions."),
            "c": (True, "Selective retrieval from durable memory balances recall and cost."),
            "d": (False, "Discarding preferences forces repetitive re-asking."),
        },
    },
    {
        "question_id": "d2-agent-guardrail-on-tool-output",
        "objective_ids": ["AIP-2.1", "AIP-3.2"],
        "prompt": (
            "An agent summarizes documents a tool returns, but some documents "
            "contain content that must never reach the end user. You need the "
            "agent's final response filtered against a policy. Which control is "
            "MOST appropriate?"
        ),
        "scenario_constraint": "Enforce a content policy on the agent's final output.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Trust the model to self-censor via the system prompt."),
            ("b", "Apply Amazon Bedrock Guardrails to the agent's input and output."),
            ("c", "Remove the summarization tool entirely."),
            ("d", "Increase temperature so output varies away from the content."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Bedrock Guardrails enforce content policy on inputs and outputs "
            "independently of the model's cooperation. Prompt self-censorship is "
            "unenforced, removing the tool kills the feature, and temperature "
            "does not filter content."
        ),
        "rationales": {
            "a": (False, "Prompt-based self-censorship is not an enforced control."),
            "b": (True, "Guardrails apply an enforced content policy to the response."),
            "c": (False, "Removing the tool eliminates the needed capability."),
            "d": (False, "Temperature changes randomness, not policy enforcement."),
        },
    },
    {
        "question_id": "d2-agent-tool-vs-rag",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An agent needs both to answer policy questions from a document "
            "corpus and to execute live account actions. Which combination of "
            "capabilities BEST serves both needs? Select TWO."
        ),
        "scenario_constraint": "Combine knowledge retrieval with live action execution.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "A knowledge base / retrieval tool for grounded policy answers."),
            ("b", "Action groups that call account-management APIs for live actions."),
            ("c", "A higher temperature to improve creativity."),
            ("d", "A larger max-tokens limit for both tasks."),
            ("e", "Disabling tools to force the model to reason unaided."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "A retrieval tool grounds policy answers while action groups execute "
            "live account operations, covering both needs. Temperature, token "
            "limits, and disabling tools do not provide retrieval or actions."
        ),
        "rationales": {
            "a": (True, "Retrieval grounds answers in the policy corpus."),
            "b": (True, "Action groups perform the live account operations."),
            "c": (False, "Creativity is not the requirement; grounding and action are."),
            "d": (False, "Token limits do not add retrieval or action capability."),
            "e": (False, "Disabling tools removes the live-action capability needed."),
        },
    },
    {
        "question_id": "d2-agent-fallback-on-tool-failure",
        "objective_ids": ["AIP-2.1", "AIP-2.5"],
        "prompt": (
            "When a pricing tool is unavailable, the agent currently returns a "
            "confident but fabricated price. You must ensure it never presents a "
            "guessed price as real. Which behavior is BEST?"
        ),
        "scenario_constraint": "Never present fabricated data as a verified result.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "On tool failure, return an explicit 'pricing unavailable' response instead of a guess.",
            ),
            ("b", "Let the model estimate a price from training data."),
            ("c", "Retry forever until the tool returns something."),
            ("d", "Cache the last price and present it as current indefinitely."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Returning an explicit unavailable state prevents passing a guess off "
            "as real data. Estimating fabricates, infinite retries hang, and "
            "serving a stale cache as current misrepresents freshness."
        ),
        "rationales": {
            "a": (True, "An explicit unavailable response avoids false confidence."),
            "b": (False, "A training-data estimate is a fabricated, unverified price."),
            "c": (False, "Infinite retries can hang the request indefinitely."),
            "d": (False, "Presenting a stale price as current misleads the user."),
        },
    },
    {
        "question_id": "d2-provisioned-vs-ondemand-steady",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A Bedrock-backed feature runs a steady, high, predictable volume "
            "24/7 and the team wants the lowest cost at guaranteed throughput. "
            "Which inference mode fits BEST?"
        ),
        "scenario_constraint": "Steady predictable high volume needing guaranteed throughput.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "On-demand inference priced per request."),
            ("b", "Batch inference submitted nightly."),
            ("c", "A SageMaker serverless endpoint."),
            ("d", "Provisioned Throughput with committed model units."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Provisioned Throughput reserves committed capacity at lower unit "
            "cost for steady, predictable high volume. On-demand costs more at "
            "scale, batch is not interactive, and serverless suits spiky, "
            "low-steady traffic."
        ),
        "rationales": {
            "a": (False, "On-demand per-request pricing is costlier at steady high volume."),
            "b": (False, "Nightly batch cannot serve interactive 24/7 traffic."),
            "c": (False, "Serverless fits spiky low-steady load, not constant high volume."),
            "d": (True, "Provisioned Throughput gives committed capacity at lower unit cost."),
        },
    },
    {
        "question_id": "d2-ondemand-spiky-traffic",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A demo feature gets sporadic, unpredictable traffic that is often "
            "zero for hours. The team wants to pay only when it is used and avoid "
            "managing capacity. Which Bedrock option fits BEST?"
        ),
        "scenario_constraint": "Sporadic traffic with pay-per-use and no capacity management.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Provisioned Throughput with reserved model units."),
            ("b", "On-demand inference."),
            ("c", "A dedicated EC2 GPU fleet always running."),
            ("d", "An EKS cluster hosting the model continuously."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "On-demand inference bills per request and requires no reserved "
            "capacity, matching sporadic usage. Provisioned units, an always-on "
            "GPU fleet, and a continuous EKS cluster all pay for idle time."
        ),
        "rationales": {
            "a": (False, "Reserved units pay for capacity during the many idle hours."),
            "b": (True, "On-demand bills only per request with no capacity to manage."),
            "c": (False, "An always-on GPU fleet wastes money while idle."),
            "d": (False, "A continuous cluster incurs cost even at zero traffic."),
        },
    },
    {
        "question_id": "d2-lambda-ondemand-inference",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A lightweight endpoint must call a Bedrock model on each API "
            "request, scale to zero between bursts, and need no servers to "
            "manage. Which compute choice fits BEST for the invocation layer?"
        ),
        "scenario_constraint": "Serverless, scale-to-zero compute to invoke the model.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A standing EC2 instance polling a queue."),
            ("b", "An ECS service with a fixed task count."),
            ("c", "AWS Lambda invoking the Bedrock model per request."),
            ("d", "A SageMaker training job per request."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Lambda scales to zero, needs no server management, and invokes "
            "Bedrock per request. A standing EC2 instance and fixed ECS tasks pay "
            "for idle, and a training job is the wrong primitive for inference."
        ),
        "rationales": {
            "a": (False, "A standing instance incurs idle cost and ops burden."),
            "b": (False, "A fixed task count cannot scale to zero between bursts."),
            "c": (True, "Lambda is serverless, scales to zero, and invokes per request."),
            "d": (False, "Training jobs are for model training, not request inference."),
        },
    },
    {
        "question_id": "d2-sagemaker-endpoint-custom-model",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A team fine-tuned an open-weights model not offered in Bedrock and "
            "must serve it behind a low-latency HTTPS endpoint with autoscaling. "
            "Which AWS option is MOST appropriate?"
        ),
        "scenario_constraint": "Host a custom open-weights model with managed real-time inference.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A Bedrock on-demand foundation model."),
            ("b", "Amazon Comprehend custom classification."),
            ("c", "AWS Lambda packaging the model weights in the ZIP."),
            ("d", "A SageMaker real-time inference endpoint."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "A SageMaker real-time endpoint hosts custom model artifacts with "
            "autoscaling and low latency. Bedrock serves its own catalog, "
            "Comprehend is a managed NLP service, and large model weights do not "
            "fit Lambda's package limits well."
        ),
        "rationales": {
            "a": (False, "Bedrock serves managed catalog models, not arbitrary custom weights."),
            "b": (False, "Comprehend is a fixed NLP service, not a model host."),
            "c": (False, "Large model weights exceed Lambda's practical package limits."),
            "d": (True, "SageMaker endpoints host custom models with autoscaling."),
        },
    },
    {
        "question_id": "d2-batch-inference-large-offline",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A nightly job must summarize ten million stored documents by "
            "morning, with no interactive latency requirement, at the lowest "
            "cost. Which inference pattern fits BEST?"
        ),
        "scenario_constraint": "High-volume offline processing with no latency requirement.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Bedrock batch inference over the document set."),
            ("b", "Synchronous on-demand calls one document at a time."),
            ("c", "Provisioned Throughput sized for peak interactive load."),
            ("d", "A streaming endpoint for each document."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Batch inference processes large offline datasets cost-effectively "
            "without latency pressure. One-at-a-time synchronous calls are slow "
            "and costly, interactive provisioning overpays, and streaming suits "
            "incremental UX, not bulk jobs."
        ),
        "rationales": {
            "a": (True, "Batch inference is built for high-volume offline workloads."),
            "b": (False, "One-at-a-time synchronous calls are slow and expensive at this scale."),
            "c": (False, "Interactive provisioning overpays for a nightly offline job."),
            "d": (False, "Streaming optimizes incremental UX, not bulk throughput."),
        },
    },
    {
        "question_id": "d2-async-inference-large-payload",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A SageMaker-hosted model handles large input payloads with "
            "processing times up to several minutes, and clients should not hold "
            "an open synchronous connection. Which inference option fits BEST?"
        ),
        "scenario_constraint": "Long-running requests with large payloads and no held connection.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "SageMaker asynchronous inference with results delivered to S3."),
            ("b", "SageMaker real-time inference with a 60-second cap."),
            ("c", "Bedrock streaming responses."),
            ("d", "AWS Lambda synchronous invocation."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Asynchronous inference queues long requests and writes results to "
            "S3, freeing the client from holding a connection. Real-time has "
            "tight latency caps, Bedrock streaming is a different host, and "
            "Lambda has a 15-minute hard limit and payload constraints."
        ),
        "rationales": {
            "a": (True, "Async inference handles minutes-long jobs and large payloads via S3."),
            "b": (False, "Real-time endpoints cap request duration too tightly for this."),
            "c": (False, "Streaming addresses token delivery, not long async queuing."),
            "d": (False, "Lambda's limits make it a poor fit for large multi-minute payloads."),
        },
    },
    {
        "question_id": "d2-model-cascading-cost",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "Most support queries are simple, but a minority need a powerful, "
            "expensive model. Which TWO approaches minimize cost without hurting "
            "answers on hard queries? Select TWO."
        ),
        "scenario_constraint": "Minimize cost while preserving quality on hard inputs.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            (
                "a",
                "Model cascading: a cheap model first, escalating to a stronger one when confidence is low.",
            ),
            ("b", "Route by measured query complexity to a cheap or premium model."),
            ("c", "Send every query to the cheapest model only."),
            ("d", "Randomly pick a model for each query."),
            ("e", "Send every query to the most powerful model."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Cascading escalates only hard queries, and complexity-based routing "
            "sends easy ones to a cheap model, both balancing cost and quality. "
            "Cheapest-only hurts hard queries, random ignores difficulty, and "
            "always-powerful overpays."
        ),
        "rationales": {
            "a": (True, "Cascading escalates only when needed, balancing cost and quality."),
            "b": (True, "Complexity-based routing matches model strength to query difficulty."),
            "c": (False, "Cheapest-only degrades answers on the hard minority."),
            "d": (False, "Random selection ignores query difficulty entirely."),
            "e": (False, "Routing everything to the big model overpays on easy queries."),
        },
    },
    {
        "question_id": "d2-concurrency-quota-throttling",
        "objective_ids": ["AIP-2.2", "AIP-2.4"],
        "prompt": (
            "During launch, a Bedrock-backed app starts receiving throttling "
            "errors at peak. The team confirmed requests are well-formed. Which "
            "TWO actions directly address the capacity limit? Select TWO."
        ),
        "scenario_constraint": "Well-formed requests throttled at peak capacity.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Request a service quota increase for the model's invocation limit."),
            ("b", "Adopt Provisioned Throughput to guarantee peak capacity."),
            ("c", "Increase the prompt's max-tokens limit."),
            ("d", "Switch the response to streaming mode."),
            ("e", "Add more fields to the request schema."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Raising the service quota and/or committing Provisioned Throughput "
            "add the capacity that throttling signals is missing. Token limits, "
            "streaming, and schema changes do not increase allowed throughput."
        ),
        "rationales": {
            "a": (True, "A quota increase raises the allowed invocation rate."),
            "b": (True, "Provisioned Throughput reserves capacity for peak load."),
            "c": (False, "Max tokens affects output length, not throttling limits."),
            "d": (False, "Streaming changes delivery, not allowed throughput."),
            "e": (False, "Schema fields do not change capacity limits."),
        },
    },
    {
        "question_id": "d2-ecs-eks-container-deploy",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A team already runs Kubernetes and wants to serve a custom model "
            "container alongside existing microservices, reusing their cluster "
            "tooling and GPU node pools. Which deployment target fits BEST?"
        ),
        "scenario_constraint": "Serve a model container inside existing Kubernetes operations.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Bedrock on-demand inference."),
            ("b", "Amazon EKS with a GPU node group hosting the model container."),
            ("c", "A SageMaker serverless endpoint."),
            ("d", "AWS Lambda with the model baked into a layer."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "EKS lets the team host the model container next to existing "
            "microservices using their Kubernetes tooling and GPU nodes. Bedrock "
            "and SageMaker serverless hide the cluster, and Lambda cannot run "
            "GPU-bound model containers."
        ),
        "rationales": {
            "a": (False, "Bedrock abstracts hosting and cannot run arbitrary containers."),
            "b": (True, "EKS reuses the existing Kubernetes cluster and GPU pools."),
            "c": (False, "Serverless endpoints do not integrate with their K8s tooling."),
            "d": (False, "Lambda does not support GPU-bound model containers."),
        },
    },
    {
        "question_id": "d2-sagemaker-multimodel-endpoint",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A team hosts dozens of small per-customer models, most invoked "
            "rarely, and wants to avoid paying for a dedicated endpoint per "
            "model. Which SageMaker feature fits BEST?"
        ),
        "scenario_constraint": "Serve many rarely-used models cost-efficiently.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "One dedicated real-time endpoint per model."),
            ("b", "A separate Bedrock agent per model."),
            ("c", "A multi-model endpoint that loads models on demand."),
            ("d", "A batch job that runs all models nightly."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "A multi-model endpoint shares infrastructure and loads models on "
            "demand, ideal for many infrequently used models. Dedicated endpoints "
            "per model are costly, Bedrock agents are unrelated, and nightly "
            "batch is not on-demand serving."
        ),
        "rationales": {
            "a": (False, "One endpoint per model multiplies idle infrastructure cost."),
            "b": (False, "Agents orchestrate reasoning, not multi-model hosting."),
            "c": (True, "Multi-model endpoints share capacity across many models."),
            "d": (False, "Batch is offline and cannot serve on-demand requests."),
        },
    },
    {
        "question_id": "d2-provisioned-throughput-latency-slo",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A regulated workload must meet a strict p99 latency SLO that "
            "on-demand sometimes misses due to variable capacity. The team "
            "accepts a higher baseline cost for predictability. Which option fits "
            "BEST?"
        ),
        "scenario_constraint": "Guarantee predictable latency over minimizing cost.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Keep on-demand and retry on slow responses."),
            ("b", "Batch inference to smooth latency."),
            ("c", "Lower max tokens to speed every call."),
            ("d", "Provisioned Throughput to reserve dedicated capacity."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Provisioned Throughput reserves dedicated capacity, giving the "
            "predictable latency the SLO demands. Retrying worsens tail latency, "
            "batch is not interactive, and trimming tokens does not fix capacity "
            "variability."
        ),
        "rationales": {
            "a": (False, "Retries add latency and do not fix variable capacity."),
            "b": (False, "Batch is offline and cannot serve an interactive SLO."),
            "c": (False, "Shorter outputs do not address capacity-driven tail latency."),
            "d": (True, "Reserved capacity delivers predictable p99 latency."),
        },
    },
    {
        "question_id": "d2-cross-region-capacity",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A workload hits regional capacity limits for a popular model during "
            "spikes, while a nearby Region has headroom and the data has no "
            "residency restriction. Which approach adds capacity with the LEAST "
            "rework?"
        ),
        "scenario_constraint": "Spiky demand exceeds one Region's model capacity.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Rewrite the app to use a smaller unrelated model."),
            ("b", "Queue all overflow for nightly batch processing."),
            ("c", "Distribute invocations across Regions using cross-Region inference."),
            ("d", "Cache responses and serve stale answers at peak."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Cross-Region inference spreads load to Regions with headroom without "
            "app redesign, given no residency constraint. Swapping models changes "
            "behavior, overnight batch breaks interactivity, and stale caching "
            "degrades correctness."
        ),
        "rationales": {
            "a": (False, "Switching models changes outputs and user experience."),
            "b": (False, "Nightly batch cannot serve interactive peak traffic."),
            "c": (True, "Cross-Region inference taps spare capacity with minimal rework."),
            "d": (False, "Serving stale cached answers sacrifices correctness."),
        },
    },
    {
        "question_id": "d2-lambda-cold-start-latency",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A Lambda that invokes Bedrock shows occasional slow first responses "
            "after idle periods, hurting a latency-sensitive path. Which change "
            "MOST reduces this specific delay with the least overhead?"
        ),
        "scenario_constraint": "Reduce cold-start latency on a serverless invocation path.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase the model's max tokens."),
            ("b", "Enable provisioned concurrency on the function."),
            ("c", "Switch the model to streaming."),
            ("d", "Move the model weights into the deployment package."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Provisioned concurrency keeps initialized execution environments "
            "warm, eliminating cold-start spikes. Token limits and streaming do "
            "not address init latency, and Bedrock weights are not shipped in the "
            "package."
        ),
        "rationales": {
            "a": (False, "Max tokens affects output size, not init latency."),
            "b": (True, "Provisioned concurrency keeps environments warm, removing cold starts."),
            "c": (False, "Streaming changes delivery, not cold-start initialization."),
            "d": (False, "Bedrock serves the model; weights are not in the Lambda package."),
        },
    },
    {
        "question_id": "d2-autoscaling-sagemaker-endpoint",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A SageMaker real-time endpoint is overprovisioned at night and "
            "throttled at midday. The team wants capacity to track demand "
            "automatically. Which mechanism fits BEST?"
        ),
        "scenario_constraint": "Match endpoint capacity to fluctuating demand automatically.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Configure endpoint autoscaling on an invocation metric."),
            ("b", "Manually resize the endpoint twice a day."),
            ("c", "Switch to batch inference."),
            ("d", "Set a fixed instance count sized for midday."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Autoscaling adjusts instance count to a target invocation metric, "
            "matching capacity to demand. Manual resizing is error-prone, batch "
            "is offline, and fixed midday sizing wastes money at night."
        ),
        "rationales": {
            "a": (True, "Autoscaling tracks demand via an invocation target metric."),
            "b": (False, "Manual resizing is slow, error-prone, and reactive."),
            "c": (False, "Batch is offline and does not serve real-time traffic."),
            "d": (False, "Fixed midday sizing overpays during off-peak hours."),
        },
    },
    {
        "question_id": "d2-shadow-deployment-eval",
        "objective_ids": ["AIP-2.2", "AIP-2.3"],
        "prompt": (
            "Before switching production to a new model version, the team wants "
            "to send a copy of live traffic to it and compare outputs without "
            "affecting users. Which deployment technique fits BEST?"
        ),
        "scenario_constraint": "Evaluate a new model on live traffic without user impact.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A hard cutover to the new version at midnight."),
            ("b", "Deleting the old version first, then deploying the new one."),
            ("c", "Serving both versions randomly to end users immediately."),
            ("d", "A shadow deployment mirroring traffic to the new version."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Shadow deployment mirrors real traffic to the new version for "
            "comparison while users still see the old one. A hard cutover and "
            "deleting first carry no safety net, and random live serving exposes "
            "users to the untested version."
        ),
        "rationales": {
            "a": (False, "A hard cutover exposes all users with no validation."),
            "b": (False, "Deleting the old version removes any rollback path."),
            "c": (False, "Random live serving exposes users to the untested model."),
            "d": (True, "Shadowing compares the new version on live traffic safely."),
        },
    },
    {
        "question_id": "d2-canary-model-rollout",
        "objective_ids": ["AIP-2.2", "AIP-2.3"],
        "prompt": (
            "A team must roll out a new model version to production gradually so "
            "that if error rates rise, only a small fraction of users are "
            "affected and rollback is quick. Which strategy fits BEST?"
        ),
        "scenario_constraint": "Limit blast radius during a model version rollout.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A full cutover for all users at once."),
            ("b", "A canary release sending a small traffic percentage to the new version first."),
            ("c", "Batch-only use of the new version."),
            ("d", "Deploying the new version to a separate account nobody uses."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "A canary routes a small percentage first, limiting impact and "
            "enabling fast rollback. A full cutover risks everyone, batch-only "
            "never tests the live path, and an unused account provides no "
            "production signal."
        ),
        "rationales": {
            "a": (False, "A full cutover exposes all users to a regression at once."),
            "b": (True, "A canary limits exposure and enables quick rollback."),
            "c": (False, "Batch-only never validates the interactive production path."),
            "d": (False, "An unused account yields no real production feedback."),
        },
    },
    {
        "question_id": "d2-quota-vs-throughput-concept",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A team keeps conflating two capacity concepts. They need the term "
            "for the maximum rate at which the account may call a Bedrock model "
            "under on-demand access before throttling. Which term applies?"
        ),
        "scenario_constraint": "Identify the account-level invocation rate limit.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Context window."),
            ("b", "Max tokens."),
            ("c", "Service quota (rate limit)."),
            ("d", "Temperature."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "The account's service quota sets the allowed invocation rate before "
            "throttling. Context window and max tokens bound a single request, "
            "and temperature controls sampling."
        ),
        "rationales": {
            "a": (False, "The context window bounds input size, not call rate."),
            "b": (False, "Max tokens limits output length per request."),
            "c": (True, "The service quota is the account invocation rate limit."),
            "d": (False, "Temperature controls randomness, not throughput."),
        },
    },
    {
        "question_id": "d2-right-size-model-cost",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A classification feature currently uses a top-tier reasoning model "
            "but only needs to pick one of five labels. The team wants to cut "
            "cost without hurting accuracy on this narrow task. What is the BEST "
            "move?"
        ),
        "scenario_constraint": "Match model size to a narrow, simple task.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Keep the top-tier model to be safe."),
            ("b", "Add Provisioned Throughput to the top-tier model."),
            ("c", "Increase the top-tier model's max tokens."),
            (
                "d",
                "Evaluate and switch to a smaller model that meets the accuracy bar for the task.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "A validated smaller model that meets the accuracy bar cuts cost on a "
            "simple task. Keeping the big model overpays, provisioning it adds "
            "cost, and more tokens do not reduce spend."
        ),
        "rationales": {
            "a": (False, "Keeping the top-tier model overpays for a trivial task."),
            "b": (False, "Provisioning the expensive model raises cost, not lowers it."),
            "c": (False, "More tokens increases cost without benefit here."),
            "d": (True, "A right-sized smaller model meets the bar at lower cost."),
        },
    },
    {
        "question_id": "d2-cross-region-residency-conflict",
        "objective_ids": ["AIP-2.2", "AIP-2.3"],
        "prompt": (
            "An EU workload is capacity-constrained, but regulation forbids "
            "processing its data outside the EU. An engineer suggests "
            "cross-Region inference to a US Region for headroom. What is the BEST "
            "response?"
        ),
        "scenario_constraint": "Capacity need must not violate data residency rules.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Keep inference within compliant EU Regions and add capacity there instead."),
            ("b", "Use the US Region since it has the most headroom."),
            ("c", "Send only the prompts, not the responses, to the US Region."),
            ("d", "Disable logging so the cross-Region use is not recorded."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Residency rules override the capacity convenience, so capacity must "
            "be added within compliant EU Regions. Using the US Region violates "
            "residency, splitting prompts still processes data abroad, and "
            "disabling logging hides a violation rather than preventing it."
        ),
        "rationales": {
            "a": (
                True,
                "Staying in compliant EU Regions respects residency while adding capacity.",
            ),
            "b": (False, "US processing of EU data violates the residency rule."),
            "c": (False, "Sending prompts abroad still processes regulated data outside the EU."),
            "d": (False, "Hiding logs conceals, not resolves, the compliance breach."),
        },
    },
    {
        "question_id": "d2-provisioned-commitment-waste",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A team bought Provisioned Throughput for a feature whose traffic "
            "later dropped to near zero most of the day, and the commitment is "
            "mostly idle. Which action BEST reduces ongoing cost?"
        ),
        "scenario_constraint": "Reserved capacity now sits idle most of the time.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Move the low, sporadic traffic to on-demand and release the unused commitment."),
            ("b", "Add more provisioned model units for headroom."),
            ("c", "Increase max tokens to use the capacity."),
            ("d", "Send synthetic requests to fill the reserved capacity."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Sporadic low traffic fits on-demand, so releasing the idle "
            "commitment stops paying for unused capacity. Adding units, more "
            "tokens, or synthetic traffic all increase waste rather than cut it."
        ),
        "rationales": {
            "a": (True, "On-demand matches sporadic traffic and ends the idle commitment cost."),
            "b": (False, "More units deepen the idle-capacity waste."),
            "c": (False, "Longer outputs do not reduce the reserved-capacity cost."),
            "d": (False, "Synthetic requests waste money to mask idleness."),
        },
    },
    {
        "question_id": "d2-blue-green-rollback",
        "objective_ids": ["AIP-2.2", "AIP-2.3"],
        "prompt": (
            "A team wants instant rollback capability when promoting a new "
            "inference stack, keeping the old environment fully running until the "
            "new one is proven. Which deployment pattern fits BEST?"
        ),
        "scenario_constraint": "Instant rollback with the prior environment intact.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "In-place upgrade of the running environment."),
            ("b", "Blue/green deployment with traffic switched between two environments."),
            ("c", "Deleting the old stack before deploying the new one."),
            ("d", "A single rolling restart with no second environment."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Blue/green keeps both environments live and flips traffic, enabling "
            "instant rollback. In-place upgrades, deleting first, and a single "
            "rolling restart all lack a ready fallback environment."
        ),
        "rationales": {
            "a": (False, "In-place upgrades leave no intact prior environment."),
            "b": (True, "Blue/green keeps the old environment ready for instant rollback."),
            "c": (False, "Deleting the old stack removes any rollback target."),
            "d": (False, "A single rolling restart has no fallback environment."),
        },
    },
    {
        "question_id": "d2-gpu-vs-cpu-inference",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A self-hosted large language model on SageMaker shows unacceptable "
            "latency on CPU instances under load. The model benefits heavily from "
            "parallel matrix operations. Which change MOST directly improves "
            "throughput?"
        ),
        "scenario_constraint": "LLM inference is compute-bound on CPU.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Add more CPU-only instances behind the endpoint."),
            ("b", "Reduce the endpoint's instance count."),
            ("c", "Move the endpoint to GPU-accelerated instances."),
            ("d", "Increase the request timeout."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "GPU instances accelerate the parallel matrix math LLM inference "
            "needs, directly improving latency. More CPU nodes scale a slow path, "
            "fewer instances worsen it, and a longer timeout only hides the "
            "slowness."
        ),
        "rationales": {
            "a": (False, "Scaling CPU-only instances multiplies a slow compute path."),
            "b": (False, "Fewer instances reduce capacity and worsen latency."),
            "c": (True, "GPUs accelerate the parallel operations the model relies on."),
            "d": (False, "A longer timeout masks slowness without fixing it."),
        },
    },
    {
        "question_id": "d2-serverless-endpoint-tradeoff",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A rarely used internal tool must host a custom model but the team "
            "will not tolerate paying for idle endpoint instances and accepts "
            "occasional cold-start latency. Which SageMaker option fits BEST?"
        ),
        "scenario_constraint": "Avoid idle cost while tolerating cold starts.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A provisioned real-time endpoint running 24/7."),
            ("b", "Provisioned Throughput on Bedrock."),
            ("c", "An always-on EKS GPU pool."),
            ("d", "SageMaker Serverless Inference."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Serverless Inference scales to zero and bills per use, accepting "
            "cold starts for rarely used models. A 24/7 endpoint, Bedrock "
            "provisioning, and an always-on pool all pay for idle time."
        ),
        "rationales": {
            "a": (False, "A 24/7 endpoint pays for mostly-idle capacity."),
            "b": (False, "Provisioned Throughput reserves and bills for capacity."),
            "c": (False, "An always-on GPU pool wastes money while idle."),
            "d": (True, "Serverless Inference scales to zero, avoiding idle cost."),
        },
    },
    {
        "question_id": "d2-model-units-estimation",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "Before committing Provisioned Throughput, a team must decide how "
            "many model units to reserve. Which input is MOST relevant to that "
            "sizing decision?"
        ),
        "scenario_constraint": "Size reserved capacity to real demand.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "The number of developers on the team."),
            ("b", "The color scheme of the UI."),
            ("c", "The feature's measured peak tokens-per-minute throughput requirement."),
            ("d", "The model's release date."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Measured peak throughput in tokens per minute drives how many model "
            "units to reserve. Team size, UI styling, and release date are "
            "irrelevant to capacity sizing."
        ),
        "rationales": {
            "a": (False, "Team size does not affect inference capacity needs."),
            "b": (False, "UI styling is unrelated to throughput sizing."),
            "c": (True, "Peak throughput demand determines required model units."),
            "d": (False, "Release date does not inform capacity requirements."),
        },
    },
    {
        "question_id": "d2-api-gateway-frontdoor",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A GenAI backend built on Lambda must be exposed to external clients "
            "with throttling, API keys, and request validation at the edge, "
            "without building those features yourself. Which service fits BEST as "
            "the front door?"
        ),
        "scenario_constraint": "Managed edge with throttling, auth, and validation.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A public Application Load Balancer with no auth layer."),
            ("b", "Amazon API Gateway in front of the Lambda."),
            ("c", "Direct Lambda function URLs exposed to clients."),
            ("d", "Amazon CloudFront serving the Lambda directly."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "API Gateway provides managed throttling, API keys, and request "
            "validation at the edge. A bare ALB and raw function URLs lack those "
            "controls, and CloudFront is a CDN, not an API management layer."
        ),
        "rationales": {
            "a": (False, "A plain ALB offers no API keys or request validation."),
            "b": (True, "API Gateway delivers throttling, keys, and validation out of the box."),
            "c": (False, "Function URLs expose Lambda without managed API controls."),
            "d": (False, "CloudFront caches content; it is not an API management layer."),
        },
    },
    {
        "question_id": "d2-eventbridge-decoupling",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "When a document is uploaded, several independent GenAI pipelines "
            "(summarize, classify, index) must each react, and the team wants to "
            "add new consumers later without touching the producer. Which TWO "
            "patterns support this decoupled fan-out? Select TWO."
        ),
        "scenario_constraint": "Fan out one event to many evolvable consumers.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            (
                "a",
                "Publish an event to Amazon EventBridge and let each pipeline subscribe via rules.",
            ),
            ("b", "Publish to an Amazon SNS topic each pipeline subscribes to."),
            ("c", "Have the producer call each pipeline synchronously in a loop."),
            ("d", "Store a flag in a database each pipeline polls every minute."),
            ("e", "Hard-code the three pipeline ARNs into the producer."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Both EventBridge rules and an SNS topic decouple the producer from "
            "consumers so new pipelines subscribe without producer changes. "
            "Synchronous loops and hard-coded ARNs couple tightly, and polling a "
            "flag adds latency and load."
        ),
        "rationales": {
            "a": (True, "EventBridge fan-out lets consumers evolve independently of the producer."),
            "b": (True, "An SNS topic broadcasts to many subscribers without producer edits."),
            "c": (False, "Synchronous calls couple the producer to every consumer."),
            "d": (False, "Polling adds latency and does not scale cleanly."),
            "e": (False, "Hard-coded ARNs require producer edits for each new consumer."),
        },
    },
    {
        "question_id": "d2-sqs-buffer-spikes",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A GenAI processing service is occasionally overwhelmed by sudden "
            "bursts of upstream requests, dropping work. The team wants to absorb "
            "spikes and process at a steady rate. Which service fits BEST?"
        ),
        "scenario_constraint": "Buffer bursty load and smooth downstream processing.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Place an Amazon SQS queue between producers and the processor."),
            ("b", "Call the processor synchronously and retry on failure."),
            ("c", "Increase the processor's timeout."),
            ("d", "Add more fields to each request."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "An SQS queue buffers bursts and lets the processor consume at a "
            "sustainable rate, preventing dropped work. Synchronous retries, "
            "longer timeouts, and extra fields do not absorb spikes."
        ),
        "rationales": {
            "a": (True, "SQS decouples and buffers bursts for steady processing."),
            "b": (False, "Synchronous calls still overload the processor during spikes."),
            "c": (False, "A longer timeout does not stop the processor being overwhelmed."),
            "d": (False, "Extra fields are irrelevant to load buffering."),
        },
    },
    {
        "question_id": "d2-step-functions-orchestration",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A multi-stage GenAI workflow has conditional branches, retries with "
            "backoff, and a human-approval wait that can last hours, and the team "
            "needs auditable state at each step. Which service orchestrates this "
            "BEST?"
        ),
        "scenario_constraint": "Durable, auditable multi-step workflow with waits and branching.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A single long-running Lambda doing all steps."),
            ("b", "A cron job polling a database."),
            ("c", "An SQS queue with no coordinator."),
            ("d", "AWS Step Functions state machine."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Step Functions models branches, retries, long waits, and per-step "
            "state with built-in auditability. A single Lambda cannot wait hours, "
            "cron polling is brittle, and a bare queue has no orchestration."
        ),
        "rationales": {
            "a": (False, "A single Lambda cannot survive multi-hour human waits."),
            "b": (False, "Cron polling lacks branching and durable per-step state."),
            "c": (False, "A bare queue provides no workflow coordination."),
            "d": (
                True,
                "Step Functions handles branching, retries, long waits, and state tracking.",
            ),
        },
    },
    {
        "question_id": "d2-genai-gateway-centralize",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "An enterprise with many teams calling foundation models adopts a "
            "shared GenAI gateway fronting all model access. Which TWO governance "
            "capabilities does centralizing on the gateway most directly enable? "
            "Select TWO."
        ),
        "scenario_constraint": "Centralize cross-team model governance and routing.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Enforcing per-team usage quotas in one place."),
            ("b", "Centralized usage logging and routing to approved models."),
            ("c", "Eliminating the need for any IAM permissions."),
            ("d", "Removing all per-request latency from model calls."),
            ("e", "Guaranteeing the model never produces an incorrect answer."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "A gateway centralizes quota enforcement and usage logging with "
            "routing to approved models. It does not remove IAM, eliminate "
            "latency, or guarantee model correctness."
        ),
        "rationales": {
            "a": (True, "A gateway enforces shared per-team quotas centrally."),
            "b": (True, "Centralized logging and approved-model routing live at the gateway."),
            "c": (False, "A gateway still relies on IAM for authorization."),
            "d": (False, "A gateway adds a hop; it does not remove model latency."),
            "e": (False, "No gateway can guarantee model output correctness."),
        },
    },
    {
        "question_id": "d2-tenant-identity-propagation",
        "objective_ids": ["AIP-2.3", "AIP-3.1"],
        "prompt": (
            "A multi-tenant SaaS must ensure each GenAI request is processed and "
            "logged under the correct tenant, so one tenant can never access "
            "another's data. Which approach is MOST reliable?"
        ),
        "scenario_constraint": "Guarantee per-tenant isolation across the request path.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Let clients send a tenant ID in a header the backend trusts without verification.",
            ),
            (
                "b",
                "Propagate a verified tenant/identity context from the edge through every layer and enforce it on data access.",
            ),
            ("c", "Store all tenants' data together and filter in the UI."),
            ("d", "Rely on the model to keep tenants separate in its context window."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Propagating a verified identity/tenant context and enforcing it at "
            "data access is the reliable isolation boundary. Trusting a "
            "client-sent header invites spoofing, UI filtering leaks data, and "
            "the model cannot enforce access control."
        ),
        "rationales": {
            "a": (False, "An unverified header can be spoofed to reach other tenants."),
            "b": (
                True,
                "Verified identity propagation enforces tenant isolation at the data layer.",
            ),
            "c": (False, "UI-only filtering still exposes cross-tenant data server-side."),
            "d": (False, "The model is not an access-control mechanism."),
        },
    },
    {
        "question_id": "d2-cicd-model-app",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A team wants automated build, test, and deployment of their GenAI "
            "application whenever code is merged, using AWS-native CI/CD. Which "
            "TWO services directly provide the pipeline and build steps? Select "
            "TWO."
        ),
        "scenario_constraint": "AWS-native automated build and deploy on merge.",
        "difficulty": "easy",
        "question_format": "multiple_response",
        "options": [
            ("a", "AWS CodePipeline to orchestrate the stages."),
            ("b", "AWS CodeBuild to compile, test, and package."),
            ("c", "Amazon QuickSight to visualize dashboards."),
            ("d", "Amazon Rekognition to scan images."),
            ("e", "Amazon Polly to synthesize speech."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "CodePipeline orchestrates the CI/CD stages and CodeBuild runs the "
            "build and test steps. QuickSight, Rekognition, and Polly are "
            "unrelated to pipeline automation."
        ),
        "rationales": {
            "a": (True, "CodePipeline orchestrates the deployment stages."),
            "b": (True, "CodeBuild compiles, tests, and packages the app."),
            "c": (False, "QuickSight is BI dashboards, not CI/CD."),
            "d": (False, "Rekognition analyzes images, unrelated to pipelines."),
            "e": (False, "Polly is text-to-speech, not a build service."),
        },
    },
    {
        "question_id": "d2-eventbridge-vs-sqs-choice",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "One upstream service emits domain events that must reach multiple "
            "unrelated subscribers based on event attributes, while another path "
            "needs a durable work queue consumed by a single worker pool. Which "
            "pairing fits BEST?"
        ),
        "scenario_constraint": "Match routing-to-many versus buffered-work-to-one.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "SQS for fan-out to many; EventBridge for the single worker queue."),
            ("b", "API Gateway for both paths."),
            (
                "c",
                "EventBridge for attribute-based fan-out; SQS for the buffered single-consumer queue.",
            ),
            ("d", "Step Functions for both paths."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "EventBridge routes events to many subscribers by attributes, while "
            "SQS buffers work for a single consumer pool. The reversed pairing "
            "misuses each service, and API Gateway and Step Functions solve "
            "different problems."
        ),
        "rationales": {
            "a": (False, "SQS does not natively fan out by attributes to many subscribers."),
            "b": (False, "API Gateway is an API front door, not an event router or queue."),
            "c": (True, "EventBridge fans out by rules; SQS buffers for one consumer pool."),
            "d": (False, "Step Functions orchestrates workflows, not pub/sub or queuing."),
        },
    },
    {
        "question_id": "d2-canary-rollback-integration",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "After deploying a new GenAI API version via a canary, error rates "
            "spike for the canary slice. The pipeline should react without a "
            "human in the loop. Which capability fits BEST?"
        ),
        "scenario_constraint": "Automatically abort a bad canary.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Wait for a weekly review to notice the errors."),
            ("b", "Increase the canary traffic to gather more data."),
            ("c", "Disable monitoring to reduce alarm noise."),
            ("d", "Automated rollback triggered by a canary CloudWatch alarm."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "An alarm-triggered automated rollback reverts the canary the moment "
            "errors breach a threshold. Weekly review is too slow, raising canary "
            "traffic worsens impact, and disabling monitoring removes the safety "
            "signal."
        ),
        "rationales": {
            "a": (False, "A weekly review leaves the regression live for days."),
            "b": (False, "More canary traffic increases user impact of the fault."),
            "c": (False, "Disabling monitoring blinds the pipeline to failures."),
            "d": (True, "Alarm-driven rollback reverts the bad canary automatically."),
        },
    },
    {
        "question_id": "d2-outposts-data-jurisdiction",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A customer must keep certain inference and data processing on "
            "premises within their own facility for jurisdictional reasons, while "
            "using AWS tooling. Which AWS option BEST addresses this placement "
            "constraint?"
        ),
        "scenario_constraint": "Process on premises under AWS operations.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AWS Outposts in the customer's data center."),
            ("b", "A standard Region in another country."),
            ("c", "Amazon CloudFront edge caching."),
            ("d", "Multi-Region replication across continents."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Outposts extends AWS into the customer's own facility, satisfying "
            "on-premises jurisdictional placement. A foreign Region violates it, "
            "CloudFront caches content, and multi-Region replication spreads data "
            "wider."
        ),
        "rationales": {
            "a": (True, "Outposts runs AWS services within the customer's premises."),
            "b": (False, "A foreign Region fails the on-premises jurisdiction requirement."),
            "c": (False, "CloudFront caches delivery, not on-prem processing."),
            "d": (False, "Multi-Region replication moves data across jurisdictions."),
        },
    },
    {
        "question_id": "d2-wavelength-low-latency-edge",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A mobile GenAI feature requires single-digit-millisecond latency to "
            "end-user devices on a carrier's 5G network. Which AWS placement "
            "option is designed for ultra-low latency at the mobile edge?"
        ),
        "scenario_constraint": "Minimize latency to 5G mobile users.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AWS Wavelength zones embedded in telecom networks."),
            ("b", "A single central Region far from users."),
            ("c", "Amazon S3 Transfer Acceleration."),
            ("d", "AWS Outposts in a corporate office."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Wavelength places compute inside carrier networks for ultra-low "
            "latency to 5G devices. A distant central Region adds latency, S3 "
            "Transfer Acceleration speeds uploads, and office Outposts does not "
            "serve the mobile edge."
        ),
        "rationales": {
            "a": (True, "Wavelength sits in carrier networks for mobile-edge latency."),
            "b": (False, "A far central Region adds network latency for mobile users."),
            "c": (False, "Transfer Acceleration speeds S3 transfers, not inference latency."),
            "d": (False, "Office Outposts does not reach the 5G mobile edge."),
        },
    },
    {
        "question_id": "d2-event-driven-vs-sync-coupling",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A GenAI ingestion step and a downstream analytics team deploy on "
            "different schedules and must not block each other if one is "
            "temporarily down. Which integration style BEST reduces coupling?"
        ),
        "scenario_constraint": "Isolate two independently-evolving services from each other's downtime.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A synchronous HTTP call from one to the other."),
            ("b", "Asynchronous event-driven integration via a queue or event bus."),
            ("c", "A shared in-process library both import."),
            ("d", "A direct database connection shared by both."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Async event-driven integration lets each service run and deploy "
            "independently and tolerate the other's downtime. Synchronous calls, "
            "a shared library, and a shared database all tighten coupling."
        ),
        "rationales": {
            "a": (False, "A synchronous call fails when the callee is down."),
            "b": (True, "Async messaging decouples availability and deploy cadence."),
            "c": (False, "A shared library couples the two codebases tightly."),
            "d": (False, "A shared database couples schemas and availability."),
        },
    },
    {
        "question_id": "d2-apigw-request-validation",
        "objective_ids": ["AIP-2.3", "AIP-2.4"],
        "prompt": (
            "Malformed client payloads reach a GenAI Lambda and waste model "
            "invocations before failing. The team wants to reject invalid "
            "requests before any compute runs. Which control fits BEST?"
        ),
        "scenario_constraint": "Reject invalid requests before invoking compute.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Validate inside the model prompt."),
            ("b", "Let the Lambda call the model, then check the input."),
            ("c", "Define a request model and enable API Gateway request validation."),
            ("d", "Increase the Lambda memory to handle bad input faster."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "API Gateway request validation rejects malformed payloads at the "
            "edge before Lambda or the model runs. Prompt-level checks run after "
            "invocation, late validation already paid for compute, and more "
            "memory ignores the problem."
        ),
        "rationales": {
            "a": (False, "Prompt-level checks happen only after the model is invoked."),
            "b": (False, "Checking after the model call already wasted the invocation."),
            "c": (True, "Edge validation blocks bad payloads before any compute runs."),
            "d": (False, "More memory does not prevent processing invalid input."),
        },
    },
    {
        "question_id": "d2-dlq-poison-messages",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": (
            "A queue-driven GenAI worker keeps retrying a few malformed messages "
            "that can never succeed, blocking healthy messages behind them. Which "
            "mechanism BEST isolates the bad messages?"
        ),
        "scenario_constraint": "Prevent poison messages from blocking the queue.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Delete the entire queue and recreate it."),
            ("b", "Disable retries so all failures drop silently."),
            ("c", "Increase the visibility timeout indefinitely."),
            ("d", "Configure a dead-letter queue after a max receive count."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "A dead-letter queue moves repeatedly failing messages aside after a "
            "threshold so healthy ones flow. Recreating the queue loses work, "
            "disabling retries drops valid transient failures, and a huge "
            "visibility timeout stalls processing."
        ),
        "rationales": {
            "a": (False, "Recreating the queue discards all in-flight work."),
            "b": (False, "Disabling retries also drops recoverable transient failures."),
            "c": (False, "An endless visibility timeout freezes message processing."),
            "d": (True, "A DLQ isolates poison messages after a max receive count."),
        },
    },
    {
        "question_id": "d2-step-functions-vs-chained-lambda",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A team built a GenAI pipeline as five Lambdas each invoking the next "
            "directly, and debugging failures across them is painful with no "
            "central view of state. Which refactor MOST improves observability "
            "and error handling?"
        ),
        "scenario_constraint": "Gain centralized state and error handling across steps.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Merge all five Lambdas into one giant function."),
            ("b", "Add print statements to each Lambda."),
            ("c", "Orchestrate the Lambdas with a Step Functions state machine."),
            ("d", "Have each Lambda write to a shared text file."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Step Functions provides centralized state, visual execution history, "
            "and built-in retry/catch across steps. Merging into one function "
            "reduces modularity, print statements lack correlation, and a shared "
            "file is fragile."
        ),
        "rationales": {
            "a": (False, "One giant function loses modularity and step-level visibility."),
            "b": (False, "Scattered prints provide no correlated execution view."),
            "c": (True, "Step Functions centralizes state, history, and error handling."),
            "d": (False, "A shared file is race-prone and not a workflow tool."),
        },
    },
    {
        "question_id": "d2-blue-green-db-migration-risk",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "During a GenAI service rollout, the new version needs a backward "
            "compatible schema change so both old and new versions can run during "
            "the canary. Which practice BEST supports safe canary and rollback?"
        ),
        "scenario_constraint": "Keep both versions working during a gradual rollout.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Drop old columns immediately when the new version deploys."),
            ("b", "Apply additive, backward-compatible schema changes before shifting traffic."),
            ("c", "Rename tables the old version still reads."),
            ("d", "Require a full downtime window for every deploy."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Additive, backward-compatible changes let old and new versions "
            "coexist, preserving rollback during a canary. Dropping columns or "
            "renaming tables breaks the old version, and mandatory downtime "
            "defeats the gradual rollout."
        ),
        "rationales": {
            "a": (False, "Dropping columns breaks the still-running old version."),
            "b": (True, "Additive changes keep both versions functional during rollout."),
            "c": (False, "Renaming tables the old version reads causes failures."),
            "d": (False, "Mandatory downtime contradicts canary and quick rollback goals."),
        },
    },
    {
        "question_id": "d2-private-connectivity-vpc",
        "objective_ids": ["AIP-2.3", "AIP-3.1"],
        "prompt": (
            "A security policy forbids GenAI traffic to Bedrock from traversing "
            "the public internet. The workload runs in a VPC. Which approach "
            "keeps the traffic private with the least custom networking?"
        ),
        "scenario_constraint": "Reach Bedrock privately without public internet.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Use a VPC interface endpoint (PrivateLink) to Bedrock."),
            ("b", "Route traffic through a public NAT gateway."),
            ("c", "Assign public IPs to the workload instances."),
            ("d", "Open the security group to 0.0.0.0/0."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A VPC interface endpoint keeps Bedrock traffic on the AWS private "
            "network via PrivateLink. A NAT gateway and public IPs still traverse "
            "the internet, and opening the security group broadly worsens "
            "exposure."
        ),
        "rationales": {
            "a": (True, "A PrivateLink endpoint keeps traffic off the public internet."),
            "b": (False, "A NAT gateway still sends traffic over the public internet."),
            "c": (False, "Public IPs expose the workload to the internet."),
            "d": (False, "Opening the security group widely increases risk, not privacy."),
        },
    },
    {
        "question_id": "d2-idempotent-event-consumer",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": (
            "An EventBridge-driven GenAI consumer may receive the same event more "
            "than once because delivery is at-least-once, and reprocessing causes "
            "duplicate charges. Which design BEST prevents double effects?"
        ),
        "scenario_constraint": "Tolerate duplicate event delivery without double side effects.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Assume each event arrives exactly once."),
            ("b", "Process faster so duplicates are unlikely."),
            ("c", "Ignore the problem since duplicates are rare."),
            ("d", "Deduplicate on a stable event ID so repeats are no-ops."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Deduplicating on a stable event ID makes reprocessing a harmless "
            "no-op under at-least-once delivery. Assuming exactly-once is false, "
            "processing faster does not remove duplicates, and ignoring the issue "
            "leaves double charges."
        ),
        "rationales": {
            "a": (False, "At-least-once delivery means exactly-once cannot be assumed."),
            "b": (False, "Speed does not eliminate duplicate deliveries."),
            "c": (False, "Ignoring duplicates leaves the double-charge bug in place."),
            "d": (True, "Event-ID dedup makes repeated delivery idempotent."),
        },
    },
    {
        "question_id": "d2-apigw-throttle-protect-backend",
        "objective_ids": ["AIP-2.3", "AIP-2.2"],
        "prompt": (
            "A public GenAI endpoint occasionally gets flooded by a single "
            "client, exhausting the shared Bedrock quota for everyone. The team "
            "wants fair usage without manual intervention. Which control fits "
            "BEST?"
        ),
        "scenario_constraint": "Prevent one client from exhausting shared capacity.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Ask clients politely not to flood the API."),
            ("b", "Apply API Gateway usage plans with per-key rate and burst limits."),
            ("c", "Raise the Bedrock quota and hope it is enough."),
            ("d", "Disable the endpoint whenever a flood occurs."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Per-key usage plans enforce fair rate and burst limits so one client "
            "cannot starve others. Polite requests are unenforced, raising quotas "
            "just delays exhaustion, and disabling the endpoint harms all "
            "clients."
        ),
        "rationales": {
            "a": (False, "A polite request is not an enforced limit."),
            "b": (True, "Usage plans cap each client's rate, enforcing fairness."),
            "c": (False, "A bigger quota still gets exhausted by one abusive client."),
            "d": (False, "Disabling the endpoint penalizes everyone, not the abuser."),
        },
    },
    {
        "question_id": "d2-multi-account-governance",
        "objective_ids": ["AIP-2.3", "AIP-3.1"],
        "prompt": (
            "A large organization wants consistent guardrails, logging, and "
            "service control policies applied across many AWS accounts running "
            "GenAI workloads. Which approach fits BEST?"
        ),
        "scenario_constraint": "Enforce consistent org-wide policy across many accounts.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Email each account owner a list of rules to follow."),
            ("b", "Grant one person admin on every account to enforce rules."),
            ("c", "Manage accounts under AWS Organizations with service control policies."),
            ("d", "Rely on each team to configure its own policies independently."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "AWS Organizations with SCPs enforces guardrails and policy "
            "consistently across accounts. Emails and per-team configuration are "
            "unenforced and drift, and a single human admin does not scale or "
            "guarantee enforcement."
        ),
        "rationales": {
            "a": (False, "Emailed rules are advisory and drift over time."),
            "b": (False, "One human admin cannot reliably enforce org-wide policy."),
            "c": (True, "Organizations with SCPs enforces policy across all accounts."),
            "d": (False, "Independent per-team config produces inconsistent governance."),
        },
    },
    {
        "question_id": "d2-genai-gateway-model-routing",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": (
            "Through a central GenAI gateway, the team wants requests routed to a "
            "primary model but automatically sent to a secondary model if the "
            "primary is unavailable, transparent to callers. Which capability "
            "fits BEST?"
        ),
        "scenario_constraint": "Transparent failover between models at the gateway.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Returning an error to callers when the primary is down."),
            ("b", "Hard-coding the primary model in each client."),
            ("c", "Asking callers to retry a different model manually."),
            ("d", "A model routing policy with a fallback target at the gateway."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "A gateway routing policy with a fallback target redirects to the "
            "secondary model transparently on primary failure. Returning errors, "
            "hard-coding clients, and manual retries all push the problem onto "
            "callers."
        ),
        "rationales": {
            "a": (False, "Erroring out defeats the transparent-failover goal."),
            "b": (False, "Hard-coded clients cannot fail over to a secondary model."),
            "c": (False, "Manual caller retries are neither transparent nor automatic."),
            "d": (True, "A routing policy with fallback fails over transparently."),
        },
    },
    {
        "question_id": "d2-eventbridge-schema-evolution",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A producer must add a new optional field to events many GenAI "
            "consumers process, without forcing every consumer to redeploy at "
            "once. Which practice BEST supports this evolution?"
        ),
        "scenario_constraint": "Evolve event payloads without breaking existing consumers.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Add the field as optional and keep existing fields backward compatible."),
            ("b", "Rename existing fields in the same release."),
            ("c", "Remove unused fields consumers still read."),
            ("d", "Change the event type for every change."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Adding optional, backward-compatible fields lets old consumers keep "
            "working while new ones adopt the field. Renaming, removing read "
            "fields, and churning event types break existing consumers."
        ),
        "rationales": {
            "a": (True, "Optional additive fields preserve backward compatibility."),
            "b": (False, "Renaming fields breaks consumers that read the old names."),
            "c": (False, "Removing read fields breaks dependent consumers."),
            "d": (False, "Changing event types forces coordinated consumer redeploys."),
        },
    },
    {
        "question_id": "d2-cicd-model-eval-gate",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": (
            "A team wants its pipeline to block promotion of a new prompt or "
            "model version if automated quality evaluations regress below a "
            "threshold. Where does this check belong?"
        ),
        "scenario_constraint": "Prevent regressions from reaching production automatically.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "As an automated evaluation gate stage in the CI/CD pipeline."),
            ("b", "As a manual spot-check after release to production."),
            ("c", "As a note in the pull request description."),
            ("d", "As a monthly report reviewed later."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "An automated evaluation gate in the pipeline blocks promotion when "
            "quality regresses, before users are affected. Post-release checks, "
            "PR notes, and monthly reports all catch regressions too late."
        ),
        "rationales": {
            "a": (True, "A pipeline eval gate blocks regressions before promotion."),
            "b": (False, "A post-release check happens after users are exposed."),
            "c": (False, "A PR note is not an enforced gate."),
            "d": (False, "A monthly report detects regressions long after release."),
        },
    },
    {
        "question_id": "d2-sync-vs-async-ux-choice",
        "objective_ids": ["AIP-2.3", "AIP-2.2"],
        "prompt": (
            "A GenAI feature kicks off a report that takes two minutes to "
            "generate, and the web client must stay responsive without holding a "
            "connection open. Which integration pattern fits BEST?"
        ),
        "scenario_constraint": "Keep the client responsive during a long-running task.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Block the HTTP request for the full two minutes."),
            ("b", "Submit the job asynchronously and notify the client when results are ready."),
            ("c", "Reject the request as too slow."),
            ("d", "Shorten the report so it fits a synchronous call."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "An async submit-and-notify pattern frees the client while the "
            "two-minute job runs. Blocking risks timeouts, rejecting removes the "
            "feature, and arbitrarily shortening the report changes the "
            "requirement."
        ),
        "rationales": {
            "a": (False, "A two-minute blocking request risks gateway timeouts."),
            "b": (True, "Async submit with later notification keeps the client responsive."),
            "c": (False, "Rejecting the request abandons the needed feature."),
            "d": (False, "Shrinking the report changes the requirement, not the pattern."),
        },
    },
    {
        "question_id": "d2-invokemodel-sync-vs-stream",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A chat UI should display the model's answer token by token as it is "
            "generated so users see progress immediately. Which Bedrock API call "
            "fits BEST?"
        ),
        "scenario_constraint": "Deliver output incrementally as it is generated.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "InvokeModel returning the full response at once."),
            ("b", "A batch inference job."),
            ("c", "InvokeModelWithResponseStream for incremental tokens."),
            ("d", "A SageMaker async endpoint."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "InvokeModelWithResponseStream streams tokens as they are produced, "
            "ideal for progressive chat UIs. Plain InvokeModel waits for the full "
            "answer, batch is offline, and async writes results later to S3."
        ),
        "rationales": {
            "a": (False, "InvokeModel returns only after the full response is ready."),
            "b": (False, "Batch is offline and cannot stream to a live UI."),
            "c": (True, "Streaming delivers tokens incrementally to the UI."),
            "d": (False, "Async delivers a completed result later, not token-by-token."),
        },
    },
    {
        "question_id": "d2-backoff-jitter-throttle",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A client hitting Bedrock sees intermittent throttling, and naive "
            "immediate retries make it worse by synchronizing with other clients. "
            "Which TWO practices BEST handle the throttling? Select TWO."
        ),
        "scenario_constraint": "Retry throttled calls without synchronized retry storms.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Add random jitter to retry delays to de-synchronize clients."),
            ("b", "Use exponential backoff with a bounded maximum attempt cap."),
            ("c", "Retry immediately at a fixed interval forever."),
            ("d", "Retry only after a human restarts the service."),
            ("e", "Send more concurrent requests to push through the limit."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Jitter de-synchronizes retries while exponential backoff with an "
            "attempt cap bounds total effort, together easing throttling. Fixed "
            "immediate retries synchronize clients, manual restarts do not scale, "
            "and more concurrency deepens the throttle."
        ),
        "rationales": {
            "a": (True, "Jitter spreads retries so clients do not retry in lockstep."),
            "b": (True, "Capped exponential backoff bounds and paces retry attempts."),
            "c": (False, "Immediate fixed retries create synchronized retry storms."),
            "d": (False, "Manual restarts are slow and do not scale."),
            "e": (False, "More concurrency intensifies the throttling it faces."),
        },
    },
    {
        "question_id": "d2-retry-classification-4xx-5xx",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A client blindly retries every failed model call, including ones "
            "caused by a malformed request, wasting quota. Which retry policy is "
            "MOST correct?"
        ),
        "scenario_constraint": "Retry only errors that can succeed on retry.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Retry every error type the same way."),
            ("b", "Retry only validation errors, since they are the client's fault."),
            ("c", "Never retry any error."),
            ("d", "Retry throttling and transient server errors; do not retry validation errors."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Throttling and transient 5xx errors can succeed on retry, while a "
            "validation error will fail identically until the request is fixed. "
            "Retrying everything wastes quota, retrying only validation errors is "
            "pointless, and never retrying drops recoverable failures."
        ),
        "rationales": {
            "a": (False, "Uniform retries waste quota on non-retryable errors."),
            "b": (False, "Validation errors recur identically; retrying them is futile."),
            "c": (False, "Never retrying abandons recoverable transient failures."),
            "d": (True, "Retrying transient errors but not validation errors is correct."),
        },
    },
    {
        "question_id": "d2-context-window-overflow",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "A summarization endpoint intermittently fails when users paste very "
            "long documents, with errors about exceeding the input limit. Which "
            "TWO fixes directly address the cause? Select TWO."
        ),
        "scenario_constraint": "Keep input within the model's context window.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Chunk the input into context-window-sized pieces and summarize hierarchically."),
            ("b", "Truncate or compress input to fit the context window before invoking."),
            ("c", "Increase the request timeout."),
            ("d", "Add more retries with backoff."),
            ("e", "Raise the account's invocation quota."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "The failure is an input-size limit, so chunking hierarchically or "
            "compressing input to fit the context window resolves it. Timeouts, "
            "retries, and quota changes address latency or throttling, not "
            "oversized input."
        ),
        "rationales": {
            "a": (True, "Chunking keeps each request within the context window."),
            "b": (True, "Compressing input fits it inside the window before invoking."),
            "c": (False, "A longer timeout does not shrink oversized input."),
            "d": (False, "Retries re-send the same too-large input and fail again."),
            "e": (False, "A higher quota addresses throttling, not input length."),
        },
    },
    {
        "question_id": "d2-idempotency-key-invoke",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A client times out after sending a request that actually succeeded "
            "server-side, then retries, risking a duplicate billable action in a "
            "downstream mutating workflow. Which mechanism BEST prevents the "
            "duplicate?"
        ),
        "scenario_constraint": "Make a retried request produce one effect, not two.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Shorten the client timeout so retries happen sooner."),
            ("b", "Disable retries entirely."),
            ("c", "Send a client-generated idempotency key the server deduplicates on."),
            ("d", "Log duplicates and reconcile them manually later."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "An idempotency key lets the server recognize the retry as the same "
            "request and avoid a second effect. Shorter timeouts increase "
            "retries, disabling retries loses genuine failures, and manual "
            "reconciliation is reactive."
        ),
        "rationales": {
            "a": (False, "A shorter timeout makes duplicate retries more likely."),
            "b": (False, "Disabling retries loses recovery from real transient failures."),
            "c": (True, "An idempotency key collapses the retry into one effect."),
            "d": (False, "Manual reconciliation is reactive and error-prone."),
        },
    },
    {
        "question_id": "d2-timeout-vs-hang",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "Occasionally a model call never returns and the calling thread hangs "
            "indefinitely, exhausting the connection pool. Which configuration "
            "BEST prevents the hang?"
        ),
        "scenario_constraint": "Bound how long a single call may block.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Add more connections to the pool."),
            ("b", "Set explicit connect and read timeouts on the client."),
            ("c", "Increase the model's max tokens."),
            ("d", "Retry the call before the first one returns."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Explicit connect and read timeouts bound how long a call can block, "
            "freeing the thread and pool. A bigger pool only delays exhaustion, "
            "more tokens lengthen responses, and overlapping retries worsen "
            "resource use."
        ),
        "rationales": {
            "a": (False, "A larger pool postpones but does not prevent exhaustion."),
            "b": (True, "Timeouts cap blocking and release pooled connections."),
            "c": (False, "More tokens can make calls longer, not safer."),
            "d": (False, "Overlapping retries consume more connections, not fewer."),
        },
    },
    {
        "question_id": "d2-request-schema-validation",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A service occasionally sends a model request body missing a required "
            "field, discovering the problem only from a provider error. Which "
            "practice catches this earlier with the LEAST overhead?"
        ),
        "scenario_constraint": "Catch malformed request bodies before the API call.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Validate the request against a typed schema before invoking."),
            ("b", "Rely on the provider to reject bad requests."),
            ("c", "Add retries so a bad request eventually works."),
            ("d", "Wrap the call in a broad try/except that ignores errors."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Validating the request against a typed schema catches missing fields "
            "before the network call. Relying on provider rejection is late, "
            "retries cannot fix a structurally invalid body, and swallowing "
            "errors hides the bug."
        ),
        "rationales": {
            "a": (True, "Schema validation catches malformed requests pre-flight."),
            "b": (False, "Provider rejection is a late and wasteful signal."),
            "c": (False, "Retries cannot complete a structurally invalid request."),
            "d": (False, "Ignoring errors hides the defect rather than fixing it."),
        },
    },
    {
        "question_id": "d2-max-tokens-truncation",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "Users complain that long answers are cut off mid-sentence. Logs show "
            "the response stop reason is the output token limit. Which change "
            "MOST directly fixes the truncation?"
        ),
        "scenario_constraint": "Stop responses from being cut off by the output cap.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Lower the temperature."),
            ("b", "Add more retries."),
            ("c", "Switch to a smaller model."),
            ("d", "Raise the max-tokens output limit within the context budget."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "The stop reason indicates the output cap, so raising max tokens "
            "within the context budget prevents the cutoff. Temperature, retries, "
            "and a smaller model do not change the output-length limit."
        ),
        "rationales": {
            "a": (False, "Temperature affects word choice, not length limits."),
            "b": (False, "Retries reproduce the same truncated length."),
            "c": (False, "A smaller model does not raise the output limit."),
            "d": (True, "Raising the output token limit removes the mid-sentence cutoff."),
        },
    },
    {
        "question_id": "d2-streaming-error-mid-stream",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "During a streamed response, the connection drops after half the "
            "tokens arrive, yet the app currently shows the partial text as a "
            "completed answer. Which handling is MOST correct?"
        ),
        "scenario_constraint": "Never present an interrupted stream as a complete answer.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Treat the partial text as the final answer."),
            (
                "b",
                "Detect the incomplete stream, mark the result as failed/partial, and retry or surface an error.",
            ),
            ("c", "Pad the response with placeholder text to look complete."),
            ("d", "Silently discard the request and show nothing."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Detecting the interrupted stream and marking it partial prevents a "
            "false-success display, enabling retry or an honest error. Treating "
            "partial text as final, padding, or silent discard all misrepresent "
            "the outcome."
        ),
        "rationales": {
            "a": (False, "Showing partial text as final misleads the user."),
            "b": (True, "Flagging the partial stream avoids a false-success result."),
            "c": (False, "Padding fabricates content to fake completeness."),
            "d": (False, "Silent discard hides the failure with no recovery."),
        },
    },
    {
        "question_id": "d2-token-budget-prompt-response",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A request fails because the prompt plus requested output exceeds the "
            "model's total token budget. The team needs long answers but a very "
            "large system prompt. Which TWO adjustments directly reduce the "
            "overflow? Select TWO."
        ),
        "scenario_constraint": "Fit prompt plus output within the total token budget.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Trim or compress the system prompt to free input tokens."),
            ("b", "Reduce retrieved context to only the most relevant passages."),
            ("c", "Increase the client read timeout."),
            ("d", "Raise the account invocation quota."),
            ("e", "Set a higher temperature."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Trimming the system prompt and reducing retrieved context both free "
            "input tokens so prompt plus output fits the budget. Timeouts, "
            "quotas, and temperature do not change token consumption."
        ),
        "rationales": {
            "a": (True, "A smaller system prompt frees input tokens for output."),
            "b": (True, "Less retrieved context lowers input token consumption."),
            "c": (False, "A longer timeout does not change the token budget."),
            "d": (False, "Quota governs rate, not per-request token totals."),
            "e": (False, "Temperature affects sampling, not token counts."),
        },
    },
    {
        "question_id": "d2-converse-api-tool-use",
        "objective_ids": ["AIP-2.4", "AIP-2.1"],
        "prompt": (
            "A team wants a consistent request/response shape across multiple "
            "Bedrock models, including structured tool-use (function calling), "
            "without hand-coding each model's native payload. Which Bedrock API "
            "fits BEST?"
        ),
        "scenario_constraint": "Uniform multi-model messaging with built-in tool use.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A separate raw InvokeModel payload hand-built per model."),
            ("b", "SageMaker batch transform."),
            ("c", "The Bedrock Converse API with its unified message and tool schema."),
            ("d", "Amazon Translate."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "The Converse API gives a unified message format and tool-use schema "
            "across models, avoiding per-model payload code. Raw InvokeModel "
            "requires model-specific bodies, batch transform is offline, and "
            "Translate is unrelated."
        ),
        "rationales": {
            "a": (False, "Raw InvokeModel bodies differ per model and need hand-coding."),
            "b": (False, "Batch transform is for offline jobs, not interactive tool use."),
            "c": (True, "Converse standardizes messaging and tool use across models."),
            "d": (False, "Translate is a language-translation service."),
        },
    },
    {
        "question_id": "d2-circuit-breaker-dependency",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "When the model endpoint is failing hard, the app keeps hammering it "
            "with retries, amplifying load and slowing recovery. Which pattern "
            "BEST protects both sides during an outage?"
        ),
        "scenario_constraint": "Stop retry amplification during a sustained outage.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Unbounded retries until the endpoint recovers."),
            ("b", "A fixed one-second retry loop with no limit."),
            ("c", "Scaling up clients to push through the failures."),
            (
                "d",
                "A circuit breaker that stops calls after repeated failures and probes before resuming.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "A circuit breaker trips after repeated failures to stop amplifying "
            "load and probes before resuming, aiding recovery. Unbounded or fixed "
            "retry loops and scaling up clients all worsen the overload."
        ),
        "rationales": {
            "a": (False, "Unbounded retries pile load onto a failing endpoint."),
            "b": (False, "A fixed uncapped loop still amplifies the outage."),
            "c": (False, "More clients increase load during an outage."),
            "d": (True, "A circuit breaker halts amplification and probes for recovery."),
        },
    },
    {
        "question_id": "d2-streaming-backpressure",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A streaming response is produced faster than a slow client can "
            "consume it, and the server buffers tokens until memory grows "
            "dangerously. Which approach BEST manages this?"
        ),
        "scenario_constraint": "Match streaming production to slow consumer rate.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Apply backpressure so production pauses when the consumer lags."),
            ("b", "Buffer all tokens in memory until the client catches up."),
            ("c", "Drop random tokens to keep up."),
            ("d", "Disable streaming and send a huge single response instead."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Backpressure pauses production when the consumer lags, bounding "
            "memory. Unbounded buffering risks exhaustion, dropping tokens "
            "corrupts output, and reverting to one giant response ignores the "
            "slow consumer problem."
        ),
        "rationales": {
            "a": (True, "Backpressure caps memory by pausing fast production."),
            "b": (False, "Unbounded buffering can exhaust server memory."),
            "c": (False, "Dropping tokens corrupts the response content."),
            "d": (False, "A single giant response does not help a slow consumer."),
        },
    },
    {
        "question_id": "d2-structured-output-parsing",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A downstream system needs the model's answer as strict JSON, but the "
            "model sometimes wraps JSON in prose, breaking the parser. Which "
            "approach MOST reliably yields parseable output?"
        ),
        "scenario_constraint": "Guarantee machine-parseable structured output.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Use a tool/function-call schema or constrained JSON output and validate the result.",
            ),
            ("b", "Ask the model nicely to output only JSON."),
            ("c", "Regex-strip prose and hope the JSON remains valid."),
            ("d", "Increase max tokens so the JSON is longer."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A tool/function-call schema or constrained JSON mode plus validation "
            "reliably produces parseable structure. Polite prompts are "
            "inconsistent, regex stripping is brittle, and longer output does not "
            "guarantee validity."
        ),
        "rationales": {
            "a": (True, "Constrained schema output with validation yields reliable JSON."),
            "b": (False, "A polite request does not guarantee strict JSON."),
            "c": (False, "Regex stripping is fragile and can corrupt the JSON."),
            "d": (False, "More tokens do not make output structurally valid."),
        },
    },
    {
        "question_id": "d2-rate-limit-token-bucket",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A high-throughput client must stay just under the model's "
            "requests-per-second quota while allowing short bursts. Which "
            "client-side control fits BEST?"
        ),
        "scenario_constraint": "Respect a rate limit while permitting brief bursts.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "No client limiting; rely on server throttling."),
            ("b", "A token-bucket rate limiter sized to the quota with a small burst allowance."),
            ("c", "A hard one-request-at-a-time serialization."),
            ("d", "Random delays between every call."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "A token-bucket limiter paces requests to the quota and permits "
            "controlled bursts. Relying on server throttling causes errors, "
            "strict serialization wastes headroom, and random delays do not track "
            "the quota."
        ),
        "rationales": {
            "a": (False, "Depending on server throttling produces avoidable errors."),
            "b": (True, "Token-bucket pacing fits the quota and allows bursts."),
            "c": (False, "One-at-a-time serialization underuses available throughput."),
            "d": (False, "Random delays do not reliably respect the rate limit."),
        },
    },
    {
        "question_id": "d2-partial-failure-batch-items",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "A client sends many prompts in one logical operation; a few "
            "individual calls fail while most succeed. The current code reports "
            "the whole operation as success. Which handling is MOST correct?"
        ),
        "scenario_constraint": "Report partial failures accurately, not blanket success.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Report success if at least one call succeeded."),
            ("b", "Report failure only if every call failed."),
            ("c", "Track per-item outcomes and report successes and failures distinctly."),
            ("d", "Discard the failed items silently."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Per-item outcome tracking reports exactly which calls succeeded or "
            "failed, enabling targeted retry. Any-success or all-fail reporting "
            "hides partial failures, and discarding failures loses work silently."
        ),
        "rationales": {
            "a": (False, "Any-success reporting masks real failures."),
            "b": (False, "All-fail-only reporting hides mixed outcomes."),
            "c": (True, "Per-item results expose partial failures accurately."),
            "d": (False, "Silently discarding failures loses work and hides errors."),
        },
    },
    {
        "question_id": "d2-connection-reuse-client",
        "objective_ids": ["AIP-2.4", "AIP-2.2"],
        "prompt": (
            "A Lambda recreates a fresh Bedrock client on every invocation, "
            "adding handshake latency. Which change reduces this overhead with "
            "the LEAST risk?"
        ),
        "scenario_constraint": "Avoid rebuilding the client on every call.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Create two clients per invocation for redundancy."),
            ("b", "Open a new TLS connection per request deliberately."),
            ("c", "Store the client in a database between calls."),
            (
                "d",
                "Initialize the client once outside the handler and reuse it across invocations.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Initializing the client outside the handler reuses it across warm "
            "invocations, cutting setup latency. Extra clients add overhead, "
            "forcing new connections hurts, and clients are not serializable to a "
            "database."
        ),
        "rationales": {
            "a": (False, "Two clients per call doubles setup overhead."),
            "b": (False, "Forcing new connections adds the latency we want to remove."),
            "c": (False, "A live client cannot be stored and reloaded from a database."),
            "d": (True, "Module-scope client reuse avoids per-call setup latency."),
        },
    },
    {
        "question_id": "d2-deterministic-output-temperature",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "An integration test asserts the model's exact output, but it flakes "
            "because responses vary run to run. Which parameter change MOST "
            "reduces this variability for testing?"
        ),
        "scenario_constraint": "Make outputs as repeatable as possible for tests.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase max tokens."),
            ("b", "Add more retries to the test."),
            ("c", "Set temperature (and top-p) to minimal values to reduce randomness."),
            ("d", "Use a larger context window."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Minimizing temperature and top-p reduces sampling randomness, making "
            "outputs more repeatable. Token limits, retries, and context size do "
            "not control output variability."
        ),
        "rationales": {
            "a": (False, "Max tokens changes length, not variability."),
            "b": (False, "Retries do not make a stochastic output deterministic."),
            "c": (True, "Low temperature/top-p reduces output randomness."),
            "d": (False, "Context size does not control sampling randomness."),
        },
    },
    {
        "question_id": "d2-streaming-first-token-latency",
        "objective_ids": ["AIP-2.4", "AIP-2.2"],
        "prompt": (
            "Users perceive the assistant as slow even though total generation "
            "time is fine, because nothing appears until the whole answer is "
            "ready. Which change MOST improves perceived responsiveness?"
        ),
        "scenario_constraint": "Reduce perceived latency without faster total generation.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Reduce the output length drastically."),
            ("b", "Stream the response so the first tokens appear quickly."),
            ("c", "Precompute all possible answers."),
            ("d", "Lower temperature to speed generation."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Streaming surfaces the first tokens quickly, improving perceived "
            "responsiveness even at the same total time. Cutting length changes "
            "the answer, precomputing is infeasible for open prompts, and "
            "temperature does not materially change latency."
        ),
        "rationales": {
            "a": (False, "Shortening the answer changes the content, not perception alone."),
            "b": (True, "Streaming shows early tokens, improving perceived speed."),
            "c": (False, "Precomputing every answer is infeasible for open-ended prompts."),
            "d": (False, "Temperature does not meaningfully change latency."),
        },
    },
    {
        "question_id": "d2-response-schema-validation-output",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "A downstream service occasionally crashes on an unexpected model "
            "response shape. The team wants to fail safely at the boundary rather "
            "than propagate bad data. Which practice fits BEST?"
        ),
        "scenario_constraint": "Contain malformed model responses at the integration boundary.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Validate the response against an expected schema and handle validation failures explicitly.",
            ),
            ("b", "Pass the raw response straight to the downstream service."),
            ("c", "Assume the response is always well-formed."),
            ("d", "Catch all exceptions downstream and ignore them."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Validating the response against an expected schema at the boundary "
            "lets the app fail safely instead of crashing downstream. Passing raw "
            "data, assuming correctness, and blanket-ignoring errors all "
            "propagate or hide the fault."
        ),
        "rationales": {
            "a": (True, "Boundary schema validation contains malformed responses safely."),
            "b": (False, "Raw pass-through propagates bad data downstream."),
            "c": (False, "Assuming correctness is exactly what causes the crash."),
            "d": (False, "Ignoring downstream exceptions hides the real defect."),
        },
    },
    {
        "question_id": "d2-pagination-long-conversation",
        "objective_ids": ["AIP-2.4", "AIP-2.1"],
        "prompt": (
            "A long multi-turn conversation keeps growing until each request "
            "nears the context limit and latency climbs. Which strategy BEST "
            "keeps requests within budget while preserving continuity?"
        ),
        "scenario_constraint": "Bound growing conversation history within the context window.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Always resend the entire raw history."),
            ("b", "Drop the most recent turns to save space."),
            ("c", "Increase temperature to compensate."),
            ("d", "Summarize or window older turns while keeping recent ones verbatim."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Summarizing or windowing older turns while keeping recent ones "
            "verbatim bounds tokens and preserves continuity. Resending "
            "everything overflows, dropping recent turns loses the most relevant "
            "context, and temperature is irrelevant."
        ),
        "rationales": {
            "a": (False, "Resending full history grows past the context limit."),
            "b": (False, "Dropping recent turns discards the most relevant context."),
            "c": (False, "Temperature does not reduce conversation token size."),
            "d": (True, "Summarizing old turns bounds tokens while keeping continuity."),
        },
    },
    {
        "question_id": "d2-retry-after-header",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "When throttled, the provider returns guidance on how long to wait "
            "before retrying. A client ignores it and retries immediately. Which "
            "behavior is MOST correct?"
        ),
        "scenario_constraint": "Honor provider-signaled retry timing.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Ignore the guidance and retry as fast as possible."),
            ("b", "Respect the suggested wait before retrying, combined with jittered backoff."),
            ("c", "Stop retrying permanently on the first throttle."),
            ("d", "Switch to a different account to bypass the limit."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Honoring the suggested wait with jittered backoff aligns retries "
            "with provider guidance and avoids storms. Ignoring it worsens "
            "throttling, permanent stop drops recoverable calls, and account "
            "hopping is an abuse pattern."
        ),
        "rationales": {
            "a": (False, "Immediate retries ignore guidance and deepen throttling."),
            "b": (True, "Respecting the retry hint plus jitter avoids retry storms."),
            "c": (False, "Stopping forever drops recoverable transient throttles."),
            "d": (False, "Account hopping to dodge limits is abusive and brittle."),
        },
    },
    {
        "question_id": "d2-embedding-request-batching",
        "objective_ids": ["AIP-2.4", "AIP-2.2"],
        "prompt": (
            "An indexing job calls an embeddings model once per text snippet for "
            "millions of snippets, driving high overhead and throttling. Which "
            "change MOST improves throughput and cost?"
        ),
        "scenario_constraint": "Reduce per-call overhead at embedding scale.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase the embedding dimension."),
            ("b", "Call the model twice per snippet for accuracy."),
            ("c", "Batch multiple snippets per embedding request where supported."),
            ("d", "Raise the output max tokens."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Batching snippets per request amortizes overhead and reduces call "
            "count, easing throttling and cost. Larger dimensions, double calls, "
            "and output token changes do not reduce per-call overhead."
        ),
        "rationales": {
            "a": (False, "A larger embedding dimension does not reduce call overhead."),
            "b": (False, "Calling twice doubles cost without throughput gain."),
            "c": (True, "Batching cuts call count and per-request overhead."),
            "d": (False, "Output token limits are irrelevant to embedding batching."),
        },
    },
    {
        "question_id": "d2-bedrock-data-automation-ingest",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A team must extract structured fields from a large mix of scanned "
            "PDFs, images, and documents to feed a GenAI pipeline, without "
            "building custom parsing per format. Which AWS capability fits BEST?"
        ),
        "scenario_constraint": "Automate structured extraction from mixed unstructured content.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A hand-written regex parser for each document type."),
            ("b", "Amazon Polly to read the documents aloud."),
            ("c", "Amazon SNS to notify on new uploads."),
            (
                "d",
                "Amazon Bedrock Data Automation to process the documents into structured output.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Bedrock Data Automation turns mixed unstructured documents into "
            "structured output without per-format custom code. Hand-written regex "
            "is brittle, Polly is text-to-speech, and SNS only sends "
            "notifications."
        ),
        "rationales": {
            "a": (False, "Per-format regex parsers are brittle and high-maintenance."),
            "b": (False, "Polly synthesizes speech, not structured extraction."),
            "c": (False, "SNS sends notifications and does not parse documents."),
            "d": (True, "Data Automation extracts structure from mixed documents natively."),
        },
    },
    {
        "question_id": "d2-model-routing-fallback-policy",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "An application must prefer a cost-efficient model but automatically "
            "fall back to a stronger model when the primary returns low "
            "confidence or errors, transparently to users. Which design fits "
            "BEST?"
        ),
        "scenario_constraint": "Automatic, transparent fallback between models.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A model routing policy with defined fallback conditions and targets."),
            ("b", "A fixed single model with no fallback."),
            ("c", "Returning an error whenever the primary struggles."),
            ("d", "Asking the user to choose a model each time."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A routing policy with explicit fallback conditions redirects to the "
            "stronger model automatically and transparently. A single fixed model "
            "has no fallback, erroring out breaks the UX, and asking the user is "
            "not transparent."
        ),
        "rationales": {
            "a": (True, "A routing policy with fallback handles low confidence transparently."),
            "b": (False, "A single fixed model offers no fallback path."),
            "c": (False, "Erroring out abandons the request instead of recovering."),
            "d": (False, "User model selection is neither automatic nor transparent."),
        },
    },
    {
        "question_id": "d2-duplicate-event-at-least-once",
        "objective_ids": ["AIP-2.5", "AIP-2.3"],
        "prompt": (
            "A GenAI workflow triggered by at-least-once message delivery "
            "occasionally sends a customer two identical emails. Which fix MOST "
            "directly prevents the duplicate side effect?"
        ),
        "scenario_constraint": "Prevent duplicate side effects under at-least-once delivery.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Make the handler idempotent by recording processed message IDs."),
            ("b", "Switch the queue to best-effort delivery."),
            ("c", "Add a delay before sending each email."),
            ("d", "Increase the consumer count."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Recording processed message IDs makes reprocessing a no-op, "
            "preventing duplicate emails. Best-effort delivery risks losing "
            "messages, a delay does not stop duplicates, and more consumers can "
            "increase concurrent duplicates."
        ),
        "rationales": {
            "a": (True, "Tracking processed IDs makes the handler idempotent."),
            "b": (False, "Best-effort delivery trades duplicates for lost messages."),
            "c": (False, "A delay does not prevent a second delivery from sending."),
            "d": (False, "More consumers can process duplicates in parallel."),
        },
    },
    {
        "question_id": "d2-trace-correlation-xray",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A request flows through API Gateway, Lambda, a model call, and a "
            "downstream service, and the team cannot follow one request across "
            "them during incidents. Which TWO practices BEST provide end-to-end "
            "traceability? Select TWO."
        ),
        "scenario_constraint": "Correlate one request across multiple services.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Enable AWS X-Ray distributed tracing across the services."),
            ("b", "Propagate a correlation/trace ID and include it in each service's logs."),
            ("c", "Keep separate unlinked logs in each service."),
            ("d", "Rely on a single CloudWatch metric for total errors."),
            ("e", "Manually grep timestamps across log groups."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "X-Ray links segments into one trace, and a propagated correlation ID "
            "ties every log line to the same request. Unlinked logs, a single "
            "aggregate metric, and manual timestamp grepping cannot reliably "
            "stitch a request across services."
        ),
        "rationales": {
            "a": (True, "X-Ray correlates segments into one end-to-end trace."),
            "b": (True, "A propagated correlation ID links logs to one request."),
            "c": (False, "Unlinked per-service logs cannot be tied to one request."),
            "d": (False, "An aggregate error metric lacks per-request correlation."),
            "e": (False, "Manual timestamp matching is unreliable and slow."),
        },
    },
    {
        "question_id": "d2-no-false-success-throttle",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A pipeline marks a step 'completed' even when the model call was "
            "throttled and returned no usable output. Which correction is MOST "
            "important?"
        ),
        "scenario_constraint": "Do not record success when the operation did not complete.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Mark success on any HTTP 200, regardless of body."),
            ("b", "Only mark success after a validated, complete response is received."),
            ("c", "Mark success when the call returns at all."),
            ("d", "Mark success optimistically and fix problems later."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Recording success only after a validated complete response prevents "
            "false-success on throttled or empty results. Trusting a 200, any "
            "return, or optimism all record success that did not happen."
        ),
        "rationales": {
            "a": (False, "A 200 with a throttled or empty body is not real success."),
            "b": (True, "Validated completion is the only honest success signal."),
            "c": (False, "A returned call can still carry a failure payload."),
            "d": (False, "Optimistic success hides failures until later damage."),
        },
    },
    {
        "question_id": "d2-prompt-chain-decompose",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A single mega-prompt tries to extract entities, classify, and "
            "summarize at once and produces inconsistent results. The team wants "
            "more reliable, debuggable steps. Which approach fits BEST?"
        ),
        "scenario_constraint": "Improve reliability of a complex multi-task prompt.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Add more instructions to the single prompt."),
            ("b", "Increase temperature for creativity."),
            (
                "c",
                "Decompose into a prompt chain where each step does one task and feeds the next.",
            ),
            ("d", "Raise max tokens so all three fit."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "A prompt chain isolates each task into a verifiable step, improving "
            "reliability and debuggability. Piling more instructions onto one "
            "prompt, raising temperature, or increasing tokens does not fix the "
            "entanglement."
        ),
        "rationales": {
            "a": (False, "More instructions deepen the overloaded single prompt."),
            "b": (False, "Higher temperature increases variability, not reliability."),
            "c": (True, "Chaining single-task steps improves reliability and debugging."),
            "d": (False, "More tokens let the tangled prompt run longer, not better."),
        },
    },
    {
        "question_id": "d2-amazon-q-developer-use",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "Developers want an AWS-native assistant integrated into their IDE to "
            "explain code, suggest fixes, and help with AWS APIs while building "
            "the GenAI app. Which service fits BEST?"
        ),
        "scenario_constraint": "In-IDE AWS-native coding assistance.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Amazon Bedrock Guardrails."),
            ("b", "Amazon Kendra."),
            ("c", "AWS Glue."),
            ("d", "Amazon Q Developer."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Amazon Q Developer is the AWS-native in-IDE assistant for code and "
            "AWS guidance. Guardrails enforce safety, Kendra is enterprise "
            "search, and Glue is ETL."
        ),
        "rationales": {
            "a": (False, "Guardrails filter content, not assist coding."),
            "b": (False, "Kendra is enterprise search, not an IDE assistant."),
            "c": (False, "Glue is an ETL service, unrelated to IDE help."),
            "d": (True, "Q Developer is the AWS in-IDE coding assistant."),
        },
    },
    {
        "question_id": "d2-embedding-drift-detection",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "After upgrading the embedding model, retrieval quality drops because "
            "old vectors in the index were produced by the previous model. Which "
            "action MOST directly resolves the mismatch?"
        ),
        "scenario_constraint": "Resolve inconsistency between old and new embeddings.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Keep the old vectors and query with the new model."),
            ("b", "Increase the number of retrieved results."),
            ("c", "Re-embed the corpus with the new model so all vectors share one space."),
            ("d", "Lower the similarity threshold."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Vectors from different embedding models live in incompatible spaces, "
            "so re-embedding the corpus with the new model restores consistency. "
            "Mixing models, returning more results, or lowering thresholds only "
            "mask the mismatch."
        ),
        "rationales": {
            "a": (False, "Mixing model spaces produces unreliable similarity scores."),
            "b": (False, "More results do not fix incompatible vector spaces."),
            "c": (True, "Re-embedding aligns all vectors in a single model's space."),
            "d": (False, "A looser threshold returns more noise, not better matches."),
        },
    },
    {
        "question_id": "d2-cloudwatch-logs-insights-debug",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "During an incident, the team must quickly query structured "
            "application logs across many Lambda invocations to find failing "
            "requests by error code and latency. Which tool fits BEST?"
        ),
        "scenario_constraint": "Ad hoc querying of structured logs at scale.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Downloading each log stream to a laptop."),
            ("b", "Amazon CloudWatch Logs Insights queries."),
            ("c", "A single error-count dashboard with no detail."),
            ("d", "Amazon QuickSight pie charts."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "CloudWatch Logs Insights runs ad hoc queries over structured logs "
            "across invocations to filter by fields like error code and latency. "
            "Manual downloads do not scale, an aggregate dashboard lacks detail, "
            "and QuickSight is for BI reporting."
        ),
        "rationales": {
            "a": (False, "Downloading streams manually is slow and unscalable."),
            "b": (True, "Logs Insights queries structured logs at scale by field."),
            "c": (False, "An aggregate dashboard lacks per-request detail."),
            "d": (False, "QuickSight is BI visualization, not log querying."),
        },
    },
    {
        "question_id": "d2-partial-stream-false-success",
        "objective_ids": ["AIP-2.5", "AIP-2.4"],
        "prompt": (
            "A monitoring job marks streamed generations as successful based on "
            "receiving the first chunk, but some streams error after that chunk. "
            "Which TWO corrections BEST ensure accurate status? Select TWO."
        ),
        "scenario_constraint": "Status must reflect full stream completion, not partial receipt.",
        "difficulty": "hard",
        "question_format": "multiple_response",
        "options": [
            ("a", "Only mark success when the stream signals a clean end-of-response."),
            ("b", "Treat a mid-stream error as a failure needing retry or surfacing."),
            ("c", "Mark success as soon as the first chunk arrives."),
            ("d", "Count the number of chunks as the success criterion."),
            ("e", "Ignore stream errors to keep metrics green."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Requiring a clean end-of-response and treating mid-stream errors as "
            "failures makes status reflect real completion. First-chunk success, "
            "chunk counting, and ignoring errors all produce false-success "
            "signals."
        ),
        "rationales": {
            "a": (True, "A clean end-of-stream signal is the correct success condition."),
            "b": (True, "Mid-stream errors must be treated as failures, not successes."),
            "c": (False, "First-chunk arrival does not prove completion."),
            "d": (False, "Chunk count does not confirm a clean completion."),
            "e": (False, "Ignoring errors manufactures false-green metrics."),
        },
    },
    {
        "question_id": "d2-fallback-degraded-response",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "When the primary model and its fallback are both unavailable, the "
            "app should still respond usefully rather than crash. Which behavior "
            "is MOST appropriate?"
        ),
        "scenario_constraint": "Degrade gracefully when all models are unavailable.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Return a clear degraded response (cached guidance or an honest unavailable message).",
            ),
            ("b", "Return a fabricated answer so the UI looks normal."),
            ("c", "Hang the request until a model recovers."),
            ("d", "Return an unhandled stack trace to the user."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A clear degraded response keeps the app usable and honest when all "
            "models are down. Fabricated answers mislead, hanging the request "
            "harms UX, and leaking a stack trace exposes internals and still "
            "fails."
        ),
        "rationales": {
            "a": (True, "An honest degraded response is usable and truthful."),
            "b": (False, "A fabricated answer deceives the user."),
            "c": (False, "Hanging indefinitely harms the user experience."),
            "d": (False, "A raw stack trace leaks internals and fails the user."),
        },
    },
    {
        "question_id": "d2-rag-stale-index-debug",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "Users report the assistant cites outdated policy even though the "
            "source documents were updated last week. The retrieval index was "
            "last built a month ago. Which action MOST directly fixes this?"
        ),
        "scenario_constraint": "Serve current content from a stale retrieval index.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase the model's temperature."),
            ("b", "Add more retrieved chunks per query."),
            ("c", "Switch to a bigger generation model."),
            ("d", "Re-ingest and reindex the updated documents."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "The index predates the document updates, so re-ingesting and "
            "reindexing brings current content into retrieval. Temperature, more "
            "chunks, and a bigger model cannot surface documents the index does "
            "not contain."
        ),
        "rationales": {
            "a": (False, "Temperature cannot retrieve content missing from the index."),
            "b": (False, "More chunks from a stale index are still stale."),
            "c": (False, "A bigger model cannot cite documents it never retrieved."),
            "d": (True, "Reindexing the updated documents makes current content retrievable."),
        },
    },
    {
        "question_id": "d2-structured-logging-correlation-id",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "To debug cross-service GenAI failures, the team wants every log line "
            "for a request tagged so they can filter one request's journey. Which "
            "practice fits BEST?"
        ),
        "scenario_constraint": "Tie all logs of one request together.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Log everything as free-form text with no IDs."),
            ("b", "Propagate a correlation/request ID and include it in structured logs."),
            ("c", "Rely on wall-clock timestamps alone."),
            ("d", "Log only errors, not the request flow."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "A propagated correlation ID in structured logs lets the team filter "
            "one request across services. Free-form text, timestamps alone, and "
            "error-only logging cannot reliably reconstruct a single request's "
            "path."
        ),
        "rationales": {
            "a": (False, "Free-form text without IDs is not reliably filterable."),
            "b": (True, "A correlation ID in structured logs filters one request end to end."),
            "c": (False, "Timestamps alone cannot disambiguate concurrent requests."),
            "d": (False, "Error-only logs omit the successful-path context needed."),
        },
    },
    {
        "question_id": "d2-model-router-cost-quality",
        "objective_ids": ["AIP-2.5", "AIP-2.2"],
        "prompt": (
            "A production router must decide per request whether to use a cheap "
            "or premium model based on query complexity, and the team wants to "
            "tune this without redeploying code. Which approach fits BEST?"
        ),
        "scenario_constraint": "Adjust routing behavior without code redeploys.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Hard-code the thresholds in the application source."),
            ("b", "Pick a model at random per request."),
            ("c", "Externalize the routing policy as configuration the router reads at runtime."),
            ("d", "Always use the premium model to be safe."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Externalizing the routing policy as runtime configuration lets the "
            "team tune thresholds without redeploying. Hard-coding requires "
            "redeploys, random choice ignores complexity, and always-premium "
            "overpays."
        ),
        "rationales": {
            "a": (False, "Hard-coded thresholds require a redeploy to change."),
            "b": (False, "Random selection ignores query complexity."),
            "c": (True, "Config-driven routing is tunable without code changes."),
            "d": (False, "Always-premium routing wastes budget on easy queries."),
        },
    },
    {
        "question_id": "d2-timeout-cascade-debug",
        "objective_ids": ["AIP-2.5", "AIP-2.4"],
        "prompt": (
            "An API Gateway endpoint returns 504s during model slowness because "
            "the Lambda waits longer than the gateway's integration timeout. "
            "Which fix MOST directly aligns the timeouts?"
        ),
        "scenario_constraint": "Align downstream timeout with the gateway integration timeout.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase the model's max tokens."),
            ("b", "Remove all timeouts from the Lambda."),
            ("c", "Retry the whole request from the client indefinitely."),
            (
                "d",
                "Set the model call timeout below the gateway integration timeout and return a controlled error.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Setting the model-call timeout below the gateway timeout lets the "
            "Lambda return a controlled error before the gateway 504s. More "
            "tokens worsen latency, removing timeouts causes hangs, and endless "
            "client retries amplify load."
        ),
        "rationales": {
            "a": (False, "More tokens increase latency and worsen the timeout."),
            "b": (False, "Removing timeouts causes indefinite hangs."),
            "c": (False, "Endless client retries add load during slowness."),
            "d": (True, "A shorter downstream timeout yields a controlled error before 504."),
        },
    },
    {
        "question_id": "d2-bedrock-data-automation-vs-textract",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A GenAI workflow needs an integrated service that both extracts "
            "content from multimodal documents and prepares normalized output "
            "ready for downstream generative processing in one managed flow. "
            "Which option fits BEST?"
        ),
        "scenario_constraint": "One managed flow from multimodal input to GenAI-ready output.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Amazon Bedrock Data Automation."),
            ("b", "A custom chain of unrelated single-purpose scripts."),
            ("c", "Amazon SQS as the extraction engine."),
            ("d", "Amazon CloudFront to transform documents."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Bedrock Data Automation provides a managed flow that processes "
            "multimodal documents into normalized, GenAI-ready output. Ad hoc "
            "scripts are brittle, SQS is a queue, and CloudFront is a CDN."
        ),
        "rationales": {
            "a": (True, "Data Automation is the managed multimodal-to-GenAI pipeline."),
            "b": (False, "A chain of ad hoc scripts is brittle and unmanaged."),
            "c": (False, "SQS queues messages; it does not extract content."),
            "d": (False, "CloudFront delivers content and does not transform documents."),
        },
    },
    {
        "question_id": "d2-dedupe-store-ttl",
        "objective_ids": ["AIP-2.5", "AIP-2.1"],
        "prompt": (
            "To deduplicate events, a team stores processed IDs in DynamoDB but "
            "the table grows unbounded over years. They need dedup within a "
            "practical window without manual cleanup. Which change fits BEST?"
        ),
        "scenario_constraint": "Bound dedup storage growth automatically.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Add a DynamoDB TTL so old dedup records expire automatically."),
            ("b", "Never delete records to be safe."),
            ("c", "Store IDs in a Lambda in-memory set."),
            ("d", "Truncate the table manually each quarter."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A DynamoDB TTL expires dedup records after the needed window, "
            "bounding growth without manual work. Never deleting grows unbounded, "
            "in-memory sets vanish between invocations, and manual truncation is "
            "error-prone."
        ),
        "rationales": {
            "a": (True, "TTL automatically expires old dedup entries."),
            "b": (False, "Never deleting lets the table grow without bound."),
            "c": (False, "In-memory sets do not persist across invocations."),
            "d": (False, "Manual quarterly truncation is error-prone and risky."),
        },
    },
    {
        "question_id": "d2-hallucination-grounding-debug",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A support bot confidently invents product features that do not "
            "exist. Which TWO changes MOST directly reduce these fabrications by "
            "grounding answers in the real catalog? Select TWO."
        ),
        "scenario_constraint": "Ground answers in authoritative source data.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Add retrieval over the product catalog as grounding context."),
            ("b", "Instruct the model to answer only from the retrieved context."),
            ("c", "Increase the model's temperature."),
            ("d", "Make the system prompt longer and more emphatic."),
            ("e", "Switch to a model with a larger context window only."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Retrieving catalog context and constraining the model to answer only "
            "from it directly reduces fabrication. Higher temperature worsens it, "
            "a longer prompt is weak alone, and a bigger context window adds no "
            "real data."
        ),
        "rationales": {
            "a": (True, "Retrieval supplies authoritative grounding content."),
            "b": (True, "Constraining to retrieved context curbs invented details."),
            "c": (False, "Higher temperature increases, not reduces, fabrication."),
            "d": (False, "A longer prompt is unreliable without grounding data."),
            "e": (False, "A bigger context window alone adds no authoritative content."),
        },
    },
    {
        "question_id": "d2-canary-metric-regression-detect",
        "objective_ids": ["AIP-2.5", "AIP-2.3"],
        "prompt": (
            "After a prompt change, user-visible answer quality quietly degraded "
            "but no system errors fired, so monitoring stayed green. Which "
            "addition would have caught this regression?"
        ),
        "scenario_constraint": "Detect quality regressions that raise no system errors.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Watch only CPU and memory utilization."),
            (
                "b",
                "Track output-quality metrics (automated evals or feedback signals), not just system errors.",
            ),
            ("c", "Alert only on HTTP 5xx rates."),
            ("d", "Count total invocations per minute."),
        ],
        "correct_option_ids": ["b"],
        "explanation": (
            "Quality metrics from automated evals or user feedback catch "
            "regressions that throw no system errors. Infrastructure utilization, "
            "5xx rates, and invocation counts all stay green while answer quality "
            "silently drops."
        ),
        "rationales": {
            "a": (False, "Resource utilization is blind to answer quality."),
            "b": (True, "Quality signals detect degradations that raise no errors."),
            "c": (False, "5xx rates miss silent quality regressions."),
            "d": (False, "Invocation counts say nothing about answer quality."),
        },
    },
    {
        "question_id": "d2-prompt-chain-error-propagation",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "In a prompt chain, an early step occasionally returns empty output, "
            "and later steps silently produce nonsense from it. Which practice "
            "BEST contains the failure?"
        ),
        "scenario_constraint": "Stop a failed chain step from corrupting later steps.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Always feed whatever the previous step returned to the next."),
            ("b", "Increase temperature on later steps."),
            (
                "c",
                "Validate each step's output and halt or retry the chain on invalid intermediate results.",
            ),
            ("d", "Combine all steps back into one prompt."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Validating each intermediate result and halting or retrying on "
            "invalid output stops error propagation through the chain. Blindly "
            "forwarding output spreads the fault, more temperature adds noise, "
            "and recombining steps loses the chain's benefits."
        ),
        "rationales": {
            "a": (False, "Forwarding bad output lets the error cascade downstream."),
            "b": (False, "More temperature adds randomness, not error containment."),
            "c": (True, "Validating intermediates halts propagation of a bad step."),
            "d": (False, "Recombining into one prompt discards the chain's structure."),
        },
    },
    {
        "question_id": "d2-throttle-vs-error-metric-confusion",
        "objective_ids": ["AIP-2.5", "AIP-2.4"],
        "prompt": (
            "An on-call engineer sees rising failures but cannot tell whether "
            "they are throttling, validation, or server errors, slowing "
            "diagnosis. Which improvement MOST speeds root-cause analysis?"
        ),
        "scenario_constraint": "Distinguish failure categories during an incident.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Emit a single combined failure counter."),
            ("b", "Log failures only as generic exceptions."),
            ("c", "Suppress error logs to reduce noise."),
            ("d", "Emit per-category error metrics (throttling, validation, server, timeout)."),
        ],
        "correct_option_ids": ["d"],
        "explanation": (
            "Per-category error metrics let the engineer immediately see whether "
            "throttling, validation, or server errors dominate. A single counter, "
            "generic logs, and suppressed logs all obscure the failure type."
        ),
        "rationales": {
            "a": (False, "A single counter hides which failure type is rising."),
            "b": (False, "Generic exceptions lack the category needed to diagnose."),
            "c": (False, "Suppressing logs removes the signal needed for diagnosis."),
            "d": (True, "Categorized metrics pinpoint the dominant failure type fast."),
        },
    },
    {
        "question_id": "d2-retry-storm-amplification",
        "objective_ids": ["AIP-2.5", "AIP-2.4"],
        "prompt": (
            "During a brief model slowdown, aggressive client retries turned a "
            "minor blip into a full outage. Which TWO changes BEST prevent this "
            "amplification next time? Select TWO."
        ),
        "scenario_constraint": "Prevent retries from amplifying a transient slowdown.",
        "difficulty": "hard",
        "question_format": "multiple_response",
        "options": [
            ("a", "Use exponential backoff with jitter and a bounded attempt cap."),
            ("b", "Add a circuit breaker that trips during sustained failures."),
            ("c", "Retry immediately and infinitely to recover faster."),
            ("d", "Increase the client fleet size during incidents."),
            ("e", "Remove all timeouts so slow calls can finish."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Jittered bounded backoff and a circuit breaker both dampen retry "
            "amplification during a slowdown. Infinite immediate retries, more "
            "clients, and removing timeouts all intensify the overload."
        ),
        "rationales": {
            "a": (True, "Bounded jittered backoff limits and de-synchronizes retries."),
            "b": (True, "A circuit breaker halts retries during sustained failure."),
            "c": (False, "Immediate infinite retries amplify the slowdown into an outage."),
            "d": (False, "More clients add load during the incident."),
            "e": (False, "Removing timeouts lets slow calls pile up and hang."),
        },
    },
    {
        "question_id": "d2-end-to-end-observability-stack",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A GenAI platform team wants metrics, logs, and distributed traces "
            "unified so they can correlate a latency spike with the exact model "
            "call and downstream dependency. Which TWO AWS services directly "
            "support this? Select TWO."
        ),
        "scenario_constraint": "Correlate metrics/logs with per-request traces.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Amazon CloudWatch for metrics and logs."),
            ("b", "AWS X-Ray for distributed tracing."),
            ("c", "Amazon Macie for data classification."),
            ("d", "AWS Shield for DDoS protection."),
            ("e", "Amazon Rekognition for image labels."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "CloudWatch provides metrics and logs while X-Ray adds distributed "
            "traces, together enabling correlation of a spike to a specific call. "
            "Macie, Shield, and Rekognition serve unrelated purposes."
        ),
        "rationales": {
            "a": (True, "CloudWatch supplies the metrics and logs layer."),
            "b": (True, "X-Ray supplies per-request distributed tracing."),
            "c": (False, "Macie classifies sensitive data, not observability."),
            "d": (False, "Shield mitigates DDoS, unrelated to tracing."),
            "e": (False, "Rekognition labels images, not telemetry."),
        },
    },
    {
        "question_id": "d2-fallback-no-silent-downgrade",
        "objective_ids": ["AIP-2.5", "AIP-2.3"],
        "prompt": (
            "A routing layer silently falls back to a weaker model so often that "
            "quality drops without anyone noticing. Which addition BEST surfaces "
            "the problem while keeping the fallback?"
        ),
        "scenario_constraint": "Keep fallback but make silent degradation visible.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Remove the fallback entirely."),
            ("b", "Fall back more aggressively to avoid errors."),
            ("c", "Emit a metric and alarm on fallback rate so sustained degradation is visible."),
            ("d", "Log nothing to keep dashboards clean."),
        ],
        "correct_option_ids": ["c"],
        "explanation": (
            "Metering and alarming on fallback rate keeps the safety net while "
            "exposing sustained degradation. Removing fallback sacrifices "
            "resilience, falling back more hides the issue further, and logging "
            "nothing guarantees it stays invisible."
        ),
        "rationales": {
            "a": (False, "Removing fallback loses the resilience it provides."),
            "b": (False, "More aggressive fallback deepens the hidden quality drop."),
            "c": (True, "A fallback-rate metric and alarm reveal silent degradation."),
            "d": (False, "Logging nothing keeps the degradation invisible."),
        },
    },
    {
        "question_id": "d2-batch-vs-provisioned-overnight-fit",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A team must choose deployment options for two workloads: a nightly "
            "bulk scoring job over millions of records, and a 24/7 interactive "
            "assistant with steady high traffic. Which TWO pairings fit BEST? "
            "Select TWO."
        ),
        "scenario_constraint": "Match offline bulk versus steady interactive to the right modes.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Batch inference for the nightly bulk scoring job."),
            ("b", "Provisioned Throughput for the steady 24/7 assistant."),
            ("c", "Provisioned Throughput for the nightly bulk job to finish faster."),
            ("d", "Batch inference for the interactive assistant to cut cost."),
            ("e", "A SageMaker training job for the interactive assistant."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Batch inference suits the offline bulk job while Provisioned "
            "Throughput fits the steady interactive assistant. Provisioning the "
            "nightly job overpays, batching an interactive assistant breaks "
            "latency, and a training job does not serve inference."
        ),
        "rationales": {
            "a": (True, "Batch is the cost-efficient choice for the offline bulk job."),
            "b": (True, "Provisioned Throughput gives the assistant guaranteed steady capacity."),
            "c": (False, "Provisioning the nightly job overpays versus batch."),
            "d": (False, "Batch is offline and cannot serve interactive traffic."),
            "e": (False, "A training job trains models; it does not serve requests."),
        },
    },
    {
        "question_id": "d2-step-functions-vs-eventbridge-combo",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A GenAI platform needs both an ordered multi-step pipeline with "
            "retries and a decoupled broadcast of completion events to many "
            "independent subscribers. Which TWO services fit these two needs? "
            "Select TWO."
        ),
        "scenario_constraint": "Separate ordered orchestration from fan-out notification.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "AWS Step Functions for the ordered multi-step pipeline with retries."),
            ("b", "Amazon EventBridge to broadcast completion events to many subscribers."),
            ("c", "Amazon API Gateway to orchestrate the ordered pipeline steps."),
            ("d", "Amazon SQS to broadcast the same event to every subscriber."),
            ("e", "AWS CodeBuild to run the pipeline steps in order."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Step Functions orchestrates the ordered, retrying pipeline while "
            "EventBridge fans completion events out to many subscribers. API "
            "Gateway is a front door, SQS does not natively broadcast, and "
            "CodeBuild is a build tool."
        ),
        "rationales": {
            "a": (True, "Step Functions handles ordered steps with built-in retries."),
            "b": (True, "EventBridge broadcasts events to many independent subscribers."),
            "c": (False, "API Gateway is an API front door, not a workflow engine."),
            "d": (False, "SQS delivers to one consumer group, not a broadcast."),
            "e": (False, "CodeBuild builds artifacts; it does not orchestrate runtime steps."),
        },
    },
    {
        "question_id": "d2-streaming-timeout-combo",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A streaming chat integration must stay robust when the model stalls "
            "mid-generation. Which TWO safeguards BEST protect the client "
            "experience? Select TWO."
        ),
        "scenario_constraint": "Keep a streaming client robust against a mid-stream stall.",
        "difficulty": "hard",
        "question_format": "multiple_response",
        "options": [
            ("a", "An inter-token read timeout that aborts if no token arrives in time."),
            ("b", "Treating an aborted stream as a failure to retry or surface."),
            ("c", "Marking the stream successful as soon as it opens."),
            ("d", "Removing timeouts so the model can finish eventually."),
            ("e", "Buffering indefinitely in memory until tokens resume."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "An inter-token read timeout detects a stall and aborting, combined "
            "with treating the abort as a failure, keeps the client honest and "
            "recoverable. Early success, no timeouts, and unbounded buffering all "
            "mask or worsen the stall."
        ),
        "rationales": {
            "a": (True, "An inter-token timeout detects and aborts a stalled stream."),
            "b": (True, "Treating the abort as failure enables retry or an honest error."),
            "c": (False, "Marking success on open ignores a later stall."),
            "d": (False, "Removing timeouts lets a stalled stream hang indefinitely."),
            "e": (False, "Unbounded buffering risks memory exhaustion during a stall."),
        },
    },
    {
        "question_id": "d2-schema-and-idempotency-combo",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A mutating model-backed endpoint must be both safe to retry and "
            "resistant to malformed input. Which TWO practices directly deliver "
            "these properties? Select TWO."
        ),
        "scenario_constraint": "Combine retry safety with input validation at the boundary.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Accept a client idempotency key the endpoint deduplicates on."),
            ("b", "Validate the request body against a typed schema before processing."),
            ("c", "Increase the client timeout to avoid retries."),
            ("d", "Raise the account invocation quota."),
            ("e", "Set a higher temperature for robustness."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "An idempotency key makes retries safe and schema validation blocks "
            "malformed input before processing. Timeouts, quotas, and temperature "
            "address neither retry safety nor input validation."
        ),
        "rationales": {
            "a": (True, "An idempotency key collapses retries into one effect."),
            "b": (True, "Schema validation rejects malformed input pre-processing."),
            "c": (False, "A longer timeout does not make a mutation retry-safe."),
            "d": (False, "Quota governs rate, not retry safety or validation."),
            "e": (False, "Temperature affects sampling, not robustness here."),
        },
    },
    {
        "question_id": "d2-observability-false-success-combo",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "After an incident where throttled calls were logged as successes, a "
            "team wants both honest status reporting and the ability to trace one "
            "request across services. Which TWO changes BEST achieve this? Select "
            "TWO."
        ),
        "scenario_constraint": "Honest completion status plus cross-service traceability.",
        "difficulty": "hard",
        "question_format": "multiple_response",
        "options": [
            ("a", "Record success only after a validated complete response."),
            ("b", "Propagate a correlation ID and emit distributed traces across services."),
            ("c", "Mark success on any non-exception return."),
            ("d", "Rely on a single aggregate success counter with no categories."),
            ("e", "Disable tracing to reduce overhead during incidents."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Recording success only on a validated complete response avoids "
            "false-success, and correlated distributed traces let the team follow "
            "one request end to end. Marking any return as success, a single "
            "counter, and disabling tracing undermine both goals."
        ),
        "rationales": {
            "a": (True, "Validated completion prevents false-success on throttled calls."),
            "b": (True, "Correlation IDs and traces enable cross-service debugging."),
            "c": (False, "Any-return success still mislabels throttled failures."),
            "d": (False, "A single counter hides failure categories and causes."),
            "e": (False, "Disabling tracing removes the cross-service visibility needed."),
        },
    },
]


def question_count() -> int:
    """Return the number of authored Domain 2 questions."""
    return len(QUESTIONS)
