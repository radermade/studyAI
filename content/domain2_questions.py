"""Authored Domain 2 (AIP-C01) scenario questions with answers and explanations.

Original, scenario-style multiple-choice questions testing agent, deployment,
integration, and API reasoning for the AWS Certified Generative AI Developer
exam. Each question has a decisive constraint, four distinct options, one
correct answer, per-option rationales, and a teaching explanation. No
proprietary exam content is reproduced.

Shape per question matches ``content/domain1_questions.py`` so the same
ingestion path consumes both.
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    # --- AIP-2.1 agents, tools, orchestration ------------------------------
    {
        "question_id": "d2-tool-schema-validation",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "A tool-using agent occasionally calls an internal API with "
            "malformed arguments, causing downstream errors. You must stop bad "
            "calls before they leave the agent. What is the most effective "
            "control?"
        ),
        "scenario_constraint": "Prevent malformed tool calls from reaching downstream systems.",
        "difficulty": "medium",
        "options": [
            ("a", "Define a typed tool schema and validate arguments before each call."),
            ("b", "Add a sentence to the prompt asking the model to be careful."),
            ("c", "Retry the tool call repeatedly until one succeeds."),
            ("d", "Log the errors and let downstream systems reject bad input."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A typed tool schema with argument validation rejects malformed "
            "calls at the boundary, before they reach downstream systems. Prompt "
            "pleading is not an enforced control, blind retries amplify the "
            "problem, and relying on downstream rejection pushes failures outward."
        ),
        "rationales": {
            "a": (True, "Schema + validation is the enforced boundary that stops bad calls."),
            "b": (False, "A prompt request is not an enforced validation control."),
            "c": (False, "Retrying malformed calls repeats the error, not fixes it."),
            "d": (False, "Downstream rejection means the bad call already left the agent."),
        },
    },
    {
        "question_id": "d2-least-privilege-agent",
        "objective_ids": ["AIP-2.1", "AIP-3.1"],
        "prompt": (
            "An agent can invoke several AWS actions through its tools. Security "
            "review requires that a compromised or misbehaving agent cannot "
            "exceed its intended scope. Which design best enforces this?"
        ),
        "scenario_constraint": "Contain blast radius if the agent misbehaves.",
        "difficulty": "medium",
        "options": [
            ("a", "Give the agent a least-privilege IAM role scoped to only the needed actions."),
            ("b", "Give the agent broad admin permissions for flexibility."),
            ("c", "Trust the model to only call actions it should."),
            ("d", "Share one powerful role across all agents and tools."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A least-privilege IAM role scoped to exactly the needed actions "
            "bounds what a misbehaving agent can do. Broad admin rights, trusting "
            "model behavior, and a shared powerful role all widen the blast "
            "radius instead of containing it."
        ),
        "rationales": {
            "a": (True, "Least-privilege identity bounds the agent's blast radius."),
            "b": (False, "Admin permissions maximize, not minimize, blast radius."),
            "c": (False, "Model behavior is not an access-control boundary."),
            "d": (False, "A shared powerful role spreads risk across every agent."),
        },
    },
    {
        "question_id": "d2-agent-stopping-conditions",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An autonomous agent sometimes loops, calling tools indefinitely and "
            "running up cost. You must guarantee it halts. Which combination of "
            "controls directly bounds its execution?"
        ),
        "scenario_constraint": "Guarantee the agent halts and cannot run up unbounded cost.",
        "difficulty": "hard",
        "options": [
            ("a", "Enforce max step count, a time/cost budget, and a timeout per run."),
            ("b", "Increase the model's context window so it finishes faster."),
            ("c", "Ask the model in the prompt to stop when it is done."),
            ("d", "Remove tools so the agent has nothing to loop on."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Explicit stopping conditions — maximum steps, a cost/time budget, "
            "and a per-run timeout — guarantee termination regardless of model "
            "behavior. A larger context does not bound iterations, a prompt "
            "request is not a hard limit, and removing tools defeats the agent."
        ),
        "rationales": {
            "a": (True, "Step/cost/time limits are hard stopping conditions that force a halt."),
            "b": (False, "Context size does not bound the number of tool-calling steps."),
            "c": (False, "A prompt request is not an enforced stopping condition."),
            "d": (False, "Removing tools removes the agent's function, not the loop risk."),
        },
    },
    {
        "question_id": "d2-human-in-the-loop",
        "objective_ids": ["AIP-2.1"],
        "prompt": (
            "An agent can trigger an irreversible, high-cost action (deleting "
            "production data). The business wants automation but cannot tolerate "
            "a wrong autonomous call. What should the design require?"
        ),
        "scenario_constraint": "Irreversible high-cost action must not fire autonomously.",
        "difficulty": "medium",
        "options": [
            ("a", "Require explicit human approval before the irreversible action executes."),
            ("b", "Let the agent act and send a notification afterward."),
            ("c", "Raise the model temperature so it is more decisive."),
            ("d", "Allow the action whenever model confidence is above 50%."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Irreversible, high-cost actions require a human approval/escalation "
            "gate before execution. After-the-fact notification is too late, "
            "temperature is irrelevant to safety, and a 50% confidence threshold "
            "still permits confident mistakes."
        ),
        "rationales": {
            "a": (True, "A human-approval gate prevents a wrong autonomous irreversible action."),
            "b": (False, "Notifying after execution cannot undo an irreversible action."),
            "c": (False, "Temperature affects randomness, not safety of irreversible acts."),
            "d": (False, "A confidence threshold still allows confident wrong actions."),
        },
    },
    # --- AIP-2.2 deployment and capacity -----------------------------------
    {
        "question_id": "d2-batch-vs-realtime",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A nightly job must summarize millions of documents by morning, with "
            "no interactive user waiting. Cost efficiency matters more than "
            "per-request latency. Which inference pattern fits best?"
        ),
        "scenario_constraint": "High volume, no interactive wait, optimize for cost.",
        "difficulty": "medium",
        "options": [
            ("a", "Batch/asynchronous inference processed overnight."),
            ("b", "Synchronous on-demand calls one document at a time."),
            ("c", "Provisioned Throughput sized for peak interactive traffic."),
            ("d", "A real-time endpoint kept warm 24/7."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Batch/asynchronous inference suits large volumes with no interactive "
            "deadline and optimizes cost. Synchronous per-document calls are slow "
            "and costly at scale, and peak-sized provisioned or always-warm "
            "real-time capacity wastes money for a nightly job."
        ),
        "rationales": {
            "a": (True, "Batch/async matches high volume with no interactive latency need."),
            "b": (False, "One-at-a-time synchronous calls do not scale cost-effectively."),
            "c": (False, "Peak-sized provisioned throughput is wasteful for a batch job."),
            "d": (False, "A warm real-time endpoint pays for idle interactive capacity."),
        },
    },
    {
        "question_id": "d2-provisioned-throughput-capacity",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A production chat feature has steady, high, predictable traffic and "
            "keeps hitting on-demand throttling at peak. You need dependable "
            "capacity and predictable cost. What is the right change?"
        ),
        "scenario_constraint": "Steady high predictable traffic; eliminate peak throttling.",
        "difficulty": "medium",
        "options": [
            ("a", "Move the model to Provisioned Throughput sized to the sustained load."),
            ("b", "Keep on-demand and simply retry on every throttle."),
            ("c", "Switch to batch inference for the interactive chat."),
            ("d", "Lower the token limit so requests are cheaper."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Provisioned Throughput reserves dependable capacity with predictable "
            "cost for steady, high traffic, eliminating peak throttling. Retrying "
            "on-demand does not add capacity, batch breaks interactivity, and "
            "cutting tokens degrades the feature without fixing capacity."
        ),
        "rationales": {
            "a": (True, "Provisioned Throughput gives dependable capacity for steady load."),
            "b": (False, "Retrying does not increase the throttled capacity ceiling."),
            "c": (False, "Batch inference cannot serve interactive chat."),
            "d": (False, "Reducing tokens degrades answers without solving throttling."),
        },
    },
    {
        "question_id": "d2-smaller-specialized-model",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "A classification step inside a pipeline uses a large general model "
            "and dominates cost and latency, though the task is narrow. You must "
            "cut cost and latency without losing accuracy on that task. What is "
            "the best move?"
        ),
        "scenario_constraint": "Narrow task; cut cost/latency while holding accuracy.",
        "difficulty": "medium",
        "options": [
            ("a", "Use a smaller/specialized model that meets the task's accuracy bar."),
            ("b", "Always use the largest available model for safety."),
            ("c", "Call the large model twice and average the answers."),
            ("d", "Remove the classification step entirely."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A smaller or specialized model that still clears the accuracy bar "
            "cuts cost and latency on a narrow task. The largest model wastes "
            "resources, double-calling doubles cost, and removing the step "
            "changes the pipeline's behavior."
        ),
        "rationales": {
            "a": (True, "A right-sized model holds accuracy while cutting cost and latency."),
            "b": (False, "The largest model is exactly the cost/latency problem here."),
            "c": (False, "Calling twice increases cost and latency."),
            "d": (False, "Deleting the step removes needed functionality."),
        },
    },
    {
        "question_id": "d2-insufficient-capacity-evidence",
        "objective_ids": ["AIP-2.2"],
        "prompt": (
            "You are asked to recommend a deployment capacity, but the request "
            "lacks expected request rate, token sizes, and latency targets. What "
            "is the correct response?"
        ),
        "scenario_constraint": "Required workload assumptions are missing.",
        "difficulty": "easy",
        "options": [
            ("a", "Mark the decision evidence insufficient and request the missing workload data."),
            ("b", "Guess typical numbers and give a confident recommendation."),
            ("c", "Recommend the biggest instance to be safe."),
            ("d", "Copy capacity from an unrelated project."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Without request rate, token sizes, and latency targets, any capacity "
            "number is misleading, so the evidence is insufficient and the "
            "missing inputs must be gathered. Guessing, oversizing, and copying "
            "unrelated capacity all produce unjustified recommendations."
        ),
        "rationales": {
            "a": (True, "Missing workload units make the decision evidence insufficient."),
            "b": (False, "Guessing produces a confident but unfounded recommendation."),
            "c": (False, "Oversizing wastes cost and is still not evidence-based."),
            "d": (False, "Unrelated capacity does not reflect this workload."),
        },
    },
    # --- AIP-2.3 enterprise integration ------------------------------------
    {
        "question_id": "d2-event-driven-decoupling",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A GenAI service must react to events from several enterprise systems "
            "without tightly coupling to each producer, and must absorb bursts "
            "without dropping events. Which integration pattern fits best?"
        ),
        "scenario_constraint": "Decouple producers/consumer and absorb bursts durably.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "An event-driven design with a durable queue/event bus between producers and the service.",
            ),
            ("b", "Direct synchronous calls from each producer into the service."),
            ("c", "A shared database that every system polls constantly."),
            ("d", "A nightly file export emailed between teams."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "An event bus/queue decouples producers from the consumer and buffers "
            "bursts durably. Direct synchronous calls couple systems and drop "
            "events under load, constant DB polling is inefficient and coupled, "
            "and nightly email is neither timely nor reliable."
        ),
        "rationales": {
            "a": (True, "A durable queue/event bus decouples producers and buffers bursts."),
            "b": (False, "Direct synchronous calls couple systems and lose events under load."),
            "c": (False, "Shared-DB polling is tightly coupled and inefficient."),
            "d": (False, "Nightly email is neither event-driven nor reliable."),
        },
    },
    {
        "question_id": "d2-api-gateway-boundary",
        "objective_ids": ["AIP-2.3", "AIP-2.4"],
        "prompt": (
            "External clients must reach a GenAI backend through a managed, "
            "authenticated, rate-limited entry point rather than calling Lambda "
            "or the model directly. Which AWS boundary fits best?"
        ),
        "scenario_constraint": "Managed, authenticated, rate-limited public entry point.",
        "difficulty": "easy",
        "options": [
            ("a", "Amazon API Gateway in front of the backend Lambda/service."),
            ("b", "Expose the Lambda function URL directly to the internet with no controls."),
            ("c", "Give external clients the model's credentials."),
            ("d", "Let clients query the production database directly."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "API Gateway provides a managed, authenticated, throttled entry point "
            "with a clean boundary to the backend. An uncontrolled function URL "
            "lacks protections, sharing model credentials is a severe risk, and "
            "direct DB access bypasses all controls."
        ),
        "rationales": {
            "a": (True, "API Gateway gives a managed, authenticated, rate-limited boundary."),
            "b": (False, "An unprotected function URL has no auth or rate limiting."),
            "c": (False, "Sharing credentials with clients is a critical security failure."),
            "d": (False, "Direct database access bypasses every control."),
        },
    },
    {
        "question_id": "d2-cicd-rollback-gate",
        "objective_ids": ["AIP-2.3"],
        "prompt": (
            "A team deploys model/prompt changes straight to production with no "
            "automated check and no way to revert quickly when quality drops. "
            "Which CI/CD additions most directly reduce release risk?"
        ),
        "scenario_constraint": "Reduce risky releases; enable fast, safe recovery.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Add automated evaluation gates, canary criteria, and a defined rollback procedure.",
            ),
            ("b", "Deploy more frequently so mistakes are smaller."),
            ("c", "Have one engineer manually test in production after release."),
            ("d", "Skip evaluation to speed up the pipeline."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Automated evaluation gates, canary thresholds, and a defined "
            "rollback procedure catch regressions and enable fast recovery. More "
            "frequent deploys without gates still ship regressions, manual prod "
            "testing is unreliable, and skipping evaluation increases risk."
        ),
        "rationales": {
            "a": (True, "Eval gates + canary + rollback reduce risk and speed recovery."),
            "b": (False, "Frequency without gates still ships undetected regressions."),
            "c": (False, "Manual prod testing is slow and unreliable as a gate."),
            "d": (False, "Skipping evaluation removes the regression safety net."),
        },
    },
    {
        "question_id": "d2-tenant-identity-propagation",
        "objective_ids": ["AIP-2.3", "AIP-3.3"],
        "prompt": (
            "A centralized GenAI gateway serves many tenants. Each request must "
            "be authorized and traced as the originating tenant, and one tenant "
            "must never see another's data. What must the gateway enforce?"
        ),
        "scenario_constraint": "Per-tenant authorization and isolation through a shared gateway.",
        "difficulty": "hard",
        "options": [
            (
                "a",
                "Propagate tenant identity and enforce per-tenant authorization and trace correlation.",
            ),
            ("b", "Use one shared service identity for all tenants."),
            ("c", "Rely on tenants to filter their own results client-side."),
            ("d", "Mix all tenant data and sort it out in the response."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A shared gateway must propagate the tenant identity and enforce "
            "per-tenant authorization plus trace correlation so isolation holds. "
            "A single shared identity erases tenancy, client-side filtering is "
            "not a security boundary, and mixing data risks cross-tenant leakage."
        ),
        "rationales": {
            "a": (True, "Identity propagation + per-tenant authorization enforces isolation."),
            "b": (False, "A shared identity cannot distinguish or isolate tenants."),
            "c": (False, "Client-side filtering is not an enforced security boundary."),
            "d": (False, "Mixing tenant data risks cross-tenant exposure."),
        },
    },
    # --- AIP-2.4 FM APIs, streaming ----------------------------------------
    {
        "question_id": "d2-streaming-ttfb",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "A chat UI feels slow because users wait for the full model response "
            "before seeing anything. The total generation time cannot be reduced "
            "much. How do you most improve perceived responsiveness?"
        ),
        "scenario_constraint": "Improve perceived latency without reducing total generation time.",
        "difficulty": "easy",
        "options": [
            ("a", "Stream tokens to the UI as they are generated."),
            ("b", "Buffer the full response and send it at the end."),
            ("c", "Shorten every answer to one sentence."),
            ("d", "Add a longer loading spinner."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Streaming tokens as they are produced shows output immediately, "
            "greatly improving perceived responsiveness even when total time is "
            "unchanged. Buffering delays all output, truncating harms quality, "
            "and a spinner does not deliver content sooner."
        ),
        "rationales": {
            "a": (True, "Streaming surfaces output immediately, improving perceived latency."),
            "b": (False, "Buffering the whole response is exactly the slow behavior."),
            "c": (False, "Forcing one-sentence answers sacrifices answer quality."),
            "d": (False, "A spinner does not deliver content any sooner."),
        },
    },
    {
        "question_id": "d2-backoff-jitter",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "Under load, many clients retry throttled model calls at the same "
            "fixed interval, creating synchronized retry storms that worsen "
            "throttling. What retry policy fixes this?"
        ),
        "scenario_constraint": "Avoid synchronized retry storms under throttling.",
        "difficulty": "medium",
        "options": [
            ("a", "Bounded exponential backoff with jitter and a max-attempt cap."),
            ("b", "Immediate fixed-interval retries with no limit."),
            ("c", "Retry forever until the call succeeds."),
            ("d", "Disable retries entirely so every throttle is a hard failure."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Exponential backoff with jitter spreads retries out and a max-attempt "
            "cap bounds them, breaking synchronized storms. Fixed-interval or "
            "infinite retries sustain the storm, and disabling retries throws "
            "away recoverable transient failures."
        ),
        "rationales": {
            "a": (True, "Backoff + jitter + cap desynchronizes and bounds retries."),
            "b": (False, "Fixed-interval unlimited retries recreate the storm."),
            "c": (False, "Infinite retries never relieve the overload."),
            "d": (False, "No retries fail even recoverable transient throttles."),
        },
    },
    {
        "question_id": "d2-idempotent-side-effects",
        "objective_ids": ["AIP-2.4", "AIP-2.5"],
        "prompt": (
            "A request that charges a customer can be retried after a timeout, "
            "but a retry must never double-charge. Which mechanism guarantees "
            "safe retries?"
        ),
        "scenario_constraint": "Retries must not duplicate a side effect (double charge).",
        "difficulty": "hard",
        "options": [
            ("a", "Make the operation idempotent using a caller-provided request/idempotency key."),
            ("b", "Hope the first call always completes before any retry."),
            ("c", "Disable timeouts so requests never retry."),
            ("d", "Charge first and refund later if it was a duplicate."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "An idempotency key lets the service recognize a replay and return "
            "the prior result without repeating the side effect. Hoping, removing "
            "timeouts, and refund-after-the-fact all permit or paper over "
            "double-charges."
        ),
        "rationales": {
            "a": (True, "An idempotency key makes replays safe with no duplicate effect."),
            "b": (False, "Hoping about timing is not a guarantee."),
            "c": (False, "Disabling timeouts trades retries for hangs, not safety."),
            "d": (False, "Charge-then-refund still double-charges transiently."),
        },
    },
    {
        "question_id": "d2-token-limit-validation",
        "objective_ids": ["AIP-2.4"],
        "prompt": (
            "Some user inputs exceed the model's context limit and cause runtime "
            "errors deep in the request path. You want to fail fast and clearly. "
            "Where should the length check happen?"
        ),
        "scenario_constraint": "Catch over-limit input before it reaches the model.",
        "difficulty": "easy",
        "options": [
            ("a", "Validate input against the token/context limit before the model call."),
            ("b", "Let the model call fail and surface the raw error to users."),
            ("c", "Silently truncate the middle of every input."),
            ("d", "Increase retries so the oversized call eventually works."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Validating against the token limit up front fails fast with a clear "
            "message and avoids deep runtime errors. Surfacing raw errors is poor "
            "UX, silent truncation corrupts meaning, and retries cannot make an "
            "over-limit request fit."
        ),
        "rationales": {
            "a": (True, "Pre-call validation fails fast and cleanly on over-limit input."),
            "b": (False, "Raw deep errors are a poor, unclear user experience."),
            "c": (False, "Silent truncation can corrupt the input's meaning."),
            "d": (False, "Retrying cannot make an over-limit request fit the context."),
        },
    },
    # --- AIP-2.5 async, routing, observability -----------------------------
    {
        "question_id": "d2-model-routing-policy",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A service wants to send simple requests to a cheap fast model and "
            "hard requests to a stronger costlier model, with a safe default when "
            "classification is unclear. What does a sound routing design require?"
        ),
        "scenario_constraint": "Route by complexity with a safe fallback when unsure.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "An explicit routing policy with criteria plus a defined no-route/fallback outcome.",
            ),
            ("b", "Randomly assign each request to a model."),
            ("c", "Always use the cheap model and accept worse answers."),
            ("d", "Let each model decide whether to answer."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Sound routing uses explicit criteria (complexity, cost, capability) "
            "and defines a fallback when no rule clearly applies. Random "
            "assignment ignores fit, cheap-only sacrifices quality, and letting "
            "models self-select has no controlled policy or fallback."
        ),
        "rationales": {
            "a": (True, "Explicit criteria plus a fallback is a controlled routing policy."),
            "b": (False, "Random routing ignores request fit entirely."),
            "c": (False, "Cheap-only abandons quality for hard requests."),
            "d": (False, "Model self-selection lacks a controlled policy and fallback."),
        },
    },
    {
        "question_id": "d2-duplicate-event-handling",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "An event-driven pipeline occasionally delivers the same event more "
            "than once (at-least-once delivery), and reprocessing causes "
            "duplicate outputs. How should consumers handle this?"
        ),
        "scenario_constraint": "At-least-once delivery must not cause duplicate processing.",
        "difficulty": "medium",
        "options": [
            ("a", "Deduplicate by event ID so repeated deliveries are processed once."),
            ("b", "Assume exactly-once delivery and ignore duplicates."),
            ("c", "Process every delivery and tolerate duplicate outputs."),
            ("d", "Drop any event that looks unfamiliar."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "At-least-once delivery requires consumer-side dedup keyed on a stable "
            "event ID so a repeat is processed once. Assuming exactly-once is "
            "false, tolerating duplicates produces wrong outputs, and dropping "
            "unfamiliar events loses real work."
        ),
        "rationales": {
            "a": (True, "Event-ID dedup makes at-least-once delivery safe."),
            "b": (False, "At-least-once delivery means duplicates do occur."),
            "c": (False, "Tolerating duplicate outputs is the defect to fix."),
            "d": (False, "Dropping unfamiliar events discards legitimate work."),
        },
    },
    {
        "question_id": "d2-trace-correlation",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "Diagnosing a failed multi-step agent request is hard because logs "
            "from the gateway, agent, tool calls, and model call cannot be tied "
            "together. What most directly enables root-cause analysis?"
        ),
        "scenario_constraint": "Tie together logs across components for one request.",
        "difficulty": "medium",
        "options": [
            ("a", "Propagate a correlation/trace ID across every component and log it."),
            ("b", "Increase the log level everywhere and read more lines."),
            ("c", "Store logs in separate systems with no shared key."),
            ("d", "Log full prompts and payloads including secrets for completeness."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A propagated correlation/trace ID lets you reconstruct one request "
            "across components, which is the basis for root-cause analysis. More "
            "verbosity without a shared key does not link events, separate "
            "unkeyed stores stay disjoint, and logging secrets is a privacy "
            "violation."
        ),
        "rationales": {
            "a": (True, "A shared trace ID correlates one request across components."),
            "b": (False, "More volume without a correlation key still cannot be joined."),
            "c": (False, "Unkeyed separate stores cannot be correlated."),
            "d": (False, "Logging secrets/PII violates privacy and is never acceptable."),
        },
    },
    {
        "question_id": "d2-no-false-success",
        "objective_ids": ["AIP-2.5"],
        "prompt": (
            "A streaming response is cut off midway by a downstream failure, but "
            "the service still returns HTTP 200 with a partial answer. Reviewers "
            "flag this as unsafe. What is the correct behavior?"
        ),
        "scenario_constraint": "A partial/failed result must not be reported as success.",
        "difficulty": "hard",
        "options": [
            (
                "a",
                "Detect the partial/failed stream and return an explicit error or safe fallback.",
            ),
            ("b", "Return 200 with whatever partial text arrived."),
            ("c", "Retry silently forever until something completes."),
            ("d", "Cache the partial answer and serve it to future users."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A truncated or failed stream must surface as an explicit error or a "
            "safe fallback, never a false success. Returning 200 on a partial "
            "answer misleads callers, infinite silent retries hang, and caching a "
            "partial answer spreads the defect."
        ),
        "rationales": {
            "a": (True, "An incomplete result must be an explicit error or safe fallback."),
            "b": (False, "A 200 on partial output is a false success."),
            "c": (False, "Unbounded silent retries hang the request."),
            "d": (False, "Caching a partial answer propagates the failure."),
        },
    },
]


def question_count() -> int:
    """Return the number of authored Domain 2 questions."""
    return len(QUESTIONS)
