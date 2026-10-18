"""Authored Domain 4 (AIP-C01) scenario questions with answers and explanations.

Original, scenario-style multiple-choice questions testing operations,
performance, and cost reasoning for the AWS Certified Generative AI Developer
exam. Each question has a decisive constraint, four distinct options, one
correct answer, per-option rationales, and a teaching explanation. No
proprietary exam content is reproduced.

Shape per question matches ``content/domain1_questions.py`` so the same
ingestion path consumes all authored domains.
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    # --- AIP-4.1 operations, monitoring, incident response -----------------
    {
        "question_id": "d4-golden-signals",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A GenAI service has no operational visibility, so the team learns "
            "about problems only from user complaints. What should they "
            "instrument first to detect issues proactively?"
        ),
        "scenario_constraint": "Detect problems before users report them.",
        "difficulty": "easy",
        "options": [
            ("a", "Metrics and alarms on latency, error rate, throughput, and cost per request."),
            ("b", "A monthly manual review of a few sample requests."),
            ("c", "Nothing; rely on users to report outages."),
            ("d", "Only a count of total requests, with no latency or errors."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Instrumenting latency, error rate, throughput, and cost with alarms "
            "surfaces problems proactively. Monthly sampling is too slow, "
            "user-reported outages are reactive, and a bare request count hides "
            "latency and error regressions."
        ),
        "rationales": {
            "a": (True, "Core signals with alarms detect regressions proactively."),
            "b": (False, "Monthly sampling cannot catch issues in time."),
            "c": (False, "User reports are reactive, not proactive detection."),
            "d": (False, "A request count alone hides latency and error problems."),
        },
    },
    {
        "question_id": "d4-trace-before-remedy",
        "objective_ids": ["AIP-4.1", "AIP-5.2"],
        "prompt": (
            "A multi-step pipeline (retrieve, rerank, generate) is intermittently "
            "slow, but it is unclear which step is responsible. What should you "
            "do before optimizing anything?"
        ),
        "scenario_constraint": "Find the bottleneck from evidence before remediating.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Use distributed traces/per-step timing to identify the slow step, then target it.",
            ),
            ("b", "Optimize the generation step because it feels slowest."),
            ("c", "Rewrite the whole pipeline and hope it is faster."),
            ("d", "Add more hardware everywhere without measuring."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Per-step tracing identifies the actual bottleneck so you remediate "
            "the right step. Guessing at the generation step, rewriting blindly, "
            "or scaling everything wastes effort and may not touch the real "
            "cause."
        ),
        "rationales": {
            "a": (True, "Trace-led diagnosis targets the real bottleneck."),
            "b": (False, "A hunch is not evidence of the slow step."),
            "c": (False, "A blind rewrite is costly and may miss the cause."),
            "d": (False, "Scaling everything without data wastes cost."),
        },
    },
    {
        "question_id": "d4-incident-rollback",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Right after a prompt/model deployment, answer quality drops and "
            "error rates spike. The priority is restoring service quickly. What "
            "is the correct first action?"
        ),
        "scenario_constraint": "Restore service fast after a bad deploy.",
        "difficulty": "medium",
        "options": [
            ("a", "Roll back to the last known-good version, then investigate root cause."),
            ("b", "Leave the bad version live while debugging in production."),
            ("c", "Disable monitoring so the alarms stop firing."),
            ("d", "Wait to see if the problem resolves itself."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Rolling back to the last known-good version restores service "
            "immediately, after which you investigate safely. Leaving the bad "
            "version live prolongs harm, silencing alarms hides the problem, and "
            "waiting gambles with the outage."
        ),
        "rationales": {
            "a": (True, "Rollback restores service fast; investigate afterward."),
            "b": (False, "Debugging live prolongs the user-facing outage."),
            "c": (False, "Silencing alarms hides the incident, not fixes it."),
            "d": (False, "Waiting gambles on self-resolution during an outage."),
        },
    },
    {
        "question_id": "d4-no-sensitive-telemetry",
        "objective_ids": ["AIP-4.1", "AIP-3.2"],
        "prompt": (
            "To improve observability, a team proposes logging full prompts and "
            "model responses, including user content. What operational logging "
            "policy is correct?"
        ),
        "scenario_constraint": "Improve observability without logging sensitive content.",
        "difficulty": "easy",
        "options": [
            (
                "a",
                "Log sanitized metrics, correlation IDs, and events; redact prompts, responses, PII, and secrets.",
            ),
            ("b", "Log everything verbatim for completeness."),
            ("c", "Log full content but keep it in a separate bucket."),
            ("d", "Log nothing to avoid any privacy risk."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Observability comes from sanitized metrics, correlation IDs, and "
            "events with sensitive content redacted. Verbatim logging leaks "
            "data, a separate bucket still stores the sensitive content, and "
            "logging nothing destroys observability."
        ),
        "rationales": {
            "a": (True, "Sanitized, correlated telemetry gives visibility without leaks."),
            "b": (False, "Verbatim logs persist private content and secrets."),
            "c": (False, "A separate bucket still stores the sensitive data."),
            "d": (False, "No logging eliminates observability entirely."),
        },
    },
    # --- AIP-4.2 performance optimization ----------------------------------
    {
        "question_id": "d4-cache-repeated-queries",
        "objective_ids": ["AIP-4.2", "AIP-4.3"],
        "prompt": (
            "Analytics show a large share of identical, deterministic prompts "
            "(e.g., the same FAQ question) hitting the model repeatedly. You "
            "want to cut latency and cost without changing answers. What helps "
            "most?"
        ),
        "scenario_constraint": "Many identical deterministic prompts; cut latency and cost.",
        "difficulty": "medium",
        "options": [
            ("a", "Cache responses for identical deterministic prompts and serve from cache."),
            ("b", "Cache every prompt indefinitely regardless of variability."),
            ("c", "Switch to a bigger model to answer faster."),
            ("d", "Remove the FAQ feature to reduce load."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Caching responses for identical, deterministic prompts cuts both "
            "latency and cost while preserving answers. Caching everything "
            "regardless of variability serves stale/wrong answers, a bigger "
            "model raises cost, and removing the feature avoids the value."
        ),
        "rationales": {
            "a": (True, "Caching deterministic repeats cuts latency and cost safely."),
            "b": (False, "Caching variable prompts returns stale/wrong answers."),
            "c": (False, "A bigger model increases cost, not reduces it."),
            "d": (False, "Removing the feature abandons its value."),
        },
    },
    {
        "question_id": "d4-prompt-token-reduction",
        "objective_ids": ["AIP-4.2", "AIP-4.3"],
        "prompt": (
            "A pipeline stuffs huge, mostly-irrelevant context into every prompt, "
            "driving up token cost and latency. Accuracy does not depend on most "
            "of that context. What is the best optimization?"
        ),
        "scenario_constraint": "Oversized prompts; most context is irrelevant.",
        "difficulty": "medium",
        "options": [
            ("a", "Retrieve and include only the relevant context, trimming prompt tokens."),
            ("b", "Always send the entire corpus to be safe."),
            ("c", "Increase the model's max tokens so big prompts fit."),
            ("d", "Lower temperature to compensate for the long prompt."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Including only relevant retrieved context cuts tokens, which lowers "
            "both cost and latency without hurting accuracy. Sending everything "
            "is the problem, raising max tokens worsens cost, and temperature is "
            "unrelated to prompt size."
        ),
        "rationales": {
            "a": (True, "Trimming to relevant context reduces tokens, cost, and latency."),
            "b": (False, "Sending the whole corpus is the oversized-prompt problem."),
            "c": (False, "Raising max tokens increases cost, not efficiency."),
            "d": (False, "Temperature does not affect prompt token size."),
        },
    },
    {
        "question_id": "d4-concurrency-throughput",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A batch workload processes items strictly one at a time, leaving "
            "model capacity idle and missing its throughput target. Latency per "
            "item is acceptable. What improves throughput?"
        ),
        "scenario_constraint": "Serial processing underutilizes capacity; need higher throughput.",
        "difficulty": "medium",
        "options": [
            ("a", "Process items concurrently up to a bounded parallelism that respects quotas."),
            ("b", "Keep strict serial processing but buy a bigger model."),
            ("c", "Remove all rate limits and fire unlimited parallel calls."),
            ("d", "Reduce the number of items to fit the serial rate."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Bounded concurrency that respects quotas raises throughput by using "
            "idle capacity without triggering throttling. Serial processing is "
            "the bottleneck, unbounded parallelism causes throttling/overload, "
            "and dropping items avoids the work."
        ),
        "rationales": {
            "a": (True, "Bounded concurrency lifts throughput within quota limits."),
            "b": (False, "A bigger model does not fix serial underutilization."),
            "c": (False, "Unbounded parallelism causes throttling and overload."),
            "d": (False, "Reducing items dodges the throughput requirement."),
        },
    },
    {
        "question_id": "d4-optimize-quality-floor",
        "objective_ids": ["AIP-4.2", "AIP-5.1"],
        "prompt": (
            "A proposed optimization (smaller model + aggressive truncation) "
            "halves cost but, in testing, drops answer accuracy below the "
            "product's quality bar. How should you proceed?"
        ),
        "scenario_constraint": "Optimization must not drop quality below the explicit threshold.",
        "difficulty": "hard",
        "options": [
            (
                "a",
                "Reject or adjust the optimization so it preserves the quality threshold, then re-measure.",
            ),
            ("b", "Ship it anyway because the cost savings are large."),
            ("c", "Lower the quality bar to make the optimization pass."),
            ("d", "Stop measuring quality so the regression is not visible."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "An optimization that breaches the quality floor must be rejected or "
            "adjusted and re-measured; cost savings never justify falling below "
            "an explicit quality threshold. Shipping it, moving the bar, or "
            "hiding the regression all trade away required quality."
        ),
        "rationales": {
            "a": (True, "Preserve the quality floor; re-measure after adjusting."),
            "b": (False, "Cost savings do not justify breaching the quality bar."),
            "c": (False, "Lowering the bar to pass defeats the threshold's purpose."),
            "d": (False, "Hiding the regression ships worse quality silently."),
        },
    },
    # --- AIP-4.3 cost optimization -----------------------------------------
    {
        "question_id": "d4-right-size-model-cost",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Most traffic is simple requests handled perfectly by a cheap model, "
            "but everything currently routes to an expensive flagship model. You "
            "must cut cost without hurting hard requests. What is the best "
            "approach?"
        ),
        "scenario_constraint": "Cut cost on simple traffic without hurting hard requests.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Route simple requests to the cheap model and reserve the flagship for hard ones.",
            ),
            ("b", "Move all traffic to the cheap model regardless of difficulty."),
            ("c", "Keep everything on the flagship for consistency."),
            ("d", "Randomly assign requests to models to spread cost."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Complexity-based routing sends cheap traffic to the cheap model and "
            "reserves the flagship for hard requests, cutting cost while "
            "preserving quality where needed. Cheap-only hurts hard requests, "
            "flagship-only keeps costs high, and random routing ignores fit."
        ),
        "rationales": {
            "a": (True, "Routing by difficulty cuts cost while protecting hard requests."),
            "b": (False, "Cheap-only degrades hard requests."),
            "c": (False, "Flagship-only leaves cost unaddressed."),
            "d": (False, "Random routing ignores request difficulty."),
        },
    },
    {
        "question_id": "d4-batch-for-cost",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "A reporting workload has no real-time requirement but runs on "
            "expensive on-demand real-time inference. You must reduce its unit "
            "cost. What is the most direct change?"
        ),
        "scenario_constraint": "No real-time need; reduce unit cost.",
        "difficulty": "easy",
        "options": [
            ("a", "Move the workload to batch/asynchronous inference."),
            ("b", "Keep real-time inference but add more replicas."),
            ("c", "Run it on an always-on provisioned endpoint sized for peak."),
            ("d", "Call the model twice per item for reliability."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Batch/asynchronous inference lowers unit cost for workloads without "
            "a latency requirement. Adding replicas and always-on peak-sized "
            "capacity raise cost, and double-calling doubles it."
        ),
        "rationales": {
            "a": (True, "Batch inference reduces unit cost for non-real-time work."),
            "b": (False, "More real-time replicas increase cost."),
            "c": (False, "Always-on peak capacity is costly for a batch job."),
            "d": (False, "Calling twice per item doubles cost."),
        },
    },
    {
        "question_id": "d4-cost-attribution",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Spend is rising but the team cannot tell which feature or tenant "
            "drives it, so they cannot target optimization. What should they add "
            "first?"
        ),
        "scenario_constraint": "Attribute cost to features/tenants to target optimization.",
        "difficulty": "medium",
        "options": [
            ("a", "Tag and track usage/cost per feature and tenant so spend is attributable."),
            ("b", "Cut the overall budget and hope usage drops."),
            ("c", "Optimize a random component and see if the bill falls."),
            ("d", "Assume the biggest model is the only cost driver."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Per-feature/per-tenant cost attribution (tagging and usage "
            "tracking) shows where spend goes so optimization can target the "
            "real drivers. Blanket budget cuts, random optimization, and "
            "assumptions are not evidence-based."
        ),
        "rationales": {
            "a": (True, "Attribution reveals the real cost drivers to target."),
            "b": (False, "A blanket cut does not identify or fix drivers."),
            "c": (False, "Random optimization is not evidence-based."),
            "d": (False, "Assuming the driver skips measurement."),
        },
    },
    {
        "question_id": "d4-provisioned-vs-ondemand-cost",
        "objective_ids": ["AIP-4.3", "AIP-2.2"],
        "prompt": (
            "A workload runs at a steady, high, predictable volume all day. On-"
            "demand per-request pricing is costing more than a reserved option "
            "would at that utilization. What reduces cost?"
        ),
        "scenario_constraint": "Steady high utilization; on-demand is overpriced here.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Use Provisioned Throughput sized to the sustained load for predictable, lower cost.",
            ),
            ("b", "Stay on-demand because it is always cheapest."),
            ("c", "Over-provision far above peak for safety."),
            ("d", "Switch models hourly to chase the lowest price."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "At steady high utilization, Provisioned Throughput sized to the "
            "load is cheaper and more predictable than per-request on-demand. "
            "On-demand is not always cheapest, over-provisioning wastes money, "
            "and hourly model-switching adds churn without a cost basis."
        ),
        "rationales": {
            "a": (True, "Provisioned Throughput is cheaper at steady high utilization."),
            "b": (False, "On-demand is not always cheapest at high steady load."),
            "c": (False, "Over-provisioning above peak wastes cost."),
            "d": (False, "Hourly switching churns without a cost rationale."),
        },
    },
]


def question_count() -> int:
    """Return the number of authored Domain 4 questions."""
    return len(QUESTIONS)
