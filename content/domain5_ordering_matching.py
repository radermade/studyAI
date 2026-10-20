"""Authored Domain 5 (AIP-C01) ordering and matching questions.

See content/domain1_ordering_matching.py for the ordering/matching dict shapes.
No proprietary exam content is reproduced; scenarios and keys are original and
grounded in the official exam guide's Domain 5 skill statements (evaluation,
AIP-5.1; troubleshooting, AIP-5.2).
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    {
        "question_id": "d5o-eval-pipeline-build",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are building an offline evaluation pipeline for a Bedrock "
            "chatbot and must gate releases on measured quality. Place the steps "
            "in the correct order."
        ),
        "scenario_constraint": "An eval pipeline must exist before it can gate a release.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Score each response against the reference answers with your chosen metrics."),
            ("b", "Assemble a labeled golden dataset of prompts and reference answers."),
            ("c", "Run the model over every golden prompt to produce candidate answers."),
            ("d", "Fail or pass the release at a quality gate based on the aggregate score."),
        ],
        "correct_sequence": ["b", "c", "a", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A golden dataset must exist first, the model then produces answers "
            "over it, those answers are scored against the references, and the "
            "aggregate score finally drives the pass/fail quality gate."
        ),
        "rationales": {
            "a": (True, "Scoring needs both candidate answers and references in hand."),
            "b": (True, "The golden dataset is the fixed input every later step depends on."),
            "c": (True, "Candidate answers must be generated before they can be scored."),
            "d": (True, "The gate decision is last and consumes the aggregate score."),
        },
    },
    {
        "question_id": "d5o-llm-judge-calibration",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You want to adopt an LLM-as-a-judge for RAG answer quality but only "
            "if it tracks human judgment. Place the steps in the correct order."
        ),
        "scenario_constraint": "A judge must be calibrated against human labels before adoption.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Measure agreement between the judge scores and the human labels."),
            ("b", "Collect human quality labels on a representative sample of answers."),
            ("c", "Run the LLM judge over the same sampled answers."),
            ("d", "Adopt the judge for scale only if agreement clears your threshold."),
        ],
        "correct_sequence": ["b", "c", "a", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Human labels are the ground truth, the judge scores the same sample, "
            "the two are compared for agreement, and adoption is gated on that "
            "measured agreement."
        ),
        "rationales": {
            "a": (True, "Agreement can only be computed once both score sets exist."),
            "b": (True, "Human labels are the reference the judge is calibrated against."),
            "c": (True, "The judge must score the sample before agreement is measured."),
            "d": (True, "Adoption is the final decision, gated on agreement."),
        },
    },
    {
        "question_id": "d5o-systematic-troubleshoot",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A production Bedrock feature intermittently returns low-quality "
            "answers and you must troubleshoot it methodically. Place the steps "
            "in the correct order."
        ),
        "scenario_constraint": "Disciplined troubleshooting reproduces before it remediates.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Reproduce the failure reliably with a concrete failing input."),
            ("b", "Gather CloudWatch Logs and AWS X-Ray traces around the failure."),
            ("c", "Isolate one variable from a known-good baseline to locate the fault."),
            ("d", "Apply a narrow fix and validate that the failure no longer recurs."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You first reproduce the fault, then gather logs and traces as "
            "evidence, isolate a single variable against a baseline to localize "
            "it, and only then apply and validate a narrow fix."
        ),
        "rationales": {
            "a": (True, "A reliable repro is the precondition for every later step."),
            "b": (True, "Evidence gathering follows a repro and precedes isolation."),
            "c": (True, "Isolating one variable needs the evidence to point somewhere."),
            "d": (True, "A narrow fix and its validation come last."),
        },
    },
    {
        "question_id": "d5o-rag-fault-localize",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A RAG assistant on Amazon Bedrock Knowledge Bases is hallucinating "
            "and you must decide whether retrieval or generation is at fault. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Localize retrieval versus generation before changing either.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Inspect the retrieved chunks to see whether they contain the answer."),
            ("b", "Confirm the hallucinated answer on a specific query."),
            ("c", "If chunks are correct, examine the prompt and generation step."),
            ("d", "If chunks are wrong, tune chunking, embeddings, or vector search."),
        ],
        "correct_sequence": ["b", "a", "d", "c"],
        "correct_option_ids": [],
        "explanation": (
            "Confirm the failing query, inspect retrieved chunks to split "
            "retrieval from generation, remediate retrieval when chunks are "
            "wrong, and otherwise move on to the generation step."
        ),
        "rationales": {
            "a": (True, "Chunk inspection is the branch point between the two layers."),
            "b": (True, "A confirmed failing query anchors the whole diagnosis."),
            "c": (True, "Generation is examined only after retrieval is cleared."),
            "d": (True, "Retrieval remediation applies once chunks are shown wrong."),
        },
    },
    {
        "question_id": "d5o-regression-suite",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "A prompt change improved one answer but you fear it broke others, so "
            "you run regression testing. Place the steps in the correct order."
        ),
        "scenario_constraint": "Regression testing compares a candidate against a saved baseline.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Record baseline scores for the current prompt on the eval set."),
            ("b", "Score the new prompt on the same eval set."),
            ("c", "Diff the new scores against the baseline to find regressions."),
            ("d", "Block the change if any required case regressed."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A baseline is captured first, the candidate is scored on the same "
            "set, the two are diffed to surface regressions, and the change is "
            "blocked if a required case got worse."
        ),
        "rationales": {
            "a": (True, "Without a baseline there is nothing to regress against."),
            "b": (True, "The candidate must be scored on the identical set to compare."),
            "c": (True, "The diff surfaces regressions after both score sets exist."),
            "d": (True, "The block decision is the final gate."),
        },
    },
    {
        "question_id": "d5o-bedrock-model-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You will choose between two foundation models using Amazon Bedrock "
            "Model Evaluations before committing to one. Place the steps in the "
            "correct order."
        ),
        "scenario_constraint": "Model selection follows a defined evaluation job workflow.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Prepare a prompt dataset and pick evaluation metrics."),
            ("b", "Create and run a Bedrock model evaluation job for each candidate."),
            ("c", "Compare the metric results across the candidate models."),
            ("d", "Select the model that best balances quality and cost."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "You define the dataset and metrics, run an evaluation job per "
            "candidate, compare results, and select on quality and cost."
        ),
        "rationales": {
            "a": (True, "The dataset and metrics are inputs the jobs need."),
            "b": (True, "Each candidate is evaluated before results can be compared."),
            "c": (True, "Comparison follows the completed evaluation jobs."),
            "d": (True, "Selection is the final decision on the comparison."),
        },
    },
    {
        "question_id": "d5o-canary-rollout",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are releasing a new prompt version behind a canary before full "
            "rollout. Place the steps in the correct order."
        ),
        "scenario_constraint": "A canary exposes a small slice before a full cutover.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Route a small percentage of live traffic to the new version."),
            ("b", "Define success metrics and a rollback trigger for the canary."),
            ("c", "Monitor the canary metrics against the rollback trigger."),
            ("d", "Promote to full traffic or roll back based on the metrics."),
        ],
        "correct_sequence": ["b", "a", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Success metrics and the rollback trigger are set first, a traffic "
            "slice is routed to the canary, the metrics are monitored, and the "
            "promote-or-rollback decision is made last."
        ),
        "rationales": {
            "a": (True, "Traffic is routed only after the trigger is defined."),
            "b": (True, "Metrics and the trigger must exist before any traffic shifts."),
            "c": (True, "Monitoring happens while the canary serves traffic."),
            "d": (True, "The promote-or-rollback call is the terminal step."),
        },
    },
    {
        "question_id": "d5o-context-overflow",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Long documents are overflowing the model context window and answers "
            "are being truncated. Place the troubleshooting steps in the correct "
            "order."
        ),
        "scenario_constraint": "Context-overflow triage confirms the cause before resizing chunks.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Measure token counts of the prompt plus retrieved context."),
            ("b", "Confirm the answers are being truncated at the context limit."),
            ("c", "Introduce dynamic chunking so retrieved context fits the window."),
            ("d", "Re-run the failing cases and confirm answers are now complete."),
        ],
        "correct_sequence": ["b", "a", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Confirm truncation, measure the token budget to prove overflow, "
            "apply dynamic chunking to fit the window, and re-run to confirm "
            "recovery."
        ),
        "rationales": {
            "a": (True, "Token measurement quantifies the overflow after it is confirmed."),
            "b": (True, "Confirming truncation is the entry point for the triage."),
            "c": (True, "Dynamic chunking is the remediation applied after diagnosis."),
            "d": (True, "Re-running the cases validates the fix."),
        },
    },
    {
        "question_id": "d5o-embedding-drift",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Retrieval relevance has quietly degraded over weeks and you suspect "
            "embedding drift. Place the diagnostic steps in the correct order."
        ),
        "scenario_constraint": "Drift is confirmed with trend evidence before re-embedding.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Chart retrieval relevance metrics over time to spot the decline."),
            ("b", "Compare current embeddings against those from the healthy period."),
            ("c", "Re-embed and re-index the affected corpus with the current model."),
            ("d", "Verify relevance metrics recover after the re-index."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A relevance trend surfaces the decline, an embedding comparison "
            "confirms drift, re-embedding and re-indexing remediate it, and the "
            "recovered metrics validate the fix."
        ),
        "rationales": {
            "a": (True, "The trend chart is what first reveals the degradation."),
            "b": (True, "Comparing embeddings confirms drift as the cause."),
            "c": (True, "Re-embedding is the remediation once drift is confirmed."),
            "d": (True, "Metric recovery is the validation step."),
        },
    },
    {
        "question_id": "d5o-deploy-validation-synthetic",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Before a GenAI feature goes live you validate it with synthetic "
            "end-to-end workflows. Place the steps in the correct order."
        ),
        "scenario_constraint": "Deployment validation runs synthetic flows before opening traffic.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Author synthetic workflows that mimic real user journeys."),
            ("b", "Execute the synthetic workflows against the deployed feature."),
            ("c", "Check the outputs for hallucination and semantic drift."),
            ("d", "Open the feature to real users once checks pass."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Synthetic workflows are authored, executed against the deployment, "
            "their outputs are checked for hallucination and drift, and only "
            "then is live traffic allowed."
        ),
        "rationales": {
            "a": (True, "The synthetic flows must exist before they can run."),
            "b": (True, "Execution produces the outputs the checks examine."),
            "c": (True, "Hallucination and drift checks follow execution."),
            "d": (True, "Opening to users is gated on passing checks."),
        },
    },
    {
        "question_id": "d5o-ab-test-prompts",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You will A/B test two prompt templates on live traffic to pick a "
            "winner. Place the steps in the correct order."
        ),
        "scenario_constraint": "An A/B test needs a defined metric and sample size up front.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Split live traffic randomly between the two templates."),
            ("b", "Define the success metric and the sample size needed."),
            ("c", "Collect results until the sample size is reached."),
            ("d", "Choose the template with the better metric once results are significant."),
        ],
        "correct_sequence": ["b", "a", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "The metric and sample size are fixed first, traffic is split, "
            "results accumulate to the planned size, and the winner is chosen "
            "on the significant result."
        ),
        "rationales": {
            "a": (True, "Random splitting happens after the plan is set."),
            "b": (True, "Metric and sample size must precede any traffic split."),
            "c": (True, "Results are gathered until the planned size is met."),
            "d": (True, "The winner is chosen last, on significant data."),
        },
    },
    {
        "question_id": "d5o-feedback-loop",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are closing a human-feedback loop to improve answer quality "
            "over time. Place the steps in the correct order."
        ),
        "scenario_constraint": "Feedback is captured and aggregated before it guides changes.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Capture user ratings and annotations on live answers."),
            ("b", "Aggregate the feedback into quality signals by topic."),
            ("c", "Prioritize the weakest topics for prompt or retrieval fixes."),
            ("d", "Ship the fixes and watch the ratings for improvement."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Ratings are captured, aggregated into signals, used to prioritize "
            "the weakest areas, and the resulting fixes are shipped and watched."
        ),
        "rationales": {
            "a": (True, "Raw feedback is the input to everything downstream."),
            "b": (True, "Aggregation turns raw ratings into usable signals."),
            "c": (True, "Prioritization needs aggregated signals to rank topics."),
            "d": (True, "Shipping and watching closes the loop."),
        },
    },
    {
        "question_id": "d5o-api-error-triage",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A client intermittently receives errors from a Bedrock integration "
            "and you must find the cause. Place the steps in the correct order."
        ),
        "scenario_constraint": "API error triage reads the error class before guessing a fix.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Read the structured error logs to classify the failures."),
            ("b", "Separate throttling from validation and server errors."),
            ("c", "Apply the matching remedy such as backoff or payload validation."),
            ("d", "Confirm the error rate drops after the change."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Logs are read to classify failures, errors are separated by type, "
            "the type-specific remedy is applied, and the error rate is checked "
            "to confirm recovery."
        ),
        "rationales": {
            "a": (True, "Classification starts from reading the logged errors."),
            "b": (True, "Separating error classes points to the right remedy."),
            "c": (True, "The remedy is chosen per error class after separation."),
            "d": (True, "The dropped error rate validates the change."),
        },
    },
    {
        "question_id": "d5o-golden-dataset-build",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are constructing a golden dataset to anchor all future "
            "evaluation. Place the steps in the correct order."
        ),
        "scenario_constraint": "A golden set is curated and reviewed before it is frozen.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Collect representative prompts from real usage."),
            ("b", "Write and expert-review the reference answers."),
            ("c", "Version and freeze the dataset for reuse."),
            ("d", "Run the first evaluation against the frozen set."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Representative prompts are collected, reference answers are written "
            "and reviewed, the set is versioned and frozen, and the first "
            "evaluation runs against it."
        ),
        "rationales": {
            "a": (True, "Prompts come first since answers attach to them."),
            "b": (True, "Reviewed references make the set trustworthy."),
            "c": (True, "Freezing preserves comparability across runs."),
            "d": (True, "Evaluation uses the frozen set last."),
        },
    },
    {
        "question_id": "d5o-agent-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are evaluating a Bedrock agent on multi-step tasks before "
            "trusting it in production. Place the steps in the correct order."
        ),
        "scenario_constraint": "Agent evaluation defines tasks and expected tool use first.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Define benchmark tasks with expected tool calls and outcomes."),
            ("b", "Run the agent and record its reasoning and tool-call traces."),
            ("c", "Score task completion and correct tool usage against expectations."),
            ("d", "Gate production use on the measured completion rate."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Benchmark tasks and expectations are defined, the agent is run with "
            "traces recorded, completion and tool usage are scored, and "
            "production use is gated on the result."
        ),
        "rationales": {
            "a": (True, "Expected outcomes must exist to score against."),
            "b": (True, "Traces are produced by running the defined tasks."),
            "c": (True, "Scoring compares recorded behavior to expectations."),
            "d": (True, "The production gate uses the completion rate last."),
        },
    },
    {
        "question_id": "d5o-prompt-version-compare",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A recent prompt edit may have caused worse answers and you want to "
            "compare versions with a prompt-testing framework. Place the steps "
            "in the correct order."
        ),
        "scenario_constraint": "Version comparison needs both versions run on one fixed set.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Retrieve the previous and current prompt versions."),
            ("b", "Run both versions on the same fixed test set."),
            ("c", "Compare the per-case outputs to spot the behavior change."),
            ("d", "Revert or keep the edit based on the comparison."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Both prompt versions are retrieved, run on one fixed set, their "
            "per-case outputs compared, and the edit is kept or reverted on the "
            "evidence."
        ),
        "rationales": {
            "a": (True, "You need both versions in hand to compare them."),
            "b": (True, "A shared fixed set isolates the prompt as the variable."),
            "c": (True, "Comparison surfaces the behavior change after both runs."),
            "d": (True, "The keep-or-revert decision is final."),
        },
    },
    {
        "question_id": "d5o-schema-validation-fix",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A downstream service rejects the model's JSON because it violates "
            "the expected schema. Place the troubleshooting steps in the correct "
            "order."
        ),
        "scenario_constraint": "Schema failures are diagnosed against the contract first.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Validate a failing response against the JSON schema."),
            ("b", "Identify which fields violate the schema."),
            ("c", "Tighten the prompt and add output validation for those fields."),
            ("d", "Re-test and confirm responses now validate."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A failing response is validated against the schema, the offending "
            "fields are identified, the prompt and validation are tightened for "
            "them, and re-testing confirms conformance."
        ),
        "rationales": {
            "a": (True, "Validation against the schema is the diagnostic entry point."),
            "b": (True, "Pinpointing bad fields scopes the remediation."),
            "c": (True, "Prompt and validation changes follow the field diagnosis."),
            "d": (True, "Re-testing confirms the responses now conform."),
        },
    },
    {
        "question_id": "d5o-quality-gate-cicd",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are adding an automated quality gate to the CodePipeline that "
            "ships prompt changes. Place the steps in the correct order."
        ),
        "scenario_constraint": "A CI quality gate runs eval before any deploy stage.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Add a pipeline stage that runs the eval suite on the golden set."),
            ("b", "Set a minimum score threshold the stage must meet."),
            ("c", "Fail the pipeline when the score is below the threshold."),
            ("d", "Allow the deploy stage to proceed only on a passing score."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "An eval stage is added, a threshold is set, the pipeline fails below "
            "it, and deployment proceeds only when the score passes."
        ),
        "rationales": {
            "a": (True, "The eval stage must exist before a threshold means anything."),
            "b": (True, "The threshold defines what passing means."),
            "c": (True, "Failing below the threshold is the enforcement."),
            "d": (True, "Deploy proceeds only after the gate passes."),
        },
    },
    {
        "question_id": "d5o-hallucination-check",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are adding an automated hallucination check to a RAG eval. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Hallucination scoring compares answers to retrieved sources.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Capture each answer alongside the sources retrieved for it."),
            ("b", "Check each answer claim against its retrieved sources."),
            ("c", "Score the hallucination rate across the eval set."),
            ("d", "Flag the run for review when the rate exceeds the limit."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Answers are captured with their sources, each claim is checked "
            "against those sources, a hallucination rate is scored, and the run "
            "is flagged above the limit."
        ),
        "rationales": {
            "a": (True, "Answer-source pairs are the input to grounding checks."),
            "b": (True, "Claim checking produces the per-answer grounding verdicts."),
            "c": (True, "The rate aggregates the per-answer verdicts."),
            "d": (True, "Flagging acts on the aggregated rate."),
        },
    },
    {
        "question_id": "d5o-vector-search-tuning",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Relevant documents exist but are not surfacing, so you tune vector "
            "search on Amazon OpenSearch Service. Place the steps in the correct "
            "order."
        ),
        "scenario_constraint": "Search tuning measures recall before and after each change.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Measure baseline retrieval recall on labeled queries."),
            ("b", "Adjust parameters such as k, similarity, and hybrid weighting."),
            ("c", "Re-measure recall on the same labeled queries."),
            ("d", "Keep the change only if recall improved."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Baseline recall is measured, search parameters are adjusted, recall "
            "is re-measured on the same queries, and the change is kept only on a "
            "measured improvement."
        ),
        "rationales": {
            "a": (True, "A baseline is needed to judge any change."),
            "b": (True, "Parameter adjustment is the lever under test."),
            "c": (True, "Re-measuring on the same queries isolates the effect."),
            "d": (True, "Keeping the change is gated on improvement."),
        },
    },
    {
        "question_id": "d5o-truncation-analysis",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Some answers cut off mid-sentence and you must run a truncation "
            "analysis. Place the steps in the correct order."
        ),
        "scenario_constraint": "Truncation analysis separates output-limit from context causes.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Collect the truncated responses and their request parameters."),
            ("b", "Check whether the max output tokens were exhausted."),
            ("c", "Check whether the input plus context filled the window."),
            ("d", "Raise the correct limit or shorten the input for the identified cause."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Truncated samples are collected, the output-token cause is checked, "
            "then the context-window cause, and the matching remedy is applied."
        ),
        "rationales": {
            "a": (True, "The samples and parameters are the evidence base."),
            "b": (True, "Output-token exhaustion is the first cause to rule in or out."),
            "c": (True, "Context-window fill is the second candidate cause."),
            "d": (True, "The remedy depends on which cause was identified."),
        },
    },
    {
        "question_id": "d5o-prompt-confusion-logs",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A model is ignoring part of its instructions and you suspect prompt "
            "confusion. Place the troubleshooting steps in the correct order."
        ),
        "scenario_constraint": "Prompt confusion is diagnosed from the logged assembled prompt.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Pull the fully assembled prompt from CloudWatch Logs."),
            ("b", "Spot conflicting or buried instructions in the assembled prompt."),
            ("c", "Restructure the prompt to separate and order the instructions."),
            ("d", "Re-test the previously failing cases for compliance."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "The assembled prompt is pulled from logs, conflicting instructions "
            "are spotted, the prompt is restructured, and the failing cases are "
            "re-tested."
        ),
        "rationales": {
            "a": (True, "You must see the real assembled prompt to diagnose it."),
            "b": (True, "Spotting the conflict localizes the confusion."),
            "c": (True, "Restructuring is the remediation after diagnosis."),
            "d": (True, "Re-testing confirms the instructions are now followed."),
        },
    },
    {
        "question_id": "d5o-xray-latency",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A RAG request is slow end to end and you use AWS X-Ray to find "
            "where the time goes. Place the steps in the correct order."
        ),
        "scenario_constraint": "Latency is attributed to a segment before anything is optimized.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Open the X-Ray trace for a slow request."),
            ("b", "Find the segment with the largest duration."),
            ("c", "Optimize that specific segment, such as retrieval or generation."),
            ("d", "Re-trace to confirm the latency improved."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A slow trace is opened, the dominant segment is found, that segment "
            "is optimized, and a re-trace confirms the improvement."
        ),
        "rationales": {
            "a": (True, "The trace is the evidence for where time is spent."),
            "b": (True, "The slowest segment is the target worth optimizing."),
            "c": (True, "Optimization is scoped to the identified segment."),
            "d": (True, "Re-tracing validates the latency gain."),
        },
    },
    {
        "question_id": "d5o-metric-selection",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You must choose and apply the right automatic metric for a "
            "summarization task. Place the steps in the correct order."
        ),
        "scenario_constraint": "Metric choice precedes scoring and interpretation.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Pick a metric suited to summarization such as ROUGE."),
            ("b", "Score candidate summaries against the reference summaries."),
            ("c", "Interpret the scores against an agreed passing bar."),
            ("d", "Record the decision for the release review."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A fit-for-purpose metric is chosen, candidates are scored against "
            "references, scores are interpreted against a bar, and the decision "
            "is recorded."
        ),
        "rationales": {
            "a": (True, "The metric must be chosen before anything is scored."),
            "b": (True, "Scoring applies the chosen metric to candidates."),
            "c": (True, "Interpretation turns raw scores into a verdict."),
            "d": (True, "Recording the decision closes the review step."),
        },
    },
    {
        "question_id": "d5o-multi-model-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are running a multi-model evaluation to find the best price-"
            "performance option. Place the steps in the correct order."
        ),
        "scenario_constraint": "Price-performance is compared only after quality is scored.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Run every candidate model on the shared eval set."),
            ("b", "Score each candidate's answer quality."),
            ("c", "Pair each quality score with the model's cost per request."),
            ("d", "Select the best price-performance model."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Each model runs on the shared set, quality is scored, cost is paired "
            "with quality, and the best price-performance model is selected."
        ),
        "rationales": {
            "a": (True, "All candidates must run on one set to be comparable."),
            "b": (True, "Quality scoring precedes any cost pairing."),
            "c": (True, "Cost is paired with quality to judge price-performance."),
            "d": (True, "Selection is the final price-performance decision."),
        },
    },
    {
        "question_id": "d5o-semantic-drift-monitor",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are adding semantic-drift monitoring to catch silent quality "
            "decay after deploy. Place the steps in the correct order."
        ),
        "scenario_constraint": "Drift monitoring needs a reference distribution to compare.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Capture a reference distribution of outputs at a healthy baseline."),
            ("b", "Continuously sample live outputs after deploy."),
            ("c", "Compare the live sample distribution to the reference."),
            ("d", "Alert when the divergence crosses the drift threshold."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A healthy reference is captured, live outputs are sampled, the two "
            "distributions are compared, and an alert fires when divergence "
            "crosses the threshold."
        ),
        "rationales": {
            "a": (True, "The reference is the baseline drift is measured against."),
            "b": (True, "Live sampling supplies the current distribution."),
            "c": (True, "Comparison quantifies the divergence."),
            "d": (True, "The alert acts on the measured drift."),
        },
    },
    {
        "question_id": "d5o-chunking-remediation",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Retrieved chunks split answers across boundaries and lose context. "
            "Place the chunking-remediation steps in the correct order."
        ),
        "scenario_constraint": "Chunking changes are validated on the same failing queries.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Confirm answers are split across chunk boundaries."),
            ("b", "Adjust chunk size and overlap or move to hierarchical chunking."),
            ("c", "Re-ingest and re-index the corpus with the new chunking."),
            ("d", "Re-run the failing queries to confirm whole answers return."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "The boundary split is confirmed, chunking is adjusted, the corpus "
            "is re-ingested, and the failing queries are re-run to validate."
        ),
        "rationales": {
            "a": (True, "Confirming the split scopes the remediation."),
            "b": (True, "Chunking adjustment is the fix under test."),
            "c": (True, "Re-indexing applies the new chunking to the corpus."),
            "d": (True, "Re-running the queries validates the result."),
        },
    },
    {
        "question_id": "d5o-vectorization-check",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "New documents are never retrieved and you suspect a vectorization "
            "failure in the ingestion job. Place the steps in the correct order."
        ),
        "scenario_constraint": "Vectorization is verified in the index before tuning search.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Confirm the new documents are absent from query results."),
            ("b", "Check whether their vectors exist in the index."),
            ("c", "Fix the ingestion so the documents are embedded and indexed."),
            ("d", "Query again to confirm the documents now retrieve."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Absence is confirmed, the index is checked for the vectors, "
            "ingestion is fixed to embed and index them, and a re-query confirms "
            "retrieval."
        ),
        "rationales": {
            "a": (True, "Confirming absence starts the diagnosis."),
            "b": (True, "Checking the index localizes the fault to vectorization."),
            "c": (True, "Fixing ingestion embeds and indexes the documents."),
            "d": (True, "The re-query validates the fix."),
        },
    },
    {
        "question_id": "d5o-retrieval-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are measuring retrieval quality independently of generation. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "Retrieval eval uses labeled relevant documents per query.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Label the relevant documents for a set of queries."),
            ("b", "Run retrieval and capture the top results per query."),
            ("c", "Compute relevance and context-match metrics against the labels."),
            ("d", "Report retrieval quality separately from answer quality."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Relevant documents are labeled, retrieval results are captured, "
            "relevance and context-match are computed, and retrieval quality is "
            "reported on its own."
        ),
        "rationales": {
            "a": (True, "Labels are the ground truth retrieval is scored against."),
            "b": (True, "Captured results are what the metrics consume."),
            "c": (True, "Metrics compare results to the labels."),
            "d": (True, "Separate reporting isolates retrieval from generation."),
        },
    },
    {
        "question_id": "d5o-synthetic-canary-monitor",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You add a CloudWatch Synthetics canary that exercises the GenAI "
            "endpoint on a schedule. Place the steps in the correct order."
        ),
        "scenario_constraint": "A synthetics canary runs a scripted journey and alarms on failure.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Script the canary to send a known prompt and assert the answer."),
            ("b", "Schedule the canary to run at a fixed interval."),
            ("c", "Wire a CloudWatch alarm to the canary success metric."),
            ("d", "Notify on-call when the alarm trips."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "The canary is scripted, scheduled, wired to an alarm on its success "
            "metric, and routed to notify on-call when it trips."
        ),
        "rationales": {
            "a": (True, "The scripted check defines what success means."),
            "b": (True, "Scheduling makes the check run repeatedly."),
            "c": (True, "The alarm watches the canary's success metric."),
            "d": (True, "Notification is the final response to a failure."),
        },
    },
    {
        "question_id": "d5o-output-diffing",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You adopt output diffing to catch unintended changes between model "
            "or prompt versions. Place the steps in the correct order."
        ),
        "scenario_constraint": "Diffing compares two versions on identical inputs.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Save the current version's outputs on a fixed input set as the baseline."),
            ("b", "Produce the new version's outputs on the same inputs."),
            ("c", "Diff the two output sets case by case."),
            ("d", "Review the diffs for regressions before shipping."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A baseline output set is saved, the new version is run on the same "
            "inputs, outputs are diffed per case, and the diffs are reviewed "
            "before shipping."
        ),
        "rationales": {
            "a": (True, "The saved baseline is what the new outputs are diffed against."),
            "b": (True, "Identical inputs make the diff meaningful."),
            "c": (True, "The case-by-case diff surfaces the changes."),
            "d": (True, "Review gates the ship on the diffs."),
        },
    },
    {
        "question_id": "d5o-reasoning-path-trace",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "An agent reaches wrong conclusions and you add reasoning-path "
            "tracing to understand why. Place the steps in the correct order."
        ),
        "scenario_constraint": "Reasoning-path tracing records each step before analysis.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Enable tracing so each reasoning and tool step is recorded."),
            ("b", "Reproduce a wrong conclusion and capture its trace."),
            ("c", "Walk the trace to find the step that went wrong."),
            ("d", "Fix that step, such as the tool or prompt, and re-trace."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Tracing is enabled, a wrong conclusion is reproduced with its trace, "
            "the faulty step is found by walking the trace, and that step is "
            "fixed and re-traced."
        ),
        "rationales": {
            "a": (True, "Tracing must be on to capture the reasoning steps."),
            "b": (True, "A captured trace of a failure is needed to analyze it."),
            "c": (True, "Walking the trace localizes the faulty step."),
            "d": (True, "The fix targets that step and re-tracing validates it."),
        },
    },
    {
        "question_id": "d5o-consistency-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You must measure answer consistency across repeated calls for the "
            "same prompt. Place the steps in the correct order."
        ),
        "scenario_constraint": "Consistency is measured by repeating identical prompts.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Send the same prompt multiple times under the same settings."),
            ("b", "Collect the set of returned answers."),
            ("c", "Score how semantically similar the answers are to each other."),
            ("d", "Adjust temperature or add determinism if consistency is too low."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "The same prompt is repeated, answers are collected, their mutual "
            "similarity is scored, and sampling settings are adjusted if "
            "consistency is too low."
        ),
        "rationales": {
            "a": (True, "Repeated identical calls generate the data."),
            "b": (True, "The collected answers are the measurement input."),
            "c": (True, "Similarity scoring quantifies consistency."),
            "d": (True, "Adjusting settings is the remediation for low consistency."),
        },
    },
    {
        "question_id": "d5o-factual-accuracy-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are measuring factual accuracy of answers against a trusted "
            "reference set. Place the steps in the correct order."
        ),
        "scenario_constraint": "Factual accuracy is judged against verified reference facts.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Curate verified reference facts for each question."),
            ("b", "Generate answers for the question set."),
            ("c", "Check each answer's claims against the verified facts."),
            ("d", "Report the factual-accuracy rate for the set."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Verified facts are curated, answers are generated, each answer is "
            "fact-checked, and the accuracy rate is reported."
        ),
        "rationales": {
            "a": (True, "Verified facts are the reference for accuracy."),
            "b": (True, "Answers must exist to be fact-checked."),
            "c": (True, "Checking claims against facts yields the verdicts."),
            "d": (True, "The accuracy rate aggregates the verdicts."),
        },
    },
    {
        "question_id": "d5o-latency-benchmark",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You benchmark retrieval latency before and after enabling a cache. "
            "Place the steps in the correct order."
        ),
        "scenario_constraint": "A latency benchmark needs a pre-change baseline.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Measure baseline retrieval latency without the cache."),
            ("b", "Enable the cache."),
            ("c", "Measure latency again with the cache under the same load."),
            ("d", "Compare the two measurements to quantify the gain."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Baseline latency is measured, the cache is enabled, latency is "
            "re-measured under the same load, and the two are compared."
        ),
        "rationales": {
            "a": (True, "The baseline is needed to judge the cache's effect."),
            "b": (True, "Enabling the cache is the change under test."),
            "c": (True, "Re-measuring under the same load isolates the effect."),
            "d": (True, "Comparison quantifies the latency gain."),
        },
    },
    {
        "question_id": "d5o-model-invocation-logs",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Quality complaints lack detail and you turn on Bedrock model "
            "invocation logging to investigate. Place the steps in the correct "
            "order."
        ),
        "scenario_constraint": "Invocation logging must be on before incidents are inspected.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Enable Bedrock model invocation logging to a destination."),
            ("b", "Wait for a complaint and locate its invocation record."),
            ("c", "Inspect the recorded prompt and response for the defect."),
            ("d", "Feed the finding into a targeted prompt or retrieval fix."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Logging is enabled, the complaint's record is located, its prompt "
            "and response are inspected, and the finding drives a targeted fix."
        ),
        "rationales": {
            "a": (True, "Logging must be on before any record exists to inspect."),
            "b": (True, "Locating the record ties the complaint to real data."),
            "c": (True, "Inspection reveals the defect in the logged exchange."),
            "d": (True, "The fix is driven by what the inspection found."),
        },
    },
    {
        "question_id": "d5o-annotation-workflow",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You set up a human annotation workflow with Amazon SageMaker Ground "
            "Truth to label answer quality. Place the steps in the correct "
            "order."
        ),
        "scenario_constraint": "Annotation needs a defined rubric before labeling starts.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Define a labeling rubric for answer quality."),
            ("b", "Create a Ground Truth labeling job over sampled answers."),
            ("c", "Collect the human labels from the completed job."),
            ("d", "Use the labels as references for automated evaluation."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A rubric is defined, a labeling job runs, labels are collected, and "
            "they become references for automated evaluation."
        ),
        "rationales": {
            "a": (True, "A rubric standardizes what labelers judge."),
            "b": (True, "The labeling job applies the rubric to samples."),
            "c": (True, "Labels are collected once the job completes."),
            "d": (True, "The labels anchor downstream automated eval."),
        },
    },
    {
        "question_id": "d5o-continuous-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You are standing up continuous evaluation that runs on every model "
            "update. Place the steps in the correct order."
        ),
        "scenario_constraint": "Continuous eval triggers automatically and gates on results.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Trigger the eval suite whenever a model or prompt version changes."),
            ("b", "Run the suite against the golden set automatically."),
            ("c", "Publish the scores and trend to a dashboard."),
            ("d", "Block promotion when scores fall below the quality gate."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "A version change triggers the suite, it runs on the golden set, "
            "scores and trends publish, and promotion is blocked below the gate."
        ),
        "rationales": {
            "a": (True, "The trigger is what makes evaluation continuous."),
            "b": (True, "The automated run produces the scores."),
            "c": (True, "Publishing exposes the trend for oversight."),
            "d": (True, "The gate blocks regressions from promoting."),
        },
    },
    {
        "question_id": "d5o-query-preprocess-fix",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Short, ambiguous user queries retrieve poorly and you add query "
            "preprocessing. Place the steps in the correct order."
        ),
        "scenario_constraint": "Preprocessing is validated on the queries that failed.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Identify the ambiguous queries that retrieve poorly."),
            ("b", "Add query expansion or rewriting before retrieval."),
            ("c", "Re-run retrieval on those queries with preprocessing."),
            ("d", "Confirm relevance improved on the previously poor queries."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Poorly performing queries are identified, preprocessing is added, "
            "retrieval is re-run on them, and improved relevance is confirmed."
        ),
        "rationales": {
            "a": (True, "Identifying bad queries scopes the change and its test."),
            "b": (True, "Expansion or rewriting is the remediation."),
            "c": (True, "Re-running on the same queries isolates the effect."),
            "d": (True, "Confirming improvement validates the change."),
        },
    },
    {
        "question_id": "d5o-synthetic-data-gen",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Coverage of rare edge cases is thin, so you expand the eval set with "
            "synthetic cases. Place the steps in the correct order."
        ),
        "scenario_constraint": "Synthetic cases are reviewed before entering the eval set.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Identify the edge-case categories lacking coverage."),
            ("b", "Generate synthetic prompts and reference answers for them."),
            ("c", "Review the synthetic cases for correctness."),
            ("d", "Add the reviewed cases to the golden set."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Gaps are identified, synthetic cases are generated for them, the "
            "cases are reviewed for correctness, and the reviewed ones join the "
            "golden set."
        ),
        "rationales": {
            "a": (True, "Coverage gaps tell you what to generate."),
            "b": (True, "Generation produces the candidate cases."),
            "c": (True, "Review keeps incorrect cases out of the set."),
            "d": (True, "Only reviewed cases are added to the golden set."),
        },
    },
    {
        "question_id": "d5o-concurrency-error-fix",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Under load the Bedrock integration throws throttling errors and "
            "fails requests. Place the troubleshooting steps in the correct "
            "order."
        ),
        "scenario_constraint": "Throttling is confirmed from errors before changing concurrency.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Confirm from logs that the failures are throttling errors."),
            ("b", "Add exponential backoff with jitter on retry."),
            ("c", "Cap client concurrency to the available throughput."),
            ("d", "Load-test again to confirm throttling errors clear."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Throttling is confirmed from logs, backoff with jitter is added, "
            "concurrency is capped to throughput, and a load test confirms the "
            "errors clear."
        ),
        "rationales": {
            "a": (True, "Confirming the error class avoids treating the wrong cause."),
            "b": (True, "Backoff smooths retries against the limit."),
            "c": (True, "Capping concurrency keeps load within throughput."),
            "d": (True, "Re-load-testing validates the fix."),
        },
    },
    {
        "question_id": "d5o-golden-regression-gate",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You convert a critical bug's fixed cases into permanent regression "
            "guards. Place the steps in the correct order."
        ),
        "scenario_constraint": "Regression guards are added to the eval set after a fix lands.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Capture the inputs that triggered the bug and their correct answers."),
            ("b", "Add those cases to the golden regression set."),
            ("c", "Wire the set into the quality gate so they always run."),
            ("d", "Confirm a reintroduced bug would now fail the gate."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "The bug's cases and correct answers are captured, added to the "
            "golden set, wired into the gate, and shown to catch a regression."
        ),
        "rationales": {
            "a": (True, "The triggering cases define the guard."),
            "b": (True, "Adding them to the set makes them durable."),
            "c": (True, "Wiring into the gate enforces them on every change."),
            "d": (True, "A failing-on-regression check proves the guard works."),
        },
    },
    {
        "question_id": "d5o-tool-call-observability",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You add observability to an agent's tool calls to catch failures "
            "early. Place the steps in the correct order."
        ),
        "scenario_constraint": "Tool-call metrics must be emitted before they can be alarmed on.",
        "difficulty": "medium",
        "question_format": "ordering",
        "options": [
            ("a", "Emit a metric for each tool call's success and latency."),
            ("b", "Build a CloudWatch dashboard of tool-call health."),
            ("c", "Set alarms on error rate and latency thresholds."),
            ("d", "Route alarms to the on-call channel."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Tool-call metrics are emitted, a dashboard is built, alarms are set "
            "on thresholds, and alarms route to on-call."
        ),
        "rationales": {
            "a": (True, "Metrics are the raw data everything else needs."),
            "b": (True, "The dashboard visualizes the emitted metrics."),
            "c": (True, "Alarms act on thresholds over those metrics."),
            "d": (True, "Routing makes the alarms actionable."),
        },
    },
    {
        "question_id": "d5o-fluency-eval",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "You add a fluency check to flag garbled or repetitive output. Place "
            "the steps in the correct order."
        ),
        "scenario_constraint": "Fluency scoring runs over generated samples before flagging.",
        "difficulty": "easy",
        "question_format": "ordering",
        "options": [
            ("a", "Sample recent generated answers."),
            ("b", "Score each sample for fluency and repetition."),
            ("c", "Flag samples below the fluency bar for review."),
            ("d", "Track the fluency rate on the monitoring dashboard."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Answers are sampled, scored for fluency, low scorers are flagged, "
            "and the rate is tracked on a dashboard."
        ),
        "rationales": {
            "a": (True, "Samples are the input to fluency scoring."),
            "b": (True, "Scoring produces the fluency verdicts."),
            "c": (True, "Flagging routes poor samples to review."),
            "d": (True, "Tracking the rate gives an ongoing signal."),
        },
    },
    {
        "question_id": "d5o-index-optimization",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Vector queries have grown slow as the index expanded and you must "
            "optimize it. Place the steps in the correct order."
        ),
        "scenario_constraint": "Index optimization is validated against a latency baseline.",
        "difficulty": "hard",
        "question_format": "ordering",
        "options": [
            ("a", "Measure current vector query latency as a baseline."),
            ("b", "Apply index optimization such as parameter or shard tuning."),
            ("c", "Re-measure latency under the same query mix."),
            ("d", "Keep the optimization if latency dropped without hurting recall."),
        ],
        "correct_sequence": ["a", "b", "c", "d"],
        "correct_option_ids": [],
        "explanation": (
            "Baseline latency is measured, the index is optimized, latency is "
            "re-measured under the same mix, and the change is kept only if it "
            "helps without hurting recall."
        ),
        "rationales": {
            "a": (True, "A baseline is needed to judge the optimization."),
            "b": (True, "Index tuning is the change under test."),
            "c": (True, "Re-measuring under the same mix isolates the effect."),
            "d": (True, "Keeping the change is gated on net benefit."),
        },
    },
    {
        "question_id": "d5m-metric-to-meaning",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each automatic evaluation metric to what it primarily "
            "measures. Match each item to the correct option."
        ),
        "scenario_constraint": "Pick the right metric for each quality dimension.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Overlap of generated summary with reference summaries"),
            ("p2", "N-gram precision of machine translation against references"),
            ("p3", "Exact string equality with the reference answer"),
            ("p4", "Semantic similarity using contextual embeddings"),
        ],
        "match_responses": [
            ("r1", "ROUGE"),
            ("r2", "BLEU"),
            ("r3", "Exact match"),
            ("r4", "BERTScore"),
            ("r5", "Latency"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "ROUGE scores summary overlap, BLEU scores translation n-gram "
            "precision, exact match requires identical strings, and BERTScore "
            "uses embeddings for semantic similarity; latency is a distractor."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-symptom-to-layer",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each RAG symptom to the layer most likely at fault. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Localize each symptom to retrieval, generation, or integration.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Correct chunks are retrieved but the answer invents facts"),
            ("p2", "The right documents never appear in the retrieved set"),
            ("p3", "Answers cut off mid-sentence on long inputs"),
            ("p4", "The downstream service rejects the model's JSON"),
        ],
        "match_responses": [
            ("r1", "Generation and prompting"),
            ("r2", "Retrieval and indexing"),
            ("r3", "Context-window limits"),
            ("r4", "Schema and integration"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Invented facts despite good chunks point to generation, missing "
            "documents point to retrieval, mid-sentence cutoffs point to context "
            "limits, and rejected JSON points to schema and integration."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-technique-to-when",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each evaluation technique to the situation where it fits best. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Choose the evaluation technique for each goal.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Scoring open-ended answer quality at scale without references"),
            ("p2", "Choosing between two prompts on live traffic"),
            ("p3", "Catching quality regressions before release"),
            ("p4", "Exposing a new version to a small slice before full rollout"),
        ],
        "match_responses": [
            ("r1", "LLM-as-a-judge"),
            ("r2", "A/B testing"),
            ("r3", "Regression testing"),
            ("r4", "Canary release"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "An LLM judge scales reference-free scoring, A/B testing compares on "
            "live traffic, regression testing guards releases, and a canary "
            "limits exposure during rollout."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-service-to-eval-role",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each evaluation or monitoring need to the AWS service that "
            "serves it. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each need to its AWS service.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Run managed model evaluation jobs on foundation models"),
            ("p2", "Chart token usage and hallucination-rate metrics"),
            ("p3", "Scheduled synthetic checks against the live endpoint"),
            ("p4", "Trace request latency across the RAG call path"),
        ],
        "match_responses": [
            ("r1", "Amazon Bedrock Model Evaluations"),
            ("r2", "Amazon CloudWatch"),
            ("r3", "Amazon CloudWatch Synthetics"),
            ("r4", "AWS X-Ray"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Bedrock Model Evaluations runs eval jobs, CloudWatch charts metrics, "
            "CloudWatch Synthetics runs scheduled canaries, and X-Ray traces the "
            "call path."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-retrieval-metric",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each retrieval evaluation concern to the metric that captures "
            "it. Match each item to the correct option."
        ),
        "scenario_constraint": "Pick the retrieval metric for each concern.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Did we return the documents labeled relevant?"),
            ("p2", "Do the retrieved chunks actually contain the answer context?"),
            ("p3", "How fast did retrieval return results?"),
        ],
        "match_responses": [
            ("r1", "Relevance"),
            ("r2", "Context match"),
            ("r3", "Retrieval latency"),
            ("r4", "Token cost"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Relevance checks that labeled documents were returned, context match "
            "checks that chunks carry the answer, and retrieval latency measures "
            "speed; token cost is unrelated to retrieval quality here."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-chunking-symptom",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each retrieval diagnostic signal to its most likely root "
            "cause. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each diagnostic signal to its cause.",
        "difficulty": "hard",
        "match_prompts": [
            ("p1", "Answers split across chunk boundaries and lose context"),
            ("p2", "Relevance declined slowly over weeks with no code change"),
            ("p3", "New documents are never retrieved at all"),
        ],
        "question_format": "matching",
        "match_responses": [
            ("r1", "Poor chunk size or overlap"),
            ("r2", "Embedding drift"),
            ("r3", "Failed vectorization during ingestion"),
            ("r4", "Oversized context window"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Boundary splits point to chunking, slow silent decline points to "
            "embedding drift, and totally missing documents point to failed "
            "vectorization."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-rollout-strategy",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each rollout goal to the deployment-validation strategy that "
            "meets it. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each rollout goal to a validation strategy.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Limit blast radius by exposing a few percent of traffic first"),
            ("p2", "Decide a winner between two variants on real users"),
            ("p3", "Exercise full user journeys before any real traffic"),
        ],
        "match_responses": [
            ("r1", "Canary release"),
            ("r2", "A/B test"),
            ("r3", "Synthetic workflow validation"),
            ("r4", "Load test"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A canary limits exposure, an A/B test picks a winner on real users, "
            "and synthetic workflow validation exercises journeys before live "
            "traffic."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-log-tool-to-use",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each troubleshooting question to the observability tool that "
            "answers it. Match each item to the correct option."
        ),
        "scenario_constraint": "Pick the observability tool for each question.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "What exact prompt did the model receive?"),
            ("p2", "Which segment of the request was slowest?"),
            ("p3", "What raw prompt and response did Bedrock log for this call?"),
        ],
        "match_responses": [
            ("r1", "Amazon CloudWatch Logs"),
            ("r2", "AWS X-Ray"),
            ("r3", "Bedrock model invocation logs"),
            ("r4", "Amazon QuickSight"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "CloudWatch Logs show the assembled prompt, X-Ray shows per-segment "
            "latency, and Bedrock invocation logs capture the raw prompt and "
            "response."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-judge-pitfall",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each LLM-as-a-judge practice to its purpose. Match each item "
            "to the correct option."
        ),
        "scenario_constraint": "Map each judge practice to why it matters.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Compare judge scores to human labels on a sample"),
            ("p2", "Use a fixed rubric and scoring scale in the judge prompt"),
            ("p3", "Re-check agreement periodically after deploy"),
        ],
        "match_responses": [
            ("r1", "Calibrate the judge against ground truth"),
            ("r2", "Make scoring consistent and repeatable"),
            ("r3", "Detect judge drift over time"),
            ("r4", "Reduce token cost per call"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Comparing to human labels calibrates the judge, a fixed rubric makes "
            "scoring repeatable, and periodic re-checks detect drift; cost "
            "reduction is a distractor."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-error-class-remedy",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each API error class to the appropriate remedy. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Map each error class to its correct remedy.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Throttling errors under burst load"),
            ("p2", "Validation errors on the request payload"),
            ("p3", "Transient server errors"),
        ],
        "match_responses": [
            ("r1", "Exponential backoff and concurrency limits"),
            ("r2", "Fix and validate the payload schema"),
            ("r3", "Retry with jitter and a fallback path"),
            ("r4", "Rotate IAM credentials"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Throttling calls for backoff and concurrency limits, validation "
            "errors call for payload fixes, and transient server errors call for "
            "retry with a fallback; credential rotation is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-eval-dim-definition",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each answer-quality dimension to its definition. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Map each quality dimension to its definition.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "The answer's claims are true"),
            ("p2", "Repeated calls give similar answers"),
            ("p3", "The answer addresses what was asked"),
            ("p4", "The answer reads naturally without garbling"),
        ],
        "match_responses": [
            ("r1", "Factual accuracy"),
            ("r2", "Consistency"),
            ("r3", "Relevance"),
            ("r4", "Fluency"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Factual accuracy is truth of claims, consistency is stability across "
            "calls, relevance is addressing the question, and fluency is natural "
            "readable text."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-monitor-metric-signal",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each production monitoring signal to what it warns about. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each monitored signal to its warning.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Rising hallucination rate"),
            ("p2", "Growing semantic divergence from the baseline distribution"),
            ("p3", "Climbing token usage per request"),
        ],
        "match_responses": [
            ("r1", "Answers increasingly ungrounded"),
            ("r2", "Output behavior is drifting"),
            ("r3", "Cost is trending up"),
            ("r4", "Index needs re-sharding"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A rising hallucination rate warns of ungrounded answers, growing "
            "divergence warns of drift, and climbing token usage warns of rising "
            "cost."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-truncation-cause",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each truncation finding to the remedy that addresses it. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each truncation cause to its remedy.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Max output tokens were exhausted"),
            ("p2", "Input plus retrieved context filled the window"),
            ("p3", "A downstream parser stopped at an unescaped character"),
        ],
        "match_responses": [
            ("r1", "Raise the max output tokens"),
            ("r2", "Apply dynamic chunking to shrink context"),
            ("r3", "Add output schema validation and escaping"),
            ("r4", "Switch AWS Region"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Exhausted output tokens call for a higher output limit, a full "
            "window calls for dynamic chunking, and a parser stop calls for "
            "schema validation and escaping."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-feedback-source",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each feedback source to the evaluation role it plays. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Map each feedback source to its role.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Expert human labels on a curated sample"),
            ("p2", "Thumbs-up and thumbs-down from end users"),
            ("p3", "Automatic metric scores against references"),
        ],
        "match_responses": [
            ("r1", "Ground-truth references and judge calibration"),
            ("r2", "Live quality signal from real usage"),
            ("r3", "Scalable offline scoring"),
            ("r4", "Billing reconciliation"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Expert labels provide ground truth, user ratings give a live signal, "
            "and automatic metrics give scalable offline scoring; billing is a "
            "distractor."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-agent-eval-dim",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each agent evaluation dimension to what it assesses. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Map each agent dimension to its assessment.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Did the agent finish the assigned task?"),
            ("p2", "Did it call the right tools with valid arguments?"),
            ("p3", "Were its intermediate reasoning steps sound?"),
        ],
        "match_responses": [
            ("r1", "Task completion"),
            ("r2", "Tool-usage correctness"),
            ("r3", "Reasoning quality"),
            ("r4", "Embedding dimensionality"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Task completion checks the outcome, tool-usage correctness checks "
            "the calls, and reasoning quality checks the intermediate steps; "
            "embedding dimensionality is a distractor."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-gate-decision",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each quality-gate outcome to the correct pipeline action. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each gate outcome to its action.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Scores at or above the threshold"),
            ("p2", "A required regression case now fails"),
            ("p3", "Scores just below the threshold with no clear cause"),
        ],
        "match_responses": [
            ("r1", "Allow promotion to proceed"),
            ("r2", "Block the pipeline"),
            ("r3", "Hold for manual review"),
            ("r4", "Delete the golden set"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Passing scores allow promotion, a failed required case blocks the "
            "pipeline, and a borderline unexplained result holds for review; "
            "deleting the golden set is never correct."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-rag-eval-metric",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each RAG evaluation focus to the metric that captures it. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each RAG focus to its metric.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Are the generated claims supported by retrieved context?"),
            ("p2", "Did retrieval surface the labeled relevant passages?"),
            ("p3", "Does the final answer address the user question?"),
        ],
        "match_responses": [
            ("r1", "Groundedness or faithfulness"),
            ("r2", "Retrieval relevance"),
            ("r3", "Answer relevance"),
            ("r4", "Provisioned throughput"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Groundedness checks claim support, retrieval relevance checks the "
            "passages surfaced, and answer relevance checks the final answer; "
            "provisioned throughput is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-prompt-test-activity",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each prompt-testing activity to its purpose. Match each item "
            "to the correct option."
        ),
        "scenario_constraint": "Map each prompt-testing activity to its goal.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Run old and new prompt versions on one fixed set"),
            ("p2", "Assert the output matches a required JSON schema"),
            ("p3", "Inspect the fully assembled prompt in the logs"),
        ],
        "match_responses": [
            ("r1", "Version comparison"),
            ("r2", "Schema validation"),
            ("r3", "Prompt-confusion diagnosis"),
            ("r4", "Index re-sharding"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Running both versions on one set is version comparison, asserting "
            "the schema is schema validation, and inspecting the assembled "
            "prompt diagnoses prompt confusion."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-dashboard-metric",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each GenAI dashboard metric to the category it belongs to. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each metric to its observability category.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "P95 end-to-end response time"),
            ("p2", "Tokens consumed per request"),
            ("p3", "Hallucination rate on sampled answers"),
            ("p4", "Questions answered per session"),
        ],
        "match_responses": [
            ("r1", "Performance"),
            ("r2", "Cost"),
            ("r3", "Quality"),
            ("r4", "Business"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Response time is performance, token usage is cost, hallucination "
            "rate is quality, and questions per session is a business metric."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-validation-boundary",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each validation check to the deployment stage where it runs. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each check to its stage.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Eval suite on the golden set in the pipeline"),
            ("p2", "Synthetic user journeys against the deployed endpoint"),
            ("p3", "Canary metrics on a small live traffic slice"),
        ],
        "match_responses": [
            ("r1", "Pre-deploy quality gate"),
            ("r2", "Post-deploy validation"),
            ("r3", "Progressive rollout"),
            ("r4", "Model fine-tuning"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "The golden-set eval is the pre-deploy gate, synthetic journeys are "
            "post-deploy validation, and canary metrics are the progressive "
            "rollout stage; fine-tuning is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-embedding-diagnostic",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each embedding diagnostic to what it reveals. Match each item "
            "to the correct option."
        ),
        "scenario_constraint": "Map each embedding diagnostic to its finding.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Compare current vectors to a healthy-period snapshot"),
            ("p2", "Confirm a document's vector is present in the index"),
            ("p3", "Measure nearest-neighbor distances for a known query"),
        ],
        "match_responses": [
            ("r1", "Whether embeddings have drifted"),
            ("r2", "Whether vectorization succeeded"),
            ("r3", "Whether similarity ranking is sane"),
            ("r4", "Whether the KMS key rotated"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Snapshot comparison reveals drift, presence in the index reveals "
            "vectorization success, and neighbor distances reveal ranking "
            "sanity; key rotation is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-canary-vs-regression",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each testing concept to its defining trait. Match each item to "
            "the correct option."
        ),
        "scenario_constraint": "Map each testing concept to its defining trait.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Ensures previously fixed behavior still holds"),
            ("p2", "Serves a small percentage of live traffic first"),
            ("p3", "Blocks a release when a metric falls below a bar"),
        ],
        "match_responses": [
            ("r1", "Regression testing"),
            ("r2", "Canary release"),
            ("r3", "Quality gate"),
            ("r4", "Data labeling"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Regression testing protects fixed behavior, a canary serves a small "
            "slice, and a quality gate blocks on a metric; data labeling is a "
            "distractor."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-hallucination-tool",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each hallucination-control task to its AWS service or "
            "technique. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each hallucination task to the right mechanism.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Ground answers in retrieved source documents"),
            ("p2", "Score ungrounded claims across an eval set"),
            ("p3", "Track hallucination rate on a live dashboard"),
        ],
        "match_responses": [
            ("r1", "Amazon Bedrock Knowledge Bases"),
            ("r2", "LLM-as-a-judge groundedness scoring"),
            ("r3", "Amazon CloudWatch"),
            ("r4", "Amazon Rekognition"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Knowledge Bases grounds answers in sources, a judge scores "
            "groundedness, and CloudWatch tracks the rate; Rekognition is "
            "unrelated to text grounding here."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-latency-segment",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each slow X-Ray segment to the optimization it suggests. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each slow segment to its optimization.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Vector query dominates the trace"),
            ("p2", "Model generation dominates the trace"),
            ("p3", "External tool call dominates the trace"),
        ],
        "match_responses": [
            ("r1", "Optimize the index and query parameters"),
            ("r2", "Use a latency-optimized model or streaming"),
            ("r3", "Cache or parallelize the tool call"),
            ("r4", "Increase the embedding dimension"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A slow vector query points to index tuning, slow generation points "
            "to a faster model or streaming, and a slow tool call points to "
            "caching or parallelism."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-synthetic-service",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each ongoing validation need to the AWS capability that meets "
            "it. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each ongoing need to its AWS capability.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Scheduled canary that asserts the endpoint still answers"),
            ("p2", "Alarm when a quality metric crosses a threshold"),
            ("p3", "Visual dashboard of quality and cost trends"),
        ],
        "match_responses": [
            ("r1", "Amazon CloudWatch Synthetics"),
            ("r2", "Amazon CloudWatch alarms"),
            ("r3", "Amazon CloudWatch dashboards"),
            ("r4", "AWS Glue Data Quality"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Synthetics runs the scheduled canary, CloudWatch alarms fire on "
            "thresholds, and CloudWatch dashboards show trends; Glue Data "
            "Quality validates input data, not live endpoints."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-regression-artifact",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each evaluation artifact to its role in the workflow. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Map each artifact to its role.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Frozen prompts with reference answers"),
            ("p2", "Saved outputs from the current version"),
            ("p3", "A minimum score the release must clear"),
        ],
        "match_responses": [
            ("r1", "Golden dataset"),
            ("r2", "Baseline outputs"),
            ("r3", "Quality threshold"),
            ("r4", "IAM policy"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "The golden dataset is the frozen reference, baseline outputs are the "
            "comparison point, and the quality threshold is the pass bar; an IAM "
            "policy is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-context-overflow-signal",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each observed behavior to the context-related cause it "
            "indicates. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each behavior to its context-related cause.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Answer stops abruptly on very long inputs"),
            ("p2", "Model ignores early instructions on long prompts"),
            ("p3", "Only the last retrieved chunks influence the answer"),
        ],
        "match_responses": [
            ("r1", "Context-window overflow"),
            ("r2", "Instruction lost in a crowded prompt"),
            ("r3", "Context truncated to the tail"),
            ("r4", "Cold start latency"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "An abrupt stop signals overflow, ignored early instructions signal a "
            "lost instruction in a crowded prompt, and tail-only influence "
            "signals truncation to the tail."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-metric-vs-method",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each evaluation question to whether a reference-based metric "
            "or a judge fits best. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each question to the better scoring method.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Exact answer with one correct string"),
            ("p2", "Open-ended answer with many valid phrasings"),
            ("p3", "Translation quality against a reference"),
        ],
        "match_responses": [
            ("r1", "Exact match"),
            ("r2", "LLM-as-a-judge"),
            ("r3", "BLEU"),
            ("r4", "Provisioned throughput"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "A single correct string fits exact match, open-ended answers fit a "
            "judge, and translation against a reference fits BLEU; provisioned "
            "throughput is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-observability-layer",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each observability focus to the thing it tracks. Match each "
            "item to the correct option."
        ),
        "scenario_constraint": "Map each observability focus to its target.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "FM interaction tracing"),
            ("p2", "Multi-agent coordination tracing"),
            ("p3", "Vector store monitoring"),
        ],
        "match_responses": [
            ("r1", "Prompt and response per model call"),
            ("r2", "Handoffs between cooperating agents"),
            ("r3", "Index health and query performance"),
            ("r4", "Billing invoices"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "FM interaction tracing tracks per-call prompts and responses, "
            "multi-agent tracing tracks handoffs, and vector store monitoring "
            "tracks index health; invoices are a distractor."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-golden-vs-synthetic",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each dataset type to its primary purpose in evaluation. Match "
            "each item to the correct option."
        ),
        "scenario_constraint": "Map each dataset type to its purpose.",
        "difficulty": "easy",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Curated real prompts with reviewed references"),
            ("p2", "Generated prompts covering rare edge cases"),
            ("p3", "Cases that previously exposed a shipped bug"),
        ],
        "match_responses": [
            ("r1", "Golden dataset"),
            ("r2", "Synthetic coverage set"),
            ("r3", "Regression set"),
            ("r4", "Training corpus"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Curated real prompts form the golden dataset, generated edge cases "
            "form a synthetic coverage set, and prior-bug cases form the "
            "regression set; a training corpus is for model training."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-fault-isolation-step",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each troubleshooting principle to the action that embodies it. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each principle to the matching action.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Make the failure happen on demand"),
            ("p2", "Change one thing at a time from a baseline"),
            ("p3", "Prove the fix with the original failing case"),
        ],
        "match_responses": [
            ("r1", "Reproduce reliably"),
            ("r2", "Isolate a single variable"),
            ("r3", "Validate recovery"),
            ("r4", "Scale out the fleet"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Making the failure repeatable is reproduction, changing one thing is "
            "variable isolation, and re-testing the failing case is validation; "
            "scaling out is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-cost-quality-metric",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each selection criterion to the measurement that informs it. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each selection criterion to its measurement.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "How good are the answers?"),
            ("p2", "How much does each request cost?"),
            ("p3", "How fast does it respond?"),
        ],
        "match_responses": [
            ("r1", "Quality score on the eval set"),
            ("r2", "Cost per request in tokens"),
            ("r3", "Response latency"),
            ("r4", "Number of IAM roles"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Answer quality is the eval score, cost is per-request tokens, and "
            "speed is latency; IAM role count is a distractor."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-drift-response",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each drift finding to the corrective action it warrants. "
            "Match each item to the correct option."
        ),
        "scenario_constraint": "Map each drift finding to its corrective action.",
        "difficulty": "hard",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Embedding drift degraded retrieval relevance"),
            ("p2", "Output distribution diverged from baseline"),
            ("p3", "New source documents are stale in the index"),
        ],
        "match_responses": [
            ("r1", "Re-embed and re-index the corpus"),
            ("r2", "Investigate model or prompt changes"),
            ("r3", "Re-sync the knowledge base"),
            ("r4", "Delete the audit logs"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Embedding drift warrants re-embedding, output divergence warrants "
            "investigating model or prompt changes, and stale sources warrant a "
            "re-sync; deleting audit logs is never correct."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-eval-stage-service",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Match each CI/CD evaluation activity to the AWS service that runs "
            "it. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each CI/CD activity to its AWS service.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Orchestrate the build and eval stages"),
            ("p2", "Execute the eval suite inside a build step"),
            ("p3", "Store the eval report artifacts"),
        ],
        "match_responses": [
            ("r1", "AWS CodePipeline"),
            ("r2", "AWS CodeBuild"),
            ("r3", "Amazon S3"),
            ("r4", "Amazon Lex"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "CodePipeline orchestrates stages, CodeBuild runs the eval suite, and "
            "S3 stores the report artifacts; Lex is unrelated."
        ),
        "rationales": {},
    },
    {
        "question_id": "d5m-troubleshoot-evidence",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "Match each troubleshooting evidence source to the fault it helps "
            "confirm. Match each item to the correct option."
        ),
        "scenario_constraint": "Map each evidence source to the fault it confirms.",
        "difficulty": "medium",
        "question_format": "matching",
        "match_prompts": [
            ("p1", "Structured API error logs"),
            ("p2", "Retrieved chunks captured with each answer"),
            ("p3", "Token counts of prompt plus context"),
        ],
        "match_responses": [
            ("r1", "The error class behind failed requests"),
            ("r2", "Whether retrieval or generation hallucinated"),
            ("r3", "Whether the context window overflowed"),
            ("r4", "Whether the bill was paid"),
        ],
        "match_key": {"p1": "r1", "p2": "r2", "p3": "r3"},
        "options": [],
        "correct_option_ids": [],
        "explanation": (
            "Error logs confirm the failing error class, captured chunks confirm "
            "whether retrieval or generation hallucinated, and token counts "
            "confirm context overflow; the bill is a distractor."
        ),
        "rationales": {},
    },
]


def question_count() -> int:
    """Return the number of authored Domain 5 ordering/matching questions."""
    return len(QUESTIONS)
