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
        "prompt": "An agentic solution must query an internal order database, call external "
        "shipping APIs, generate PDF reports, recover from transient tool failures, and "
        "remember prior turns across a long conversation. Which TWO AWS building blocks "
        "most directly deliver this with the least custom orchestration code? Select "
        "TWO.",
        "scenario_constraint": "Tool invocation plus durable conversation state with minimal "
        "custom code.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            (
                "a",
                "Amazon Bedrock Agents with action groups for the database, APIs, and "
                "report tasks.",
            ),
            ("b", "A DynamoDB table keyed by session ID for conversation and task state."),
            ("c", "Amazon Comprehend to classify the user's intent on every turn."),
            ("d", "Amazon Kinesis Data Streams to buffer each conversational message."),
            ("e", "Amazon Rekognition to inspect the generated PDF reports."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": "Bedrock Agents with action groups expose the database, shipping, and "
        "report tools to a reasoning loop, and DynamoDB gives low-latency durable "
        "session state keyed by conversation. Comprehend, Kinesis, and Rekognition "
        "solve unrelated problems here.",
        "rationales": {
            "a": (
                True,
                "Action groups wire the agent to the DB, APIs, and report tools "
                "under one reasoning loop.",
            ),
            "b": (
                True,
                "DynamoDB keyed by session ID holds durable per-conversation " "state cheaply.",
            ),
            "c": (
                False,
                "Intent classification is not the stated need and adds an extra " "model hop.",
            ),
            "d": (False, "A streaming buffer does not provide addressable conversation " "state."),
            "e": (False, "Image analysis has no role in text-driven report " "generation."),
        },
    },
    {
        "question_id": "d2-tool-schema-validation",
        "objective_ids": ["AIP-2.1"],
        "prompt": "A tool-using agent occasionally calls an internal API with malformed arguments, "
        "causing downstream 500s. Which TWO controls block bad calls before they leave "
        "the agent? Select TWO.",
        "scenario_constraint": "Stop malformed tool calls at the agent boundary.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Add a sentence to the system prompt asking the model to be careful."),
            ("b", "Define a typed tool schema and validate arguments before each " "invocation."),
            ("c", "Retry the tool call until one eventually succeeds."),
            ("d", "Log the failures and let the downstream API reject bad input."),
            ("e", "Reject calls whose arguments fail a boundary validation check."),
        ],
        "correct_option_ids": ["b", "e"],
        "explanation": "A typed tool schema plus a boundary validation check reject bad calls "
        "before they reach downstream systems. Prompt pleading is not enforced, "
        "blind retries amplify the fault, and downstream rejection means the bad "
        "call already escaped.",
        "rationales": {
            "a": (False, "A prompt request is advisory, not an enforced validation " "gate."),
            "b": (
                True,
                "Schema validation is the enforced boundary that rejects " "malformed calls.",
            ),
            "c": (
                False,
                "Retrying malformed arguments repeats the error rather than " "fixing it.",
            ),
            "d": (
                False,
                "Downstream rejection fires after the bad call has already left " "the agent.",
            ),
            "e": (True, "A boundary validation check stops invalid arguments before " "dispatch."),
        },
    },
    {
        "question_id": "d2-react-loop-step-limit",
        "objective_ids": ["AIP-2.1"],
        "prompt": "A ReAct-style Bedrock agent sometimes loops between two tools and never returns "
        "an answer, running up cost. Which TWO safeguards guarantee the loop terminates "
        "within budget? Select TWO.",
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
        "explanation": "A hard step budget and a wall-clock timeout each guarantee termination and "
        "bound cost regardless of model behavior. Temperature is probabilistic, "
        "dropping a needed tool breaks the task, and a larger context window does "
        "nothing to stop a loop.",
        "rationales": {
            "a": (
                False,
                "Temperature only shifts probabilities; it cannot guarantee " "termination.",
            ),
            "b": (False, "Removing a required tool breaks legitimate workflows that need " "it."),
            "c": (True, "A bounded step budget deterministically ends the loop and caps " "cost."),
            "d": (False, "A bigger context window lets the loop run longer, not stop."),
            "e": (True, "A wall-clock timeout bounds total runtime and forces " "termination."),
        },
    },
    {
        "question_id": "d2-least-privilege-action-group",
        "objective_ids": ["AIP-2.1", "AIP-3.1"],
        "prompt": "An agent invokes several AWS actions through action groups. Security review "
        "requires that a compromised agent cannot exceed its intended scope. Which "
        "design BEST enforces containment?",
        "scenario_constraint": "Limit blast radius if the agent is compromised.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Scope the agent's execution-role IAM policy to the exact actions and "
                "resource ARNs it needs.",
            ),
            (
                "b",
                "Attach a broad administrator role to the agent and rely on reviewing "
                "CloudTrail events afterward to catch any misuse.",
            ),
            (
                "c",
                "Embed long-lived IAM access keys inside the Lambda that backs the "
                "action group.",
            ),
            (
                "d",
                "Keep the role wide and list the allowed actions only in the agent's "
                "system prompt.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "A least-privilege IAM policy on the execution role is the enforced "
        "boundary that caps what the agent can ever do. Broad roles plus "
        "after-the-fact audit, embedded keys, and prompt-level rules do not "
        "actually constrain a misbehaving agent.",
        "rationales": {
            "a": (
                True,
                "A scoped execution-role policy is the enforced ceiling on " "agent actions.",
            ),
            "b": (
                False,
                "Auditing CloudTrail after the fact does not prevent an " "over-broad action.",
            ),
            "c": (False, "Long-lived embedded keys widen exposure and bypass role " "scoping."),
            "d": (
                False,
                "Prompt text is advisory and cannot stop an action IAM already " "allows.",
            ),
        },
    },
    {
        "question_id": "d2-human-in-the-loop-approval",
        "objective_ids": ["AIP-2.1"],
        "prompt": "An agent can issue customer refunds via a tool. The business requires that "
        "refunds above $500 get human approval before they execute, while smaller "
        "refunds proceed automatically. Which design meets this with the LEAST "
        "operational overhead?",
        "scenario_constraint": "Gate only high-value actions on human approval without blocking "
        "the rest.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Route every proposed refund to a human reviewer before the tool is "
                "allowed to execute.",
            ),
            (
                "b",
                "Add a human-in-the-loop approval step that fires only when the refund "
                "exceeds the threshold.",
            ),
            (
                "c",
                "Let the agent self-approve each refund and email a reconciliation "
                "summary to a manager daily.",
            ),
            (
                "d",
                "Lower the model temperature so the agent proposes refunds more "
                "conservatively on its own.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "A conditional human-in-the-loop gate on the high-value branch preserves "
        "automation for small refunds while enforcing review where it matters. "
        "Reviewing everything is wasteful, daily summaries are after-the-fact, and "
        "temperature does not enforce a dollar threshold.",
        "rationales": {
            "a": (False, "Reviewing every refund removes the automation benefit " "entirely."),
            "b": (True, "A threshold-triggered approval gate blocks only the risky " "actions."),
            "c": (
                False,
                "A daily summary cannot stop an incorrect large refund before " "it executes.",
            ),
            "d": (False, "Temperature does not implement a deterministic approval " "threshold."),
        },
    },
    {
        "question_id": "d2-mcp-tool-exposure",
        "objective_ids": ["AIP-2.1"],
        "prompt": "Your team wants one agent to reuse the same catalog of internal tools that "
        "several other applications already expose over a standardized protocol, without "
        "re-implementing adapters per client. Which approach fits BEST?",
        "scenario_constraint": "Reuse a shared, standardized tool catalog across multiple clients.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Hard-code each tool's HTTP call directly inside this agent and "
                "maintain it separately per app.",
            ),
            (
                "b",
                "Copy the tool implementation code into every application that needs to "
                "call those tools.",
            ),
            (
                "c",
                "Publish the tools from a Model Context Protocol server the agent "
                "connects to as a client.",
            ),
            (
                "d",
                "Describe the tool definitions as prompt text and trust the model to "
                "invoke them correctly.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "An MCP server publishes tools over a standard protocol so any MCP-aware "
        "client, including the agent, consumes them uniformly. Hard-coding and "
        "copying duplicate adapters, and prompt-only definitions have no execution "
        "layer.",
        "rationales": {
            "a": (False, "Hard-coded calls defeat reuse and must be rewritten per " "client."),
            "b": (False, "Copying tool code creates duplicated, drift-prone adapters."),
            "c": (True, "An MCP server standardizes tool exposure across all MCP " "clients."),
            "d": (False, "Prompt text describes tools but provides no shared execution " "path."),
        },
    },
    {
        "question_id": "d2-agentcore-memory",
        "objective_ids": ["AIP-2.1"],
        "prompt": "You are building on Amazon Bedrock AgentCore and need managed short- and "
        "long-term memory for an agent so it recalls prior sessions without you "
        "operating a custom store. Which AgentCore capability addresses this directly?",
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
        "explanation": "AgentCore Memory is the managed capability for retaining agent context "
        "across turns and sessions. Code Interpreter runs code, Gateway exposes "
        "tools/APIs, and Observability handles tracing.",
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
        "prompt": "An AgentCore-based agent must call a dozen existing REST APIs as tools, with "
        "auth and schema translation handled for it. Which AgentCore component is "
        "designed for turning those APIs into agent tools?",
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
        "explanation": "AgentCore Gateway turns APIs and services into agent-callable tools with "
        "auth and schema handling. Runtime hosts the agent, Identity manages "
        "access, and Memory stores context.",
        "rationales": {
            "a": (False, "Runtime is the managed execution environment, not the tool " "broker."),
            "b": (False, "Identity governs access and credentials, not API-to-tool " "conversion."),
            "c": (True, "Gateway converts APIs into governed agent tools."),
            "d": (False, "Memory stores context and has no tool-brokering role."),
        },
    },
    {
        "question_id": "d2-session-state-dynamodb",
        "objective_ids": ["AIP-2.1"],
        "prompt": "A custom agent runs across stateless Lambda invocations and must resume each "
        "user's multi-turn conversation exactly where it left off at low read latency. "
        "Which TWO stores are appropriate for durable per-session state? Select TWO.",
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
        "explanation": "DynamoDB keyed by session ID and a managed agent memory service both "
        "provide durable state that survives cold starts. In-memory dicts vanish, "
        "per-turn S3 rewrites are slow and race-prone, and the context window is "
        "lost between invocations.",
        "rationales": {
            "a": (True, "DynamoDB by session ID is durable and low-latency."),
            "b": (True, "A managed memory service persists durable per-session " "context."),
            "c": (False, "Module memory is per-container and lost on cold starts."),
            "d": (False, "Rewriting an S3 object per turn is slow and conflict-prone."),
            "e": (False, "The context window does not persist across stateless " "invocations."),
        },
    },
    {
        "question_id": "d2-multi-agent-orchestration",
        "objective_ids": ["AIP-2.1"],
        "prompt": "A workflow needs a planner agent to delegate subtasks to a research agent and a "
        "coding agent, then merge their outputs. The team wants a framework "
        "purpose-built for coordinating multiple collaborating agents on AWS. Which "
        "choice fits BEST?",
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
        "explanation": "AWS Agent Squad is built to route and coordinate multiple specialized "
        "agents. A single mega-prompt loses role isolation, SQS fan-out lacks "
        "orchestration logic, and Athena is an analytics query engine.",
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
        "prompt": "A Python team wants a lightweight, code-first open-source SDK to define a "
        "single agent's model, tools, and prompt, deployable to AWS, without adopting a "
        "heavy orchestration platform. Which option best matches?",
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
        "explanation": "Strands Agents is a code-first SDK for defining an agent's model, tools, "
        "and prompt loop. Guardrails filter content, Step Functions is a workflow "
        "engine, and Ground Truth is for labeling.",
        "rationales": {
            "a": (True, "Strands is the lightweight code-first agent SDK described."),
            "b": (False, "Guardrails enforce safety policy, not agent definition."),
            "c": (False, "Step Functions orchestrates workflows, not agent reasoning " "loops."),
            "d": (False, "Ground Truth is a data-labeling service."),
        },
    },
    {
        "question_id": "d2-function-calling-vs-freeform",
        "objective_ids": ["AIP-2.1"],
        "prompt": "A model should return parameters an application can execute deterministically "
        "against a weather tool, rather than prose the app must parse. Which model "
        "capability enforces a machine-readable call?",
        "scenario_constraint": "Produce structured, directly-executable tool arguments.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Enable streaming token output so the application can parse arguments "
                "as they arrive.",
            ),
            (
                "b",
                "Raise the sampling temperature so the model phrases the tool arguments "
                "more decisively.",
            ),
            (
                "c",
                "Increase the max-tokens limit so the full argument list always fits in "
                "the output.",
            ),
            (
                "d",
                "Use function calling with a declared tool schema the model fills in "
                "structurally.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Function calling with a declared schema makes the model emit structured "
        "arguments the app can execute without brittle parsing. Streaming, "
        "temperature, and max-tokens affect delivery or length, not structure.",
        "rationales": {
            "a": (False, "Streaming changes delivery timing, not output structure."),
            "b": (False, "Higher temperature increases variability, hurting structure."),
            "c": (False, "A larger token limit allows longer output, not structured " "calls."),
            "d": (True, "Function calling yields schema-conformant executable " "arguments."),
        },
    },
    {
        "question_id": "d2-agent-cost-time-limits",
        "objective_ids": ["AIP-2.1"],
        "prompt": "An autonomous agent occasionally fans out dozens of tool calls on a single "
        "request, spiking cost and latency unpredictably. You must cap per-request "
        "resource use. Which TWO controls directly bound it? Select TWO.",
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
        "explanation": "A step cap and a wall-clock timeout are the direct, deterministic bounds "
        "on per-request work. A bigger context window, a higher quota, and "
        "temperature changes do not limit fan-out or runtime.",
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
        "prompt": "An agent retries a 'create invoice' tool after a timeout and sometimes creates "
        "duplicate invoices. You must make retries safe. What is the MOST reliable fix?",
        "scenario_constraint": "Make a mutating tool safe to retry.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Instruct the agent in its system prompt never to retry the "
                "create-invoice tool call.",
            ),
            (
                "b",
                "Have the agent send a client-generated idempotency key the tool "
                "deduplicates on.",
            ),
            (
                "c",
                "Raise the create-invoice tool timeout so slow responses rarely trigger "
                "a retry.",
            ),
            (
                "d",
                "Run a nightly cleanup job that finds and deletes duplicate invoices "
                "after the fact.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "A caller-supplied idempotency key lets the tool collapse repeated requests "
        "to one invoice regardless of retries. Prompt instructions are not "
        "enforced, longer timeouts only reduce frequency, and nightly cleanup is a "
        "lossy afterthought.",
        "rationales": {
            "a": (False, "A prompt instruction cannot reliably prevent retries."),
            "b": (True, "An idempotency key makes repeated creates resolve to one " "record."),
            "c": (False, "A longer timeout reduces but does not eliminate duplicates."),
            "d": (False, "Nightly cleanup is reactive and risks removing valid " "records."),
        },
    },
    {
        "question_id": "d2-agent-tool-timeout-isolation",
        "objective_ids": ["AIP-2.1"],
        "prompt": "One slow external tool occasionally hangs for minutes, stalling the whole agent "
        "run. You want the agent to give up on that tool quickly and continue reasoning. "
        "Which control fits BEST?",
        "scenario_constraint": "Prevent one slow tool from blocking the whole run.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Wrap the run in a global retry that restarts the whole agent from the "
                "first step on any hang.",
            ),
            (
                "b",
                "Remove the tool's timeout entirely so the slow dependency is always "
                "given time to finish.",
            ),
            (
                "c",
                "Set a per-tool timeout that fails the slow call fast and lets the "
                "agent keep reasoning.",
            ),
            (
                "d",
                "Cache the tool's last successful response and serve it indefinitely to "
                "avoid the call.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "A per-tool timeout isolates the slow dependency and returns control to the "
        "reasoning loop quickly. Restarting the whole run wastes work, removing "
        "timeouts worsens hangs, and permanent caching returns stale data.",
        "rationales": {
            "a": (False, "Restarting the whole run discards progress and repeats the " "hang."),
            "b": (False, "Removing timeouts guarantees the stall continues."),
            "c": (True, "A per-tool timeout contains the hang and keeps the agent " "moving."),
            "d": (False, "Caching forever serves stale data and ignores fresh needs."),
        },
    },
    {
        "question_id": "d2-agentcore-identity",
        "objective_ids": ["AIP-2.1", "AIP-3.1"],
        "prompt": "An AgentCore agent must act on behalf of the signed-in end user when it calls "
        "downstream services, carrying that user's identity rather than a single shared "
        "role. Which AgentCore capability provides this?",
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
        "explanation": "AgentCore Identity handles authenticated, per-user access when the agent "
        "calls downstream resources. Observability traces, Code Interpreter runs "
        "code, and Memory stores context.",
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
        "prompt": "An agent must run user-provided Python to compute statistics on an uploaded "
        "CSV, in a sandbox you do not have to operate. Which AgentCore capability is "
        "designed for this?",
        "scenario_constraint": "Safely execute generated code in a managed sandbox.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "AgentCore Code Interpreter, which runs the generated Python in a "
                "managed sandbox.",
            ),
            (
                "b",
                "AgentCore Gateway, exposing the CSV-processing script as a brokered "
                "agent tool.",
            ),
            (
                "c",
                "AgentCore Memory, persisting the uploaded CSV and computed statistics "
                "across turns.",
            ),
            (
                "d",
                "AgentCore Identity, authorizing the user before the statistics code is "
                "allowed to run.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "AgentCore Code Interpreter runs generated code in a managed sandbox. "
        "Gateway exposes tools, Memory stores context, and Identity handles access.",
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
        "prompt": "Users report that an agent 'sometimes does the wrong thing,' but you cannot see "
        "which tools it chose or why. You want end-to-end visibility into each reasoning "
        "step and tool call. Which AgentCore capability addresses this?",
        "scenario_constraint": "Gain step-level visibility into agent decisions.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "AgentCore Observability, surfacing per-step traces of each reasoning "
                "hop and tool call.",
            ),
            (
                "b",
                "AgentCore Runtime, the managed environment that executes the agent's "
                "reasoning loop and tool invocations end to end.",
            ),
            (
                "c",
                "AgentCore Memory, retaining the agent's conversation context across "
                "its sessions.",
            ),
            (
                "d",
                "AgentCore Gateway, brokering the agent's calls to downstream APIs and " "tools.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "AgentCore Observability surfaces traces and metrics for each reasoning "
        "step and tool call. Runtime hosts execution, Memory stores context, and "
        "Gateway brokers tools.",
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
        "prompt": "An agent occasionally invents a tool name that does not exist and fails. You "
        "want the agent to only ever call tools that are actually registered. What is "
        "the BEST control?",
        "scenario_constraint": "Restrict calls to the registered tool catalog only.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Raise the max-tokens limit so the model has more room to name the "
                "correct tool.",
            ),
            (
                "b",
                "Validate each proposed tool name against the registered catalog and "
                "reject unknown ones.",
            ),
            (
                "c",
                "Ask the model in the system prompt to call only tools that genuinely "
                "exist in the registered catalog and never invent names.",
            ),
            (
                "d",
                "Set temperature to zero so the model deterministically stops inventing "
                "tool names.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Validating the proposed tool name against the registry and rejecting "
        "unknowns deterministically prevents calls to nonexistent tools. More "
        "tokens, prompt pleas, and zero temperature reduce but never guarantee the "
        "behavior.",
        "rationales": {
            "a": (False, "More tokens do not constrain which tools are callable."),
            "b": (True, "Registry validation is the enforced gate against invented " "tools."),
            "c": (False, "A prompt request is advisory, not enforced."),
            "d": (False, "Zero temperature lowers variance but can still emit a bad " "name."),
        },
    },
    {
        "question_id": "d2-agent-vs-single-prompt",
        "objective_ids": ["AIP-2.1"],
        "prompt": "A request requires looking up live inventory, checking a shipping API, and only "
        "then answering. A single zero-shot prompt keeps fabricating numbers. Which "
        "design change MOST improves correctness?",
        "scenario_constraint": "Ground answers in live data instead of fabrication.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Raise the max-tokens limit so the zero-shot answer has room to include "
                "the numbers.",
            ),
            (
                "b",
                "Add several examples of the fabricated-number answers to the prompt as "
                "references.",
            ),
            (
                "c",
                "Give the model tools and action groups so it fetches live data before "
                "answering.",
            ),
            (
                "d",
                "Switch to a smaller, cheaper foundation model to reduce the fabricated " "detail.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Equipping the model with tools lets it retrieve live inventory and "
        "shipping data instead of guessing. Longer outputs, bad examples, and a "
        "smaller model do not add grounding.",
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
        "prompt": "An agent must gather three independent data points from three unrelated APIs "
        "before composing an answer, and latency is critical. Which execution strategy "
        "is BEST?",
        "scenario_constraint": "Minimize latency across independent tool calls.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Call the three independent APIs strictly in sequence to keep the "
                "control flow simple.",
            ),
            (
                "b",
                "Call one of the three APIs three separate times and reconcile the "
                "differing answers into a single composite value.",
            ),
            (
                "c",
                "Call one API and extrapolate the two missing data points from that "
                "single result.",
            ),
            (
                "d",
                "Invoke the three independent tools in parallel and join their results "
                "before composing.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Because the three calls are independent, running them in parallel cuts "
        "total latency to roughly the slowest call. Sequencing is slower, repeating "
        "one tool is wrong, and extrapolating drops required data.",
        "rationales": {
            "a": (False, "Sequential calls add their latencies unnecessarily."),
            "b": (False, "Repeating one tool does not fetch the other data points."),
            "c": (False, "Extrapolating omits required real values."),
            "d": (True, "Parallelizing independent calls minimizes end-to-end " "latency."),
        },
    },
    {
        "question_id": "d2-agent-memory-vs-context",
        "objective_ids": ["AIP-2.1"],
        "prompt": "A support agent must remember a customer's preferences across sessions that may "
        "be days apart, but each session's prompt should stay small for cost reasons. "
        "Which approach fits BEST?",
        "scenario_constraint": "Persist long-term memory without bloating every prompt.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Paste the customer's entire prior conversation history into the prompt "
                "on every new session so nothing is ever lost.",
            ),
            (
                "b",
                "Keep all preferences resident in the model's context window across "
                "days-apart sessions.",
            ),
            (
                "c",
                "Store durable preferences in a memory store and retrieve only the "
                "relevant items per session.",
            ),
            (
                "d",
                "Discard the customer's preferences after each session and simply "
                "re-ask them next time.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "A durable memory store with selective retrieval keeps per-session prompts "
        "small while preserving long-term recall. Pasting all history inflates "
        "cost, the context window does not persist across sessions, and re-asking "
        "harms experience.",
        "rationales": {
            "a": (False, "Pasting full history bloats every prompt and raises cost."),
            "b": (False, "The context window is not retained across separate sessions."),
            "c": (
                True,
                "A memory store with selective retrieval keeps prompts small " "and durable.",
            ),
            "d": (False, "Re-asking each time loses the long-term memory the scenario " "needs."),
        },
    },
    {
        "question_id": "d2-agent-guardrail-on-tool-output",
        "objective_ids": ["AIP-2.1", "AIP-3.2"],
        "prompt": "An agent summarizes documents a tool returns, but some documents contain "
        "content that must never reach the end user. You need the agent's final response "
        "filtered against a policy. Which control is MOST appropriate?",
        "scenario_constraint": "Enforce a content policy on the agent's final output.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Rely on a system-prompt instruction telling the model to self-censor "
                "unsafe tool output.",
            ),
            (
                "b",
                "Apply Amazon Bedrock Guardrails to the agent's input and the "
                "summarized tool output.",
            ),
            (
                "c",
                "Remove the summarization tool so the unsafe content can never reach "
                "the user at all.",
            ),
            (
                "d",
                "Raise the temperature so the summary drifts away from the sensitive "
                "source content.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Bedrock Guardrails enforce content policy on inputs and outputs "
        "independently of the model's cooperation. Prompt self-censorship is "
        "unenforced, removing the tool kills the feature, and temperature does not "
        "filter content.",
        "rationales": {
            "a": (False, "Prompt self-censoring is advisory and not an enforced filter."),
            "b": (True, "Guardrails apply an enforced content policy to inputs and " "outputs."),
            "c": (
                False,
                "Deleting the tool removes needed functionality rather than " "filtering it.",
            ),
            "d": (False, "Temperature changes wording, not whether unsafe content " "passes."),
        },
    },
    {
        "question_id": "d2-agent-tool-vs-rag",
        "objective_ids": ["AIP-2.1"],
        "prompt": "An agent needs both to answer policy questions from a document corpus and to "
        "execute live account actions. Which combination of capabilities BEST serves "
        "both needs? Select TWO.",
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
        "explanation": "A retrieval tool grounds policy answers while action groups execute live "
        "account operations, covering both needs. Temperature, token limits, and "
        "disabling tools do not provide retrieval or actions.",
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
        "prompt": "When a pricing tool is unavailable, the agent currently returns a confident but "
        "fabricated price. You must ensure it never presents a guessed price as real. "
        "Which behavior is BEST?",
        "scenario_constraint": "Never present fabricated data as a verified result.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "On tool failure, return an explicit 'pricing unavailable' response "
                "rather than a guess.",
            ),
            (
                "b",
                "Let the model estimate the price from its training data when the "
                "pricing tool fails.",
            ),
            (
                "c",
                "Retry the failed pricing tool in a tight loop until it eventually "
                "returns a value.",
            ),
            (
                "d",
                "Serve the last cached price when the pricing tool fails and keep "
                "presenting it to users as the current price indefinitely.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Returning an explicit unavailable state prevents passing a guess off as "
        "real data. Estimating fabricates, infinite retries hang, and serving a "
        "stale cache as current misrepresents freshness.",
        "rationales": {
            "a": (
                True,
                "An explicit unavailable response avoids presenting a " "fabricated price.",
            ),
            "b": (False, "Estimating from training data invents an unverified price."),
            "c": (False, "Retrying forever can hang the request and amplify the fault."),
            "d": (False, "Serving a stale cached price as current misleads the user."),
        },
    },
    {
        "question_id": "d2-provisioned-vs-ondemand-steady",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A Bedrock-backed feature runs a steady, high, predictable volume 24/7 and the "
        "team wants the lowest cost at guaranteed throughput. Which inference mode fits "
        "BEST?",
        "scenario_constraint": "Steady predictable high volume needing guaranteed throughput.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "On-demand inference billed per request, scaling elastically with each "
                "incoming call.",
            ),
            (
                "b",
                "Bedrock batch inference submitted as a nightly job against the "
                "accumulated prompts.",
            ),
            (
                "c",
                "A SageMaker serverless endpoint that scales to zero between sporadic " "requests.",
            ),
            (
                "d",
                "Provisioned Throughput with committed model units reserved for the "
                "steady load.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Provisioned Throughput reserves committed capacity at lower unit cost for "
        "steady, predictable high volume. On-demand costs more at scale, batch is "
        "not interactive, and serverless suits spiky, low-steady traffic.",
        "rationales": {
            "a": (False, "On-demand is cost-inefficient for predictable sustained high " "volume."),
            "b": (False, "Batch is offline and cannot serve interactive steady traffic."),
            "c": (False, "Serverless suits bursty low volume, not constant high " "throughput."),
            "d": (True, "Provisioned Throughput reserves capacity for predictable " "steady load."),
        },
    },
    {
        "question_id": "d2-ondemand-spiky-traffic",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A demo feature gets sporadic, unpredictable traffic that is often zero for "
        "hours. The team wants to pay only when it is used and avoid managing capacity. "
        "Which Bedrock option fits BEST?",
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
        "explanation": "On-demand inference bills per request and requires no reserved capacity, "
        "matching sporadic usage. Provisioned units, an always-on GPU fleet, and a "
        "continuous EKS cluster all pay for idle time.",
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
        "prompt": "A lightweight endpoint must call a Bedrock model on each API request, scale to "
        "zero between bursts, and need no servers to manage. Which compute choice fits "
        "BEST for the invocation layer?",
        "scenario_constraint": "Serverless, scale-to-zero compute to invoke the model.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "A standing EC2 instance that polls a queue and calls the model for "
                "each message.",
            ),
            (
                "b",
                "An ECS service with a fixed task count kept running to call the model "
                "on demand.",
            ),
            ("c", "AWS Lambda invoking the Bedrock model per request and scaling with " "traffic."),
            (
                "d",
                "A SageMaker training job launched per request to produce the single " "inference.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Lambda scales to zero, needs no server management, and invokes Bedrock per "
        "request. A standing EC2 instance and fixed ECS tasks pay for idle, and a "
        "training job is the wrong primitive for inference.",
        "rationales": {
            "a": (False, "A standing instance pays for idle time between sporadic " "requests."),
            "b": (False, "A fixed ECS task count wastes capacity under spiky request " "patterns."),
            "c": (True, "Lambda per request scales to zero and bills only for " "execution."),
            "d": (False, "A training job per request is wildly inappropriate for " "inference."),
        },
    },
    {
        "question_id": "d2-sagemaker-endpoint-custom-model",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A team fine-tuned an open-weights model not offered in Bedrock and must serve "
        "it behind a low-latency HTTPS endpoint with autoscaling. Which AWS option is "
        "MOST appropriate?",
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
        "explanation": "A SageMaker real-time endpoint hosts custom model artifacts with "
        "autoscaling and low latency. Bedrock serves its own catalog, Comprehend is "
        "a managed NLP service, and large model weights do not fit Lambda's package "
        "limits well.",
        "rationales": {
            "a": (False, "Bedrock serves managed catalog models, not arbitrary custom " "weights."),
            "b": (False, "Comprehend is a fixed NLP service, not a model host."),
            "c": (False, "Large model weights exceed Lambda's practical package limits."),
            "d": (True, "SageMaker endpoints host custom models with autoscaling."),
        },
    },
    {
        "question_id": "d2-batch-inference-large-offline",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A nightly job must summarize ten million stored documents by morning, with no "
        "interactive latency requirement, at the lowest cost. Which inference pattern "
        "fits BEST?",
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
        "explanation": "Batch inference processes large offline datasets cost-effectively without "
        "latency pressure. One-at-a-time synchronous calls are slow and costly, "
        "interactive provisioning overpays, and streaming suits incremental UX, not "
        "bulk jobs.",
        "rationales": {
            "a": (True, "Batch inference is built for high-volume offline workloads."),
            "b": (
                False,
                "One-at-a-time synchronous calls are slow and expensive at this " "scale.",
            ),
            "c": (False, "Interactive provisioning overpays for a nightly offline job."),
            "d": (False, "Streaming optimizes incremental UX, not bulk throughput."),
        },
    },
    {
        "question_id": "d2-async-inference-large-payload",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A SageMaker-hosted model handles large input payloads with processing times up "
        "to several minutes, and clients should not hold an open synchronous connection. "
        "Which inference option fits BEST?",
        "scenario_constraint": "Long-running requests with large payloads and no held connection.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "SageMaker asynchronous inference with the large results delivered to "
                "Amazon S3.",
            ),
            (
                "b",
                "SageMaker real-time inference, accepting its 60-second synchronous "
                "response cap.",
            ),
            (
                "c",
                "Bedrock streaming responses that return the large payload "
                "incrementally in-request.",
            ),
            (
                "d",
                "An AWS Lambda synchronous invocation that holds the connection open "
                "for the result.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Asynchronous inference queues long requests and writes results to S3, "
        "freeing the client from holding a connection. Real-time has tight latency "
        "caps, Bedrock streaming is a different host, and Lambda has a 15-minute "
        "hard limit and payload constraints.",
        "rationales": {
            "a": (
                True,
                "Async inference handles large payloads and long runtimes via " "S3 delivery.",
            ),
            "b": (False, "The real-time timeout cannot cover long large-payload " "processing."),
            "c": (False, "Streaming still runs within a synchronous request window."),
            "d": (False, "Lambda synchronous limits block long large-payload " "inference."),
        },
    },
    {
        "question_id": "d2-model-cascading-cost",
        "objective_ids": ["AIP-2.2"],
        "prompt": "Most support queries are simple, but a minority need a powerful, expensive "
        "model. Which TWO approaches minimize cost without hurting answers on hard "
        "queries? Select TWO.",
        "scenario_constraint": "Minimize cost while preserving quality on hard inputs.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            (
                "a",
                "Model cascading: a cheap model first, escalating to a stronger one "
                "when confidence is low.",
            ),
            ("b", "Route by measured query complexity to a cheap or premium model."),
            ("c", "Send every query to the cheapest model only."),
            ("d", "Randomly pick a model for each query."),
            ("e", "Send every query to the most powerful model."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": "Cascading escalates only hard queries, and complexity-based routing sends "
        "easy ones to a cheap model, both balancing cost and quality. Cheapest-only "
        "hurts hard queries, random ignores difficulty, and always-powerful "
        "overpays.",
        "rationales": {
            "a": (True, "Cascading escalates only when needed, balancing cost and " "quality."),
            "b": (True, "Complexity-based routing matches model strength to query " "difficulty."),
            "c": (False, "Cheapest-only degrades answers on the hard minority."),
            "d": (False, "Random selection ignores query difficulty entirely."),
            "e": (False, "Routing everything to the big model overpays on easy " "queries."),
        },
    },
    {
        "question_id": "d2-concurrency-quota-throttling",
        "objective_ids": ["AIP-2.2", "AIP-2.4"],
        "prompt": "During launch, a Bedrock-backed app starts receiving throttling errors at peak. "
        "The team confirmed requests are well-formed. Which TWO actions directly address "
        "the capacity limit? Select TWO.",
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
        "explanation": "Raising the service quota and/or committing Provisioned Throughput add the "
        "capacity that throttling signals is missing. Token limits, streaming, and "
        "schema changes do not increase allowed throughput.",
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
        "prompt": "A team already runs Kubernetes and wants to serve a custom model container "
        "alongside existing microservices, reusing their cluster tooling and GPU node "
        "pools. Which deployment target fits BEST?",
        "scenario_constraint": "Serve a model container inside existing Kubernetes operations.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Bedrock on-demand inference calling the managed foundation model "
                "instead of the container.",
            ),
            (
                "b",
                "Amazon EKS with a GPU node group running the team's own model " "container image.",
            ),
            (
                "c",
                "A SageMaker serverless endpoint that packages the container and scales "
                "to zero.",
            ),
            (
                "d",
                "AWS Lambda with the custom model baked into a layer and invoked per " "request.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "EKS lets the team host the model container next to existing microservices "
        "using their Kubernetes tooling and GPU nodes. Bedrock and SageMaker "
        "serverless hide the cluster, and Lambda cannot run GPU-bound model "
        "containers.",
        "rationales": {
            "a": (False, "Bedrock serves managed models, not a team's custom container."),
            "b": (
                True,
                "EKS with GPU nodes hosts the custom container with full " "orchestration.",
            ),
            "c": (False, "Serverless endpoints do not run an arbitrary GPU container " "image."),
            "d": (False, "Lambda cannot host a large GPU-bound model container."),
        },
    },
    {
        "question_id": "d2-sagemaker-multimodel-endpoint",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A team hosts dozens of small per-customer models, most invoked rarely, and "
        "wants to avoid paying for a dedicated endpoint per model. Which SageMaker "
        "feature fits BEST?",
        "scenario_constraint": "Serve many rarely-used models cost-efficiently.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "One dedicated real-time endpoint per model, each sized and billed "
                "independently.",
            ),
            ("b", "A separate Bedrock agent per model, each wrapping one of the many " "variants."),
            (
                "c",
                "A SageMaker multi-model endpoint that loads each model into memory on " "demand.",
            ),
            (
                "d",
                "A nightly batch job that scores against every model regardless of "
                "request volume.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "A multi-model endpoint shares infrastructure and loads models on demand, "
        "ideal for many infrequently used models. Dedicated endpoints per model are "
        "costly, Bedrock agents are unrelated, and nightly batch is not on-demand "
        "serving.",
        "rationales": {
            "a": (False, "One endpoint per model multiplies idle cost across many " "models."),
            "b": (False, "A Bedrock agent per model does not host custom model " "artifacts."),
            "c": (
                True,
                "A multi-model endpoint shares infrastructure and loads models " "on demand.",
            ),
            "d": (False, "Nightly batch cannot serve interactive per-request " "inference."),
        },
    },
    {
        "question_id": "d2-provisioned-throughput-latency-slo",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A regulated workload must meet a strict p99 latency SLO that on-demand "
        "sometimes misses due to variable capacity. The team accepts a higher baseline "
        "cost for predictability. Which option fits BEST?",
        "scenario_constraint": "Guarantee predictable latency over minimizing cost.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Stay on on-demand inference and simply retry whenever a response comes "
                "back slow.",
            ),
            ("b", "Move the workload to batch inference to smooth out the latency over " "time."),
            ("c", "Lower the max-tokens limit on every call so each response completes " "faster."),
            (
                "d",
                "Adopt Provisioned Throughput to reserve dedicated capacity for the "
                "latency SLO.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Provisioned Throughput reserves dedicated capacity, giving the predictable "
        "latency the SLO demands. Retrying worsens tail latency, batch is not "
        "interactive, and trimming tokens does not fix capacity variability.",
        "rationales": {
            "a": (False, "Retrying on-demand does not guarantee the latency SLO."),
            "b": (False, "Batch inference increases latency rather than bounding it."),
            "c": (False, "Shorter output does not control queueing or contention " "latency."),
            "d": (True, "Reserved capacity gives predictable latency for the SLO."),
        },
    },
    {
        "question_id": "d2-cross-region-capacity",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A workload hits regional capacity limits for a popular model during spikes, "
        "while a nearby Region has headroom and the data has no residency restriction. "
        "Which approach adds capacity with the LEAST rework?",
        "scenario_constraint": "Spiky demand exceeds one Region's model capacity.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Rewrite the application to call a smaller, unrelated model that has "
                "spare capacity.",
            ),
            (
                "b",
                "Queue all overflow requests for a nightly batch run instead of serving "
                "them live.",
            ),
            ("c", "Distribute invocations across Regions using Bedrock cross-Region " "inference."),
            (
                "d",
                "Cache prior responses and serve stale answers to callers during peak " "demand.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Cross-Region inference spreads load to Regions with headroom without app "
        "redesign, given no residency constraint. Swapping models changes behavior, "
        "overnight batch breaks interactivity, and stale caching degrades "
        "correctness.",
        "rationales": {
            "a": (False, "Swapping to an unrelated model changes behavior and quality."),
            "b": (False, "Deferring live traffic to batch breaks the interactive use " "case."),
            "c": (True, "Cross-Region inference spreads load to add effective " "capacity."),
            "d": (False, "Serving stale cached answers degrades correctness at peak."),
        },
    },
    {
        "question_id": "d2-lambda-cold-start-latency",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A Lambda that invokes Bedrock shows occasional slow first responses after idle "
        "periods, hurting a latency-sensitive path. Which change MOST reduces this "
        "specific delay with the least overhead?",
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
        "explanation": "Provisioned concurrency keeps initialized execution environments warm, "
        "eliminating cold-start spikes. Token limits and streaming do not address "
        "init latency, and Bedrock weights are not shipped in the package.",
        "rationales": {
            "a": (False, "Max tokens affects output size, not init latency."),
            "b": (
                True,
                "Provisioned concurrency keeps environments warm, removing cold " "starts.",
            ),
            "c": (False, "Streaming changes delivery, not cold-start initialization."),
            "d": (False, "Bedrock serves the model; weights are not in the Lambda " "package."),
        },
    },
    {
        "question_id": "d2-autoscaling-sagemaker-endpoint",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A SageMaker real-time endpoint is overprovisioned at night and throttled at "
        "midday. The team wants capacity to track demand automatically. Which mechanism "
        "fits BEST?",
        "scenario_constraint": "Match endpoint capacity to fluctuating demand automatically.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Configure endpoint autoscaling driven by an invocation or concurrency " "metric.",
            ),
            (
                "b",
                "Manually resize the endpoint's instance count twice a day on a fixed "
                "schedule based on yesterday's traffic shape.",
            ),
            ("c", "Switch the endpoint to batch inference so capacity is provisioned per " "job."),
            ("d", "Set a fixed instance count sized for the midday peak and leave it " "running."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Autoscaling adjusts instance count to a target invocation metric, matching "
        "capacity to demand. Manual resizing is error-prone, batch is offline, and "
        "fixed midday sizing wastes money at night.",
        "rationales": {
            "a": (True, "Metric-driven autoscaling matches capacity to real demand."),
            "b": (False, "Twice-daily manual resizing lags the actual traffic curve."),
            "c": (False, "Batch inference cannot serve the interactive endpoint " "traffic."),
            "d": (False, "Fixed peak sizing overpays during off-peak hours."),
        },
    },
    {
        "question_id": "d2-shadow-deployment-eval",
        "objective_ids": ["AIP-2.2", "AIP-2.3"],
        "prompt": "Before switching production to a new model version, the team wants to send a "
        "copy of live traffic to it and compare outputs without affecting users. Which "
        "deployment technique fits BEST?",
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
        "explanation": "Shadow deployment mirrors real traffic to the new version for comparison "
        "while users still see the old one. A hard cutover and deleting first carry "
        "no safety net, and random live serving exposes users to the untested "
        "version.",
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
        "prompt": "A team must roll out a new model version to production gradually so that if "
        "error rates rise, only a small fraction of users are affected and rollback is "
        "quick. Which strategy fits BEST?",
        "scenario_constraint": "Limit blast radius during a model version rollout.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A full cutover that sends every user to the new model version at " "once."),
            (
                "b",
                "A canary release routing a small traffic percentage to the new version " "first.",
            ),
            (
                "c",
                "Batch-only use of the new version so live users never touch it during " "rollout.",
            ),
            (
                "d",
                "Deploying the new version to a separate idle account that receives no " "traffic.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "A canary routes a small percentage first, limiting impact and enabling "
        "fast rollback. A full cutover risks everyone, batch-only never tests the "
        "live path, and an unused account provides no production signal.",
        "rationales": {
            "a": (False, "A full cutover exposes all users to an unproven version at " "once."),
            "b": (
                True,
                "A canary limits blast radius while real traffic validates the " "version.",
            ),
            "c": (False, "Batch-only use never validates the interactive serving path."),
            "d": (False, "An idle account produces no real validation signal."),
        },
    },
    {
        "question_id": "d2-quota-vs-throughput-concept",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A team keeps conflating two capacity concepts. They need the term for the "
        "maximum rate at which the account may call a Bedrock model under on-demand "
        "access before throttling. Which term applies?",
        "scenario_constraint": "Identify the account-level invocation rate limit.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Context window, the maximum tokens the model can attend to in one " "request."),
            (
                "b",
                "Max tokens, the cap on how many output tokens a single model response "
                "is permitted to contain before it stops.",
            ),
            (
                "c",
                "Service quota, the account-level rate limit on model invocations per " "interval.",
            ),
            ("d", "Temperature, the sampling parameter that controls output randomness."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "The account's service quota sets the allowed invocation rate before "
        "throttling. Context window and max tokens bound a single request, and "
        "temperature controls sampling.",
        "rationales": {
            "a": (False, "Context window bounds prompt size, not invocation rate."),
            "b": (False, "Max tokens limits output length, not request frequency."),
            "c": (True, "A service quota is the account rate limit the scenario " "describes."),
            "d": (False, "Temperature affects randomness, unrelated to rate limits."),
        },
    },
    {
        "question_id": "d2-right-size-model-cost",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A classification feature currently uses a top-tier reasoning model but only "
        "needs to pick one of five labels. The team wants to cut cost without hurting "
        "accuracy on this narrow task. What is the BEST move?",
        "scenario_constraint": "Match model size to a narrow, simple task.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Keep the top-tier model everywhere to stay safely above the accuracy " "bar."),
            (
                "b",
                "Add Provisioned Throughput commitments to the top-tier model to lower "
                "its effective per-call cost at this volume.",
            ),
            ("c", "Increase the top-tier model's max tokens so each answer carries more " "value."),
            (
                "d",
                "Evaluate and switch to a smaller model that still meets the task's "
                "accuracy bar.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "A validated smaller model that meets the accuracy bar cuts cost on a "
        "simple task. Keeping the big model overpays, provisioning it adds cost, "
        "and more tokens do not reduce spend.",
        "rationales": {
            "a": (False, "Over-provisioning the top model wastes cost on simple tasks."),
            "b": (False, "Provisioned Throughput commits spend rather than cutting it " "here."),
            "c": (False, "More output tokens raise cost without improving right-sizing."),
            "d": (True, "A smaller model that meets the bar cuts cost appropriately."),
        },
    },
    {
        "question_id": "d2-cross-region-residency-conflict",
        "objective_ids": ["AIP-2.2", "AIP-2.3"],
        "prompt": "An EU workload is capacity-constrained, but regulation forbids processing its "
        "data outside the EU. An engineer suggests cross-Region inference to a US Region "
        "for headroom. What is the BEST response?",
        "scenario_constraint": "Capacity need must not violate data residency rules.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Keep inference inside the compliant EU Regions and add capacity there " "instead.",
            ),
            ("b", "Shift the overflow to the US Region because it has the most spare " "headroom."),
            (
                "c",
                "Send only the user prompts, not the generated responses, across to the "
                "US Region to keep most data in the EU.",
            ),
            ("d", "Disable request logging so the cross-Region processing is never " "recorded."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Residency rules override the capacity convenience, so capacity must be "
        "added within compliant EU Regions. Using the US Region violates residency, "
        "splitting prompts still processes data abroad, and disabling logging hides "
        "a violation rather than preventing it.",
        "rationales": {
            "a": (True, "Staying in compliant Regions honors residency while adding " "capacity."),
            "b": (False, "Using the US Region violates the EU data-residency " "requirement."),
            "c": (False, "Sending prompts out of Region still breaches residency."),
            "d": (False, "Hiding logs does not make the violation compliant."),
        },
    },
    {
        "question_id": "d2-provisioned-commitment-waste",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A team bought Provisioned Throughput for a feature whose traffic later dropped "
        "to near zero most of the day, and the commitment is mostly idle. Which action "
        "BEST reduces ongoing cost?",
        "scenario_constraint": "Reserved capacity now sits idle most of the time.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Move the low, sporadic traffic to on-demand and release the unused " "commitment.",
            ),
            (
                "b",
                "Add more provisioned model units so there is extra headroom for future " "spikes.",
            ),
            ("c", "Raise the max-tokens limit on each call to make fuller use of the " "capacity."),
            (
                "d",
                "Send synthetic filler requests to keep the reserved capacity "
                "continuously busy.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Sporadic low traffic fits on-demand, so releasing the idle commitment "
        "stops paying for unused capacity. Adding units, more tokens, or synthetic "
        "traffic all increase waste rather than cut it.",
        "rationales": {
            "a": (True, "On-demand fits sporadic traffic and ends the wasted " "commitment."),
            "b": (False, "Adding units increases the waste rather than removing it."),
            "c": (False, "Longer outputs do not fix idle reserved capacity."),
            "d": (False, "Synthetic traffic burns money to disguise the waste."),
        },
    },
    {
        "question_id": "d2-blue-green-rollback",
        "objective_ids": ["AIP-2.2", "AIP-2.3"],
        "prompt": "A team wants instant rollback capability when promoting a new inference stack, "
        "keeping the old environment fully running until the new one is proven. Which "
        "deployment pattern fits BEST?",
        "scenario_constraint": "Instant rollback with the prior environment intact.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "An in-place upgrade of the single running environment with no standby "
                "to revert to.",
            ),
            (
                "b",
                "A blue/green deployment that switches traffic between two parallel "
                "environments.",
            ),
            ("c", "Deleting the old stack first and then deploying the new one into its " "place."),
            (
                "d",
                "A rolling restart within one environment, with no second environment "
                "to fall back on.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Blue/green keeps both environments live and flips traffic, enabling "
        "instant rollback. In-place upgrades, deleting first, and a single rolling "
        "restart all lack a ready fallback environment.",
        "rationales": {
            "a": (False, "In-place upgrades leave no clean environment to roll back to."),
            "b": (True, "Blue/green keeps a known-good environment for instant " "rollback."),
            "c": (False, "Deleting the old stack removes the rollback target."),
            "d": (False, "A single-environment rolling restart offers no safe " "fallback."),
        },
    },
    {
        "question_id": "d2-gpu-vs-cpu-inference",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A self-hosted large language model on SageMaker shows unacceptable latency on "
        "CPU instances under load. The model benefits heavily from parallel matrix "
        "operations. Which change MOST directly improves throughput?",
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
        "explanation": "GPU instances accelerate the parallel matrix math LLM inference needs, "
        "directly improving latency. More CPU nodes scale a slow path, fewer "
        "instances worsen it, and a longer timeout only hides the slowness.",
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
        "prompt": "A rarely used internal tool must host a custom model but the team will not "
        "tolerate paying for idle endpoint instances and accepts occasional cold-start "
        "latency. Which SageMaker option fits BEST?",
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
        "explanation": "Serverless Inference scales to zero and bills per use, accepting cold "
        "starts for rarely used models. A 24/7 endpoint, Bedrock provisioning, and "
        "an always-on pool all pay for idle time.",
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
        "prompt": "Before committing Provisioned Throughput, a team must decide how many model "
        "units to reserve. Which input is MOST relevant to that sizing decision?",
        "scenario_constraint": "Size reserved capacity to real demand.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "The number of developers on the team building the feature this " "quarter."),
            ("b", "The color scheme and layout chosen for the feature's user interface."),
            ("c", "The feature's measured peak tokens-per-minute throughput requirement."),
            ("d", "The foundation model's public release date and version identifier."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Measured peak throughput in tokens per minute drives how many model units "
        "to reserve. Team size, UI styling, and release date are irrelevant to "
        "capacity sizing.",
        "rationales": {
            "a": (False, "Team size does not determine inference throughput needs."),
            "b": (False, "UI styling is unrelated to capacity sizing."),
            "c": (True, "Peak tokens-per-minute throughput sizes the model units."),
            "d": (False, "A model's release date does not size committed capacity."),
        },
    },
    {
        "question_id": "d2-api-gateway-frontdoor",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A GenAI backend built on Lambda must be exposed to external clients with "
        "throttling, API keys, and request validation at the edge, without building "
        "those features yourself. Which service fits BEST as the front door?",
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
        "explanation": "API Gateway provides managed throttling, API keys, and request validation "
        "at the edge. A bare ALB and raw function URLs lack those controls, and "
        "CloudFront is a CDN, not an API management layer.",
        "rationales": {
            "a": (False, "A plain ALB offers no API keys or request validation."),
            "b": (True, "API Gateway delivers throttling, keys, and validation out of " "the box."),
            "c": (False, "Function URLs expose Lambda without managed API controls."),
            "d": (False, "CloudFront caches content; it is not an API management " "layer."),
        },
    },
    {
        "question_id": "d2-eventbridge-decoupling",
        "objective_ids": ["AIP-2.3"],
        "prompt": "When a document is uploaded, several independent GenAI pipelines (summarize, "
        "classify, index) must each react, and the team wants to add new consumers later "
        "without touching the producer. Which TWO patterns support this decoupled "
        "fan-out? Select TWO.",
        "scenario_constraint": "Fan out one event to many evolvable consumers.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            (
                "a",
                "Publish an event to Amazon EventBridge and let each pipeline subscribe "
                "via rules.",
            ),
            ("b", "Publish to an Amazon SNS topic each pipeline subscribes to."),
            ("c", "Have the producer call each pipeline synchronously in a loop."),
            ("d", "Store a flag in a database each pipeline polls every minute."),
            ("e", "Hard-code the three pipeline ARNs into the producer."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": "Both EventBridge rules and an SNS topic decouple the producer from "
        "consumers so new pipelines subscribe without producer changes. Synchronous "
        "loops and hard-coded ARNs couple tightly, and polling a flag adds latency "
        "and load.",
        "rationales": {
            "a": (
                True,
                "EventBridge fan-out lets consumers evolve independently of the " "producer.",
            ),
            "b": (True, "An SNS topic broadcasts to many subscribers without producer " "edits."),
            "c": (False, "Synchronous calls couple the producer to every consumer."),
            "d": (False, "Polling adds latency and does not scale cleanly."),
            "e": (False, "Hard-coded ARNs require producer edits for each new " "consumer."),
        },
    },
    {
        "question_id": "d2-sqs-buffer-spikes",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A GenAI processing service is occasionally overwhelmed by sudden bursts of "
        "upstream requests, dropping work. The team wants to absorb spikes and process "
        "at a steady rate. Which service fits BEST?",
        "scenario_constraint": "Buffer bursty load and smooth downstream processing.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Place an Amazon SQS queue between the producers and the downstream " "processor.",
            ),
            (
                "b",
                "Call the processor synchronously and simply retry whenever a spike "
                "causes failures.",
            ),
            (
                "c",
                "Increase the processor's request timeout so it can absorb each traffic "
                "spike itself.",
            ),
            (
                "d",
                "Add extra fields to each request so the processor can prioritize "
                "during spikes.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "An SQS queue buffers bursts and lets the processor consume at a "
        "sustainable rate, preventing dropped work. Synchronous retries, longer "
        "timeouts, and extra fields do not absorb spikes.",
        "rationales": {
            "a": (True, "An SQS queue buffers spikes and decouples producer from " "processor."),
            "b": (False, "Synchronous calls with retries amplify load during spikes."),
            "c": (False, "A longer timeout does not stop the processor from being " "overwhelmed."),
            "d": (False, "Extra request fields do nothing to absorb traffic spikes."),
        },
    },
    {
        "question_id": "d2-step-functions-orchestration",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A multi-stage GenAI workflow has conditional branches, retries with backoff, "
        "and a human-approval wait that can last hours, and the team needs auditable "
        "state at each step. Which service orchestrates this BEST?",
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
        "explanation": "Step Functions models branches, retries, long waits, and per-step state "
        "with built-in auditability. A single Lambda cannot wait hours, cron "
        "polling is brittle, and a bare queue has no orchestration.",
        "rationales": {
            "a": (False, "A single Lambda cannot survive multi-hour human waits."),
            "b": (False, "Cron polling lacks branching and durable per-step state."),
            "c": (False, "A bare queue provides no workflow coordination."),
            "d": (
                True,
                "Step Functions handles branching, retries, long waits, and " "state tracking.",
            ),
        },
    },
    {
        "question_id": "d2-genai-gateway-centralize",
        "objective_ids": ["AIP-2.3"],
        "prompt": "An enterprise with many teams calling foundation models adopts a shared GenAI "
        "gateway fronting all model access. Which TWO governance capabilities does "
        "centralizing on the gateway most directly enable? Select TWO.",
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
        "explanation": "A gateway centralizes quota enforcement and usage logging with routing to "
        "approved models. It does not remove IAM, eliminate latency, or guarantee "
        "model correctness.",
        "rationales": {
            "a": (True, "A gateway enforces shared per-team quotas centrally."),
            "b": (True, "Centralized logging and approved-model routing live at the " "gateway."),
            "c": (False, "A gateway still relies on IAM for authorization."),
            "d": (False, "A gateway adds a hop; it does not remove model latency."),
            "e": (False, "No gateway can guarantee model output correctness."),
        },
    },
    {
        "question_id": "d2-tenant-identity-propagation",
        "objective_ids": ["AIP-2.3", "AIP-3.1"],
        "prompt": "A multi-tenant SaaS must ensure each GenAI request is processed and logged "
        "under the correct tenant, so one tenant can never access another's data. Which "
        "approach is MOST reliable?",
        "scenario_constraint": "Guarantee per-tenant isolation across the request path.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Let clients pass a tenant ID header that the backend trusts without "
                "any verification.",
            ),
            (
                "b",
                "Propagate a verified tenant identity from the edge through each layer "
                "and enforce it on data access.",
            ),
            (
                "c",
                "Store every tenant's data together and filter it to the right tenant "
                "only in the UI.",
            ),
            (
                "d",
                "Trust the model to keep each tenant's data separate inside its own "
                "context window.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Propagating a verified identity/tenant context and enforcing it at data "
        "access is the reliable isolation boundary. Trusting a client-sent header "
        "invites spoofing, UI filtering leaks data, and the model cannot enforce "
        "access control.",
        "rationales": {
            "a": (False, "An unverified header is trivially spoofed to reach other " "tenants."),
            "b": (
                True,
                "A verified, enforced identity context isolates tenant data at " "the source.",
            ),
            "c": (False, "UI-only filtering leaves cross-tenant data exposed at the " "backend."),
            "d": (False, "The model cannot be relied on to enforce tenant isolation."),
        },
    },
    {
        "question_id": "d2-cicd-model-app",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A team wants automated build, test, and deployment of their GenAI application "
        "whenever code is merged, using AWS-native CI/CD. Which TWO services directly "
        "provide the pipeline and build steps? Select TWO.",
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
        "explanation": "CodePipeline orchestrates the CI/CD stages and CodeBuild runs the build "
        "and test steps. QuickSight, Rekognition, and Polly are unrelated to "
        "pipeline automation.",
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
        "prompt": "One upstream service emits domain events that must reach multiple unrelated "
        "subscribers based on event attributes, while another path needs a durable work "
        "queue consumed by a single worker pool. Which pairing fits BEST?",
        "scenario_constraint": "Match routing-to-many versus buffered-work-to-one.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Use SQS to fan out to many independent subscribers and reserve "
                "EventBridge for the single buffered worker queue.",
            ),
            (
                "b",
                "Use Amazon API Gateway for both the fan-out path and the buffered "
                "worker queue.",
            ),
            (
                "c",
                "Use EventBridge for attribute-based fan-out and SQS for the buffered "
                "single-consumer queue.",
            ),
            (
                "d",
                "Use AWS Step Functions as the mechanism for both the fan-out and the "
                "worker queue.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "EventBridge routes events to many subscribers by attributes, while SQS "
        "buffers work for a single consumer pool. The reversed pairing misuses each "
        "service, and API Gateway and Step Functions solve different problems.",
        "rationales": {
            "a": (
                False,
                "SQS does not fan out to many independent subscribers; the " "roles are reversed.",
            ),
            "b": (False, "API Gateway is a request front door, not a fan-out or queue " "service."),
            "c": (
                True,
                "EventBridge routes by attributes to many; SQS buffers for one " "consumer.",
            ),
            "d": (
                False,
                "Step Functions orchestrates workflows, not pub/sub fan-out or " "buffering.",
            ),
        },
    },
    {
        "question_id": "d2-canary-rollback-integration",
        "objective_ids": ["AIP-2.3"],
        "prompt": "After deploying a new GenAI API version via a canary, error rates spike for the "
        "canary slice. The pipeline should react without a human in the loop. Which "
        "capability fits BEST?",
        "scenario_constraint": "Automatically abort a bad canary.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Wait for the weekly deployment review to notice the elevated error "
                "rate manually.",
            ),
            (
                "b",
                "Increase the canary's traffic share so the regression produces more "
                "data to study.",
            ),
            (
                "c",
                "Disable the canary monitoring temporarily to reduce the volume of " "alarm noise.",
            ),
            (
                "d",
                "Trigger an automated rollback from a canary CloudWatch alarm on the "
                "error metric.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "An alarm-triggered automated rollback reverts the canary the moment errors "
        "breach a threshold. Weekly review is too slow, raising canary traffic "
        "worsens impact, and disabling monitoring removes the safety signal.",
        "rationales": {
            "a": (False, "A weekly manual review reacts far too slowly to a live " "regression."),
            "b": (False, "Raising canary traffic exposes more users to the regression."),
            "c": (False, "Disabling monitoring hides the very signal needed to react."),
            "d": (True, "An alarm-driven automated rollback reverts the bad version " "fast."),
        },
    },
    {
        "question_id": "d2-outposts-data-jurisdiction",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A customer must keep certain inference and data processing on premises within "
        "their own facility for jurisdictional reasons, while using AWS tooling. Which "
        "AWS option BEST addresses this placement constraint?",
        "scenario_constraint": "Process on premises under AWS operations.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "AWS Outposts installed in the customer's own data center within the "
                "jurisdiction.",
            ),
            ("b", "A standard AWS Region located in a different country with ample " "capacity."),
            ("c", "Amazon CloudFront edge caching to keep the data physically close to " "users."),
            ("d", "Multi-Region replication spread across continents for durability and " "reach."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Outposts extends AWS into the customer's own facility, satisfying "
        "on-premises jurisdictional placement. A foreign Region violates it, "
        "CloudFront caches content, and multi-Region replication spreads data "
        "wider.",
        "rationales": {
            "a": (
                True,
                "Outposts keeps processing on-premises within the required " "jurisdiction.",
            ),
            "b": (False, "A Region in another country violates the data-jurisdiction " "rule."),
            "c": (False, "CloudFront caches content and does not control data " "residency."),
            "d": (False, "Cross-continent replication moves data out of jurisdiction."),
        },
    },
    {
        "question_id": "d2-wavelength-low-latency-edge",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A mobile GenAI feature requires single-digit-millisecond latency to end-user "
        "devices on a carrier's 5G network. Which AWS placement option is designed for "
        "ultra-low latency at the mobile edge?",
        "scenario_constraint": "Minimize latency to 5G mobile users.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "AWS Wavelength zones embedded inside telecom networks near the end " "users."),
            (
                "b",
                "A single central Region located far from most of the latency-sensitive " "users.",
            ),
            ("c", "Amazon S3 Transfer Acceleration to speed uploads toward a distant " "Region."),
            ("d", "AWS Outposts installed in a corporate office away from the mobile " "users."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Wavelength places compute inside carrier networks for ultra-low latency to "
        "5G devices. A distant central Region adds latency, S3 Transfer "
        "Acceleration speeds uploads, and office Outposts does not serve the mobile "
        "edge.",
        "rationales": {
            "a": (True, "Wavelength places compute at the telecom edge for lowest " "latency."),
            "b": (False, "A distant central Region adds the latency the scenario wants " "to cut."),
            "c": (
                False,
                "Transfer Acceleration speeds S3 uploads, not model inference " "latency.",
            ),
            "d": (False, "An office Outpost is not near the mobile end users."),
        },
    },
    {
        "question_id": "d2-event-driven-vs-sync-coupling",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A GenAI ingestion step and a downstream analytics team deploy on different "
        "schedules and must not block each other if one is temporarily down. Which "
        "integration style BEST reduces coupling?",
        "scenario_constraint": "Isolate two independently-evolving services from each other's "
        "downtime.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Make a synchronous HTTP call from the first service directly into the "
                "second on every single request path.",
            ),
            (
                "b",
                "Asynchronous event-driven integration through a queue or an event bus "
                "between them.",
            ),
            (
                "c",
                "A shared in-process library that both services import and call "
                "directly in code.",
            ),
            (
                "d",
                "A single database connection shared by both services to pass work "
                "between them.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Async event-driven integration lets each service run and deploy "
        "independently and tolerate the other's downtime. Synchronous calls, a "
        "shared library, and a shared database all tighten coupling.",
        "rationales": {
            "a": (
                False,
                "A synchronous call tightly couples the services and their " "availability.",
            ),
            "b": (True, "An event bus or queue decouples the services asynchronously."),
            "c": (False, "A shared library couples their deploy and runtime lifecycles."),
            "d": (False, "A shared database connection couples their internal " "schemas."),
        },
    },
    {
        "question_id": "d2-apigw-request-validation",
        "objective_ids": ["AIP-2.3", "AIP-2.4"],
        "prompt": "Malformed client payloads reach a GenAI Lambda and waste model invocations "
        "before failing. The team wants to reject invalid requests before any compute "
        "runs. Which control fits BEST?",
        "scenario_constraint": "Reject invalid requests before invoking compute.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Validate the incoming request inside the model prompt by asking the "
                "model to check it.",
            ),
            (
                "b",
                "Let the Lambda call the model first and then inspect the input after "
                "the response.",
            ),
            (
                "c",
                "Define a request model and enable API Gateway request validation at " "the edge.",
            ),
            (
                "d",
                "Increase the Lambda's memory so it can process malformed input more " "quickly.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "API Gateway request validation rejects malformed payloads at the edge "
        "before Lambda or the model runs. Prompt-level checks run after invocation, "
        "late validation already paid for compute, and more memory ignores the "
        "problem.",
        "rationales": {
            "a": (False, "Prompt-based checking is not an enforced input validation " "layer."),
            "b": (False, "Validating after the model call wastes the invocation on bad " "input."),
            "c": (True, "API Gateway request validation rejects bad input before " "compute runs."),
            "d": (False, "More memory does not validate or reject malformed requests."),
        },
    },
    {
        "question_id": "d2-dlq-poison-messages",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": "A queue-driven GenAI worker keeps retrying a few malformed messages that can "
        "never succeed, blocking healthy messages behind them. Which mechanism BEST "
        "isolates the bad messages?",
        "scenario_constraint": "Prevent poison messages from blocking the queue.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Delete the entire queue and recreate it whenever poison messages pile " "up."),
            (
                "b",
                "Disable retries so every failing message is dropped silently on first " "failure.",
            ),
            (
                "c",
                "Increase the visibility timeout indefinitely so bad messages stop " "reappearing.",
            ),
            (
                "d",
                "Configure a dead-letter queue to capture messages after a max receive " "count.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "A dead-letter queue moves repeatedly failing messages aside after a "
        "threshold so healthy ones flow. Recreating the queue loses work, disabling "
        "retries drops valid transient failures, and a huge visibility timeout "
        "stalls processing.",
        "rationales": {
            "a": (False, "Recreating the queue destroys good messages along with poison " "ones."),
            "b": (False, "Dropping failures silently loses messages and hides the " "problem."),
            "c": (False, "An endless visibility timeout just hides the stuck message."),
            "d": (True, "A DLQ isolates poison messages after a bounded retry count."),
        },
    },
    {
        "question_id": "d2-step-functions-vs-chained-lambda",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A team built a GenAI pipeline as five Lambdas each invoking the next directly, "
        "and debugging failures across them is painful with no central view of state. "
        "Which refactor MOST improves observability and error handling?",
        "scenario_constraint": "Gain centralized state and error handling across steps.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Merge all five Lambda functions into one giant function that runs " "every step.",
            ),
            (
                "b",
                "Add verbose print statements to each Lambda and trace the flow through " "logs.",
            ),
            ("c", "Orchestrate the five Lambdas with an AWS Step Functions state " "machine."),
            ("d", "Have each Lambda write progress to a shared text file the next one " "reads."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Step Functions provides centralized state, visual execution history, and "
        "built-in retry/catch across steps. Merging into one function reduces "
        "modularity, print statements lack correlation, and a shared file is "
        "fragile.",
        "rationales": {
            "a": (False, "One giant function loses isolation, retries, and step " "visibility."),
            "b": (False, "Print statements do not provide orchestration or error " "handling."),
            "c": (True, "Step Functions sequences the Lambdas with built-in retries and " "state."),
            "d": (False, "A shared file for coordination is fragile and race-prone."),
        },
    },
    {
        "question_id": "d2-blue-green-db-migration-risk",
        "objective_ids": ["AIP-2.3"],
        "prompt": "During a GenAI service rollout, the new version needs a backward compatible "
        "schema change so both old and new versions can run during the canary. Which "
        "practice BEST supports safe canary and rollback?",
        "scenario_constraint": "Keep both versions working during a gradual rollout.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Drop the old columns immediately the moment the new application "
                "version deploys.",
            ),
            (
                "b",
                "Apply additive, backward-compatible schema changes before shifting any "
                "traffic.",
            ),
            (
                "c",
                "Rename the tables that the old version still reads during the overlap " "window.",
            ),
            (
                "d",
                "Require a full downtime maintenance window for every schema-touching " "deploy.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Additive, backward-compatible changes let old and new versions coexist, "
        "preserving rollback during a canary. Dropping columns or renaming tables "
        "breaks the old version, and mandatory downtime defeats the gradual "
        "rollout.",
        "rationales": {
            "a": (False, "Dropping columns breaks the old version still serving " "traffic."),
            "b": (True, "Additive backward-compatible changes let both versions run " "safely."),
            "c": (False, "Renaming live tables breaks the old version mid-rollout."),
            "d": (False, "Mandatory downtime defeats the point of blue/green deploys."),
        },
    },
    {
        "question_id": "d2-private-connectivity-vpc",
        "objective_ids": ["AIP-2.3", "AIP-3.1"],
        "prompt": "A security policy forbids GenAI traffic to Bedrock from traversing the public "
        "internet. The workload runs in a VPC. Which approach keeps the traffic private "
        "with the least custom networking?",
        "scenario_constraint": "Reach Bedrock privately without public internet.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Use a VPC interface endpoint (PrivateLink) so Bedrock traffic stays on "
                "the private network.",
            ),
            (
                "b",
                "Route the workload's Bedrock traffic out through a public NAT gateway "
                "and across the internet to the service endpoint.",
            ),
            (
                "c",
                "Assign public IP addresses to the workload instances so they can reach "
                "Bedrock directly.",
            ),
            (
                "d",
                "Open the security group to 0.0.0.0/0 so the instances can call the "
                "Bedrock endpoint.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "A VPC interface endpoint keeps Bedrock traffic on the AWS private network "
        "via PrivateLink. A NAT gateway and public IPs still traverse the internet, "
        "and opening the security group broadly worsens exposure.",
        "rationales": {
            "a": (
                True,
                "A PrivateLink interface endpoint keeps traffic off the public " "internet.",
            ),
            "b": (False, "A NAT gateway still routes the traffic over the public " "internet."),
            "c": (False, "Public IPs expose the workload rather than keeping traffic " "private."),
            "d": (False, "Opening the group to the world is an unrelated security " "regression."),
        },
    },
    {
        "question_id": "d2-idempotent-event-consumer",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": "An EventBridge-driven GenAI consumer may receive the same event more than once "
        "because delivery is at-least-once, and reprocessing causes duplicate charges. "
        "Which design BEST prevents double effects?",
        "scenario_constraint": "Tolerate duplicate event delivery without double side effects.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Assume each event is delivered exactly once and process it without any " "dedup.",
            ),
            (
                "b",
                "Process events faster so duplicate deliveries become statistically " "unlikely.",
            ),
            (
                "c",
                "Ignore the duplicate problem entirely because repeats are expected to " "be rare.",
            ),
            ("d", "Deduplicate on a stable event ID so a repeated delivery becomes a " "no-op."),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Deduplicating on a stable event ID makes reprocessing a harmless no-op "
        "under at-least-once delivery. Assuming exactly-once is false, processing "
        "faster does not remove duplicates, and ignoring the issue leaves double "
        "charges.",
        "rationales": {
            "a": (False, "At-least-once delivery means exactly-once cannot be assumed."),
            "b": (False, "Processing faster does not prevent duplicate deliveries."),
            "c": (False, "Ignoring duplicates leaves double-processing bugs in place."),
            "d": (True, "Keying on a stable event ID makes reprocessing harmless."),
        },
    },
    {
        "question_id": "d2-apigw-throttle-protect-backend",
        "objective_ids": ["AIP-2.3", "AIP-2.2"],
        "prompt": "A public GenAI endpoint occasionally gets flooded by a single client, "
        "exhausting the shared Bedrock quota for everyone. The team wants fair usage "
        "without manual intervention. Which control fits BEST?",
        "scenario_constraint": "Prevent one client from exhausting shared capacity.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Ask client teams politely not to flood the API during their peak " "periods."),
            (
                "b",
                "Apply API Gateway usage plans with per-key rate and burst limits on " "callers.",
            ),
            (
                "c",
                "Raise the account's Bedrock invocation quota and hope the extra "
                "headroom absorbs the floods from noisy callers.",
            ),
            ("d", "Disable the API endpoint entirely whenever a traffic flood is " "detected."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Per-key usage plans enforce fair rate and burst limits so one client "
        "cannot starve others. Polite requests are unenforced, raising quotas just "
        "delays exhaustion, and disabling the endpoint harms all clients.",
        "rationales": {
            "a": (False, "A polite request does not enforce any rate limit."),
            "b": (True, "Usage plans enforce per-caller rate and burst limits at the " "edge."),
            "c": (False, "A higher quota just lets more traffic reach the backend."),
            "d": (False, "Disabling the endpoint denies all legitimate callers too."),
        },
    },
    {
        "question_id": "d2-multi-account-governance",
        "objective_ids": ["AIP-2.3", "AIP-3.1"],
        "prompt": "A large organization wants consistent guardrails, logging, and service control "
        "policies applied across many AWS accounts running GenAI workloads. Which "
        "approach fits BEST?",
        "scenario_constraint": "Enforce consistent org-wide policy across many accounts.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Email each account owner a list of rules and trust them to apply the " "rules."),
            (
                "b",
                "Grant one administrator access to every account to enforce the rules "
                "centrally.",
            ),
            ("c", "Manage the accounts under AWS Organizations with service control " "policies."),
            (
                "d",
                "Let each team configure its own account policies independently of the " "others.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "AWS Organizations with SCPs enforces guardrails and policy consistently "
        "across accounts. Emails and per-team configuration are unenforced and "
        "drift, and a single human admin does not scale or guarantee enforcement.",
        "rationales": {
            "a": (False, "Emailed rules are not technically enforced across accounts."),
            "b": (False, "One admin everywhere is a huge blast-radius and audit risk."),
            "c": (True, "Organizations with SCPs enforce guardrails across all " "accounts."),
            "d": (False, "Independent per-team policies produce inconsistent " "governance."),
        },
    },
    {
        "question_id": "d2-genai-gateway-model-routing",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": "Through a central GenAI gateway, the team wants requests routed to a primary "
        "model but automatically sent to a secondary model if the primary is "
        "unavailable, transparent to callers. Which capability fits BEST?",
        "scenario_constraint": "Transparent failover between models at the gateway.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Return an error to every caller whenever the primary model is "
                "temporarily down.",
            ),
            (
                "b",
                "Hard-code the primary model identifier into each client application "
                "separately.",
            ),
            (
                "c",
                "Ask callers to retry against a different model manually when the "
                "primary struggles.",
            ),
            (
                "d",
                "Define a model routing policy with a fallback target enforced at the " "gateway.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "A gateway routing policy with a fallback target redirects to the secondary "
        "model transparently on primary failure. Returning errors, hard-coding "
        "clients, and manual retries all push the problem onto callers.",
        "rationales": {
            "a": (False, "Erroring out on primary failure gives no resilience."),
            "b": (False, "Hard-coding the model per client blocks central failover."),
            "c": (False, "Manual caller retries are slow and inconsistent."),
            "d": (True, "A gateway routing policy fails over to the fallback " "automatically."),
        },
    },
    {
        "question_id": "d2-eventbridge-schema-evolution",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A producer must add a new optional field to events many GenAI consumers "
        "process, without forcing every consumer to redeploy at once. Which practice "
        "BEST supports this evolution?",
        "scenario_constraint": "Evolve event payloads without breaking existing consumers.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Add the new field as optional and keep all existing fields backward "
                "compatible.",
            ),
            (
                "b",
                "Rename several existing event fields in the very same release that "
                "introduces the brand-new field consumers want.",
            ),
            ("c", "Remove fields that look unused even though some consumers still read " "them."),
            (
                "d",
                "Change the event's type for every schema change so consumers must "
                "re-subscribe.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Adding optional, backward-compatible fields lets old consumers keep "
        "working while new ones adopt the field. Renaming, removing read fields, "
        "and churning event types break existing consumers.",
        "rationales": {
            "a": (True, "Optional additive fields keep existing consumers working."),
            "b": (False, "Renaming live fields breaks consumers reading the old names."),
            "c": (False, "Removing still-read fields breaks those consumers."),
            "d": (False, "Churning the event type forces constant consumer rework."),
        },
    },
    {
        "question_id": "d2-cicd-model-eval-gate",
        "objective_ids": ["AIP-2.3", "AIP-2.5"],
        "prompt": "A team wants its pipeline to block promotion of a new prompt or model version "
        "if automated quality evaluations regress below a threshold. Where does this "
        "check belong?",
        "scenario_constraint": "Prevent regressions from reaching production automatically.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Run the model evaluation as an automated gate stage inside the CI/CD " "pipeline.",
            ),
            (
                "b",
                "Perform a manual spot-check of the model's quality only after it has "
                "already been promoted to the production stage.",
            ),
            ("c", "Record the evaluation results as a note in the pull request " "description."),
            ("d", "Compile the evaluation into a monthly report reviewed well after " "release."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "An automated evaluation gate in the pipeline blocks promotion when quality "
        "regresses, before users are affected. Post-release checks, PR notes, and "
        "monthly reports all catch regressions too late.",
        "rationales": {
            "a": (True, "An automated eval gate blocks regressions before release."),
            "b": (False, "A post-release spot-check lets regressions reach users first."),
            "c": (False, "A PR note is not an enforced quality gate."),
            "d": (False, "A monthly report reacts long after the bad deploy."),
        },
    },
    {
        "question_id": "d2-sync-vs-async-ux-choice",
        "objective_ids": ["AIP-2.3", "AIP-2.2"],
        "prompt": "A GenAI feature kicks off a report that takes two minutes to generate, and the "
        "web client must stay responsive without holding a connection open. Which "
        "integration pattern fits BEST?",
        "scenario_constraint": "Keep the client responsive during a long-running task.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Block the HTTP request for the full two minutes until the report " "finishes."),
            (
                "b",
                "Submit the report job asynchronously and notify the client when "
                "results are ready.",
            ),
            ("c", "Reject the request outright as too slow to serve within the request " "window."),
            (
                "d",
                "Shorten the report content drastically so it fits inside a synchronous " "call.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "An async submit-and-notify pattern frees the client while the two-minute "
        "job runs. Blocking risks timeouts, rejecting removes the feature, and "
        "arbitrarily shortening the report changes the requirement.",
        "rationales": {
            "a": (False, "A two-minute blocking request risks client and gateway " "timeouts."),
            "b": (True, "Async submission with notification fits the long-running job."),
            "c": (False, "Rejecting the request fails the legitimate use case."),
            "d": (False, "Truncating the report sacrifices the required output."),
        },
    },
    {
        "question_id": "d2-invokemodel-sync-vs-stream",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A chat UI should display the model's answer token by token as it is generated "
        "so users see progress immediately. Which Bedrock API call fits BEST?",
        "scenario_constraint": "Deliver output incrementally as it is generated.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "InvokeModel returning the entire response at once after full " "generation."),
            (
                "b",
                "A Bedrock batch inference job that produces the full answer offline "
                "and writes it out for retrieval later.",
            ),
            ("c", "InvokeModelWithResponseStream delivering tokens incrementally as " "generated."),
            ("d", "A SageMaker asynchronous endpoint writing the result to S3 when " "done."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "InvokeModelWithResponseStream streams tokens as they are produced, ideal "
        "for progressive chat UIs. Plain InvokeModel waits for the full answer, "
        "batch is offline, and async writes results later to S3.",
        "rationales": {
            "a": (False, "Returning everything at once delays the first visible token."),
            "b": (False, "Batch inference is offline and not interactive."),
            "c": (True, "Response streaming shows tokens as they are generated."),
            "d": (False, "An async S3-delivered result is not an interactive stream."),
        },
    },
    {
        "question_id": "d2-backoff-jitter-throttle",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A client hitting Bedrock sees intermittent throttling, and naive immediate "
        "retries make it worse by synchronizing with other clients. Which TWO practices "
        "BEST handle the throttling? Select TWO.",
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
        "explanation": "Jitter de-synchronizes retries while exponential backoff with an attempt "
        "cap bounds total effort, together easing throttling. Fixed immediate "
        "retries synchronize clients, manual restarts do not scale, and more "
        "concurrency deepens the throttle.",
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
        "prompt": "A client blindly retries every failed model call, including ones caused by a "
        "malformed request, wasting quota. Which retry policy is MOST correct?",
        "scenario_constraint": "Retry only errors that can succeed on retry.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Retry every error type the same way with the same backoff and attempt " "cap."),
            (
                "b",
                "Retry only validation errors, treating malformed input as the client's "
                "own recoverable and transient fault.",
            ),
            ("c", "Never retry any error and surface every failure immediately to the " "caller."),
            (
                "d",
                "Retry throttling and transient server errors but never retry "
                "validation errors.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Throttling and transient 5xx errors can succeed on retry, while a "
        "validation error will fail identically until the request is fixed. "
        "Retrying everything wastes quota, retrying only validation errors is "
        "pointless, and never retrying drops recoverable failures.",
        "rationales": {
            "a": (False, "Retrying validation errors identically just repeats the " "failure."),
            "b": (False, "Validation errors are deterministic and should not be " "retried."),
            "c": (False, "Never retrying wastes recoverable throttling and transient " "faults."),
            "d": (
                True,
                "Retrying only transient faults, not validation, is the correct " "policy.",
            ),
        },
    },
    {
        "question_id": "d2-context-window-overflow",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": "A summarization endpoint intermittently fails when users paste very long "
        "documents, with errors about exceeding the input limit. Which TWO fixes "
        "directly address the cause? Select TWO.",
        "scenario_constraint": "Keep input within the model's context window.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            (
                "a",
                "Chunk the input into context-window-sized pieces and summarize " "hierarchically.",
            ),
            ("b", "Truncate or compress input to fit the context window before invoking."),
            ("c", "Increase the request timeout."),
            ("d", "Add more retries with backoff."),
            ("e", "Raise the account's invocation quota."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": "The failure is an input-size limit, so chunking hierarchically or "
        "compressing input to fit the context window resolves it. Timeouts, "
        "retries, and quota changes address latency or throttling, not oversized "
        "input.",
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
        "prompt": "A client times out after sending a request that actually succeeded server-side, "
        "then retries, risking a duplicate billable action in a downstream mutating "
        "workflow. Which mechanism BEST prevents the duplicate?",
        "scenario_constraint": "Make a retried request produce one effect, not two.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Shorten the client timeout so retries fire sooner after a slow " "response."),
            ("b", "Disable client retries entirely so a request is never sent more than " "once."),
            (
                "c",
                "Send a client-generated idempotency key the server deduplicates "
                "repeated calls on.",
            ),
            (
                "d",
                "Log any duplicate invocations and reconcile the extra results manually " "later.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "An idempotency key lets the server recognize the retry as the same request "
        "and avoid a second effect. Shorter timeouts increase retries, disabling "
        "retries loses genuine failures, and manual reconciliation is reactive.",
        "rationales": {
            "a": (False, "A shorter timeout increases retries and duplication."),
            "b": (False, "Disabling retries sacrifices resilience to transient faults."),
            "c": (True, "An idempotency key makes repeated calls resolve to one " "effect."),
            "d": (False, "Manual reconciliation is reactive and error-prone."),
        },
    },
    {
        "question_id": "d2-timeout-vs-hang",
        "objective_ids": ["AIP-2.4"],
        "prompt": "Occasionally a model call never returns and the calling thread hangs "
        "indefinitely, exhausting the connection pool. Which configuration BEST prevents "
        "the hang?",
        "scenario_constraint": "Bound how long a single call may block.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Add more connections to the client pool so a hung call has company."),
            ("b", "Set explicit connect and read timeouts on the client for every call."),
            ("c", "Increase the model's max tokens so responses are less likely to " "stall."),
            ("d", "Retry the call eagerly before the first attempt has even returned."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Explicit connect and read timeouts bound how long a call can block, "
        "freeing the thread and pool. A bigger pool only delays exhaustion, more "
        "tokens lengthen responses, and overlapping retries worsen resource use.",
        "rationales": {
            "a": (False, "More connections do not stop an individual call from hanging."),
            "b": (True, "Explicit connect and read timeouts bound a hung call."),
            "c": (False, "Max tokens affects length, not hang behavior."),
            "d": (False, "Overlapping retries amplify load without bounding the hang."),
        },
    },
    {
        "question_id": "d2-request-schema-validation",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A service occasionally sends a model request body missing a required field, "
        "discovering the problem only from a provider error. Which practice catches this "
        "earlier with the LEAST overhead?",
        "scenario_constraint": "Catch malformed request bodies before the API call.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Validate the request against a typed schema before invoking the " "model."),
            ("b", "Rely on the model provider to reject malformed requests on your " "behalf."),
            (
                "c",
                "Add retries so a malformed request eventually succeeds after enough " "attempts.",
            ),
            ("d", "Wrap the call in a broad try/except that swallows and ignores any " "errors."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Validating the request against a typed schema catches missing fields "
        "before the network call. Relying on provider rejection is late, retries "
        "cannot fix a structurally invalid body, and swallowing errors hides the "
        "bug.",
        "rationales": {
            "a": (True, "Schema validation rejects bad requests before the model call."),
            "b": (False, "Relying on the provider wastes calls and leaks bad input."),
            "c": (False, "Retrying a malformed request never makes it valid."),
            "d": (False, "Swallowing errors hides failures instead of handling them."),
        },
    },
    {
        "question_id": "d2-max-tokens-truncation",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": "Users complain that long answers are cut off mid-sentence. Logs show the "
        "response stop reason is the output token limit. Which change MOST directly "
        "fixes the truncation?",
        "scenario_constraint": "Stop responses from being cut off by the output cap.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Lower the sampling temperature so the model stops cutting answers " "short."),
            ("b", "Add more client-side retries so a truncated answer is eventually " "complete."),
            (
                "c",
                "Switch to a smaller foundation model so each response naturally fits "
                "inside the configured token budget.",
            ),
            ("d", "Raise the max-tokens output limit while staying within the context " "budget."),
        ],
        "correct_option_ids": ["d"],
        "explanation": "The stop reason indicates the output cap, so raising max tokens within the "
        "context budget prevents the cutoff. Temperature, retries, and a smaller "
        "model do not change the output-length limit.",
        "rationales": {
            "a": (False, "Temperature does not control output truncation."),
            "b": (False, "Retrying returns the same truncated length."),
            "c": (False, "A smaller model does not grant more output room."),
            "d": (True, "Raising the output token limit lets the full answer return."),
        },
    },
    {
        "question_id": "d2-streaming-error-mid-stream",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": "During a streamed response, the connection drops after half the tokens arrive, "
        "yet the app currently shows the partial text as a completed answer. Which "
        "handling is MOST correct?",
        "scenario_constraint": "Never present an interrupted stream as a complete answer.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Treat the partial text received before the error as the final complete " "answer.",
            ),
            (
                "b",
                "Detect the incomplete stream, mark the result failed or partial, and "
                "retry or surface it.",
            ),
            (
                "c",
                "Pad the truncated response with placeholder text so it looks complete "
                "to the user.",
            ),
            ("d", "Silently discard the whole request and show the user nothing at all."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Detecting the interrupted stream and marking it partial prevents a "
        "false-success display, enabling retry or an honest error. Treating partial "
        "text as final, padding, or silent discard all misrepresent the outcome.",
        "rationales": {
            "a": (False, "Partial text is not a validated complete answer."),
            "b": (
                True,
                "Detecting and flagging the incomplete stream enables correct " "recovery.",
            ),
            "c": (False, "Padding fakes completeness and misleads the user."),
            "d": (False, "Silently dropping the request hides the failure."),
        },
    },
    {
        "question_id": "d2-token-budget-prompt-response",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A request fails because the prompt plus requested output exceeds the model's "
        "total token budget. The team needs long answers but a very large system prompt. "
        "Which TWO adjustments directly reduce the overflow? Select TWO.",
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
        "explanation": "Trimming the system prompt and reducing retrieved context both free input "
        "tokens so prompt plus output fits the budget. Timeouts, quotas, and "
        "temperature do not change token consumption.",
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
        "prompt": "A team wants a consistent request/response shape across multiple Bedrock "
        "models, including structured tool-use (function calling), without hand-coding "
        "each model's native payload. Which Bedrock API fits BEST?",
        "scenario_constraint": "Uniform multi-model messaging with built-in tool use.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "A hand-built raw InvokeModel payload crafted separately for each model "
                "provider.",
            ),
            ("b", "A SageMaker batch transform job that scores the conversation turns " "offline."),
            ("c", "The Bedrock Converse API with its unified message and tool-use " "schema."),
            ("d", "Amazon Translate wrapping each turn to normalize the conversation " "format."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "The Converse API gives a unified message format and tool-use schema across "
        "models, avoiding per-model payload code. Raw InvokeModel requires "
        "model-specific bodies, batch transform is offline, and Translate is "
        "unrelated.",
        "rationales": {
            "a": (False, "Hand-built per-model payloads lose the unified tool " "interface."),
            "b": (False, "Batch transform is offline and not conversational."),
            "c": (True, "Converse gives one unified message and tool-use schema across " "models."),
            "d": (False, "Translate changes language, not conversation tool handling."),
        },
    },
    {
        "question_id": "d2-circuit-breaker-dependency",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": "When the model endpoint is failing hard, the app keeps hammering it with "
        "retries, amplifying load and slowing recovery. Which pattern BEST protects both "
        "sides during an outage?",
        "scenario_constraint": "Stop retry amplification during a sustained outage.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Issue unbounded retries against the failing endpoint until it finally "
                "recovers.",
            ),
            (
                "b",
                "Run a fixed one-second retry loop against the dependency with no "
                "attempt limit.",
            ),
            (
                "c",
                "Scale up the client fleet to push more requests through the failing "
                "dependency.",
            ),
            (
                "d",
                "Add a circuit breaker that stops calls after repeated failures and "
                "probes before resuming.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "A circuit breaker trips after repeated failures to stop amplifying load "
        "and probes before resuming, aiding recovery. Unbounded or fixed retry "
        "loops and scaling up clients all worsen the overload.",
        "rationales": {
            "a": (False, "Unbounded retries hammer a failing dependency and spread the " "outage."),
            "b": (False, "A fixed no-limit loop keeps overloading the dependency."),
            "c": (False, "Scaling clients up amplifies the failure load."),
            "d": (True, "A circuit breaker sheds load during failure and probes " "recovery."),
        },
    },
    {
        "question_id": "d2-streaming-backpressure",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A streaming response is produced faster than a slow client can consume it, and "
        "the server buffers tokens until memory grows dangerously. Which approach BEST "
        "manages this?",
        "scenario_constraint": "Match streaming production to slow consumer rate.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Apply backpressure so token production pauses whenever the consumer "
                "falls behind.",
            ),
            (
                "b",
                "Buffer every produced token in memory until the slow client eventually "
                "catches up.",
            ),
            ("c", "Drop random tokens from the stream to keep pace with the slow " "consumer."),
            (
                "d",
                "Disable streaming and send the entire large response in a single final "
                "payload.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Backpressure pauses production when the consumer lags, bounding memory. "
        "Unbounded buffering risks exhaustion, dropping tokens corrupts output, and "
        "reverting to one giant response ignores the slow consumer problem.",
        "rationales": {
            "a": (True, "Backpressure matches production to the consumer's rate " "safely."),
            "b": (False, "Unbounded buffering risks exhausting memory."),
            "c": (False, "Dropping tokens corrupts the response."),
            "d": (False, "A single huge payload defeats the streaming use case."),
        },
    },
    {
        "question_id": "d2-structured-output-parsing",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A downstream system needs the model's answer as strict JSON, but the model "
        "sometimes wraps JSON in prose, breaking the parser. Which approach MOST "
        "reliably yields parseable output?",
        "scenario_constraint": "Guarantee machine-parseable structured output.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Use a tool/function-call schema or constrained JSON output and "
                "validate the result.",
            ),
            (
                "b",
                "Ask the model nicely in the prompt to output only valid JSON and " "nothing else.",
            ),
            ("c", "Regex-strip the surrounding prose and hope the remaining JSON still " "parses."),
            ("d", "Increase the max-tokens limit so the generated JSON has room to be " "longer."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "A tool/function-call schema or constrained JSON mode plus validation "
        "reliably produces parseable structure. Polite prompts are inconsistent, "
        "regex stripping is brittle, and longer output does not guarantee validity.",
        "rationales": {
            "a": (True, "A schema plus validation enforces parseable structured " "output."),
            "b": (False, "A prompt request does not guarantee valid JSON."),
            "c": (False, "Regex stripping is brittle and fails on edge cases."),
            "d": (False, "More tokens do not make the output structurally valid."),
        },
    },
    {
        "question_id": "d2-rate-limit-token-bucket",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A high-throughput client must stay just under the model's requests-per-second "
        "quota while allowing short bursts. Which client-side control fits BEST?",
        "scenario_constraint": "Respect a rate limit while permitting brief bursts.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Apply no client-side limiting and rely entirely on server throttling "
                "to protect you.",
            ),
            (
                "b",
                "Use a token-bucket rate limiter sized to the quota with a small burst "
                "allowance.",
            ),
            (
                "c",
                "Serialize everything to strictly one in-flight request at a time, no "
                "concurrency.",
            ),
            (
                "d",
                "Insert random delays between every call and hope they keep you under "
                "the limit.",
            ),
        ],
        "correct_option_ids": ["b"],
        "explanation": "A token-bucket limiter paces requests to the quota and permits controlled "
        "bursts. Relying on server throttling causes errors, strict serialization "
        "wastes headroom, and random delays do not track the quota.",
        "rationales": {
            "a": (False, "Relying on server throttling means hitting errors by design."),
            "b": (True, "A token bucket paces calls to the quota with controlled " "bursts."),
            "c": (False, "Strict serialization wastes available quota and throughput."),
            "d": (False, "Random delays do not reliably stay under the rate limit."),
        },
    },
    {
        "question_id": "d2-partial-failure-batch-items",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": "A client sends many prompts in one logical operation; a few individual calls "
        "fail while most succeed. The current code reports the whole operation as "
        "success. Which handling is MOST correct?",
        "scenario_constraint": "Report partial failures accurately, not blanket success.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Report overall success as long as at least one call in the batch " "succeeded."),
            ("b", "Report overall failure only when every single call in the batch " "failed."),
            ("c", "Track each item's outcome and report successes and failures " "distinctly."),
            ("d", "Discard the items that failed silently and return only the successful " "ones."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Per-item outcome tracking reports exactly which calls succeeded or failed, "
        "enabling targeted retry. Any-success or all-fail reporting hides partial "
        "failures, and discarding failures loses work silently.",
        "rationales": {
            "a": (False, "One success hides the failed items from callers."),
            "b": (False, "All-or-nothing failure masks partial failures."),
            "c": (True, "Per-item outcomes let callers handle each result correctly."),
            "d": (False, "Silently dropping failures loses required results."),
        },
    },
    {
        "question_id": "d2-connection-reuse-client",
        "objective_ids": ["AIP-2.4", "AIP-2.2"],
        "prompt": "A Lambda recreates a fresh Bedrock client on every invocation, adding handshake "
        "latency. Which change reduces this overhead with the LEAST risk?",
        "scenario_constraint": "Avoid rebuilding the client on every call.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Create two fresh clients on every invocation to add redundancy to each " "call.",
            ),
            ("b", "Open a brand-new TLS connection per request deliberately for " "isolation."),
            ("c", "Serialize the client into a database between calls and reload it each " "time."),
            (
                "d",
                "Initialize the client once outside the handler and reuse it across "
                "invocations.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Initializing the client outside the handler reuses it across warm "
        "invocations, cutting setup latency. Extra clients add overhead, forcing "
        "new connections hurts, and clients are not serializable to a database.",
        "rationales": {
            "a": (False, "Rebuilding clients per call adds latency and overhead."),
            "b": (False, "A new TLS handshake per request is wasteful."),
            "c": (False, "Persisting a client to a database is slow and nonsensical."),
            "d": (True, "Reusing one client across invocations amortizes setup cost."),
        },
    },
    {
        "question_id": "d2-deterministic-output-temperature",
        "objective_ids": ["AIP-2.4"],
        "prompt": "An integration test asserts the model's exact output, but it flakes because "
        "responses vary run to run. Which parameter change MOST reduces this variability "
        "for testing?",
        "scenario_constraint": "Make outputs as repeatable as possible for tests.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase the max-tokens limit so the test output has room to " "stabilize."),
            ("b", "Add more retries to the test so a flaky output eventually matches."),
            (
                "c",
                "Set temperature and top-p to minimal values to minimize sampling " "randomness.",
            ),
            (
                "d",
                "Use a larger context window so the model has more grounding to repeat " "itself.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Minimizing temperature and top-p reduces sampling randomness, making "
        "outputs more repeatable. Token limits, retries, and context size do not "
        "control output variability.",
        "rationales": {
            "a": (False, "Output length does not control nondeterminism."),
            "b": (False, "Retrying masks flakiness instead of removing it."),
            "c": (True, "Minimal temperature and top-p reduce sampling variability."),
            "d": (False, "A bigger context window does not make sampling " "deterministic."),
        },
    },
    {
        "question_id": "d2-streaming-first-token-latency",
        "objective_ids": ["AIP-2.4", "AIP-2.2"],
        "prompt": "Users perceive the assistant as slow even though total generation time is fine, "
        "because nothing appears until the whole answer is ready. Which change MOST "
        "improves perceived responsiveness?",
        "scenario_constraint": "Reduce perceived latency without faster total generation.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Reduce the output length drastically so the whole response returns " "sooner."),
            ("b", "Stream the response so the first tokens reach the user almost " "immediately."),
            (
                "c",
                "Precompute every possible answer offline in advance and serve the "
                "matching one from a lookup table instantly.",
            ),
            ("d", "Lower the temperature so the model generates its answer more " "quickly."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Streaming surfaces the first tokens quickly, improving perceived "
        "responsiveness even at the same total time. Cutting length changes the "
        "answer, precomputing is infeasible for open prompts, and temperature does "
        "not materially change latency.",
        "rationales": {
            "a": (False, "Shorter output does not improve time-to-first-token."),
            "b": (True, "Streaming surfaces the first tokens with minimal delay."),
            "c": (False, "Precomputing all answers is infeasible for open prompts."),
            "d": (False, "Temperature does not control first-token latency."),
        },
    },
    {
        "question_id": "d2-response-schema-validation-output",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": "A downstream service occasionally crashes on an unexpected model response "
        "shape. The team wants to fail safely at the boundary rather than propagate bad "
        "data. Which practice fits BEST?",
        "scenario_constraint": "Contain malformed model responses at the integration boundary.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Validate the model response against an expected schema and handle "
                "failures explicitly.",
            ),
            ("b", "Pass the raw model response straight to the downstream service " "unchecked."),
            ("c", "Assume the response is always well-formed and skip validation " "entirely."),
            ("d", "Catch every downstream exception and ignore it so processing " "continues."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Validating the response against an expected schema at the boundary lets "
        "the app fail safely instead of crashing downstream. Passing raw data, "
        "assuming correctness, and blanket-ignoring errors all propagate or hide "
        "the fault.",
        "rationales": {
            "a": (
                True,
                "Validating the response catches malformed output before it " "propagates.",
            ),
            "b": (False, "Passing unchecked output lets malformed data break " "downstream."),
            "c": (False, "Assuming well-formed output ignores real failure modes."),
            "d": (False, "Swallowing downstream errors hides the malformed response."),
        },
    },
    {
        "question_id": "d2-pagination-long-conversation",
        "objective_ids": ["AIP-2.4", "AIP-2.1"],
        "prompt": "A long multi-turn conversation keeps growing until each request nears the "
        "context limit and latency climbs. Which strategy BEST keeps requests within "
        "budget while preserving continuity?",
        "scenario_constraint": "Bound growing conversation history within the context window.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Always resend the entire raw conversation history on every single " "turn."),
            ("b", "Drop the most recent turns to save space in the growing conversation."),
            (
                "c",
                "Increase the temperature to compensate for the missing conversation " "context.",
            ),
            ("d", "Summarize or window the older turns while keeping recent ones " "verbatim."),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Summarizing or windowing older turns while keeping recent ones verbatim "
        "bounds tokens and preserves continuity. Resending everything overflows, "
        "dropping recent turns loses the most relevant context, and temperature is "
        "irrelevant.",
        "rationales": {
            "a": (False, "Resending everything blows the token budget as it grows."),
            "b": (False, "Dropping recent turns loses the most relevant context."),
            "c": (False, "Temperature cannot replace missing conversation history."),
            "d": (True, "Summarizing old turns and keeping recent ones fits the " "budget."),
        },
    },
    {
        "question_id": "d2-retry-after-header",
        "objective_ids": ["AIP-2.4"],
        "prompt": "When throttled, the provider returns guidance on how long to wait before "
        "retrying. A client ignores it and retries immediately. Which behavior is MOST "
        "correct?",
        "scenario_constraint": "Honor provider-signaled retry timing.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Ignore the Retry-After guidance entirely and retry as fast as the "
                "client is able to resend each throttled call.",
            ),
            ("b", "Respect the suggested wait before retrying, combined with jittered " "backoff."),
            ("c", "Stop retrying permanently the first time the service returns a " "throttle."),
            ("d", "Switch to a different AWS account to bypass the rate limit " "altogether."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Honoring the suggested wait with jittered backoff aligns retries with "
        "provider guidance and avoids storms. Ignoring it worsens throttling, "
        "permanent stop drops recoverable calls, and account hopping is an abuse "
        "pattern.",
        "rationales": {
            "a": (False, "Ignoring Retry-After keeps hammering the throttled service."),
            "b": (True, "Honoring Retry-After with jitter recovers without a retry " "storm."),
            "c": (False, "Giving up on first throttle sacrifices recoverable requests."),
            "d": (False, "Account-hopping to dodge limits is abusive and unreliable."),
        },
    },
    {
        "question_id": "d2-embedding-request-batching",
        "objective_ids": ["AIP-2.4", "AIP-2.2"],
        "prompt": "An indexing job calls an embeddings model once per text snippet for millions of "
        "snippets, driving high overhead and throttling. Which change MOST improves "
        "throughput and cost?",
        "scenario_constraint": "Reduce per-call overhead at embedding scale.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Increase the embedding vector dimension to make each request carry " "more work.",
            ),
            (
                "b",
                "Call the embedding model twice for every snippet and average the two "
                "vectors to chase slightly higher accuracy.",
            ),
            (
                "c",
                "Batch multiple snippets into each embedding request where the API " "supports it.",
            ),
            ("d", "Raise the output max-tokens limit so each embedding call does more at " "once."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Batching snippets per request amortizes overhead and reduces call count, "
        "easing throttling and cost. Larger dimensions, double calls, and output "
        "token changes do not reduce per-call overhead.",
        "rationales": {
            "a": (False, "Higher dimension does not reduce request count or latency."),
            "b": (False, "Doubling calls per snippet increases cost and latency."),
            "c": (True, "Batching snippets per request cuts round-trips and cost."),
            "d": (False, "Max tokens is irrelevant to embedding throughput."),
        },
    },
    {
        "question_id": "d2-bedrock-data-automation-ingest",
        "objective_ids": ["AIP-2.5"],
        "prompt": "A team must extract structured fields from a large mix of scanned PDFs, images, "
        "and documents to feed a GenAI pipeline, without building custom parsing per "
        "format. Which AWS capability fits BEST?",
        "scenario_constraint": "Automate structured extraction from mixed unstructured content.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A hand-written regex parser maintained separately for each document " "type."),
            ("b", "Amazon Polly reading the documents aloud before they are ingested."),
            ("c", "Amazon SNS notifying a topic whenever new documents are uploaded."),
            (
                "d",
                "Amazon Bedrock Data Automation processing the documents into "
                "structured output.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Bedrock Data Automation turns mixed unstructured documents into structured "
        "output without per-format custom code. Hand-written regex is brittle, "
        "Polly is text-to-speech, and SNS only sends notifications.",
        "rationales": {
            "a": (False, "Per-type regex parsers are brittle and high-maintenance."),
            "b": (False, "Polly synthesizes speech and does not extract document data."),
            "c": (False, "SNS sends notifications and performs no extraction."),
            "d": (True, "Bedrock Data Automation extracts structured data from " "documents."),
        },
    },
    {
        "question_id": "d2-model-routing-fallback-policy",
        "objective_ids": ["AIP-2.5"],
        "prompt": "An application must prefer a cost-efficient model but automatically fall back "
        "to a stronger model when the primary returns low confidence or errors, "
        "transparently to users. Which design fits BEST?",
        "scenario_constraint": "Automatic, transparent fallback between models.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "A model routing policy with defined fallback conditions and target " "models."),
            ("b", "A fixed single model with no fallback path when it is unavailable."),
            ("c", "Returning an error to callers whenever the primary model struggles."),
            (
                "d",
                "Ask the end user to pick which model to try on each individual request "
                "whenever the primary model is unavailable.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "A routing policy with explicit fallback conditions redirects to the "
        "stronger model automatically and transparently. A single fixed model has "
        "no fallback, erroring out breaks the UX, and asking the user is not "
        "transparent.",
        "rationales": {
            "a": (True, "A routing policy with fallbacks keeps serving when the primary " "fails."),
            "b": (False, "A single fixed model has no resilience to failure."),
            "c": (False, "Erroring out provides no failover at all."),
            "d": (False, "Pushing model choice to users is a poor experience."),
        },
    },
    {
        "question_id": "d2-duplicate-event-at-least-once",
        "objective_ids": ["AIP-2.5", "AIP-2.3"],
        "prompt": "A GenAI workflow triggered by at-least-once message delivery occasionally sends "
        "a customer two identical emails. Which fix MOST directly prevents the duplicate "
        "side effect?",
        "scenario_constraint": "Prevent duplicate side effects under at-least-once delivery.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Make the handler idempotent by recording processed message IDs and "
                "skipping repeats.",
            ),
            ("b", "Switch the queue to best-effort delivery so duplicates are simply " "dropped."),
            ("c", "Add a delay before sending each email so duplicates spread out over " "time."),
            ("d", "Increase the consumer count so duplicate messages are processed " "faster."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "Recording processed message IDs makes reprocessing a no-op, preventing "
        "duplicate emails. Best-effort delivery risks losing messages, a delay does "
        "not stop duplicates, and more consumers can increase concurrent "
        "duplicates.",
        "rationales": {
            "a": (True, "Recording processed IDs makes duplicate deliveries harmless."),
            "b": (False, "Best-effort delivery risks losing legitimate messages."),
            "c": (False, "Delaying sends does not prevent duplicate emails."),
            "d": (False, "More consumers increases, not reduces, duplicate " "processing."),
        },
    },
    {
        "question_id": "d2-trace-correlation-xray",
        "objective_ids": ["AIP-2.5"],
        "prompt": "A request flows through API Gateway, Lambda, a model call, and a downstream "
        "service, and the team cannot follow one request across them during incidents. "
        "Which TWO practices BEST provide end-to-end traceability? Select TWO.",
        "scenario_constraint": "Correlate one request across multiple services.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Enable AWS X-Ray distributed tracing across the services."),
            ("b", "Propagate a correlation/trace ID and include it in each service's " "logs."),
            ("c", "Keep separate unlinked logs in each service."),
            ("d", "Rely on a single CloudWatch metric for total errors."),
            ("e", "Manually grep timestamps across log groups."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": "X-Ray links segments into one trace, and a propagated correlation ID ties "
        "every log line to the same request. Unlinked logs, a single aggregate "
        "metric, and manual timestamp grepping cannot reliably stitch a request "
        "across services.",
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
        "prompt": "A pipeline marks a step 'completed' even when the model call was throttled and "
        "returned no usable output. Which correction is MOST important?",
        "scenario_constraint": "Do not record success when the operation did not complete.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Mark the call a success on any HTTP 200 regardless of the response " "body."),
            ("b", "Mark success only after a validated, complete response has been " "received."),
            ("c", "Mark success whenever the call returns at all, even on a throttle " "body."),
            ("d", "Mark success optimistically up front and reconcile problems later " "offline."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Recording success only after a validated complete response prevents "
        "false-success on throttled or empty results. Trusting a 200, any return, "
        "or optimism all record success that did not happen.",
        "rationales": {
            "a": (False, "A 200 can still carry a throttle or error body."),
            "b": (True, "Confirming a validated complete response avoids false " "success."),
            "c": (False, "Returning at all does not mean the operation succeeded."),
            "d": (False, "Optimistic success records failures as if they worked."),
        },
    },
    {
        "question_id": "d2-prompt-chain-decompose",
        "objective_ids": ["AIP-2.5"],
        "prompt": "A single mega-prompt tries to extract entities, classify, and summarize at once "
        "and produces inconsistent results. The team wants more reliable, debuggable "
        "steps. Which approach fits BEST?",
        "scenario_constraint": "Improve reliability of a complex multi-task prompt.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Add more and more instructions to the single prompt until it covers "
                "all three tasks.",
            ),
            (
                "b",
                "Increase the temperature on the single prompt to make it handle the "
                "tasks creatively.",
            ),
            (
                "c",
                "Decompose into a prompt chain where each step does one task and feeds "
                "the next.",
            ),
            ("d", "Raise the max-tokens limit so all three tasks fit in one large " "response."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "A prompt chain isolates each task into a verifiable step, improving "
        "reliability and debuggability. Piling more instructions onto one prompt, "
        "raising temperature, or increasing tokens does not fix the entanglement.",
        "rationales": {
            "a": (False, "Overloading one prompt degrades reliability on each task."),
            "b": (False, "Temperature does not help a prompt juggle multiple tasks."),
            "c": (True, "A prompt chain isolates each task for reliable, checkable " "steps."),
            "d": (False, "More output room does not fix multi-task prompt confusion."),
        },
    },
    {
        "question_id": "d2-amazon-q-developer-use",
        "objective_ids": ["AIP-2.5"],
        "prompt": "Developers want an AWS-native assistant integrated into their IDE to explain "
        "code, suggest fixes, and help with AWS APIs while building the GenAI app. Which "
        "service fits BEST?",
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
        "explanation": "Amazon Q Developer is the AWS-native in-IDE assistant for code and AWS "
        "guidance. Guardrails enforce safety, Kendra is enterprise search, and Glue "
        "is ETL.",
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
        "prompt": "After upgrading the embedding model, retrieval quality drops because old "
        "vectors in the index were produced by the previous model. Which action MOST "
        "directly resolves the mismatch?",
        "scenario_constraint": "Resolve inconsistency between old and new embeddings.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Keep the old vectors in place and query them with the new embedding " "model."),
            ("b", "Increase the number of retrieved results to compensate for the " "mismatch."),
            (
                "c",
                "Re-embed the whole corpus with the new model so all vectors share one " "space.",
            ),
            ("d", "Lower the similarity threshold so more near-matches get returned " "anyway."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Vectors from different embedding models live in incompatible spaces, so "
        "re-embedding the corpus with the new model restores consistency. Mixing "
        "models, returning more results, or lowering thresholds only mask the "
        "mismatch.",
        "rationales": {
            "a": (False, "Mixing model versions compares vectors in different spaces."),
            "b": (False, "More results do not fix mismatched embedding spaces."),
            "c": (True, "Re-embedding aligns the whole corpus to one vector space."),
            "d": (False, "A looser threshold returns noisier, not corrected, matches."),
        },
    },
    {
        "question_id": "d2-cloudwatch-logs-insights-debug",
        "objective_ids": ["AIP-2.5"],
        "prompt": "During an incident, the team must quickly query structured application logs "
        "across many Lambda invocations to find failing requests by error code and "
        "latency. Which tool fits BEST?",
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
        "explanation": "CloudWatch Logs Insights runs ad hoc queries over structured logs across "
        "invocations to filter by fields like error code and latency. Manual "
        "downloads do not scale, an aggregate dashboard lacks detail, and "
        "QuickSight is for BI reporting.",
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
        "prompt": "A monitoring job marks streamed generations as successful based on receiving "
        "the first chunk, but some streams error after that chunk. Which TWO corrections "
        "BEST ensure accurate status? Select TWO.",
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
        "explanation": "Requiring a clean end-of-response and treating mid-stream errors as "
        "failures makes status reflect real completion. First-chunk success, chunk "
        "counting, and ignoring errors all produce false-success signals.",
        "rationales": {
            "a": (True, "A clean end-of-stream signal is the correct success " "condition."),
            "b": (True, "Mid-stream errors must be treated as failures, not successes."),
            "c": (False, "First-chunk arrival does not prove completion."),
            "d": (False, "Chunk count does not confirm a clean completion."),
            "e": (False, "Ignoring errors manufactures false-green metrics."),
        },
    },
    {
        "question_id": "d2-fallback-degraded-response",
        "objective_ids": ["AIP-2.5"],
        "prompt": "When the primary model and its fallback are both unavailable, the app should "
        "still respond usefully rather than crash. Which behavior is MOST appropriate?",
        "scenario_constraint": "Degrade gracefully when all models are unavailable.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Return a clear degraded response, such as cached guidance or an honest "
                "unavailable message.",
            ),
            ("b", "Return a fabricated answer so the user interface still looks fully " "normal."),
            ("c", "Hang the request indefinitely until a model finally recovers and " "responds."),
            ("d", "Return the raw unhandled stack trace directly to the end user on " "failure."),
        ],
        "correct_option_ids": ["a"],
        "explanation": "A clear degraded response keeps the app usable and honest when all models "
        "are down. Fabricated answers mislead, hanging the request harms UX, and "
        "leaking a stack trace exposes internals and still fails.",
        "rationales": {
            "a": (True, "An honest degraded response fails gracefully without " "fabrication."),
            "b": (False, "A fabricated answer misleads the user during an outage."),
            "c": (False, "Hanging the request produces a poor timeout experience."),
            "d": (False, "Leaking a stack trace is unhelpful and insecure."),
        },
    },
    {
        "question_id": "d2-rag-stale-index-debug",
        "objective_ids": ["AIP-2.5"],
        "prompt": "Users report the assistant cites outdated policy even though the source "
        "documents were updated last week. The retrieval index was last built a month "
        "ago. Which action MOST directly fixes this?",
        "scenario_constraint": "Serve current content from a stale retrieval index.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Increase the generation model's temperature to shake loose fresher " "answers."),
            (
                "b",
                "Add more retrieved chunks per query so the newer content is "
                "statistically more likely to appear in the context.",
            ),
            (
                "c",
                "Switch to a bigger generation model that can reason over the stale " "retrieval.",
            ),
            (
                "d",
                "Re-ingest and reindex the updated documents so retrieval returns "
                "current content.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "The index predates the document updates, so re-ingesting and reindexing "
        "brings current content into retrieval. Temperature, more chunks, and a "
        "bigger model cannot surface documents the index does not contain.",
        "rationales": {
            "a": (False, "Temperature cannot surface content missing from the index."),
            "b": (False, "More chunks of stale content stay stale."),
            "c": (False, "A bigger model still retrieves from the outdated index."),
            "d": (True, "Reindexing updated documents fixes the stale retrieval root " "cause."),
        },
    },
    {
        "question_id": "d2-structured-logging-correlation-id",
        "objective_ids": ["AIP-2.5"],
        "prompt": "To debug cross-service GenAI failures, the team wants every log line for a "
        "request tagged so they can filter one request's journey. Which practice fits "
        "BEST?",
        "scenario_constraint": "Tie all logs of one request together.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Log everything as free-form text with no identifiers tying related "
                "lines together across the services involved.",
            ),
            (
                "b",
                "Propagate a correlation/request ID and include it in every structured "
                "log line.",
            ),
            (
                "c",
                "Rely on wall-clock timestamps alone to piece the request flow back " "together.",
            ),
            ("d", "Log only error lines and omit the normal request-flow entries " "entirely."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "A propagated correlation ID in structured logs lets the team filter one "
        "request across services. Free-form text, timestamps alone, and error-only "
        "logging cannot reliably reconstruct a single request's path.",
        "rationales": {
            "a": (False, "Free-form text with no IDs cannot be correlated across " "services."),
            "b": (True, "A propagated correlation ID stitches the request flow " "together."),
            "c": (False, "Timestamps alone cannot reliably correlate concurrent " "requests."),
            "d": (False, "Logging only errors loses the context needed to trace flow."),
        },
    },
    {
        "question_id": "d2-model-router-cost-quality",
        "objective_ids": ["AIP-2.5", "AIP-2.2"],
        "prompt": "A production router must decide per request whether to use a cheap or premium "
        "model based on query complexity, and the team wants to tune this without "
        "redeploying code. Which approach fits BEST?",
        "scenario_constraint": "Adjust routing behavior without code redeploys.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Hard-code the routing thresholds directly in the application source "
                "and redeploy whenever they need adjusting.",
            ),
            ("b", "Pick a model at random for each request to balance cost over time."),
            (
                "c",
                "Externalize the routing policy as configuration the router reads at " "runtime.",
            ),
            ("d", "Always use the premium model for every request to stay safely " "accurate."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Externalizing the routing policy as runtime configuration lets the team "
        "tune thresholds without redeploying. Hard-coding requires redeploys, "
        "random choice ignores complexity, and always-premium overpays.",
        "rationales": {
            "a": (False, "Hard-coded thresholds require a redeploy for every tweak."),
            "b": (False, "Random routing ignores cost and quality tradeoffs."),
            "c": (True, "Externalized policy lets routing change without redeploys."),
            "d": (False, "Always-premium routing abandons the cost goal."),
        },
    },
    {
        "question_id": "d2-timeout-cascade-debug",
        "objective_ids": ["AIP-2.5", "AIP-2.4"],
        "prompt": "An API Gateway endpoint returns 504s during model slowness because the Lambda "
        "waits longer than the gateway's integration timeout. Which fix MOST directly "
        "aligns the timeouts?",
        "scenario_constraint": "Align downstream timeout with the gateway integration timeout.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Increase the model call's max tokens so each response completes in " "less time.",
            ),
            (
                "b",
                "Remove all timeouts from the Lambda so the slow model call can finish " "fully.",
            ),
            (
                "c",
                "Retry the whole request from the client indefinitely until something " "returns.",
            ),
            (
                "d",
                "Set the model call timeout below the gateway integration timeout and "
                "return a controlled error.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Setting the model-call timeout below the gateway timeout lets the Lambda "
        "return a controlled error before the gateway 504s. More tokens worsen "
        "latency, removing timeouts causes hangs, and endless client retries "
        "amplify load.",
        "rationales": {
            "a": (False, "Max tokens does not fix a cascading timeout chain."),
            "b": (False, "Removing timeouts lets the slow call hang the whole chain."),
            "c": (False, "Indefinite client retries amplify the cascading failure."),
            "d": (True, "Nesting timeouts inside the gateway limit yields a clean " "error."),
        },
    },
    {
        "question_id": "d2-bedrock-data-automation-vs-textract",
        "objective_ids": ["AIP-2.5"],
        "prompt": "A GenAI workflow needs an integrated service that both extracts content from "
        "multimodal documents and prepares normalized output ready for downstream "
        "generative processing in one managed flow. Which option fits BEST?",
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
        "explanation": "Bedrock Data Automation provides a managed flow that processes multimodal "
        "documents into normalized, GenAI-ready output. Ad hoc scripts are brittle, "
        "SQS is a queue, and CloudFront is a CDN.",
        "rationales": {
            "a": (True, "Data Automation is the managed multimodal-to-GenAI pipeline."),
            "b": (False, "A chain of ad hoc scripts is brittle and unmanaged."),
            "c": (False, "SQS queues messages; it does not extract content."),
            "d": (False, "CloudFront delivers content and does not transform " "documents."),
        },
    },
    {
        "question_id": "d2-dedupe-store-ttl",
        "objective_ids": ["AIP-2.5", "AIP-2.1"],
        "prompt": "To deduplicate events, a team stores processed IDs in DynamoDB but the table "
        "grows unbounded over years. They need dedup within a practical window without "
        "manual cleanup. Which change fits BEST?",
        "scenario_constraint": "Bound dedup storage growth automatically.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Add a DynamoDB TTL so old dedup records expire and are removed " "automatically.",
            ),
            ("b", "Never delete any dedup records so no duplicate can ever slip through " "later."),
            (
                "c",
                "Store the processed IDs in a per-Lambda in-memory set that resets on "
                "cold start.",
            ),
            (
                "d",
                "Truncate the entire dedup table manually once each quarter to control " "growth.",
            ),
        ],
        "correct_option_ids": ["a"],
        "explanation": "A DynamoDB TTL expires dedup records after the needed window, bounding "
        "growth without manual work. Never deleting grows unbounded, in-memory sets "
        "vanish between invocations, and manual truncation is error-prone.",
        "rationales": {
            "a": (True, "A DynamoDB TTL expires stale dedup entries without manual " "cleanup."),
            "b": (False, "Keeping records forever grows the table without bound."),
            "c": (False, "An in-memory set is lost on cold start and misses duplicates."),
            "d": (False, "Manual quarterly truncation is error-prone and risky."),
        },
    },
    {
        "question_id": "d2-hallucination-grounding-debug",
        "objective_ids": ["AIP-2.5"],
        "prompt": "A support bot confidently invents product features that do not exist. Which TWO "
        "changes MOST directly reduce these fabrications by grounding answers in the "
        "real catalog? Select TWO.",
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
        "explanation": "Retrieving catalog context and constraining the model to answer only from "
        "it directly reduces fabrication. Higher temperature worsens it, a longer "
        "prompt is weak alone, and a bigger context window adds no real data.",
        "rationales": {
            "a": (True, "Retrieval supplies authoritative grounding content."),
            "b": (True, "Constraining to retrieved context curbs invented details."),
            "c": (False, "Higher temperature increases, not reduces, fabrication."),
            "d": (False, "A longer prompt is unreliable without grounding data."),
            "e": (False, "A bigger context window alone adds no authoritative " "content."),
        },
    },
    {
        "question_id": "d2-canary-metric-regression-detect",
        "objective_ids": ["AIP-2.5", "AIP-2.3"],
        "prompt": "After a prompt change, user-visible answer quality quietly degraded but no "
        "system errors fired, so monitoring stayed green. Which addition would have "
        "caught this regression?",
        "scenario_constraint": "Detect quality regressions that raise no system errors.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Watch only CPU and memory utilization on the canary during the " "rollout."),
            (
                "b",
                "Track output-quality metrics from automated evals or feedback, not "
                "just system errors.",
            ),
            ("c", "Alert only on HTTP 5xx rates and treat everything else as healthy."),
            ("d", "Count total invocations per minute as the sole canary health signal."),
        ],
        "correct_option_ids": ["b"],
        "explanation": "Quality metrics from automated evals or user feedback catch regressions "
        "that throw no system errors. Infrastructure utilization, 5xx rates, and "
        "invocation counts all stay green while answer quality silently drops.",
        "rationales": {
            "a": (False, "Resource metrics miss output-quality regressions."),
            "b": (True, "Quality metrics catch regressions that system health misses."),
            "c": (False, "5xx rates ignore silent quality degradation."),
            "d": (False, "Invocation counts say nothing about answer quality."),
        },
    },
    {
        "question_id": "d2-prompt-chain-error-propagation",
        "objective_ids": ["AIP-2.5"],
        "prompt": "In a prompt chain, an early step occasionally returns empty output, and later "
        "steps silently produce nonsense from it. Which practice BEST contains the "
        "failure?",
        "scenario_constraint": "Stop a failed chain step from corrupting later steps.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Always feed whatever the previous step returned straight into the next " "step.",
            ),
            (
                "b",
                "Increase the temperature on the later steps to recover from earlier " "mistakes.",
            ),
            (
                "c",
                "Validate each step's output and halt or retry the chain on invalid "
                "intermediate results.",
            ),
            ("d", "Combine all the chained steps back into one prompt to avoid passing " "errors."),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Validating each intermediate result and halting or retrying on invalid "
        "output stops error propagation through the chain. Blindly forwarding "
        "output spreads the fault, more temperature adds noise, and recombining "
        "steps loses the chain's benefits.",
        "rationales": {
            "a": (False, "Blindly forwarding bad output cascades the error downstream."),
            "b": (False, "Temperature cannot fix an upstream step's bad output."),
            "c": (True, "Validating each step stops bad intermediates from " "propagating."),
            "d": (False, "Collapsing the chain loses the per-step checks entirely."),
        },
    },
    {
        "question_id": "d2-throttle-vs-error-metric-confusion",
        "objective_ids": ["AIP-2.5", "AIP-2.4"],
        "prompt": "An on-call engineer sees rising failures but cannot tell whether they are "
        "throttling, validation, or server errors, slowing diagnosis. Which improvement "
        "MOST speeds root-cause analysis?",
        "scenario_constraint": "Distinguish failure categories during an incident.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Emit a single combined failure counter that lumps every error type " "together.",
            ),
            ("b", "Log all failures only as generic exceptions with no category " "attached."),
            ("c", "Suppress most error logs during incidents to cut down on dashboard " "noise."),
            (
                "d",
                "Emit per-category error metrics for throttling, validation, server, "
                "and timeout.",
            ),
        ],
        "correct_option_ids": ["d"],
        "explanation": "Per-category error metrics let the engineer immediately see whether "
        "throttling, validation, or server errors dominate. A single counter, "
        "generic logs, and suppressed logs all obscure the failure type.",
        "rationales": {
            "a": (False, "A single counter hides which failure mode is occurring."),
            "b": (False, "Generic exceptions cannot be told apart for diagnosis."),
            "c": (False, "Suppressing logs removes the signal needed to react."),
            "d": (True, "Per-category metrics distinguish throttling from other " "failures."),
        },
    },
    {
        "question_id": "d2-retry-storm-amplification",
        "objective_ids": ["AIP-2.5", "AIP-2.4"],
        "prompt": "During a brief model slowdown, aggressive client retries turned a minor blip "
        "into a full outage. Which TWO changes BEST prevent this amplification next "
        "time? Select TWO.",
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
        "explanation": "Jittered bounded backoff and a circuit breaker both dampen retry "
        "amplification during a slowdown. Infinite immediate retries, more clients, "
        "and removing timeouts all intensify the overload.",
        "rationales": {
            "a": (True, "Bounded jittered backoff limits and de-synchronizes retries."),
            "b": (True, "A circuit breaker halts retries during sustained failure."),
            "c": (False, "Immediate infinite retries amplify the slowdown into an " "outage."),
            "d": (False, "More clients add load during the incident."),
            "e": (False, "Removing timeouts lets slow calls pile up and hang."),
        },
    },
    {
        "question_id": "d2-end-to-end-observability-stack",
        "objective_ids": ["AIP-2.5"],
        "prompt": "A GenAI platform team wants metrics, logs, and distributed traces unified so "
        "they can correlate a latency spike with the exact model call and downstream "
        "dependency. Which TWO AWS services directly support this? Select TWO.",
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
        "explanation": "CloudWatch provides metrics and logs while X-Ray adds distributed traces, "
        "together enabling correlation of a spike to a specific call. Macie, "
        "Shield, and Rekognition serve unrelated purposes.",
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
        "prompt": "A routing layer silently falls back to a weaker model so often that quality "
        "drops without anyone noticing. Which addition BEST surfaces the problem while "
        "keeping the fallback?",
        "scenario_constraint": "Keep fallback but make silent degradation visible.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Remove the fallback path entirely so failures surface as hard errors " "instead.",
            ),
            (
                "b",
                "Fall back more aggressively to the degraded path to avoid user-visible " "errors.",
            ),
            (
                "c",
                "Emit a metric and alarm on the fallback rate so sustained degradation "
                "stays visible.",
            ),
            (
                "d",
                "Log nothing about fallbacks to keep the operational dashboards clean "
                "and quiet.",
            ),
        ],
        "correct_option_ids": ["c"],
        "explanation": "Metering and alarming on fallback rate keeps the safety net while exposing "
        "sustained degradation. Removing fallback sacrifices resilience, falling "
        "back more hides the issue further, and logging nothing guarantees it stays "
        "invisible.",
        "rationales": {
            "a": (False, "Removing the fallback sacrifices resilience during outages."),
            "b": (False, "Silently falling back more hides the underlying degradation."),
            "c": (True, "Alarming on fallback rate makes sustained degradation " "visible."),
            "d": (False, "Logging nothing hides the degradation from operators."),
        },
    },
    {
        "question_id": "d2-batch-vs-provisioned-overnight-fit",
        "objective_ids": ["AIP-2.2"],
        "prompt": "A team must choose deployment options for two workloads: a nightly bulk scoring "
        "job over millions of records, and a 24/7 interactive assistant with steady high "
        "traffic. Which TWO pairings fit BEST? Select TWO.",
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
        "explanation": "Batch inference suits the offline bulk job while Provisioned Throughput "
        "fits the steady interactive assistant. Provisioning the nightly job "
        "overpays, batching an interactive assistant breaks latency, and a training "
        "job does not serve inference.",
        "rationales": {
            "a": (True, "Batch is the cost-efficient choice for the offline bulk job."),
            "b": (
                True,
                "Provisioned Throughput gives the assistant guaranteed steady " "capacity.",
            ),
            "c": (False, "Provisioning the nightly job overpays versus batch."),
            "d": (False, "Batch is offline and cannot serve interactive traffic."),
            "e": (False, "A training job trains models; it does not serve requests."),
        },
    },
    {
        "question_id": "d2-step-functions-vs-eventbridge-combo",
        "objective_ids": ["AIP-2.3"],
        "prompt": "A GenAI platform needs both an ordered multi-step pipeline with retries and a "
        "decoupled broadcast of completion events to many independent subscribers. Which "
        "TWO services fit these two needs? Select TWO.",
        "scenario_constraint": "Separate ordered orchestration from fan-out notification.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "AWS Step Functions for the ordered multi-step pipeline with retries."),
            ("b", "Amazon EventBridge to broadcast completion events to many " "subscribers."),
            ("c", "Amazon API Gateway to orchestrate the ordered pipeline steps."),
            ("d", "Amazon SQS to broadcast the same event to every subscriber."),
            ("e", "AWS CodeBuild to run the pipeline steps in order."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": "Step Functions orchestrates the ordered, retrying pipeline while "
        "EventBridge fans completion events out to many subscribers. API Gateway is "
        "a front door, SQS does not natively broadcast, and CodeBuild is a build "
        "tool.",
        "rationales": {
            "a": (True, "Step Functions handles ordered steps with built-in retries."),
            "b": (True, "EventBridge broadcasts events to many independent " "subscribers."),
            "c": (False, "API Gateway is an API front door, not a workflow engine."),
            "d": (False, "SQS delivers to one consumer group, not a broadcast."),
            "e": (False, "CodeBuild builds artifacts; it does not orchestrate runtime " "steps."),
        },
    },
    {
        "question_id": "d2-streaming-timeout-combo",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A streaming chat integration must stay robust when the model stalls "
        "mid-generation. Which TWO safeguards BEST protect the client experience? Select "
        "TWO.",
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
        "explanation": "An inter-token read timeout detects a stall and aborting, combined with "
        "treating the abort as a failure, keeps the client honest and recoverable. "
        "Early success, no timeouts, and unbounded buffering all mask or worsen the "
        "stall.",
        "rationales": {
            "a": (True, "An inter-token timeout detects and aborts a stalled stream."),
            "b": (True, "Treating the abort as failure enables retry or an honest " "error."),
            "c": (False, "Marking success on open ignores a later stall."),
            "d": (False, "Removing timeouts lets a stalled stream hang indefinitely."),
            "e": (False, "Unbounded buffering risks memory exhaustion during a stall."),
        },
    },
    {
        "question_id": "d2-schema-and-idempotency-combo",
        "objective_ids": ["AIP-2.4"],
        "prompt": "A mutating model-backed endpoint must be both safe to retry and resistant to "
        "malformed input. Which TWO practices directly deliver these properties? Select "
        "TWO.",
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
        "explanation": "An idempotency key makes retries safe and schema validation blocks "
        "malformed input before processing. Timeouts, quotas, and temperature "
        "address neither retry safety nor input validation.",
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
        "prompt": "After an incident where throttled calls were logged as successes, a team wants "
        "both honest status reporting and the ability to trace one request across "
        "services. Which TWO changes BEST achieve this? Select TWO.",
        "scenario_constraint": "Honest completion status plus cross-service traceability.",
        "difficulty": "hard",
        "question_format": "multiple_response",
        "options": [
            ("a", "Record success only after a validated complete response."),
            ("b", "Propagate a correlation ID and emit distributed traces across " "services."),
            ("c", "Mark success on any non-exception return."),
            ("d", "Rely on a single aggregate success counter with no categories."),
            ("e", "Disable tracing to reduce overhead during incidents."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": "Recording success only on a validated complete response avoids "
        "false-success, and correlated distributed traces let the team follow one "
        "request end to end. Marking any return as success, a single counter, and "
        "disabling tracing undermine both goals.",
        "rationales": {
            "a": (True, "Validated completion prevents false-success on throttled " "calls."),
            "b": (True, "Correlation IDs and traces enable cross-service debugging."),
            "c": (False, "Any-return success still mislabels throttled failures."),
            "d": (False, "A single counter hides failure categories and causes."),
            "e": (False, "Disabling tracing removes the cross-service visibility " "needed."),
        },
    },
]


def question_count() -> int:
    """Return the number of authored Domain 2 questions."""
    return len(QUESTIONS)
