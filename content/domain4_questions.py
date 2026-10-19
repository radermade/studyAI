"""Authored Domain 4 (AIP-C01) scenario questions with answers and explanations.

Original scenario-style questions grounded in the AWS exam guide. Domain 4 is
Operational Efficiency and Optimization: cost optimization (AIP-4.1), performance
optimization (AIP-4.2), and monitoring systems (AIP-4.3). No proprietary exam
content is reproduced.
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    # ----- AIP-4.1 cost optimization and resource efficiency ---------------
    {
        "question_id": "d4-cascading-mixed-traffic",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A Bedrock chat application serves a mix of simple FAQ lookups and "
            "complex analytical questions. Spend is three times budget and most "
            "traffic is the simple kind. Which change reduces cost the MOST "
            "while keeping quality on hard questions?"
        ),
        "scenario_constraint": "Mostly simple traffic; protect quality on the hard minority.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Add a lightweight classifier that routes easy queries to a small model and hard ones to the large model.",
            ),
            ("b", "Send every request to the largest model so quality is never at risk."),
            ("c", "Buy provisioned throughput sized to the busiest minute of the day."),
            ("d", "Cache every response and replay it for all future requests."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Model cascading sends cheap traffic to a cheap model and reserves "
            "the expensive model for the hard minority, cutting cost without "
            "losing quality where it matters. Using the largest model everywhere "
            "raises cost, peak-sized provisioning over-pays, and caching unique "
            "analytical answers returns wrong results."
        ),
        "rationales": {
            "a": (True, "Routing by difficulty spends on the large model only when needed."),
            "b": (False, "Large-model-everywhere is the cost problem, not the fix."),
            "c": (False, "Peak-sized provisioned throughput pays for idle capacity."),
            "d": (False, "Caching unique analytical answers serves wrong responses."),
        },
    },
    {
        "question_id": "d4-provisioned-breakeven",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A steady production workload runs near-constant high throughput on "
            "Bedrock on-demand pricing, and finance wants lower, predictable "
            "cost. Usage is flat around the clock. What is the MOST cost-"
            "effective change?"
        ),
        "scenario_constraint": "Flat, high, predictable utilization all day.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Move the model to provisioned throughput sized to the sustained load."),
            ("b", "Stay on-demand because per-request pricing is always cheapest."),
            ("c", "Provision far above peak so there is never any throttling."),
            ("d", "Rotate the request across several models each hour to find a lower rate."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "At flat high utilization, provisioned throughput sized to the load "
            "is cheaper and more predictable than per-request on-demand. On-demand "
            "is not always cheapest at that volume, over-provisioning wastes "
            "money, and hourly model rotation adds churn without a cost basis."
        ),
        "rationales": {
            "a": (True, "Provisioned throughput beats on-demand at steady high utilization."),
            "b": (False, "On-demand loses its edge once utilization is flat and high."),
            "c": (False, "Provisioning above peak reintroduces the waste you are cutting."),
            "d": (False, "Hourly rotation churns the system with no cost rationale."),
        },
    },
    {
        "question_id": "d4-batch-nightly-reports",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A reporting pipeline summarizes documents overnight with no "
            "interactive user waiting, yet it runs on real-time on-demand "
            "inference. Which change lowers unit cost with the LEAST downside?"
        ),
        "scenario_constraint": "No real-time requirement; results needed by morning.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Move the workload to batch or asynchronous inference."),
            ("b", "Add more real-time replicas to finish faster."),
            ("c", "Keep an always-warm endpoint sized for peak interactive load."),
            ("d", "Invoke each document twice and keep the better summary."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Batch or asynchronous inference suits work with no latency deadline "
            "and lowers unit cost. More replicas and always-warm peak capacity "
            "add cost, and double-invoking doubles it."
        ),
        "rationales": {
            "a": (True, "Batch/async fits non-interactive work at lower unit cost."),
            "b": (False, "More real-time replicas increase cost, not reduce it."),
            "c": (False, "An always-warm peak endpoint pays for idle time."),
            "d": (False, "Invoking twice per document doubles cost."),
        },
    },
    {
        "question_id": "d4-token-reduction-context",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A RAG pipeline pastes an entire manual into every prompt, and token "
            "charges dominate the bill even though answers depend on only a few "
            "sections. What reduces cost MOST without hurting accuracy?"
        ),
        "scenario_constraint": "Most of the stuffed context is irrelevant to the answer.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Retrieve and include only the passages relevant to each query."),
            ("b", "Raise the model's max output tokens so larger prompts fit."),
            ("c", "Always send the whole manual to be safe."),
            ("d", "Switch to a model with a bigger context window and keep stuffing it."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Including only relevant retrieved passages cuts input tokens, which "
            "lowers cost and latency without hurting accuracy. Raising output "
            "tokens, sending the whole manual, or buying a bigger window all keep "
            "or grow the wasteful token volume."
        ),
        "rationales": {
            "a": (True, "Relevant-only context removes the wasted tokens driving cost."),
            "b": (False, "Output-token limits do not address oversized input context."),
            "c": (False, "Sending the whole manual is the cost problem."),
            "d": (False, "A bigger window just lets you waste more tokens."),
        },
    },
    {
        "question_id": "d4-cache-deterministic",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Analytics show that a quarter of traffic is the same handful of "
            "deterministic FAQ prompts answered identically each time. Which "
            "optimization safely cuts cost and latency for that slice?"
        ),
        "scenario_constraint": "Repeated identical prompts with stable answers.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Cache responses for the identical deterministic prompts and serve from cache."),
            ("b", "Cache every prompt indefinitely regardless of how variable it is."),
            ("c", "Move the FAQ path to a larger model for faster answers."),
            ("d", "Remove the FAQ feature to shed the load."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Caching only the identical, deterministic prompts cuts cost and "
            "latency while preserving correctness. Caching variable prompts "
            "returns stale answers, a larger model raises cost, and removing the "
            "feature discards its value."
        ),
        "rationales": {
            "a": (True, "Caching deterministic repeats is safe and cheap."),
            "b": (False, "Caching variable prompts yields stale or wrong answers."),
            "c": (False, "A larger model increases cost for a cacheable path."),
            "d": (False, "Removing the feature abandons the use case."),
        },
    },
    {
        "question_id": "d4-cost-attribution-tags",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "GenAI spend is rising but leadership cannot tell which feature or "
            "team drives it, so they cannot target cuts. What should be "
            "established FIRST?"
        ),
        "scenario_constraint": "Cannot attribute spend to features or teams.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Tag resources and track usage so cost is attributable per feature and team."),
            ("b", "Cut the overall budget and hope usage falls into line."),
            ("c", "Optimize a component at random and watch the total bill."),
            ("d", "Assume the largest model is the only driver and swap it."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Cost attribution through tagging and usage tracking shows where "
            "spend goes so optimization can target real drivers. Blanket cuts, "
            "random optimization, and assumptions are not evidence-based."
        ),
        "rationales": {
            "a": (True, "Attribution reveals the real drivers to target."),
            "b": (False, "A blanket cut neither finds nor fixes the driver."),
            "c": (False, "Random optimization is guesswork."),
            "d": (False, "Assuming the driver skips the measurement step."),
        },
    },
    {
        "question_id": "d4-rightsize-sagemaker",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A self-hosted model runs on a large GPU SageMaker endpoint that sits "
            "under 15% utilization most of the day. The team must cut cost while "
            "meeting the same modest latency target. What is the BEST first move?"
        ),
        "scenario_constraint": "Chronically low utilization against a modest latency target.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Right-size to a smaller instance type and enable autoscaling to the real load."),
            ("b", "Keep the instance but double its size for headroom."),
            ("c", "Add a second identical endpoint behind a load balancer."),
            ("d", "Leave it running continuously to avoid any cold starts ever."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Right-sizing to actual utilization plus autoscaling removes the idle "
            "waste while still meeting a modest latency target. Doubling size, "
            "adding a second endpoint, or pinning it always-on all increase cost "
            "against an already underused resource."
        ),
        "rationales": {
            "a": (True, "Right-sizing plus autoscaling matches cost to real load."),
            "b": (False, "Doubling size worsens the underutilization problem."),
            "c": (False, "A second endpoint multiplies idle cost."),
            "d": (False, "Always-on pays for the idle time you are trying to cut."),
        },
    },
    {
        "question_id": "d4-cross-region-cost-latency",
        "objective_ids": ["AIP-4.1", "AIP-4.2"],
        "prompt": (
            "A workload occasionally throttles in its primary Region at peak. The "
            "team wants to absorb the overflow without permanently paying for "
            "extra reserved capacity. Which approach fits BEST?"
        ),
        "scenario_constraint": "Absorb occasional peaks without standing reserved capacity.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Use cross-region inference to spread overflow demand across Regions on demand."),
            ("b", "Permanently provision double capacity in the primary Region."),
            ("c", "Drop requests that would exceed the current Region's quota."),
            ("d", "Retry throttled calls in a tight loop until they succeed."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Cross-region inference absorbs occasional overflow without a standing "
            "reserved commitment. Permanent double capacity pays for rare peaks, "
            "dropping requests fails users, and tight-loop retries worsen "
            "throttling."
        ),
        "rationales": {
            "a": (True, "Cross-region inference handles overflow on demand, not reserved."),
            "b": (False, "Permanent double capacity pays constantly for rare peaks."),
            "c": (False, "Dropping requests sacrifices availability."),
            "d": (False, "Tight-loop retries amplify the throttling."),
        },
    },
    {
        "question_id": "d4-smaller-model-task",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A pipeline uses a flagship model for a narrow intent-classification "
            "step that a much smaller model handles with equal accuracy in "
            "testing. The step dominates cost. What should the team do?"
        ),
        "scenario_constraint": "Narrow task; a smaller model matches accuracy in testing.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Move the classification step to the smaller model that meets the accuracy bar."),
            ("b", "Keep the flagship model everywhere for consistency."),
            ("c", "Run both models and compare on every request."),
            ("d", "Remove the classification step to save calls."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A smaller model that clears the accuracy bar on a narrow task cuts "
            "cost with no quality loss. Keeping the flagship wastes money, running "
            "both doubles cost, and removing the step changes behavior."
        ),
        "rationales": {
            "a": (True, "Right-sized model holds accuracy and cuts the dominant cost."),
            "b": (False, "Flagship-everywhere is the cost being targeted."),
            "c": (False, "Running both models doubles the step's cost."),
            "d": (False, "Deleting the step removes needed functionality."),
        },
    },
    {
        "question_id": "d4-prompt-caching-shared-prefix",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "Every request begins with the same long system preamble and tool "
            "definitions, and only a short user turn varies. Token cost on the "
            "repeated prefix is high. Which capability reduces that cost MOST "
            "directly?"
        ),
        "scenario_constraint": "A large static prefix repeats on every call.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Prompt caching of the shared static prefix so it is not reprocessed each call."),
            ("b", "Lowering the temperature to make responses shorter."),
            ("c", "Switching to a model with a smaller context window."),
            ("d", "Removing the tool definitions the agent relies on."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Prompt caching of a stable prefix avoids reprocessing the same tokens "
            "on every call, cutting cost directly. Temperature affects randomness "
            "not prefix cost, a smaller window does not reduce the repeated prefix, "
            "and removing tool definitions breaks the agent."
        ),
        "rationales": {
            "a": (True, "Caching the static prefix stops paying for it every call."),
            "b": (False, "Temperature does not change input-prefix token cost."),
            "c": (False, "A smaller window does not remove the repeated prefix."),
            "d": (False, "Dropping tool definitions breaks required functionality."),
        },
    },
    {
        "question_id": "d4-cost-levers-select-two",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A team must cut the per-request cost of a RAG assistant that answers "
            "many repeated questions over a bloated context, without changing the "
            "answers users get. Which TWO levers apply? (Select TWO.)"
        ),
        "scenario_constraint": "Repeated questions plus oversized context; answers must not change.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Cache responses for identical deterministic queries."),
            ("b", "Trim retrieved context to only the relevant passages."),
            ("c", "Raise the sampling temperature on every request."),
            ("d", "Fine-tune a new model nightly on the whole corpus."),
            ("e", "Add a second large model to vote on every answer."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Caching identical queries and trimming irrelevant context both lower "
            "cost without changing correct answers. Higher temperature changes "
            "outputs, nightly fine-tuning is expensive and lagging, and a second "
            "voting model raises cost."
        ),
        "rationales": {
            "a": (True, "Caching deterministic repeats avoids recomputation."),
            "b": (True, "Trimming context removes wasted input tokens."),
            "c": (False, "Raising temperature changes the answers users get."),
            "d": (False, "Nightly fine-tuning adds large cost and lag."),
            "e": (False, "A second voting model increases per-request cost."),
        },
    },
    {
        "question_id": "d4-ondemand-spiky-low-volume",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "An internal tool is used sporadically a few times an hour with long "
            "idle gaps. A proposal is to buy provisioned throughput for "
            "'predictable cost.' What is the MOST cost-effective choice?"
        ),
        "scenario_constraint": "Sporadic, low-volume usage with long idle gaps.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Stay on on-demand pricing so idle time costs nothing."),
            ("b", "Buy provisioned throughput sized to the busiest hour."),
            ("c", "Buy provisioned throughput sized to the daily average."),
            ("d", "Keep a dedicated warm endpoint for instant responses."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "For sporadic low-volume use, on-demand avoids paying for the long "
            "idle gaps, so it is cheaper than any provisioned commitment. "
            "Provisioned options and a warm endpoint all pay during idle time."
        ),
        "rationales": {
            "a": (True, "On-demand costs nothing while idle, fitting sporadic use."),
            "b": (False, "Peak-sized provisioning pays through the long idle gaps."),
            "c": (False, "Even average-sized provisioning pays during idle time."),
            "d": (False, "A warm endpoint pays continuously for rare use."),
        },
    },
    {
        "question_id": "d4-output-token-cap",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A classification endpoint should return a single label, but it is "
            "billed for long explanations the model adds unprompted. What change "
            "cuts output-token cost with no accuracy impact?"
        ),
        "scenario_constraint": "Only a short label is needed; model emits verbose output.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Constrain the output to the label and set a small max-output-tokens limit."),
            ("b", "Increase max-output-tokens so responses are never cut off."),
            ("c", "Switch to the largest available model."),
            ("d", "Add more few-shot examples to every prompt."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Constraining output to the label and capping output tokens removes "
            "the billed verbosity without affecting the label's accuracy. Raising "
            "the limit, using a larger model, or adding examples all increase "
            "tokens or cost."
        ),
        "rationales": {
            "a": (True, "A label-only constraint and token cap cut wasted output."),
            "b": (False, "Raising the limit permits even more wasted output."),
            "c": (False, "A larger model costs more for a trivial task."),
            "d": (False, "More few-shot examples add input tokens."),
        },
    },
    {
        "question_id": "d4-distillation-tradeoff",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A high-volume, narrow task runs on an expensive general model. The "
            "team can distill a small task-specific model that matches quality in "
            "evaluation but needs upfront effort. The task will run for a year at "
            "high volume. What is the MOST defensible decision?"
        ),
        "scenario_constraint": "Sustained high volume justifies upfront optimization effort.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Distill the small model since sustained volume amortizes the upfront cost."),
            ("b", "Keep the general model because any custom model is risky."),
            ("c", "Distill only if the task runs for a single day."),
            ("d", "Choose based on which model has the larger context window."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "At sustained high volume for a year, the per-request savings from a "
            "distilled model that matches quality outweigh the one-time effort. "
            "Avoiding it on principle ignores the amortization, a single day would "
            "not amortize it, and context window is irrelevant to this task."
        ),
        "rationales": {
            "a": (True, "High sustained volume amortizes the upfront distillation cost."),
            "b": (False, "Blanket risk-aversion ignores the measured quality match."),
            "c": (False, "A single day would not amortize the effort."),
            "d": (False, "Context window does not drive this cost decision."),
        },
    },
    {
        "question_id": "d4-avoid-overprovision-trap",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "To eliminate rare throttling, an engineer proposes provisioning for "
            "the single highest spike ever observed. Traffic is otherwise "
            "moderate. What is the MOST cost-aware response?"
        ),
        "scenario_constraint": "One rare spike; otherwise moderate steady traffic.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Provision for the sustained load and absorb rare spikes with on-demand or cross-region overflow.",
            ),
            ("b", "Provision for the all-time peak so throttling is impossible."),
            ("c", "Disable throttling limits entirely."),
            ("d", "Add a fixed delay to every request to flatten spikes."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Provisioning for the sustained load and handling rare spikes with "
            "on-demand or cross-region overflow avoids paying all year for a "
            "one-off peak. Peak provisioning wastes money, disabling limits risks "
            "overload, and delaying every request harms normal users."
        ),
        "rationales": {
            "a": (True, "Size to sustained load; absorb spikes elastically."),
            "b": (False, "All-time-peak provisioning pays constantly for a rare event."),
            "c": (False, "Removing limits invites overload, not savings."),
            "d": (False, "A blanket delay degrades the common case."),
        },
    },
    {
        "question_id": "d4-embedding-reuse",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A pipeline re-embeds the entire document corpus on every ingestion "
            "run even though most documents are unchanged. Embedding cost is a "
            "large share of the bill. What reduces it MOST?"
        ),
        "scenario_constraint": "Most documents are unchanged between runs.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Embed only new or changed documents and reuse existing vectors."),
            ("b", "Re-embed everything but on a cheaper schedule."),
            ("c", "Switch to a higher-dimension embedding model."),
            ("d", "Embed each document twice to improve recall."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Incremental embedding of only changed documents reuses existing "
            "vectors and removes the dominant waste. Re-embedding everything on "
            "any schedule still pays for unchanged docs, higher dimensions cost "
            "more, and double-embedding doubles cost."
        ),
        "rationales": {
            "a": (True, "Incremental embedding skips unchanged documents."),
            "b": (False, "Re-embedding all still pays for unchanged documents."),
            "c": (False, "Higher dimensions raise storage and compute cost."),
            "d": (False, "Embedding twice doubles the embedding bill."),
        },
    },
    {
        "question_id": "d4-cost-vs-quality-floor",
        "objective_ids": ["AIP-4.1", "AIP-4.2"],
        "prompt": (
            "A cost-cutting proposal swaps in a cheaper model and truncates "
            "context aggressively, halving cost but dropping measured accuracy "
            "below the product's committed quality bar. How should the team "
            "proceed?"
        ),
        "scenario_constraint": "Savings breach an explicit quality threshold.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Reject or adjust the change so the quality bar holds, then re-measure cost."),
            ("b", "Ship it because the savings are large."),
            ("c", "Lower the quality bar so the change passes."),
            ("d", "Stop measuring quality so the regression is not visible."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Cost savings never justify falling below a committed quality bar; the "
            "change must be rejected or adjusted and re-measured. Shipping it, "
            "moving the bar, or hiding the regression all trade away required "
            "quality."
        ),
        "rationales": {
            "a": (True, "Preserve the quality floor, then re-evaluate the savings."),
            "b": (False, "Savings do not justify breaching the quality bar."),
            "c": (False, "Lowering the bar defeats its purpose."),
            "d": (False, "Hiding the regression ships worse quality silently."),
        },
    },
    {
        "question_id": "d4-guardrail-cost-order",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "An application pays for an expensive model call and then rejects "
            "about 20% of outputs with a cheap policy check that could run on the "
            "input instead. What change avoids paying for work that gets "
            "discarded?"
        ),
        "scenario_constraint": "A fifth of expensive calls are discarded by a cheap post-check.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Run the cheap input check first and skip the model call when it fails."),
            ("b", "Keep the order but buy provisioned throughput for the model."),
            ("c", "Call the model twice and keep whichever output passes."),
            ("d", "Remove the policy check to stop discarding outputs."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Moving the cheap input check ahead of the expensive model call avoids "
            "paying for calls that will be discarded. Provisioning does not stop "
            "the waste, double-calling worsens it, and removing the check "
            "sacrifices the policy it enforces."
        ),
        "rationales": {
            "a": (True, "Screening input first avoids the discarded expensive calls."),
            "b": (False, "Provisioning the model does not stop wasted calls."),
            "c": (False, "Double-calling increases, not decreases, cost."),
            "d": (False, "Dropping the check abandons the required policy."),
        },
    },
    {
        "question_id": "d4-storage-tier-vectors",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A large archive of rarely queried historical embeddings sits in the "
            "same hot, high-throughput vector tier as active data, inflating "
            "cost. Queries against the archive are rare and latency-tolerant. "
            "What is the MOST cost-effective change?"
        ),
        "scenario_constraint": "Rarely queried, latency-tolerant archival vectors.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Move archival vectors to a lower-cost tier and keep active data hot."),
            ("b", "Keep everything in the hot tier for simplicity."),
            ("c", "Delete the archive outright to save cost."),
            ("d", "Duplicate the archive into a second hot store for resilience."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Tiering rarely queried, latency-tolerant vectors to lower-cost "
            "storage while keeping active data hot matches cost to access "
            "pattern. Keeping all hot is the waste, deleting loses data, and "
            "duplicating into another hot store doubles cost."
        ),
        "rationales": {
            "a": (True, "Tiering by access pattern cuts cost without losing data."),
            "b": (False, "All-hot is the inflated cost being addressed."),
            "c": (False, "Deleting the archive loses potentially needed data."),
            "d": (False, "A second hot copy increases cost."),
        },
    },
    {
        "question_id": "d4-fine-tune-vs-prompt-cost",
        "objective_ids": ["AIP-4.1"],
        "prompt": (
            "A team gets acceptable quality today by sending very long few-shot "
            "prompts on every call, and token cost is high at scale. A one-time "
            "fine-tune could achieve the same quality with short prompts. Volume "
            "is high and stable. What is the MOST cost-effective direction?"
        ),
        "scenario_constraint": "High stable volume; long few-shot prompts drive token cost.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Fine-tune once so inference uses short prompts, amortizing over the volume."),
            ("b", "Keep the long few-shot prompts because fine-tuning has upfront cost."),
            ("c", "Shorten prompts by removing instructions the task needs."),
            ("d", "Raise max output tokens to compensate for shorter prompts."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "At high stable volume, a one-time fine-tune that enables short "
            "prompts amortizes quickly against the saved per-call tokens. "
            "Avoiding it on upfront cost ignores amortization, cutting needed "
            "instructions hurts quality, and raising output tokens adds cost."
        ),
        "rationales": {
            "a": (True, "Fine-tuning once trades upfront cost for lasting per-call savings."),
            "b": (False, "Upfront cost is amortized by the high stable volume."),
            "c": (False, "Removing needed instructions degrades quality."),
            "d": (False, "More output tokens raise cost, not lower it."),
        },
    },
    # ----- AIP-4.2 performance optimization --------------------------------
    {
        "question_id": "d4-streaming-perceived-latency",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Users complain a chat feature feels sluggish because nothing appears "
            "until the whole answer is generated. Total generation time cannot be "
            "reduced much. What improves perceived responsiveness MOST?"
        ),
        "scenario_constraint": "Total time is fixed; improve perceived latency.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Stream tokens to the client as they are generated."),
            ("b", "Buffer the full response and send it once complete."),
            ("c", "Truncate every answer to one sentence."),
            ("d", "Show a longer loading animation."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Streaming surfaces output immediately, greatly improving perceived "
            "latency even when total time is unchanged. Buffering delays all "
            "output, truncation harms quality, and an animation delivers nothing "
            "sooner."
        ),
        "rationales": {
            "a": (True, "Streaming shows partial output right away."),
            "b": (False, "Buffering is exactly the slow behavior."),
            "c": (False, "One-sentence answers sacrifice quality."),
            "d": (False, "An animation does not deliver content sooner."),
        },
    },
    {
        "question_id": "d4-bounded-concurrency-throughput",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A batch job processes items strictly one at a time, leaving model "
            "capacity idle and missing its throughput target. Per-item latency is "
            "already acceptable. What raises throughput safely?"
        ),
        "scenario_constraint": "Serial processing underuses capacity; respect quotas.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Process items with bounded parallelism that stays within service quotas."),
            ("b", "Keep it serial but switch to a larger model."),
            ("c", "Fire unlimited parallel calls with no concurrency cap."),
            ("d", "Reduce the item count to fit the serial rate."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Bounded concurrency within quotas uses idle capacity to raise "
            "throughput without triggering throttling. A larger model does not "
            "fix serial underuse, unbounded parallelism causes throttling, and "
            "cutting items dodges the requirement."
        ),
        "rationales": {
            "a": (True, "Bounded parallelism lifts throughput within quota limits."),
            "b": (False, "A bigger model does not address serial underutilization."),
            "c": (False, "Unbounded parallelism triggers throttling and overload."),
            "d": (False, "Reducing items evades the throughput target."),
        },
    },
    {
        "question_id": "d4-retrieval-latency-bottleneck",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A RAG endpoint's p99 latency is dominated by the vector search step, "
            "not generation, according to traces. What is the MOST targeted fix?"
        ),
        "scenario_constraint": "Traces show retrieval, not generation, is the bottleneck.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Tune the vector index and query (e.g., ANN parameters, filters) to cut retrieval time.",
            ),
            ("b", "Switch to a faster generation model."),
            ("c", "Increase max output tokens."),
            ("d", "Add more few-shot examples to the prompt."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Since traces localize the cost to retrieval, tuning the index and "
            "query is the targeted fix. Changing the generation model, output "
            "tokens, or prompt examples addresses the wrong stage."
        ),
        "rationales": {
            "a": (True, "Optimizing the identified retrieval step targets the real bottleneck."),
            "b": (False, "Generation is not the bottleneck here."),
            "c": (False, "Output tokens do not affect retrieval latency."),
            "d": (False, "More examples add prompt tokens, not retrieval speed."),
        },
    },
    {
        "question_id": "d4-context-trim-latency",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A prompt includes thousands of tokens of mostly irrelevant context, "
            "and latency scales with input size. Accuracy does not depend on most "
            "of it. What reduces latency without hurting accuracy?"
        ),
        "scenario_constraint": "Oversized input context dominates latency.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Trim the context to the relevant passages before sending."),
            ("b", "Lower the temperature to speed up generation."),
            ("c", "Request more output tokens so the model finishes sooner."),
            ("d", "Send the full context but to a bigger-window model."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Trimming to relevant context reduces input tokens and the latency "
            "that scales with them, with no accuracy loss. Temperature does not "
            "change input size, more output tokens add time, and a bigger window "
            "still processes the oversized input."
        ),
        "rationales": {
            "a": (True, "Less input context means lower input-bound latency."),
            "b": (False, "Temperature does not reduce input processing time."),
            "c": (False, "More output tokens increase generation time."),
            "d": (False, "A bigger window still processes the bloated input."),
        },
    },
    {
        "question_id": "d4-autoscale-sagemaker",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A SageMaker real-time endpoint meets latency at average load but "
            "times out during predictable midday surges. The team wants to meet "
            "p99 during surges without paying for peak capacity all day. What "
            "fits BEST?"
        ),
        "scenario_constraint": "Predictable surges; meet p99 without all-day peak cost.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Configure autoscaling that adds instances on the surge signal and scales back after.",
            ),
            ("b", "Permanently provision for the midday peak."),
            ("c", "Lower the latency target so the timeouts count as passing."),
            ("d", "Disable health checks so slow instances keep serving."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Autoscaling to the surge and back meets p99 during peaks while "
            "avoiding all-day peak cost. Permanent peak provisioning overpays, "
            "lowering the target hides the problem, and disabling health checks "
            "keeps bad instances in rotation."
        ),
        "rationales": {
            "a": (True, "Autoscaling matches capacity to the predictable surge."),
            "b": (False, "All-day peak provisioning overpays for a midday surge."),
            "c": (False, "Relaxing the target hides the latency failure."),
            "d": (False, "Disabling health checks serves from unhealthy instances."),
        },
    },
    {
        "question_id": "d4-parallel-tool-calls-agent",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "An agent makes several independent tool calls sequentially, and their "
            "combined latency dominates response time. The calls have no ordering "
            "dependency. What reduces end-to-end latency MOST?"
        ),
        "scenario_constraint": "Independent tool calls run one after another.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Issue the independent tool calls in parallel and await all results."),
            ("b", "Add a retry to each call to make them faster."),
            ("c", "Increase the model's temperature."),
            ("d", "Move the calls into the system prompt as text."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Running independent tool calls in parallel collapses their latency "
            "from a sum toward the slowest single call. Retries add time, "
            "temperature is irrelevant, and inlining calls as text does not "
            "execute them."
        ),
        "rationales": {
            "a": (True, "Parallelizing independent calls cuts combined latency."),
            "b": (False, "Retries add latency, not remove it."),
            "c": (False, "Temperature does not affect tool-call latency."),
            "d": (False, "Describing calls in text does not run them concurrently."),
        },
    },
    {
        "question_id": "d4-speculative-small-model-first",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Most queries are answered correctly by a fast small model, but a "
            "minority need the slow large model. The team wants low average "
            "latency while preserving accuracy on hard queries. Which pattern "
            "fits BEST?"
        ),
        "scenario_constraint": "Fast model handles most; large model needed for a minority.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Try the small model first and escalate to the large model only when confidence is low.",
            ),
            ("b", "Always call the large model for maximum accuracy."),
            ("c", "Always call the small model and accept the misses."),
            ("d", "Call both models for every query and pick randomly."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A small-model-first cascade with escalation on low confidence gives "
            "low average latency while preserving accuracy on the hard minority. "
            "Large-model-always is slow, small-model-always misses, and calling "
            "both everywhere wastes latency and cost."
        ),
        "rationales": {
            "a": (True, "Escalate-on-low-confidence keeps the common path fast."),
            "b": (False, "Large-model-always maximizes latency."),
            "c": (False, "Small-model-always sacrifices accuracy on hard queries."),
            "d": (False, "Calling both every time adds latency and cost."),
        },
    },
    {
        "question_id": "d4-p99-vs-average",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A dashboard shows a healthy average latency, yet users report "
            "frequent slow responses. Which measurement BEST reveals the user-"
            "felt problem?"
        ),
        "scenario_constraint": "Average looks fine but tail is bad.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Track p95/p99 tail latency, not just the average."),
            ("b", "Track only the minimum observed latency."),
            ("c", "Track total request count per day."),
            ("d", "Track the average over a longer window."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Tail percentiles like p95/p99 expose the slow responses users feel "
            "that an average hides. Minimum and request count say nothing about "
            "the tail, and a longer-window average smooths it further."
        ),
        "rationales": {
            "a": (True, "Tail percentiles capture the user-felt slow responses."),
            "b": (False, "Minimum latency ignores the slow tail entirely."),
            "c": (False, "Request count is not a latency measure."),
            "d": (False, "A longer-window average hides the tail more."),
        },
    },
    {
        "question_id": "d4-batch-inference-throughput",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "An embedding job must process millions of documents by a deadline. "
            "Per-document latency is irrelevant; total completion time is what "
            "matters. Which approach maximizes throughput?"
        ),
        "scenario_constraint": "Optimize total completion time, not per-item latency.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Use batch processing with high bounded parallelism within quotas."),
            ("b", "Process documents one at a time to protect per-item latency."),
            ("c", "Use a streaming endpoint sized for a single interactive user."),
            ("d", "Lower the embedding dimension to speed each call and ignore quotas."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Batch processing with high bounded parallelism maximizes aggregate "
            "throughput for a deadline-bound job. Serial processing is slow, a "
            "single-user streaming endpoint underuses capacity, and ignoring "
            "quotas risks throttling."
        ),
        "rationales": {
            "a": (True, "High bounded parallelism maximizes batch throughput."),
            "b": (False, "Serial processing cannot meet a large-volume deadline."),
            "c": (False, "A single-user endpoint wastes available capacity."),
            "d": (False, "Ignoring quotas invites throttling that slows the job."),
        },
    },
    {
        "question_id": "d4-warm-pool-cold-start",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A rarely used self-hosted endpoint has acceptable steady latency but "
            "the first request after idle periods is very slow due to cold "
            "starts, and that first request is user-facing. What addresses the "
            "cold-start latency MOST directly?"
        ),
        "scenario_constraint": "Cold-start latency on the first user-facing request after idle.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Keep a minimum warm capacity (or warm pool) so a ready instance serves the first request.",
            ),
            ("b", "Increase max output tokens to make generation finish sooner."),
            ("c", "Lower temperature to reduce cold-start time."),
            ("d", "Add retries so the slow first request eventually returns."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A minimum warm capacity or warm pool keeps a ready instance so the "
            "first request skips the cold start. Output tokens and temperature do "
            "not affect startup, and retries just repeat the slow path."
        ),
        "rationales": {
            "a": (True, "A warm instance eliminates the first-request cold start."),
            "b": (False, "Output tokens do not affect startup latency."),
            "c": (False, "Temperature is unrelated to cold-start time."),
            "d": (False, "Retrying the slow path does not remove the cold start."),
        },
    },
    {
        "question_id": "d4-perf-levers-select-two",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A user-facing RAG endpoint must lower both perceived latency and "
            "tail latency without reducing answer quality. Which TWO changes "
            "apply? (Select TWO.)"
        ),
        "scenario_constraint": "Improve perceived and tail latency; hold quality.",
        "difficulty": "medium",
        "question_format": "multiple_response",
        "options": [
            ("a", "Stream tokens to the client as they are produced."),
            ("b", "Trim retrieved context to the relevant passages."),
            ("c", "Lower the quality bar to allow a smaller model everywhere."),
            ("d", "Remove retrieval so there is nothing to wait on."),
            ("e", "Add a fixed artificial delay to smooth the dashboard."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Streaming improves perceived latency and trimming context cuts the "
            "input-bound latency, both without lowering quality. Lowering the bar "
            "trades quality, removing retrieval breaks grounding, and an "
            "artificial delay worsens real latency."
        ),
        "rationales": {
            "a": (True, "Streaming improves perceived latency with no quality loss."),
            "b": (True, "Trimming irrelevant context cuts latency without hurting accuracy."),
            "c": (False, "Lowering the quality bar violates the no-quality-loss constraint."),
            "d": (False, "Removing retrieval breaks grounded answers."),
            "e": (False, "An artificial delay increases real latency."),
        },
    },
    {
        "question_id": "d4-measure-before-optimize-perf",
        "objective_ids": ["AIP-4.2", "AIP-4.3"],
        "prompt": (
            "A multi-stage pipeline is slow and the team wants to speed it up. "
            "What should they do BEFORE choosing an optimization?"
        ),
        "scenario_constraint": "Unknown which stage is slow.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Add per-stage timing/traces to find the actual bottleneck."),
            ("b", "Optimize the generation step because it is usually slowest."),
            ("c", "Rewrite the whole pipeline for speed."),
            ("d", "Add capacity everywhere at once."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Per-stage timing identifies the real bottleneck so the optimization "
            "targets it. Guessing, rewriting blindly, or scaling everything "
            "wastes effort and may miss the cause."
        ),
        "rationales": {
            "a": (True, "Measurement localizes the bottleneck before acting."),
            "b": (False, "A hunch about generation is not evidence."),
            "c": (False, "A blind rewrite is costly and unfocused."),
            "d": (False, "Scaling everything ignores where the time goes."),
        },
    },
    {
        "question_id": "d4-reranker-latency-tradeoff",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "Adding a reranker improved answer quality but pushed p99 latency "
            "past the SLA. Quality must stay above its bar and latency must meet "
            "the SLA. What is the BEST approach?"
        ),
        "scenario_constraint": "Reranker helps quality but breaks the latency SLA.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Rerank a smaller candidate set (lower first-stage top-k) to cut rerank time while holding quality above the bar.",
            ),
            ("b", "Remove the reranker entirely to meet the SLA."),
            ("c", "Raise the SLA so the current latency passes."),
            ("d", "Rerank an even larger candidate set for maximum quality."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Reranking a smaller candidate set reduces rerank latency while "
            "keeping quality above the bar, satisfying both constraints. Removing "
            "the reranker drops quality, raising the SLA hides the miss, and a "
            "larger set worsens latency."
        ),
        "rationales": {
            "a": (True, "A smaller rerank set balances the latency SLA and quality bar."),
            "b": (False, "Removing the reranker sacrifices the quality gain."),
            "c": (False, "Relaxing the SLA hides the latency failure."),
            "d": (False, "A larger rerank set increases latency further."),
        },
    },
    {
        "question_id": "d4-async-decouple-slow-path",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A synchronous API blocks the caller while a long document-generation "
            "job runs, causing timeouts. The result is not needed instantly. "
            "What design keeps the API responsive?"
        ),
        "scenario_constraint": "Long job blocks a synchronous request; result not needed instantly.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Accept the request, return a job handle, and process it asynchronously."),
            ("b", "Raise the client timeout so it waits longer."),
            ("c", "Make the job run faster by lowering temperature."),
            ("d", "Retry the whole request if it times out."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Returning a job handle and processing asynchronously keeps the API "
            "responsive for work that is not needed instantly. A longer timeout "
            "just blocks longer, temperature does not materially speed the job, "
            "and retrying repeats the long blocking call."
        ),
        "rationales": {
            "a": (True, "Async with a job handle unblocks the request path."),
            "b": (False, "A longer timeout still blocks the caller."),
            "c": (False, "Temperature does not meaningfully shorten the job."),
            "d": (False, "Retrying repeats the long blocking operation."),
        },
    },
    {
        "question_id": "d4-connection-reuse",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A high-QPS service creates a new client and connection for every "
            "model call, and profiling shows setup overhead per request. What "
            "reduces this overhead MOST?"
        ),
        "scenario_constraint": "Per-request client/connection setup overhead at high QPS.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Reuse a pooled client/connection across requests."),
            ("b", "Create two clients per request for redundancy."),
            ("c", "Add a sleep between requests to pace them."),
            ("d", "Increase output tokens to amortize setup."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Reusing a pooled client avoids repeated connection setup, cutting "
            "per-request overhead at high QPS. More clients add overhead, sleeping "
            "slows throughput, and output tokens are unrelated to connection "
            "setup."
        ),
        "rationales": {
            "a": (True, "Connection/client reuse removes repeated setup cost."),
            "b": (False, "Two clients per request add overhead."),
            "c": (False, "Sleeping reduces throughput."),
            "d": (False, "Output tokens do not amortize connection setup."),
        },
    },
    {
        "question_id": "d4-semantic-cache-latency",
        "objective_ids": ["AIP-4.2", "AIP-4.1"],
        "prompt": (
            "Many user questions are near-duplicates phrased differently, and "
            "each triggers a full model call. The team wants to shortcut "
            "repeated intents to cut latency and cost while avoiding wrong "
            "answers. What is the BEST approach?"
        ),
        "scenario_constraint": "Near-duplicate intents, different wording; must not serve wrong answers.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Use a semantic cache with a high similarity threshold and validation before serving a cached answer.",
            ),
            ("b", "Cache by exact string only, so paraphrases always miss."),
            ("c", "Serve the nearest cached answer regardless of similarity."),
            ("d", "Disable caching because paraphrases differ."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A semantic cache with a strict similarity threshold and validation "
            "shortcuts true duplicates while guarding against serving a loosely "
            "related wrong answer. Exact-string caching misses paraphrases, "
            "serving the nearest regardless risks wrong answers, and disabling "
            "caching forgoes the win."
        ),
        "rationales": {
            "a": (True, "A thresholded, validated semantic cache is safe and effective."),
            "b": (False, "Exact-string caching misses the paraphrased duplicates."),
            "c": (False, "Serving the nearest match blindly risks wrong answers."),
            "d": (False, "Disabling caching abandons a real latency/cost win."),
        },
    },
    {
        "question_id": "d4-batching-requests-endpoint",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A self-hosted model endpoint handles many small concurrent requests "
            "inefficiently, leaving the accelerator underused. Latency per "
            "request is acceptable. What improves throughput on the endpoint?"
        ),
        "scenario_constraint": "Many small concurrent requests underuse the accelerator.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Enable dynamic request batching so concurrent requests share accelerator passes.",
            ),
            ("b", "Force strictly one request at a time for predictability."),
            ("c", "Shrink the model to a tenth of its size regardless of quality."),
            ("d", "Add a fixed delay before each inference."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Dynamic batching lets concurrent requests share accelerator passes, "
            "raising throughput and utilization. Serializing wastes the "
            "accelerator, shrinking the model may break quality, and a fixed delay "
            "reduces throughput."
        ),
        "rationales": {
            "a": (True, "Dynamic batching raises accelerator utilization and throughput."),
            "b": (False, "Serial processing wastes the accelerator."),
            "c": (False, "Arbitrarily shrinking the model risks quality."),
            "d": (False, "A fixed delay lowers throughput."),
        },
    },
    {
        "question_id": "d4-prefetch-pipeline-overlap",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "In a retrieve-then-generate pipeline, generation waits idly while "
            "retrieval runs, and vice versa, for independent sub-steps. What "
            "technique reduces total latency without changing results?"
        ),
        "scenario_constraint": "Independent sub-steps run strictly sequentially.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Overlap independent stages (e.g., prefetch/parallelize) so idle time is reused.",
            ),
            ("b", "Serialize the stages more strictly to avoid contention."),
            ("c", "Raise temperature to speed generation."),
            ("d", "Increase top-k so retrieval returns more and generation waits longer."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Overlapping genuinely independent stages reuses otherwise idle time "
            "and cuts total latency without changing outputs. Stricter "
            "serialization adds idle time, temperature is irrelevant, and larger "
            "top-k increases work."
        ),
        "rationales": {
            "a": (True, "Overlapping independent stages removes idle waiting."),
            "b": (False, "Stricter serialization adds, not removes, idle time."),
            "c": (False, "Temperature does not reduce stage latency."),
            "d": (False, "Larger top-k increases retrieval and generation work."),
        },
    },
    {
        "question_id": "d4-quantization-latency",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A self-hosted model's latency is tied to its memory footprint and "
            "accelerator throughput. The team can apply quantization that cuts "
            "latency and keeps evaluation accuracy above the bar. The task runs "
            "at high volume. What is the MOST appropriate decision?"
        ),
        "scenario_constraint": "Quantization cuts latency and holds accuracy above the bar.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Adopt quantization since it cuts latency while holding accuracy above the bar."),
            (
                "b",
                "Reject quantization because any accuracy change is unacceptable even above the bar.",
            ),
            ("c", "Quantize only if latency is already acceptable."),
            ("d", "Choose based on which option has the larger context window."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "If quantization lowers latency while keeping measured accuracy above "
            "the committed bar, it is a sound optimization. Rejecting any change "
            "above the bar is over-strict, quantizing only when latency is fine "
            "misses the point, and context window is irrelevant here."
        ),
        "rationales": {
            "a": (True, "Latency gains with accuracy above the bar justify quantization."),
            "b": (False, "Changes that stay above the bar are acceptable by definition."),
            "c": (False, "The point is to fix latency that is not acceptable."),
            "d": (False, "Context window does not drive this latency decision."),
        },
    },
    {
        "question_id": "d4-timeout-budget-stages",
        "objective_ids": ["AIP-4.2"],
        "prompt": (
            "A multi-stage request has an overall latency SLA, but one slow stage "
            "occasionally blows the entire budget. The team wants to protect the "
            "overall SLA. What is the BEST approach?"
        ),
        "scenario_constraint": "One stage can consume the whole latency budget.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Set per-stage timeouts/deadline budgets with a defined fallback when a stage exceeds its slice.",
            ),
            ("b", "Remove all timeouts so no stage is interrupted."),
            ("c", "Give the slow stage the entire budget and skip the others."),
            ("d", "Retry the slow stage until it finishes, however long it takes."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Per-stage deadline budgets with a defined fallback keep one slow "
            "stage from blowing the overall SLA. Removing timeouts invites "
            "runaway latency, starving other stages breaks correctness, and "
            "unbounded retries ignore the budget."
        ),
        "rationales": {
            "a": (True, "Per-stage budgets plus fallback protect the overall SLA."),
            "b": (False, "No timeouts lets a slow stage run unbounded."),
            "c": (False, "Starving other stages breaks the request."),
            "d": (False, "Unbounded retries ignore the latency budget."),
        },
    },
    # ----- AIP-4.3 monitoring systems for GenAI applications ---------------
    {
        "question_id": "d4-core-signals-alarms",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "A GenAI service has no telemetry, so the team hears about outages "
            "only from users. What should they instrument FIRST to detect issues "
            "proactively?"
        ),
        "scenario_constraint": "No visibility; find problems before users report them.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "CloudWatch metrics and alarms on latency, error rate, throughput, and cost per request.",
            ),
            ("b", "A monthly manual review of a few sampled requests."),
            ("c", "A single counter of total requests with no errors or latency."),
            ("d", "Nothing; wait for user reports."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Instrumenting the core signals with alarms surfaces problems "
            "proactively. Monthly sampling is too slow, a bare request counter "
            "hides regressions, and waiting for users is reactive."
        ),
        "rationales": {
            "a": (True, "Core signals plus alarms detect regressions proactively."),
            "b": (False, "Monthly sampling is far too slow."),
            "c": (False, "A request counter hides latency and error problems."),
            "d": (False, "User reports are reactive, not proactive."),
        },
    },
    {
        "question_id": "d4-trace-correlation-ids",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Diagnosing a failed multi-step request is hard because gateway, "
            "agent, tool, and model logs cannot be tied together. What enables "
            "root-cause analysis MOST directly?"
        ),
        "scenario_constraint": "Logs across components cannot be joined per request.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Propagate a correlation/trace ID across every component (e.g., with X-Ray) and log it.",
            ),
            ("b", "Raise the log level everywhere and read more lines."),
            ("c", "Store each component's logs in separate systems with no shared key."),
            ("d", "Log full prompts and payloads including secrets for completeness."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A propagated correlation/trace ID reconstructs one request across "
            "components, the basis for diagnosis. More verbosity without a shared "
            "key cannot be joined, separate unkeyed stores stay disjoint, and "
            "logging secrets violates privacy."
        ),
        "rationales": {
            "a": (True, "A shared trace ID correlates one request end to end."),
            "b": (False, "Volume without a correlation key cannot be joined."),
            "c": (False, "Unkeyed separate stores cannot be correlated."),
            "d": (False, "Logging secrets/PII is never acceptable."),
        },
    },
    {
        "question_id": "d4-no-sensitive-telemetry",
        "objective_ids": ["AIP-4.3", "AIP-3.2"],
        "prompt": (
            "A team wants richer observability and proposes logging full prompts "
            "and model responses, which include user PII and credentials. What "
            "is the correct logging policy?"
        ),
        "scenario_constraint": "Improve observability without storing sensitive content.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Log sanitized metrics, events, and correlation IDs; redact prompts, responses, PII, and secrets.",
            ),
            ("b", "Log everything verbatim for maximum debuggability."),
            ("c", "Log full content but restrict who can read it."),
            ("d", "Disable logging entirely to avoid any risk."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Sanitized metrics, events, and correlation IDs give visibility "
            "without storing sensitive data. Verbatim logging leaks it, access "
            "control does not un-store it, and disabling logging destroys "
            "observability."
        ),
        "rationales": {
            "a": (True, "Sanitized, correlated telemetry is observable and safe."),
            "b": (False, "Verbatim logs persist PII and secrets."),
            "c": (False, "Access control does not undo storing the secret."),
            "d": (False, "No logging eliminates observability."),
        },
    },
    {
        "question_id": "d4-rollback-first-incident",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Immediately after a prompt/model deployment, error rate spikes and "
            "quality drops. The priority is restoring service. What is the "
            "correct FIRST action?"
        ),
        "scenario_constraint": "Fresh deploy caused a regression; restore service fast.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Roll back to the last known-good version, then investigate."),
            ("b", "Leave the bad version live and debug in production."),
            ("c", "Silence the alarms so paging stops."),
            ("d", "Wait to see whether it resolves on its own."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Rolling back to the last known-good version restores service, then "
            "you investigate safely. Debugging live prolongs harm, silencing "
            "alarms hides the incident, and waiting gambles with the outage."
        ),
        "rationales": {
            "a": (True, "Rollback restores service first; investigate after."),
            "b": (False, "Debugging live prolongs the outage."),
            "c": (False, "Silencing alarms hides, not fixes, the incident."),
            "d": (False, "Waiting gambles during a live regression."),
        },
    },
    {
        "question_id": "d4-diagnose-before-remediate",
        "objective_ids": ["AIP-4.3", "AIP-5.2"],
        "prompt": (
            "An intermittent latency alarm fires. An engineer wants to immediately "
            "double the instance count. What is the better MONITORING-led step "
            "first?"
        ),
        "scenario_constraint": "Act on evidence before changing capacity.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Correlate the alarm to traces to find which stage is slow, then remediate that.",
            ),
            ("b", "Double instances now and see if the alarm clears."),
            ("c", "Delete the alarm because it is noisy."),
            ("d", "Lower the latency threshold so the alarm stops firing."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Correlating the alarm to traces localizes the real cause before "
            "spending on capacity that may not be the bottleneck. Doubling blindly "
            "may not help, deleting the alarm hides the signal, and lowering the "
            "threshold masks the problem."
        ),
        "rationales": {
            "a": (True, "Trace-led diagnosis targets the actual slow stage."),
            "b": (False, "Blind scaling may not address the cause."),
            "c": (False, "Deleting the alarm removes the signal."),
            "d": (False, "Lowering the threshold masks the issue."),
        },
    },
    {
        "question_id": "d4-quality-drift-monitoring",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Infrastructure metrics are all green, but users report the "
            "assistant's answers have gotten worse over weeks. What monitoring "
            "capability is MISSING?"
        ),
        "scenario_constraint": "Healthy infra metrics but declining answer quality.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Ongoing output-quality/drift monitoring (e.g., sampled evaluation against a golden set).",
            ),
            ("b", "A higher-resolution CPU utilization graph."),
            ("c", "More frequent latency percentile sampling."),
            ("d", "A larger log retention window."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Green infra metrics do not capture answer quality; ongoing quality/"
            "drift monitoring against a golden set does. CPU graphs, latency "
            "sampling, and log retention are infrastructure signals that miss "
            "quality decline."
        ),
        "rationales": {
            "a": (True, "Quality/drift monitoring detects declining answers infra metrics miss."),
            "b": (False, "CPU graphs do not reflect answer quality."),
            "c": (False, "Latency sampling is unrelated to quality drift."),
            "d": (False, "Longer retention does not measure quality."),
        },
    },
    {
        "question_id": "d4-cost-metric-emit",
        "objective_ids": ["AIP-4.3", "AIP-4.1"],
        "prompt": (
            "A team wants an alarm when per-request cost rises sharply, but their "
            "dashboards only show invocation counts. What must they add to "
            "monitor cost directly?"
        ),
        "scenario_constraint": "Need to alarm on cost, not just call volume.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Emit a cost-per-request metric (e.g., from token usage) and alarm on it."),
            ("b", "Alarm on invocation count and assume cost tracks it."),
            ("c", "Check the monthly bill and react afterward."),
            ("d", "Alarm on CPU utilization as a cost proxy."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Emitting a cost-per-request metric from token usage lets you alarm on "
            "cost directly. Invocation count ignores token-size changes, the "
            "monthly bill is too late, and CPU is a poor proxy for token-priced "
            "cost."
        ),
        "rationales": {
            "a": (True, "A cost-per-request metric enables direct cost alarms."),
            "b": (False, "Call count misses changes in tokens per call."),
            "c": (False, "The monthly bill reacts far too late."),
            "d": (False, "CPU does not track token-based cost."),
        },
    },
    {
        "question_id": "d4-dashboards-golden-signals-select-two",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "A new GenAI endpoint needs an operational dashboard that supports "
            "fast incident response. Which TWO signal groups are MOST essential "
            "to include? (Select TWO.)"
        ),
        "scenario_constraint": "Build a dashboard for incident response.",
        "difficulty": "easy",
        "question_format": "multiple_response",
        "options": [
            ("a", "Latency percentiles (p50/p99) over time."),
            ("b", "Error rate and throughput over time."),
            ("c", "The color palette of the dashboard."),
            ("d", "The number of dashboard widgets."),
            ("e", "The font used for metric labels."),
        ],
        "correct_option_ids": ["a", "b"],
        "explanation": (
            "Latency percentiles and error-rate/throughput are the operational "
            "signals that drive incident response. Palette, widget count, and "
            "font are cosmetic and do not inform diagnosis."
        ),
        "rationales": {
            "a": (True, "Latency percentiles reveal user-felt slowness."),
            "b": (True, "Error rate and throughput reveal failures and load."),
            "c": (False, "Color palette is cosmetic."),
            "d": (False, "Widget count does not inform diagnosis."),
            "e": (False, "Label font is irrelevant to incident response."),
        },
    },
    {
        "question_id": "d4-alarm-threshold-baseline",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "An alarm set at a round-number latency keeps firing during normal "
            "operation and is being ignored. The team wants meaningful alerts. "
            "What is the BEST fix?"
        ),
        "scenario_constraint": "Noisy alarm trained the team to ignore it.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Set thresholds from observed baselines so alarms fire on real anomalies."),
            ("b", "Delete the alarm since it is noisy."),
            ("c", "Raise the threshold so high it essentially never fires."),
            ("d", "Keep the alarm and tell the team to ignore it during peaks."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Threshold set from observed baselines fire on genuine anomalies and "
            "restore trust in the alarm. Deleting it loses the signal, an "
            "impossibly high threshold never warns, and training the team to "
            "ignore it defeats the purpose."
        ),
        "rationales": {
            "a": (True, "Baseline-derived thresholds alarm on real anomalies."),
            "b": (False, "Deleting the alarm removes the signal."),
            "c": (False, "A never-firing alarm provides no warning."),
            "d": (False, "Teaching the team to ignore alarms is unsafe."),
        },
    },
    {
        "question_id": "d4-synthetic-canary-monitoring",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "The team wants to know an endpoint is healthy and answering "
            "correctly even during quiet periods with little real traffic. What "
            "monitoring approach provides that?"
        ),
        "scenario_constraint": "Detect problems during low-traffic periods.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Run periodic synthetic canary requests with known expected answers and alarm on failures.",
            ),
            ("b", "Rely only on real user traffic, which is sparse at night."),
            ("c", "Check the endpoint manually once a day."),
            ("d", "Assume health as long as the instance is running."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Synthetic canaries with known expected answers continuously verify "
            "health and correctness even without real traffic. Sparse real "
            "traffic, daily manual checks, and 'instance is up' all miss quiet-"
            "period failures."
        ),
        "rationales": {
            "a": (True, "Synthetic canaries verify health during quiet periods."),
            "b": (False, "Sparse night traffic leaves gaps."),
            "c": (False, "Daily manual checks miss most of the day."),
            "d": (False, "A running instance can still answer incorrectly."),
        },
    },
    {
        "question_id": "d4-tool-call-observability",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "An agent intermittently returns poor results and the team cannot "
            "tell whether a specific tool is failing or returning bad data. What "
            "should they add?"
        ),
        "scenario_constraint": "Cannot see per-tool behavior inside the agent.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Instrument per-tool spans with sanitized inputs/outputs, latency, and error status.",
            ),
            ("b", "Log only the agent's final answer."),
            ("c", "Increase the model temperature to vary behavior."),
            ("d", "Remove tools until the problem disappears."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Per-tool spans with sanitized metadata, latency, and error status "
            "reveal which tool fails or returns bad data. Logging only the final "
            "answer hides the tools, temperature is irrelevant, and removing "
            "tools cripples the agent."
        ),
        "rationales": {
            "a": (True, "Per-tool spans localize tool failures and bad data."),
            "b": (False, "Final-answer-only logging hides tool behavior."),
            "c": (False, "Temperature does not diagnose tool failures."),
            "d": (False, "Removing tools breaks required functionality."),
        },
    },
    {
        "question_id": "d4-alarm-actionable-runbook",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "On-call engineers receive alarms but waste time deciding what to do "
            "when one fires. What MOST improves response time without adding "
            "noise?"
        ),
        "scenario_constraint": "Alarms fire but response is slow and ad hoc.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Attach a runbook with diagnosis and remediation steps to each actionable alarm.",
            ),
            ("b", "Add many more alarms so nothing is missed."),
            ("c", "Route every alarm to every engineer."),
            ("d", "Lower all thresholds to catch issues earlier."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A runbook per actionable alarm speeds consistent response without "
            "adding noise. More alarms, broad routing, and lower thresholds all "
            "increase noise and alarm fatigue."
        ),
        "rationales": {
            "a": (True, "Runbooks turn alarms into fast, consistent action."),
            "b": (False, "More alarms add noise and fatigue."),
            "c": (False, "Routing everything to everyone dilutes ownership."),
            "d": (False, "Lower thresholds increase false alarms."),
        },
    },
    {
        "question_id": "d4-record-incident-evidence",
        "objective_ids": ["AIP-4.3", "AIP-5.2"],
        "prompt": (
            "After resolving an incident, the team wants to prevent recurrence "
            "and improve future diagnosis. What should the incident record "
            "capture?"
        ),
        "scenario_constraint": "Build durable learning from the incident.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "The symptoms, evidence/traces, root cause, remediation, and how recovery was verified.",
            ),
            ("b", "Only the final fix that was applied."),
            ("c", "Just the timestamp the alarm cleared."),
            ("d", "A note that it is resolved, with no detail."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Capturing symptoms, evidence, root cause, remediation, and recovery "
            "verification makes the incident a reusable diagnostic asset. Recording "
            "only the fix, a timestamp, or a bare 'resolved' loses the learning."
        ),
        "rationales": {
            "a": (True, "Full evidence-to-recovery record enables future diagnosis."),
            "b": (False, "The fix alone omits why and how it was found."),
            "c": (False, "A clear-time timestamp carries no diagnostic value."),
            "d": (False, "A bare 'resolved' note teaches nothing."),
        },
    },
    {
        "question_id": "d4-sampling-high-volume-traces",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Full tracing of a very high-volume service is itself adding cost and "
            "overhead, but the team still needs representative traces and all "
            "error traces. What is the BEST approach?"
        ),
        "scenario_constraint": "Tracing overhead is high at volume; errors must not be missed.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Sample a fraction of normal traces but keep all error/anomaly traces."),
            ("b", "Trace every single request regardless of overhead."),
            ("c", "Turn tracing off entirely to remove overhead."),
            ("d", "Trace only successful requests to keep dashboards clean."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Sampling normal traffic while retaining all error/anomaly traces "
            "controls overhead without losing the traces that matter most. Full "
            "tracing keeps the overhead, disabling it loses visibility, and "
            "tracing only successes discards the failures you need."
        ),
        "rationales": {
            "a": (True, "Sample normal traffic, keep all error traces."),
            "b": (False, "Full tracing keeps the overhead problem."),
            "c": (False, "Disabling tracing loses needed visibility."),
            "d": (False, "Tracing only successes drops the error traces."),
        },
    },
    {
        "question_id": "d4-slo-error-budget",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Leadership wants a principled way to decide when to prioritize "
            "reliability work versus shipping features for a GenAI service. Which "
            "monitoring construct supports that decision?"
        ),
        "scenario_constraint": "Balance reliability work against feature work.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Define SLOs with an error budget and gate feature work on remaining budget."),
            ("b", "Track only raw uptime percentage with no target."),
            ("c", "Decide reliability priorities by gut feel each sprint."),
            ("d", "Alarm on every metric and treat all as equally urgent."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "SLOs with an error budget give an objective basis to balance "
            "reliability and feature work. Raw uptime without a target, gut feel, "
            "and treating all alarms as equal provide no principled trade-off."
        ),
        "rationales": {
            "a": (True, "SLOs and error budgets objectively guide the trade-off."),
            "b": (False, "Uptime with no target gives no decision rule."),
            "c": (False, "Gut feel is not a principled basis."),
            "d": (False, "Treating all alarms equally prevents prioritization."),
        },
    },
    {
        "question_id": "d4-guardrail-block-metric",
        "objective_ids": ["AIP-4.3", "AIP-3.1"],
        "prompt": (
            "A team wants to know whether their safety guardrails are suddenly "
            "over-blocking legitimate requests after a config change. Which "
            "monitoring signal MOST directly detects this?"
        ),
        "scenario_constraint": "Detect a spike in guardrail blocks of legitimate traffic.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Track guardrail block rate over time and alarm on sudden increases."),
            ("b", "Track only total request volume."),
            ("c", "Track CPU utilization of the guardrail service."),
            ("d", "Track the number of guardrail policies configured."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Monitoring the guardrail block rate reveals an over-blocking spike "
            "after a change. Request volume, CPU, and policy count do not indicate "
            "how often legitimate requests are being blocked."
        ),
        "rationales": {
            "a": (True, "Block-rate trends reveal over-blocking directly."),
            "b": (False, "Total volume does not show block behavior."),
            "c": (False, "CPU is unrelated to block rate."),
            "d": (False, "Policy count does not measure blocking outcomes."),
        },
    },
    {
        "question_id": "d4-structured-logs-query",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "Engineers struggle to query logs because entries are free-text and "
            "inconsistent, slowing incident response. What change MOST improves "
            "log usefulness?"
        ),
        "scenario_constraint": "Free-text logs are hard to query under pressure.",
        "difficulty": "easy",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Emit structured logs with consistent fields (correlation id, stage, outcome)."),
            ("b", "Write longer free-text messages."),
            ("c", "Log less so there is less to search."),
            ("d", "Store logs as images for readability."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Structured logs with consistent fields are queryable and speed "
            "incident response. Longer prose, logging less, and image logs all "
            "make querying harder or impossible."
        ),
        "rationales": {
            "a": (True, "Structured fields make logs queryable under pressure."),
            "b": (False, "More prose does not make logs queryable."),
            "c": (False, "Logging less can drop needed evidence."),
            "d": (False, "Image logs are not searchable."),
        },
    },
    {
        "question_id": "d4-monitor-retrieval-quality",
        "objective_ids": ["AIP-4.3", "AIP-5.1"],
        "prompt": (
            "A RAG assistant's answer quality depends on retrieval, which can "
            "silently degrade as the index drifts. The team wants early warning "
            "specific to retrieval. What should they monitor?"
        ),
        "scenario_constraint": "Catch silent retrieval degradation early.",
        "difficulty": "hard",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Periodically evaluate retrieval relevance/recall on a labeled probe set and alarm on drops.",
            ),
            ("b", "Monitor only generation latency."),
            ("c", "Monitor the vector store's disk usage."),
            ("d", "Monitor the number of documents ingested."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A labeled probe set evaluated over time gives early warning when "
            "retrieval relevance or recall drops. Generation latency, disk usage, "
            "and ingest counts do not measure retrieval quality."
        ),
        "rationales": {
            "a": (True, "Probe-set relevance/recall over time catches retrieval drift."),
            "b": (False, "Generation latency is not retrieval quality."),
            "c": (False, "Disk usage says nothing about relevance."),
            "d": (False, "Ingest count does not measure retrieval quality."),
        },
    },
    {
        "question_id": "d4-dashboard-business-outcome",
        "objective_ids": ["AIP-4.3"],
        "prompt": (
            "A dashboard shows only infrastructure metrics, but stakeholders want "
            "to see whether the GenAI feature is actually helping users (e.g., "
            "deflection or task completion). What should be added?"
        ),
        "scenario_constraint": "Connect monitoring to business outcomes.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            (
                "a",
                "Add outcome metrics such as task-completion or deflection rate alongside infra metrics.",
            ),
            ("b", "Add more CPU and memory graphs."),
            ("c", "Add the count of deployed Lambda functions."),
            ("d", "Add the number of lines of code shipped."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Outcome metrics like task completion or deflection connect "
            "monitoring to business value. CPU graphs, function counts, and lines "
            "of code are not outcome measures."
        ),
        "rationales": {
            "a": (True, "Outcome metrics show whether the feature helps users."),
            "b": (False, "More infra graphs do not show business outcomes."),
            "c": (False, "Function count is not an outcome."),
            "d": (False, "Lines of code is not an outcome measure."),
        },
    },
    {
        "question_id": "d4-detect-cost-spike-anomaly",
        "objective_ids": ["AIP-4.3", "AIP-4.1"],
        "prompt": (
            "Overnight, a bug caused an agent to loop and multiply token usage, "
            "and the team only noticed on the monthly bill. What monitoring would "
            "have caught this within minutes?"
        ),
        "scenario_constraint": "A runaway cost event went unnoticed until billing.",
        "difficulty": "medium",
        "question_format": "multiple_choice",
        "options": [
            ("a", "Real-time token-usage/cost-rate metrics with an anomaly alarm."),
            ("b", "A quarterly cost review meeting."),
            ("c", "A static monthly budget with no alerting."),
            ("d", "Manual spot checks of the console when someone remembers."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Real-time token/cost-rate metrics with anomaly alarms catch a "
            "runaway loop within minutes. Quarterly reviews, static budgets "
            "without alerts, and ad hoc checks all discover it far too late."
        ),
        "rationales": {
            "a": (True, "Real-time cost-rate alarms catch runaway usage fast."),
            "b": (False, "A quarterly review is far too slow."),
            "c": (False, "A static budget without alerts never warns."),
            "d": (False, "Ad hoc checks miss overnight spikes."),
        },
    },
    # ----- end AIP-4.3 -----------------------------------------------------
]


def question_count() -> int:
    """Return the number of authored Domain 4 questions."""
    return len(QUESTIONS)
