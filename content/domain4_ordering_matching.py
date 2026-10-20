"""Authored Domain 4 (AIP-C01) ordering and matching questions."""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    # === ORDERING: 4.1 cost optimization (15) ===
    {
        "question_id": "d4o-cost-baseline-lever",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Your generative AI assistant's monthly bill is rising and you want "
            "to cut token cost without guessing. Place the steps in the correct order."
        ),
        "scenario_constraint": "Measure before optimizing; change one lever and re-measure.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Apply one lever such as prompt compression to the costliest path."),
            ("b", "Enable token usage tracking to establish a per-request baseline."),
            ("c", "Attribute cost to features using Cost Explorer and resource tags."),
            ("d", "Re-measure token usage and cost to confirm the saving is real."),
        ],
        "correct_sequence": ["b", "c", "a", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You baseline token usage first, attribute spend to find the costly path, "
            "apply a single lever, then re-measure to confirm the reduction."
        ),
        "rationales": {
            "a": (True, "Changing one lever at a time keeps the result interpretable."),
            "b": (True, "A per-request baseline must exist before you can show savings."),
            "c": (True, "Attribution points the lever at the costliest path."),
            "d": (True, "Re-measurement verifies the change actually lowered cost."),
        },
    },
    {
        "question_id": "d4o-model-cascade-build",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "You want a model cascade that sends only hard requests to an expensive "
            "model to control cost. Place the steps in the correct order."
        ),
        "scenario_constraint": "Route by complexity; escalate only when the cheap tier fails.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Define a complexity signal that classifies each incoming request."),
            ("b", "Route low-complexity requests to a smaller, cheaper model first."),
            ("c", "Escalate to the larger model only when the cheap tier is low-confidence."),
            ("d", "Track cost per tier to confirm the cascade reduces average spend."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A complexity signal gates routing, cheap-first handles the easy cases, "
            "escalation covers the rest, and per-tier cost tracking confirms the saving."
        ),
        "rationales": {
            "a": (True, "Routing needs a complexity classification to decide on."),
            "b": (True, "Cheap-first captures the majority of easy traffic."),
            "c": (True, "Escalation is conditional on the cheap tier falling short."),
            "d": (True, "Per-tier cost tracking proves the cascade pays off."),
        },
    },
    {
        "question_id": "d4o-provisioned-breakeven",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "You are deciding whether to move a steady high-volume workload from "
            "on-demand to Amazon Bedrock provisioned throughput. Place the steps "
            "in the correct order."
        ),
        "scenario_constraint": "Compute break-even before committing provisioned capacity.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Measure sustained throughput and on-demand cost over a stable window."),
            ("b", "Compute the break-even utilization versus provisioned throughput pricing."),
            ("c", "Commit provisioned throughput only if sustained demand exceeds break-even."),
            ("d", "Monitor utilization to confirm the commitment stays above break-even."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You measure real demand, compute break-even, commit only above it, and "
            "then monitor to confirm the commitment remains justified."
        ),
        "rationales": {
            "a": (True, "Break-even math needs measured throughput and cost."),
            "b": (True, "Break-even defines the threshold for committing."),
            "c": (True, "Commitment is justified only above break-even utilization."),
            "d": (True, "Ongoing monitoring catches demand dropping below break-even."),
        },
    },
    {
        "question_id": "d4o-semantic-cache-setup",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "You want to add semantic caching with Amazon ElastiCache so repeated "
            "similar questions skip the model. Place the steps in the correct order."
        ),
        "scenario_constraint": "Check the cache before the model; populate it after a miss.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Embed the incoming prompt and look for a semantically similar cache hit."),
            ("b", "Return the cached response immediately when a close match is found."),
            ("c", "Invoke the model only on a cache miss."),
            ("d", "Store the new response in ElastiCache keyed by the prompt embedding."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You look up by embedding first, serve a hit, fall through to the model "
            "on a miss, then populate the cache for next time."
        ),
        "rationales": {
            "a": (True, "The lookup must happen before deciding to call the model."),
            "b": (True, "A hit should short-circuit the expensive model call."),
            "c": (True, "The model runs only when the cache cannot answer."),
            "d": (True, "Populating the cache makes future similar prompts cheap."),
        },
    },
    {
        "question_id": "d4o-prompt-compression",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A verbose prompt template inflates input tokens on every call. Place "
            "the steps in the correct order."
        ),
        "scenario_constraint": "Compress prompts without dropping below the quality floor.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Measure the current input token count per request."),
            ("b", "Prune redundant instructions and compress the template."),
            ("c", "Re-run a quality check to confirm answers stay above the quality floor."),
            ("d", "Roll the leaner template out and track token savings."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You baseline tokens, prune the template, verify quality holds, then roll "
            "out and track the savings."
        ),
        "rationales": {
            "a": (True, "A token baseline is needed to quantify the saving."),
            "b": (True, "Pruning is the lever that reduces input tokens."),
            "c": (True, "Quality must be re-checked before shipping a leaner prompt."),
            "d": (True, "Rollout and tracking confirm the realized saving."),
        },
    },
    {
        "question_id": "d4o-batch-offline",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A nightly summarization job does not need real-time responses, so you "
            "move it to batch inference for cost. Place the steps in the correct order."
        ),
        "scenario_constraint": "Shift latency-tolerant work to batch to cut per-request cost.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Identify the job as latency-tolerant and safe to defer."),
            ("b", "Accumulate inputs into a batch instead of calling per item."),
            ("c", "Submit the batch inference job during off-peak hours."),
            ("d", "Compare batch cost against the prior per-request spend."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You confirm the job tolerates latency, accumulate inputs, submit the "
            "batch, then compare cost against the per-request baseline."
        ),
        "rationales": {
            "a": (True, "Batching is only appropriate for latency-tolerant work."),
            "b": (True, "Inputs must be accumulated before a batch can be submitted."),
            "c": (True, "Off-peak submission is the batch execution step."),
            "d": (True, "Comparison confirms batch actually saved money."),
        },
    },
    {
        "question_id": "d4o-response-limiting",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Unbounded completions are driving up output token cost. Place the steps "
            "in the correct order."
        ),
        "scenario_constraint": "Cap output length without truncating needed answers.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Measure the distribution of output token counts."),
            ("b", "Set a max-token limit sized to the real answer length."),
            ("c", "Validate that capped responses are not being cut off mid-answer."),
            ("d", "Deploy the limit and track output token reduction."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You measure output lengths, set a limit matched to real answers, verify "
            "no truncation, then deploy and track savings."
        ),
        "rationales": {
            "a": (True, "Knowing the output distribution sizes the cap correctly."),
            "b": (True, "The max-token limit is the cost lever."),
            "c": (True, "Validation ensures the cap does not truncate answers."),
            "d": (True, "Deployment with tracking confirms the reduction."),
        },
    },
    {
        "question_id": "d4o-cost-attribution",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Finance wants per-feature cost visibility for your generative AI app. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Attribute spend by tagging and analysis, not estimation.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Apply cost-allocation tags identifying each feature's resources."),
            ("b", "Activate the tags as cost-allocation tags in the billing settings."),
            ("c", "Group spend by tag in AWS Cost Explorer."),
            ("d", "Report per-feature cost and flag the most expensive feature."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You tag resources, activate the tags for billing, group spend in Cost "
            "Explorer, then report and flag the costly feature."
        ),
        "rationales": {
            "a": (True, "Tags are the foundation of per-feature attribution."),
            "b": (True, "Tags must be activated before they appear in billing."),
            "c": (True, "Cost Explorer groups the activated tags into spend views."),
            "d": (True, "Reporting is the output that drives the decision."),
        },
    },
    {
        "question_id": "d4o-context-window-trim",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A chat feature stuffs the full history into every call, growing context "
            "cost over a session. Place the steps in the correct order."
        ),
        "scenario_constraint": "Optimize the context window while preserving answer quality.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Measure how context tokens grow across a typical session."),
            ("b", "Summarize older turns and keep only recent full turns."),
            ("c", "Confirm the trimmed context still answers follow-up questions."),
            ("d", "Track the per-session token and cost reduction after rollout."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You measure context growth, summarize old turns, confirm quality holds, "
            "then track the per-session saving."
        ),
        "rationales": {
            "a": (True, "Measuring growth shows where context tokens accumulate."),
            "b": (True, "Summarizing old turns is the context-optimization lever."),
            "c": (True, "Quality must survive the trimming before rollout."),
            "d": (True, "Tracking confirms the per-session reduction."),
        },
    },
    {
        "question_id": "d4o-tiered-fm-selection",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "You want to pick the cheapest model that still meets each task's quality "
            "bar. Place the steps in the correct order."
        ),
        "scenario_constraint": "Trade cost against capability using measured quality.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Define the minimum acceptable quality bar for the task."),
            ("b", "Benchmark candidate models for quality and cost on that task."),
            ("c", "Select the lowest-cost model that clears the quality bar."),
            ("d", "Monitor production quality to confirm the choice still holds."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You set the quality bar, benchmark candidates, pick the cheapest that "
            "clears it, then monitor that the choice holds in production."
        ),
        "rationales": {
            "a": (True, "A quality bar is the constraint the selection must meet."),
            "b": (True, "Benchmarking supplies the cost-capability data."),
            "c": (True, "Choosing the cheapest qualifying model optimizes the tradeoff."),
            "d": (True, "Monitoring guards against drift away from the quality bar."),
        },
    },
    {
        "question_id": "d4o-prompt-cache-reuse",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A long shared system prompt is re-sent on every call. You want to reuse "
            "a cached prompt prefix. Place the steps in the correct order."
        ),
        "scenario_constraint": "Cache the stable prefix so its tokens are not re-billed.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Identify the stable prompt prefix shared across requests."),
            ("b", "Enable prompt caching for that prefix."),
            ("c", "Send only the variable suffix on subsequent calls."),
            ("d", "Measure the input token reduction from reused prefixes."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You find the stable prefix, enable caching, send only the variable part, "
            "then measure the token reduction."
        ),
        "rationales": {
            "a": (True, "Caching only helps for a genuinely stable prefix."),
            "b": (True, "Enabling prompt caching is the lever itself."),
            "c": (True, "Sending only the suffix is what avoids re-billing the prefix."),
            "d": (True, "Measurement confirms the input-token saving."),
        },
    },
    {
        "question_id": "d4o-token-estimation-budget",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Before launch you need a defensible cost forecast for a new feature. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Estimate from measured token counts, not round guesses.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Estimate average input and output tokens per request from samples."),
            ("b", "Multiply token estimates by model price and expected request volume."),
            ("c", "Add a margin for peak traffic and retries."),
            ("d", "Compare the forecast to the approved budget."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You estimate tokens per request, scale by price and volume, add a peak "
            "margin, then compare against the budget."
        ),
        "rationales": {
            "a": (True, "Per-request token estimates are the forecast's basis."),
            "b": (True, "Price times volume turns tokens into projected spend."),
            "c": (True, "A margin accounts for peaks and retries."),
            "d": (True, "Comparison to budget is the decision the forecast supports."),
        },
    },
    {
        "question_id": "d4o-autoscale-cost-floor",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A SageMaker endpoint runs oversized around the clock, wasting money at "
            "night. Place the steps in the correct order."
        ),
        "scenario_constraint": "Auto-scale to match demand without starving peak traffic.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Measure the daily demand curve against current fixed capacity."),
            ("b", "Configure auto scaling with a demand-based target metric."),
            ("c", "Set minimum capacity that still meets peak latency needs."),
            ("d", "Verify cost drops off-peak while peak performance holds."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You measure demand versus capacity, configure auto scaling, set a safe "
            "minimum, then verify off-peak savings without hurting peak latency."
        ),
        "rationales": {
            "a": (True, "The demand curve shows the over-provisioning to fix."),
            "b": (True, "Auto scaling ties capacity to actual demand."),
            "c": (True, "A minimum protects peak latency from under-scaling."),
            "d": (True, "Verification confirms savings without a performance regression."),
        },
    },
    {
        "question_id": "d4o-cost-anomaly-response",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "AWS Cost Anomaly Detection flags a sudden spike in Bedrock spend. Place "
            "the steps in the correct order."
        ),
        "scenario_constraint": "Diagnose the cost spike before changing anything.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Acknowledge the Cost Anomaly Detection alert."),
            ("b", "Drill into Cost Explorer to find the feature and token driver."),
            ("c", "Confirm the root cause, such as a retry loop inflating calls."),
            ("d", "Apply the targeted fix and watch spend return to baseline."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You acknowledge the anomaly, drill into Cost Explorer, confirm the root "
            "cause, then fix it and watch spend normalize."
        ),
        "rationales": {
            "a": (True, "Acknowledging the alert starts the investigation."),
            "b": (True, "Cost Explorer isolates which driver spiked."),
            "c": (True, "Confirming root cause prevents treating a symptom."),
            "d": (True, "Watching spend normalize validates the fix."),
        },
    },
    {
        "question_id": "d4o-fingerprint-dedupe",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Identical requests from a buggy client hit the model repeatedly. You add "
            "result fingerprinting to dedupe. Place the steps in the correct order."
        ),
        "scenario_constraint": "Deduplicate exact-repeat calls before they reach the model.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Compute a stable fingerprint of each normalized request."),
            ("b", "Check whether a result already exists for that fingerprint."),
            ("c", "Return the stored result when the fingerprint matches."),
            ("d", "Invoke the model and store the result only on a new fingerprint."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You fingerprint the request, check for an existing result, serve it on a "
            "match, and invoke plus store only for new fingerprints."
        ),
        "rationales": {
            "a": (True, "A stable fingerprint is the dedupe key."),
            "b": (True, "The existence check decides hit versus miss."),
            "c": (True, "Serving the stored result avoids a duplicate model call."),
            "d": (True, "Only new fingerprints justify invoking and storing."),
        },
    },
    # === ORDERING: 4.2 performance (15) ===
    {
        "question_id": "d4o-perf-profile-bottleneck",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "End-to-end latency is too high and you do not yet know which stage is "
            "slow. Place the steps in the correct order."
        ),
        "scenario_constraint": "Profile to find the bottleneck before optimizing any stage.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Instrument each stage with AWS X-Ray to capture per-stage latency."),
            ("b", "Identify the single stage contributing the most latency."),
            ("c", "Optimize that stage specifically."),
            ("d", "Re-benchmark end to end to confirm the improvement."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You profile with tracing, locate the dominant stage, optimize it, then "
            "re-benchmark to confirm the gain."
        ),
        "rationales": {
            "a": (True, "Per-stage tracing reveals where time is spent."),
            "b": (True, "You must identify the bottleneck before optimizing."),
            "c": (True, "Optimizing the dominant stage yields the biggest gain."),
            "d": (True, "Re-benchmarking confirms the latency actually dropped."),
        },
    },
    {
        "question_id": "d4o-streaming-perceived",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Users complain the chat feels slow even though total generation time is "
            "fine. You add streaming. Place the steps in the correct order."
        ),
        "scenario_constraint": "Stream tokens to improve perceived latency, same model.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Measure time-to-first-token as the perceived-latency metric."),
            ("b", "Call the Bedrock streaming API instead of the synchronous one."),
            ("c", "Render tokens incrementally to the client as they arrive."),
            ("d", "Confirm time-to-first-token dropped for users."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You baseline time-to-first-token, switch to streaming, render "
            "incrementally, then confirm the perceived-latency metric improved."
        ),
        "rationales": {
            "a": (True, "Time-to-first-token captures perceived latency."),
            "b": (True, "The streaming API is what lets tokens arrive early."),
            "c": (True, "Incremental rendering is what the user actually sees."),
            "d": (True, "Confirming the metric drop validates the change."),
        },
    },
    {
        "question_id": "d4o-parallel-fanout",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A request needs three independent model calls that currently run "
            "sequentially. Place the steps in the correct order."
        ),
        "scenario_constraint": "Parallelize only genuinely independent calls.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Confirm the three calls have no data dependency on each other."),
            ("b", "Issue the three calls in parallel."),
            ("c", "Wait for all results and combine them."),
            ("d", "Measure that wall-clock latency dropped toward the slowest call."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You verify independence, fan out in parallel, join the results, then "
            "confirm latency approaches the slowest single call."
        ),
        "rationales": {
            "a": (True, "Parallelism is only safe when calls are independent."),
            "b": (True, "Issuing in parallel is the optimization."),
            "c": (True, "Combining requires waiting for all results."),
            "d": (True, "The expected gain is latency near the slowest call."),
        },
    },
    {
        "question_id": "d4o-latency-optimized-model",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A real-time feature needs lower latency and you are evaluating a "
            "latency-optimized Bedrock model. Place the steps in the correct order."
        ),
        "scenario_constraint": "Switch models only if latency improves and quality holds.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Benchmark the current model's p50 and p99 latency."),
            ("b", "Benchmark the latency-optimized model on the same prompts."),
            ("c", "Confirm its output quality still meets the quality floor."),
            ("d", "Cut over to the faster model and watch p99 in production."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You baseline latency, benchmark the candidate, confirm quality holds, "
            "then cut over and monitor p99."
        ),
        "rationales": {
            "a": (True, "A latency baseline is needed to compare."),
            "b": (True, "Benchmarking the candidate quantifies the speedup."),
            "c": (True, "Quality must survive the faster model."),
            "d": (True, "Monitoring p99 confirms the gain under real load."),
        },
    },
    {
        "question_id": "d4o-retrieval-index-tune",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "RAG retrieval is the slow stage in your pipeline. Place the steps in the "
            "correct order."
        ),
        "scenario_constraint": "Optimize the vector query stage specifically.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Profile the retrieval stage to confirm it dominates latency."),
            ("b", "Tune the index and query, such as narrowing the candidate set."),
            ("c", "Re-check that top-k relevance did not regress."),
            ("d", "Re-benchmark retrieval latency after tuning."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You confirm retrieval is the bottleneck, tune index and query, verify "
            "relevance holds, then re-benchmark latency."
        ),
        "rationales": {
            "a": (True, "Profiling confirms retrieval is worth optimizing."),
            "b": (True, "Index and query tuning is the retrieval lever."),
            "c": (True, "Relevance must not regress when tuning for speed."),
            "d": (True, "Re-benchmarking shows the latency improvement."),
        },
    },
    {
        "question_id": "d4o-precompute-cache",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A dashboard shows the same expensive summary to many users each morning. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Pre-compute predictable results instead of generating on demand.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Identify the summary as predictable and shared across users."),
            ("b", "Pre-compute it on a schedule before the morning peak."),
            ("c", "Serve the pre-computed result to users on request."),
            ("d", "Confirm request latency dropped to a cache read."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You identify the predictable result, pre-compute it before peak, serve "
            "it on request, then confirm latency is just a cache read."
        ),
        "rationales": {
            "a": (True, "Pre-computation only helps for predictable, shared results."),
            "b": (True, "Scheduling ahead of peak is the pre-compute step."),
            "c": (True, "Serving the stored result is what users experience."),
            "d": (True, "The expected result is cache-read latency."),
        },
    },
    {
        "question_id": "d4o-decoding-params",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Responses are slower and more verbose than needed because decoding "
            "parameters are untuned. Place the steps in the correct order."
        ),
        "scenario_constraint": "Tune temperature, top-k, and top-p against a measured target.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Define the target output style and length."),
            ("b", "Adjust temperature, top-k, and top-p toward that target."),
            ("c", "Run an A/B comparison of quality and latency."),
            ("d", "Promote the parameter set that best meets the target."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You set the target, adjust decoding parameters, A/B test, then promote "
            "the best set."
        ),
        "rationales": {
            "a": (True, "A target defines what tuning aims at."),
            "b": (True, "Decoding parameters are the levers being tuned."),
            "c": (True, "A/B comparison measures the effect objectively."),
            "d": (True, "Promotion rolls out the winning parameters."),
        },
    },
    {
        "question_id": "d4o-concurrency-scale",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Under load, requests queue because concurrency is capped too low. Place "
            "the steps in the correct order."
        ),
        "scenario_constraint": "Raise concurrency only up to the point of diminishing returns.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Measure utilization and queue time at current concurrency."),
            ("b", "Increase concurrency and auto scaling headroom."),
            ("c", "Load-test to find where throughput stops improving."),
            ("d", "Set the concurrency limit at the sustainable throughput point."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You measure utilization, add headroom, load-test for the knee, then set "
            "concurrency at the sustainable point."
        ),
        "rationales": {
            "a": (True, "Queue time shows the current cap is the problem."),
            "b": (True, "Adding headroom is the scaling lever."),
            "c": (True, "Load testing finds diminishing returns."),
            "d": (True, "The final limit is set at sustainable throughput."),
        },
    },
    {
        "question_id": "d4o-hybrid-search-latency",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "You add hybrid search to improve relevance but must keep latency in "
            "check. Place the steps in the correct order."
        ),
        "scenario_constraint": "Add hybrid search while watching the latency budget.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Baseline relevance and latency of the current vector-only search."),
            ("b", "Add a keyword branch and a reranker to form hybrid search."),
            ("c", "Measure the relevance gain and the latency added."),
            ("d", "Keep hybrid search only if it stays within the latency budget."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You baseline, add the hybrid branches, measure the tradeoff, then keep "
            "it only if latency stays within budget."
        ),
        "rationales": {
            "a": (True, "A baseline is needed to judge the tradeoff."),
            "b": (True, "The keyword branch and reranker create hybrid search."),
            "c": (True, "Measuring both relevance and latency quantifies the tradeoff."),
            "d": (True, "The latency budget gates whether to keep hybrid search."),
        },
    },
    {
        "question_id": "d4o-batch-inference-throughput",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A scoring job must process millions of records with high throughput, not "
            "low per-item latency. Place the steps in the correct order."
        ),
        "scenario_constraint": "Optimize for throughput using batch inference.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Confirm the job optimizes for throughput, not per-item latency."),
            ("b", "Group records into appropriately sized batches."),
            ("c", "Run batch inference across the batches concurrently."),
            ("d", "Measure records-per-hour throughput against the deadline."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You confirm throughput is the goal, batch the records, run batch "
            "inference concurrently, then measure throughput against the deadline."
        ),
        "rationales": {
            "a": (True, "Batch inference suits throughput-oriented jobs."),
            "b": (True, "Right-sized batches drive efficient throughput."),
            "c": (True, "Concurrent batch runs maximize records processed."),
            "d": (True, "Throughput against the deadline is the success metric."),
        },
    },
    {
        "question_id": "d4o-p99-tail-fix",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Median latency is fine but p99 is far too high. Place the steps in the "
            "correct order."
        ),
        "scenario_constraint": "Attack the tail using trace data, not the median.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Confirm p99 is the problem while p50 is acceptable."),
            ("b", "Use X-Ray traces of slow requests to find the tail cause."),
            ("c", "Apply a tail-specific fix such as a timeout plus retry or hedged request."),
            ("d", "Re-measure p99 to confirm the tail shrank."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You confirm the tail is the issue, trace slow requests, apply a "
            "tail-specific fix, then re-measure p99."
        ),
        "rationales": {
            "a": (True, "Separating p99 from p50 targets the right problem."),
            "b": (True, "Traces of slow requests reveal the tail cause."),
            "c": (True, "Tail fixes differ from median optimizations."),
            "d": (True, "Re-measuring p99 confirms the tail improved."),
        },
    },
    {
        "question_id": "d4o-query-preprocess",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Noisy user queries bloat retrieval and slow responses. Place the steps "
            "in the correct order."
        ),
        "scenario_constraint": "Preprocess queries before they hit the vector store.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Normalize and trim the raw query text."),
            ("b", "Embed the cleaned query."),
            ("c", "Run the vector search with the cleaned embedding."),
            ("d", "Compare retrieval latency and relevance against the raw baseline."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You clean the query, embed it, search, then compare against the raw " "baseline."
        ),
        "rationales": {
            "a": (True, "Preprocessing reduces noise before embedding."),
            "b": (True, "Embedding happens on the cleaned query."),
            "c": (True, "Search uses the cleaned embedding."),
            "d": (True, "Comparison confirms the preprocessing helped."),
        },
    },
    {
        "question_id": "d4o-benchmark-harness",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "You need a repeatable way to compare model and parameter changes for "
            "latency. Place the steps in the correct order."
        ),
        "scenario_constraint": "Benchmark on a fixed workload for comparable numbers.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Assemble a fixed, representative prompt workload."),
            ("b", "Run the current configuration to record a baseline."),
            ("c", "Run each candidate configuration against the same workload."),
            ("d", "Compare p50/p99 across configurations and pick the winner."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You fix the workload, record a baseline, run candidates on the same "
            "workload, then compare percentiles."
        ),
        "rationales": {
            "a": (True, "A fixed workload makes runs comparable."),
            "b": (True, "A baseline anchors the comparison."),
            "c": (True, "Candidates must run the same workload to compare fairly."),
            "d": (True, "Comparing percentiles selects the winner."),
        },
    },
    {
        "question_id": "d4o-warm-capacity",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Cold starts spike latency when a traffic surge hits an idle endpoint. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Plan capacity so surges do not pay cold-start latency.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Measure the cold-start latency penalty on scale-up."),
            ("b", "Forecast the surge window from historical traffic."),
            ("c", "Pre-warm capacity ahead of the forecast surge."),
            ("d", "Verify surge latency now stays within target."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You quantify the cold-start penalty, forecast the surge, pre-warm "
            "capacity, then verify surge latency stays on target."
        ),
        "rationales": {
            "a": (True, "Quantifying the penalty justifies pre-warming."),
            "b": (True, "A forecast says when to pre-warm."),
            "c": (True, "Pre-warming avoids cold starts during the surge."),
            "d": (True, "Verification confirms the surge stays within target."),
        },
    },
    {
        "question_id": "d4o-vector-query-optimize",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Vector queries scan too many candidates, inflating retrieval time. Place "
            "the steps in the correct order."
        ),
        "scenario_constraint": "Optimize the vector query without sacrificing recall.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Measure current query latency and recall."),
            ("b", "Apply metadata pre-filters to shrink the candidate set."),
            ("c", "Confirm recall of relevant results is preserved."),
            ("d", "Re-measure query latency after filtering."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You baseline latency and recall, pre-filter candidates, confirm recall "
            "holds, then re-measure latency."
        ),
        "rationales": {
            "a": (True, "A latency and recall baseline is required."),
            "b": (True, "Metadata pre-filtering shrinks the search space."),
            "c": (True, "Recall must survive the narrower candidate set."),
            "d": (True, "Re-measuring confirms the latency win."),
        },
    },
    # === ORDERING: 4.3 monitoring (15) ===
    {
        "question_id": "d4o-incident-rollback-first",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "A CloudWatch alarm fires right after a deployment and error rates jump. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Restore service first, then diagnose at leisure.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Acknowledge the CloudWatch alarm and confirm user impact."),
            ("b", "Roll back to the last known-good deployment to restore service."),
            ("c", "Verify the alarm clears and users recover."),
            ("d", "Diagnose the root cause in the failed build offline."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You confirm impact, roll back to restore service, verify recovery, then "
            "diagnose the bad build without user pressure."
        ),
        "rationales": {
            "a": (True, "Confirming impact scopes the incident."),
            "b": (True, "Rollback restores service fastest after a bad deploy."),
            "c": (True, "Verifying recovery closes the user-facing incident."),
            "d": (True, "Root-cause analysis follows once service is safe."),
        },
    },
    {
        "question_id": "d4o-trace-correlate-diagnose",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "A user reports a wrong answer and gives you a correlation ID. Place the "
            "steps in the correct order."
        ),
        "scenario_constraint": "Use the correlation ID to trace the exact request.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Look up the request by its correlation ID in X-Ray."),
            ("b", "Follow the trace across retrieval, model, and tool stages."),
            ("c", "Identify the stage that produced the faulty output."),
            ("d", "Reproduce and confirm the root cause at that stage."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You find the request by correlation ID, follow the trace, locate the "
            "faulty stage, then reproduce to confirm root cause."
        ),
        "rationales": {
            "a": (True, "The correlation ID locates the exact request trace."),
            "b": (True, "Following the trace shows each stage's behavior."),
            "c": (True, "Identifying the faulty stage narrows the search."),
            "d": (True, "Reproduction confirms the diagnosis before fixing."),
        },
    },
    {
        "question_id": "d4o-hallucination-alarm",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "You want an alarm when the hallucination rate rises against a golden "
            "dataset. Place the steps in the correct order."
        ),
        "scenario_constraint": "Compute the metric, publish it, then alarm on it.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Score outputs against the golden dataset to compute a hallucination rate."),
            ("b", "Publish the hallucination rate as a CloudWatch custom metric."),
            ("c", "Create a CloudWatch alarm with a threshold on that metric."),
            ("d", "Route the alarm to the on-call responder."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You compute the rate, publish it as a metric, alarm on the threshold, "
            "then route the alarm to on-call."
        ),
        "rationales": {
            "a": (True, "The golden dataset yields a measurable hallucination rate."),
            "b": (True, "Publishing the metric makes it alarmable."),
            "c": (True, "The alarm watches the metric against a threshold."),
            "d": (True, "Routing ensures a human sees the alarm."),
        },
    },
    {
        "question_id": "d4o-invocation-logs-enable",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "You need auditable records of model inputs and outputs for debugging. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Enable Bedrock invocation logging to a sanitized destination.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Choose a log destination such as CloudWatch Logs or Amazon S3."),
            ("b", "Enable Bedrock Model Invocation Logging to that destination."),
            ("c", "Confirm sensitive fields are redacted before logging."),
            ("d", "Query the logs to investigate a specific invocation."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You pick a destination, enable invocation logging, confirm redaction, "
            "then query the logs during investigation."
        ),
        "rationales": {
            "a": (True, "A destination must exist before logging can write to it."),
            "b": (True, "Enabling invocation logging captures inputs and outputs."),
            "c": (True, "Redaction keeps PII and secrets out of logs."),
            "d": (True, "Querying logs is the payoff during debugging."),
        },
    },
    {
        "question_id": "d4o-canary-synthetics",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "You want to catch outages before users do using a synthetic probe. Place "
            "the steps in the correct order."
        ),
        "scenario_constraint": "Use CloudWatch Synthetics to probe the endpoint on a schedule.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Write a canary that exercises the critical request path."),
            ("b", "Schedule the CloudWatch Synthetics canary to run periodically."),
            ("c", "Alarm when the canary fails or exceeds a latency threshold."),
            ("d", "Page on-call on sustained canary failure."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You author the canary, schedule it, alarm on failure, then page on-call "
            "when it stays down."
        ),
        "rationales": {
            "a": (True, "The canary must exercise the real critical path."),
            "b": (True, "Scheduling makes the probe continuous."),
            "c": (True, "An alarm turns canary failure into a signal."),
            "d": (True, "Paging ensures a human responds to sustained failure."),
        },
    },
    {
        "question_id": "d4o-cost-dashboard-build",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Leadership wants a single dashboard for token usage, latency, and cost. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Emit metrics, then compose a CloudWatch dashboard.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Emit token-usage, latency, and cost metrics to CloudWatch."),
            ("b", "Create a CloudWatch dashboard with widgets for each metric."),
            ("c", "Add thresholds and annotations for the target ranges."),
            ("d", "Share the dashboard link with leadership."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You emit the metrics, build the dashboard, annotate targets, then share " "it."
        ),
        "rationales": {
            "a": (True, "Dashboards need the metrics to exist first."),
            "b": (True, "Widgets visualize the emitted metrics."),
            "c": (True, "Thresholds give the numbers context."),
            "d": (True, "Sharing delivers the dashboard to its audience."),
        },
    },
    {
        "question_id": "d4o-drift-detect-respond",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Output quality is slowly degrading and you suspect data drift. Place the "
            "steps in the correct order."
        ),
        "scenario_constraint": "Detect drift from monitoring before changing the model.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Track a quality metric trend over time in CloudWatch."),
            ("b", "Detect the downward drift crossing an anomaly threshold."),
            ("c", "Diagnose whether inputs or the model changed."),
            ("d", "Apply the targeted remediation and watch the trend recover."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You trend the quality metric, detect the drift, diagnose the cause, then "
            "remediate and watch recovery."
        ),
        "rationales": {
            "a": (True, "A trend is needed to see drift at all."),
            "b": (True, "Anomaly detection flags the drift."),
            "c": (True, "Diagnosis separates input drift from model issues."),
            "d": (True, "Watching the trend confirms the remediation worked."),
        },
    },
    {
        "question_id": "d4o-sanitized-telemetry",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "You want rich request telemetry without logging private prompt content. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Capture structure and identifiers, never sensitive payloads.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Decide which fields are safe identifiers versus sensitive content."),
            ("b", "Redact or hash sensitive content before it reaches logs."),
            ("c", "Emit the sanitized telemetry to CloudWatch."),
            ("d", "Audit a sample of logs to confirm no PII leaked."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You classify fields, redact sensitive ones, emit the sanitized "
            "telemetry, then audit to confirm no leakage."
        ),
        "rationales": {
            "a": (True, "Classifying fields decides what may be logged."),
            "b": (True, "Redaction happens before anything is written."),
            "c": (True, "Only sanitized telemetry is emitted."),
            "d": (True, "An audit verifies the redaction held."),
        },
    },
    {
        "question_id": "d4o-tool-call-observability",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "An agent sometimes loops on tool calls and you need visibility. Place the "
            "steps in the correct order."
        ),
        "scenario_constraint": "Trace each tool call with X-Ray to see the loop.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Instrument each tool call as an X-Ray subsegment."),
            ("b", "Emit a metric for tool-call count per request."),
            ("c", "Alarm when tool-call count exceeds a sane ceiling."),
            ("d", "Open the trace of a flagged request to see the loop."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You instrument tool calls, emit a count metric, alarm on excess, then "
            "open the trace of a flagged request."
        ),
        "rationales": {
            "a": (True, "Subsegments make each tool call visible."),
            "b": (True, "A count metric quantifies looping."),
            "c": (True, "An alarm flags runaway tool-call counts."),
            "d": (True, "The trace shows the actual loop for diagnosis."),
        },
    },
    {
        "question_id": "d4o-golden-regression",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "You want to catch quality regressions before each release. Place the "
            "steps in the correct order."
        ),
        "scenario_constraint": "Diff new outputs against a golden dataset as a quality gate.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Maintain a golden dataset of expected outputs."),
            ("b", "Run the candidate build against the golden dataset."),
            ("c", "Diff candidate outputs against the expected baseline."),
            ("d", "Block the release if the regression exceeds the gate."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You keep a golden dataset, run the candidate, diff outputs, then gate the "
            "release on the regression size."
        ),
        "rationales": {
            "a": (True, "The golden dataset defines expected behavior."),
            "b": (True, "Running the candidate produces comparable outputs."),
            "c": (True, "Diffing surfaces regressions."),
            "d": (True, "The gate stops a regressed build from shipping."),
        },
    },
    {
        "question_id": "d4o-anomaly-baseline",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "You want anomaly detection on token usage instead of a static threshold. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Let CloudWatch learn a baseline before alerting.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Emit the token-usage metric to CloudWatch."),
            ("b", "Enable anomaly detection so a baseline band is learned."),
            ("c", "Alarm when usage falls outside the learned band."),
            ("d", "Investigate flagged anomalies before acting."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You emit the metric, enable anomaly detection to learn a band, alarm on "
            "deviations, then investigate before acting."
        ),
        "rationales": {
            "a": (True, "The metric must exist to detect anomalies on."),
            "b": (True, "Anomaly detection learns the normal band."),
            "c": (True, "Alarming on deviations replaces static thresholds."),
            "d": (True, "Investigation precedes any remediation."),
        },
    },
    {
        "question_id": "d4o-business-metric-link",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "You want to connect model behavior to a business outcome like deflection "
            "rate. Place the steps in the correct order."
        ),
        "scenario_constraint": "Instrument the business metric alongside operational ones.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Define the business metric, such as ticket deflection rate."),
            ("b", "Emit the business metric to CloudWatch with operational metrics."),
            ("c", "Correlate the business metric against latency and quality."),
            ("d", "Alert when the business metric degrades."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You define the business metric, emit it with operational metrics, "
            "correlate it, then alert on degradation."
        ),
        "rationales": {
            "a": (True, "A defined business metric anchors the analysis."),
            "b": (True, "Emitting it alongside ops metrics enables correlation."),
            "c": (True, "Correlation links model behavior to outcomes."),
            "d": (True, "Alerting catches business-level regressions."),
        },
    },
    {
        "question_id": "d4o-vector-store-monitor",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Retrieval quality is slipping and you suspect the vector index. Place the "
            "steps in the correct order."
        ),
        "scenario_constraint": "Monitor index health before re-indexing blindly.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Track retrieval relevance and query latency in CloudWatch."),
            ("b", "Spot the relevance drop while latency stays flat."),
            ("c", "Inspect index freshness and staleness as the suspect."),
            ("d", "Re-index the stale segments and confirm relevance recovers."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You monitor relevance and latency, spot the relevance drop, inspect "
            "freshness, then re-index and confirm recovery."
        ),
        "rationales": {
            "a": (True, "Monitoring surfaces the relevance slip."),
            "b": (True, "Isolating relevance from latency narrows the cause."),
            "c": (True, "Freshness is the likely suspect to inspect."),
            "d": (True, "Re-indexing and confirming closes the loop."),
        },
    },
    {
        "question_id": "d4o-reasoning-path-trace",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "A multi-step agent gave a wrong final answer and you must find where its "
            "reasoning went wrong. Place the steps in the correct order."
        ),
        "scenario_constraint": "Trace the reasoning path step by step.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Open the X-Ray trace for the failing request."),
            ("b", "Walk the reasoning steps in order from the trace."),
            ("c", "Pinpoint the first step that produced a wrong intermediate result."),
            ("d", "Fix that step and re-run to confirm the final answer corrects."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You open the trace, walk the reasoning steps, pinpoint the first wrong "
            "step, then fix it and re-run."
        ),
        "rationales": {
            "a": (True, "The trace contains the reasoning path."),
            "b": (True, "Walking steps in order follows the reasoning."),
            "c": (True, "The first wrong step is the true fault location."),
            "d": (True, "Fixing and re-running confirms the correction."),
        },
    },
    {
        "question_id": "d4o-alarm-tune-noise",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "On-call is being paged by a noisy alarm that often self-resolves. Place "
            "the steps in the correct order."
        ),
        "scenario_constraint": "Reduce alarm noise without hiding real incidents.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Review the alarm history to quantify false pages."),
            ("b", "Adjust the threshold and evaluation period to require sustained breach."),
            ("c", "Observe the alarm over a week to confirm fewer false pages."),
            ("d", "Verify real incidents still trigger the tuned alarm."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You quantify false pages, require a sustained breach, observe the "
            "reduction, then verify real incidents still fire."
        ),
        "rationales": {
            "a": (True, "History quantifies how noisy the alarm is."),
            "b": (True, "A sustained-breach condition cuts transient noise."),
            "c": (True, "Observation confirms the noise dropped."),
            "d": (True, "Verifying real triggers avoids hiding incidents."),
        },
    },
    # === MATCHING: 4.1 cost optimization (12) ===
    {
        "question_id": "d4m-cost-lever-to-problem",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each cost-optimization lever to the problem it best solves. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Pick the lever that targets each specific cost driver.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Repeated similar questions re-invoke the model"),
            ("p2", "Easy requests are sent to an expensive model"),
            ("p3", "Verbose template inflates input tokens"),
            ("p4", "Completions run longer than needed"),
        ],
        "match_responses": [
            ("r1", "Semantic caching"),
            ("r2", "Model cascading by complexity"),
            ("r3", "Prompt compression"),
            ("r4", "Response length limiting"),
            ("r5", "Provisioned throughput"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Caching stops re-invocation, cascading routes easy work cheaply, "
            "compression cuts input tokens, and length limiting caps output tokens."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-cost-service-purpose",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each cost task to the AWS service that performs it. Match each item "
            "to the correct option."
        ),
        "scenario_constraint": "Use the service AWS associates with each cost capability.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Explore spend grouped by feature tag"),
            ("p2", "Alert on an unexpected spend spike"),
            ("p3", "Cache similar results to skip model calls"),
            ("p4", "Commit capacity for steady high volume"),
        ],
        "match_responses": [
            ("r1", "AWS Cost Explorer"),
            ("r2", "AWS Cost Anomaly Detection"),
            ("r3", "Amazon ElastiCache"),
            ("r4", "Amazon Bedrock provisioned throughput"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Cost Explorer explores tagged spend, Cost Anomaly Detection alerts on "
            "spikes, ElastiCache backs semantic caching, and provisioned throughput "
            "commits steady capacity."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-token-component-cost",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each prompt component to the cost lever that reduces its tokens. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Different token sources need different levers.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "A stable shared system prefix re-sent every call"),
            ("p2", "A long growing chat history"),
            ("p3", "An over-long model answer"),
            ("p4", "A bloated instruction block"),
        ],
        "match_responses": [
            ("r1", "Prompt caching of the prefix"),
            ("r2", "Context-window summarization"),
            ("r3", "Max-token response limit"),
            ("r4", "Instruction pruning"),
            ("r5", "Batch inference"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Prefix caching reuses a stable prefix, summarization trims history, a "
            "max-token limit caps answers, and pruning shrinks instructions."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-pricing-mode-workload",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each workload shape to the most cost-effective pricing mode. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Match demand pattern to the cheapest pricing mode.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Spiky, unpredictable low volume"),
            ("p2", "Steady high sustained volume above break-even"),
            ("p3", "Large latency-tolerant offline job"),
        ],
        "match_responses": [
            ("r1", "On-demand invocation"),
            ("r2", "Provisioned throughput"),
            ("r3", "Batch inference"),
            ("r4", "Edge caching"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "On-demand suits spiky low volume, provisioned throughput wins above "
            "break-even, and batch inference is cheapest for latency-tolerant jobs."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-cache-layer-use",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each caching strategy to the situation it fits. Match each item to "
            "the correct option."
        ),
        "scenario_constraint": "Each caching style targets a different repeat pattern.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Exact-duplicate requests from a buggy client"),
            ("p2", "Paraphrased questions with the same intent"),
            ("p3", "A stable prompt prefix reused across calls"),
        ],
        "match_responses": [
            ("r1", "Result fingerprinting"),
            ("r2", "Semantic caching"),
            ("r3", "Prompt caching"),
            ("r4", "Provisioned throughput"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Fingerprinting catches exact duplicates, semantic caching catches "
            "paraphrases, and prompt caching reuses a stable prefix."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-cost-metric-meaning",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each cost signal to what it tells you. Match each item to the " "correct option."
        ),
        "scenario_constraint": "Read each cost signal for its actual meaning.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Rising average tokens per request"),
            ("p2", "Spend grouped by cost-allocation tag"),
            ("p3", "A sudden deviation from the cost baseline"),
        ],
        "match_responses": [
            ("r1", "Prompts or outputs are growing"),
            ("r2", "Which feature drives spend"),
            ("r3", "A possible cost anomaly to investigate"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Rising tokens signal growing prompts or outputs, tag-grouped spend "
            "attributes cost to features, and a baseline deviation flags an anomaly."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-cascade-tier-request",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each request type to the cascade tier that should handle it. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Route by complexity to the cheapest capable tier.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "A simple FAQ lookup"),
            ("p2", "A low-confidence ambiguous query"),
            ("p3", "A complex multi-step reasoning task"),
        ],
        "match_responses": [
            ("r1", "Small cheap model"),
            ("r2", "Escalation to a mid-tier model"),
            ("r3", "Largest capable model"),
            ("r4", "No model call at all"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "FAQs go to the cheap tier, ambiguous queries escalate to mid-tier, and "
            "complex reasoning needs the largest capable model."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-cost-tag-dimension",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each attribution question to the tag dimension that answers it. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Tag by the dimension each question asks about.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Which feature costs the most?"),
            ("p2", "Which environment is spending?"),
            ("p3", "Which team owns the spend?"),
        ],
        "match_responses": [
            ("r1", "Feature tag"),
            ("r2", "Environment tag"),
            ("r3", "Team or cost-center tag"),
            ("r4", "Region tag"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Feature tags attribute to features, environment tags separate stages, "
            "and team tags map spend to cost centers."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-saving-vs-tradeoff",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each cost lever to its main tradeoff risk. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Every saving carries a specific risk to watch.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Aggressive prompt compression"),
            ("p2", "Low max-token limit"),
            ("p3", "Routing everything to the cheapest model"),
        ],
        "match_responses": [
            ("r1", "Lost instructions degrade quality"),
            ("r2", "Answers get truncated"),
            ("r3", "Hard tasks exceed the cheap model's ability"),
            ("r4", "Higher latency"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Over-compression drops needed instructions, a tight limit truncates "
            "answers, and cheap-only routing fails on hard tasks."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-cost-term-definition",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each cost concept to its definition. Match each item to the correct " "option."
        ),
        "scenario_constraint": "Match cost terms to their precise meaning.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Break-even utilization"),
            ("p2", "Token estimation"),
            ("p3", "Cost attribution"),
        ],
        "match_responses": [
            ("r1", "Usage where provisioned beats on-demand"),
            ("r2", "Projecting tokens per request from samples"),
            ("r3", "Assigning spend to features or teams"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Break-even is where provisioned wins, token estimation projects per-"
            "request tokens, and attribution assigns spend to owners."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-batch-vs-realtime",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each job to whether it belongs in batch or real time for cost. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Latency tolerance decides batch versus real time.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Nightly report generation"),
            ("p2", "Interactive chat reply"),
            ("p3", "Bulk re-scoring of a backlog"),
        ],
        "match_responses": [
            ("r1", "Batch inference"),
            ("r2", "Real-time invocation"),
            ("r3", "Batch inference "),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Nightly reports and backlog re-scoring tolerate latency so they batch, "
            "while an interactive reply must run in real time."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-cost-anomaly-cause",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Match each observed cost symptom to its likely root cause. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Map the symptom to its most likely driver.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Call count doubled overnight"),
            ("p2", "Average output tokens jumped"),
            ("p3", "Spend shifted to a pricier model"),
        ],
        "match_responses": [
            ("r1", "A client retry loop"),
            ("r2", "A removed response length limit"),
            ("r3", "A cascade misroute to the large model"),
            ("r4", "A dropped cache layer"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Doubled calls suggest a retry loop, longer outputs suggest a lost length "
            "limit, and a pricier-model shift suggests a cascade misroute."
        ),
        "rationales": {},
    },
    # === MATCHING: 4.2 performance (12) ===
    {
        "question_id": "d4m-perf-technique-problem",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each performance technique to the problem it solves. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Each technique targets a distinct latency problem.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Users wait with a blank screen during generation"),
            ("p2", "Independent sub-calls run one after another"),
            ("p3", "An expensive result is recomputed for everyone"),
            ("p4", "The vector query scans too many candidates"),
        ],
        "match_responses": [
            ("r1", "Response streaming"),
            ("r2", "Parallel requests"),
            ("r3", "Pre-computation"),
            ("r4", "Vector query optimization"),
            ("r5", "Prompt compression"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Streaming fixes the blank wait, parallelism fixes serial sub-calls, pre-"
            "computation fixes repeated work, and query optimization fixes bloated "
            "scans."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-latency-metric-meaning",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each latency metric to what it measures. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Each percentile and timing answers a different question.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Time-to-first-token"),
            ("p2", "p50 latency"),
            ("p3", "p99 latency"),
        ],
        "match_responses": [
            ("r1", "Perceived responsiveness"),
            ("r2", "Typical request experience"),
            ("r3", "Worst-case tail experience"),
            ("r4", "Total token throughput"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Time-to-first-token reflects perceived responsiveness, p50 the typical "
            "case, and p99 the worst-case tail."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-param-effect",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each decoding parameter to its primary effect. Match each item to "
            "the correct option."
        ),
        "scenario_constraint": "Each sampling parameter controls a different behavior.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Temperature"),
            ("p2", "Max tokens"),
            ("p3", "Top-p"),
        ],
        "match_responses": [
            ("r1", "Randomness of the output"),
            ("r2", "Upper bound on output length"),
            ("r3", "Nucleus of candidate tokens considered"),
            ("r4", "Number of parallel requests"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Temperature controls randomness, max tokens caps length, and top-p sets "
            "the nucleus of candidate tokens."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-bottleneck-fix",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each bottleneck stage to the fix that targets it. Match each item "
            "to the correct option."
        ),
        "scenario_constraint": "Optimize the stage that is actually slow.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Retrieval dominates latency"),
            ("p2", "Model generation is slow"),
            ("p3", "Idle endpoint cold starts on surge"),
        ],
        "match_responses": [
            ("r1", "Index and query tuning"),
            ("r2", "Latency-optimized Bedrock model"),
            ("r3", "Pre-warmed capacity"),
            ("r4", "Longer prompts"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Index tuning speeds retrieval, a latency-optimized model speeds "
            "generation, and pre-warming avoids cold-start spikes."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-throughput-vs-latency",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each goal to the approach that serves it. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Throughput and latency call for opposite approaches.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Lowest per-request latency"),
            ("p2", "Maximum records processed per hour"),
            ("p3", "Fastest first visible token"),
        ],
        "match_responses": [
            ("r1", "Real-time single invocation"),
            ("r2", "Batch inference"),
            ("r3", "Response streaming"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Real-time invocation minimizes per-request latency, batch inference "
            "maximizes throughput, and streaming speeds the first token."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-scaling-signal",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each scaling observation to the correct action. Match each item to "
            "the correct option."
        ),
        "scenario_constraint": "Scale in the direction the signal indicates.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Queue time rising under steady load"),
            ("p2", "Throughput flat despite more concurrency"),
            ("p3", "Endpoint idle most of the night"),
        ],
        "match_responses": [
            ("r1", "Increase concurrency and capacity"),
            ("r2", "Stop adding concurrency at the knee"),
            ("r3", "Scale down off-peak capacity"),
            ("r4", "Disable auto scaling"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Rising queue time calls for more capacity, flat throughput means you hit "
            "the knee, and idle nights call for scaling down."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-perf-service-role",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each performance task to the AWS capability that supports it. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Use the AWS feature AWS associates with each task.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Scale an inference endpoint to demand"),
            ("p2", "Trace per-stage latency"),
            ("p3", "Stream tokens to the client"),
        ],
        "match_responses": [
            ("r1", "SageMaker endpoint auto scaling"),
            ("r2", "AWS X-Ray"),
            ("r3", "Bedrock streaming API"),
            ("r4", "Amazon Macie"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Endpoint auto scaling matches demand, X-Ray traces per-stage latency, "
            "and the Bedrock streaming API streams tokens."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-hybrid-component-role",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each hybrid-search component to its role. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Each retrieval component plays a distinct role.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Vector search branch"),
            ("p2", "Keyword search branch"),
            ("p3", "Reranker"),
        ],
        "match_responses": [
            ("r1", "Semantic similarity matches"),
            ("r2", "Exact-term matches"),
            ("r3", "Reordering merged results by relevance"),
            ("r4", "Token compression"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "The vector branch finds semantic matches, the keyword branch finds exact "
            "terms, and the reranker reorders the merged set."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-perceived-vs-real",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each symptom to whether it is perceived or actual latency. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Distinguish perceived latency from real total time.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Blank screen before any output"),
            ("p2", "Total generation time too long"),
            ("p3", "Users feel it is fast once text starts"),
        ],
        "match_responses": [
            ("r1", "Perceived latency problem"),
            ("r2", "Actual latency problem"),
            ("r3", "Perceived latency improved"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A blank wait is a perceived-latency problem, long total time is an actual "
            "problem, and early text improves perceived latency."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-tail-strategy",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each tail-latency strategy to its mechanism. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Each tail strategy works by a different mechanism.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Timeout plus retry"),
            ("p2", "Hedged request"),
            ("p3", "Concurrency cap"),
        ],
        "match_responses": [
            ("r1", "Abandon and re-issue a slow call"),
            ("r2", "Send a duplicate and take the first response"),
            ("r3", "Prevent overload-induced tail latency"),
            ("r4", "Lower the temperature"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Timeout-and-retry re-issues a slow call, a hedged request races a "
            "duplicate, and a concurrency cap prevents overload tails."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-benchmark-term",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each benchmarking concept to its definition. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Match benchmarking terms to their meaning.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Fixed workload"),
            ("p2", "Baseline run"),
            ("p3", "A/B comparison"),
        ],
        "match_responses": [
            ("r1", "The same prompts used across configs"),
            ("r2", "The current config's reference numbers"),
            ("r3", "Side-by-side evaluation of two configs"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A fixed workload keeps prompts constant, the baseline is the reference, "
            "and A/B compares two configs side by side."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-quality-floor-guard",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Match each speed optimization to the quality risk it must guard against. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Speed changes must not breach the quality floor.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Switching to a faster, smaller model"),
            ("p2", "Narrowing the retrieval candidate set"),
            ("p3", "Raising temperature for variety"),
        ],
        "match_responses": [
            ("r1", "Answer quality may drop"),
            ("r2", "Recall of relevant docs may fall"),
            ("r3", "Outputs may become less consistent"),
            ("r4", "Costs may rise"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A smaller model risks quality, a narrower candidate set risks recall, and "
            "higher temperature risks consistency."
        ),
        "rationales": {},
    },
    # === MATCHING: 4.3 monitoring (11) ===
    {
        "question_id": "d4m-metric-reveals",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each monitoring metric to what it reveals. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Each metric exposes a different aspect of health.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Hallucination rate"),
            ("p2", "Token usage"),
            ("p3", "p99 latency"),
            ("p4", "Tool-call count per request"),
        ],
        "match_responses": [
            ("r1", "Output trustworthiness"),
            ("r2", "Cost and prompt growth"),
            ("r3", "Worst-case responsiveness"),
            ("r4", "Possible agent looping"),
            ("r5", "Vector index size"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Hallucination rate reveals trustworthiness, token usage reveals cost and "
            "growth, p99 reveals tail responsiveness, and tool-call count reveals "
            "looping."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-monitor-feature-purpose",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each AWS monitoring feature to its purpose. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Each feature serves a distinct monitoring purpose.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "AWS X-Ray"),
            ("p2", "CloudWatch Synthetics canary"),
            ("p3", "Bedrock Model Invocation Logging"),
            ("p4", "CloudWatch alarm"),
        ],
        "match_responses": [
            ("r1", "Distributed per-stage request tracing"),
            ("r2", "Proactive synthetic probing of the endpoint"),
            ("r3", "Auditable record of model inputs and outputs"),
            ("r4", "Threshold-based alerting on a metric"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "X-Ray traces requests, Synthetics probes proactively, invocation logging "
            "records inputs and outputs, and an alarm alerts on thresholds."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-incident-step-goal",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each incident-response action to its immediate goal. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Restore first, then diagnose and prevent.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Roll back the bad deployment"),
            ("p2", "Open the X-Ray trace of a failure"),
            ("p3", "Add a regression test"),
        ],
        "match_responses": [
            ("r1", "Restore service quickly"),
            ("r2", "Diagnose the root cause"),
            ("r3", "Prevent recurrence"),
            ("r4", "Reduce cost"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Rollback restores service, the trace diagnoses the cause, and a "
            "regression test prevents recurrence."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-telemetry-safe-field",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each field to whether it is safe to log or must be redacted. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Log identifiers, never sensitive content.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Correlation ID"),
            ("p2", "Raw private prompt text"),
            ("p3", "Request latency"),
            ("p4", "User PII in the payload"),
        ],
        "match_responses": [
            ("r1", "Safe to log"),
            ("r2", "Must be redacted"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r1", "p4": "r2"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Correlation IDs and latency are safe operational fields, while private "
            "prompt text and user PII must be redacted."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-alarm-signal-action",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each alarm signal to the appropriate first response. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Respond to each alarm by its nature.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Error rate spiked right after a deploy"),
            ("p2", "Hallucination rate drifting up slowly"),
            ("p3", "Canary failing on the critical path"),
        ],
        "match_responses": [
            ("r1", "Roll back the deployment"),
            ("r2", "Investigate drift before changing the model"),
            ("r3", "Treat as a likely outage and page on-call"),
            ("r4", "Ignore as noise"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A post-deploy spike warrants rollback, slow drift warrants investigation, "
            "and a failing canary signals a likely outage."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-dashboard-audience",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each dashboard view to its intended audience. Match each item to "
            "the correct option."
        ),
        "scenario_constraint": "Tailor each view to who consumes it.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Per-stage latency traces"),
            ("p2", "Monthly cost by feature"),
            ("p3", "Deflection-rate business metric"),
        ],
        "match_responses": [
            ("r1", "On-call engineers"),
            ("r2", "Finance"),
            ("r3", "Product leadership"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Latency traces serve engineers, cost-by-feature serves finance, and the "
            "deflection metric serves product leadership."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-anomaly-vs-static",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each alerting approach to when it fits best. Match each item to the "
            "correct option."
        ),
        "scenario_constraint": "Choose static or anomaly-based alerting by the signal.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "A hard contractual latency limit"),
            ("p2", "Token usage with daily and weekly seasonality"),
            ("p3", "A metric with an unknown normal range"),
        ],
        "match_responses": [
            ("r1", "Static threshold alarm"),
            ("r2", "Anomaly detection"),
            ("r3", "Anomaly detection "),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A fixed limit suits a static threshold, while seasonal or unknown-range "
            "metrics suit anomaly detection that learns a baseline."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-trace-artifact-use",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each observability artifact to how you use it in debugging. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Each artifact plays a specific debugging role.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Correlation ID"),
            ("p2", "X-Ray subsegment"),
            ("p3", "Invocation log entry"),
        ],
        "match_responses": [
            ("r1", "Find the exact request across systems"),
            ("r2", "See one stage's timing and status"),
            ("r3", "Inspect the actual model input and output"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A correlation ID locates the request, a subsegment shows one stage, and "
            "an invocation log entry shows the model's input and output."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-quality-signal-source",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each quality signal to its source. Match each item to the correct " "option."
        ),
        "scenario_constraint": "Each quality signal comes from a specific source.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Hallucination rate"),
            ("p2", "Output diff flag"),
            ("p3", "Reasoning-path fault"),
        ],
        "match_responses": [
            ("r1", "Scoring against a golden dataset"),
            ("r2", "Comparing new outputs to a baseline"),
            ("r3", "Walking a traced chain of steps"),
            ("r4", "A cost report"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Hallucination rate comes from golden-dataset scoring, output diffs from "
            "baseline comparison, and reasoning faults from walking the trace."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-rollback-readiness",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each deployment practice to the incident capability it enables. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Preparation determines how fast you can respond.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Keeping the last known-good build"),
            ("p2", "Emitting correlation IDs on every request"),
            ("p3", "Maintaining a golden dataset"),
        ],
        "match_responses": [
            ("r1", "Fast rollback"),
            ("r2", "Fast root-cause tracing"),
            ("r3", "Pre-release regression gating"),
            ("r4", "Lower token cost"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A known-good build enables rollback, correlation IDs enable tracing, and "
            "a golden dataset enables regression gating."
        ),
        "rationales": {},
    },
    {
        "question_id": "d4m-diagnose-before-fix",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Match each observation to the correct next step under a diagnose-before-"
            "remediate discipline. Match each item to the correct option."
        ),
        "scenario_constraint": "Confirm the cause before changing anything.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Alarm fired but cause unknown"),
            ("p2", "Trace points to one faulty stage"),
            ("p3", "Fix applied in staging"),
        ],
        "match_responses": [
            ("r1", "Gather traces and logs first"),
            ("r2", "Reproduce and confirm the root cause"),
            ("r3", "Validate recovery before closing"),
            ("r4", "Delete the metric"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "An unexplained alarm needs evidence first, a suspect stage needs "
            "confirmation, and an applied fix needs recovery validation."
        ),
        "rationales": {},
    },
]


def question_count() -> int:
    """Return the number of authored Domain 4 ordering/matching questions."""
    return len(QUESTIONS)
