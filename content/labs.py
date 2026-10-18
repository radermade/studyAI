"""Authored hands-on labs 1-4 for the AIP-C01 study platform.

Each lab is an original, learner-operated AWS Console walkthrough. Content is
subject material and therefore lives under ``content/`` rather than in
``study_core``. Labs are shaped for :func:`study_core.ingestion.ingest_handoff`
via ``build_authored_labs`` and surface through the Labs view.

Shape per lab::

    {
      "lab_id", "title", "objective_ids", "cost_class", "regions",
      "scenario", "architecture", "prerequisites", "objectives_text",
      "region_note", "recall_prompt", "cleanup",
      "steps": [
        {
          "step_id", "display_order", "instruction", "prediction_prompt",
          "mandatory", "reflection",
          "hints": [concept, service_area, procedure, full_solution],
        }, ...
      ],
      "checkpoints": [
        {"checkpoint_id", "label", "step_id", "validator_id" | None,
         "is_cleanup", "mandatory"}, ...
      ],
    }

Validators are read-only and must be allowlisted in ``study_aws.validators``.
A checkpoint with ``validator_id is None`` is self-report only and can never
reach ``Verified``.
"""

from __future__ import annotations

from typing import Any

# --- Lab 1: Bedrock model comparison --------------------------------------

_LAB_1: dict[str, Any] = {
    "lab_id": "lab-01-model-comparison",
    "title": "Lab 1: Bedrock model comparison",
    "objective_ids": ["AIP-1.1", "AIP-1.2", "AIP-2.2", "AIP-4.1"],
    "cost_class": "low",
    "regions": ["us-east-1"],
    "scenario": (
        "Your team must choose a foundation model for a customer-support "
        "summarization feature. Leadership wants a defensible choice, not a "
        "gut feel, so you will compare two Bedrock models on the same "
        "representative prompt and measure quality, latency, and cost."
    ),
    "architecture": (
        "A single representative prompt is sent to two Amazon Bedrock "
        "foundation models. Each response is measured for quality, latency, "
        "and token cost, and the results drive a documented selection."
    ),
    "prerequisites": (
        "Bedrock model access enabled for at least two text models in "
        "us-east-1; an IAM identity allowed to call bedrock:InvokeModel and "
        "bedrock:ListFoundationModels."
    ),
    "objectives_text": (
        "Practice evidence-based model selection (AIP-1.1/1.2), reason about "
        "throughput and cost (AIP-2.2), and record a quality/latency/cost "
        "trade-off (AIP-4.1)."
    ),
    "region_note": "Use us-east-1, where the broadest set of models is available.",
    "recall_prompt": (
        "Without looking: which three dimensions did you compare, and which one "
        "was decisive for the summarization use case?"
    ),
    "cleanup": (
        "This lab invokes models on demand and creates no persistent resources. "
        "Confirm no Provisioned Throughput commitment, custom model, or saved "
        "playground session was created."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Open the Bedrock console in us-east-1 and go to Model access. "
                "Confirm at least two text models are enabled; request access "
                "to a second model if only one is available."
            ),
            "prediction_prompt": (
                "Before you look: which model families do you expect to be "
                "available by default, and which require an access request?"
            ),
            "mandatory": True,
            "reflection": (
                "Did model availability differ from your prediction? Note why "
                "access gating matters for a production rollout plan."
            ),
            "hints": [
                "Access is per account, per Region, and per model family.",
                "The Bedrock console 'Model access' page lists enabled vs. "
                "available-on-request models.",
                "If fewer than two are enabled, use 'Manage model access', "
                "select a second text model, and submit the request.",
                "You need two enabled text models in us-east-1. Enable them on "
                "the Model access page before continuing; the catalog call will "
                "then show both.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "In the Bedrock Chat/Text playground, send the same support "
                "transcript summarization prompt to each model. Record output "
                "quality notes, end-to-end latency, and input/output tokens."
            ),
            "prediction_prompt": (
                "Predict which model will be faster and which will be cheaper "
                "per 1K tokens, and whether the faster one is also the cheaper."
            ),
            "mandatory": True,
            "reflection": (
                "Was the faster model also the cheaper or higher-quality one? "
                "Capture the trade-off you actually observed."
            ),
            "hints": [
                "A fair comparison holds the prompt and decoding settings "
                "constant across both models.",
                "Latency and token counts are visible in the playground; "
                "pricing is on the Bedrock pricing page per model.",
                "Run each model two or three times, discard the first (cold) "
                "call, and average the latency.",
                "Compute latency-adjusted cost = price-per-1K-tokens scaled by "
                "the tokens used, then pick the model that clears your quality "
                "floor at the lowest cost. Record the measured numbers as the "
                "rationale.",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Write a one-paragraph selection rationale naming the chosen "
                "model and the decisive dimension (quality, latency, or cost) "
                "for this summarization use case."
            ),
            "prediction_prompt": (
                "Which dimension do you think should decide a support-"
                "summarization feature, and why?"
            ),
            "mandatory": True,
            "reflection": (
                "Would your choice change for a latency-critical chat feature "
                "instead of batch summarization? Explain in one sentence."
            ),
            "hints": [
                "The decisive dimension depends on the use case, not on the " "model's reputation.",
                "Map each dimension to a business constraint: SLA (latency), "
                "budget (cost), accuracy (quality).",
                "State the quality floor first, then choose the cheapest/fastest "
                "model that meets it.",
                "A defensible rationale: 'Model X meets the quality floor on our "
                "sample set at the lowest latency-adjusted cost (numbers), so we "
                "select it for batch summarization.'",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-model-access",
            "label": "Two text models enabled",
            "step_id": "s1",
            "validator_id": "bedrock-models-present",
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-comparison-recorded",
            "label": "Comparison measurements recorded",
            "step_id": "s2",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": False,
        },
        {
            "checkpoint_id": "c3-rationale-written",
            "label": "Selection rationale written",
            "step_id": "s3",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": False,
        },
    ],
}

# --- Lab 2: Prompt lifecycle and structured output ------------------------

_LAB_2: dict[str, Any] = {
    "lab_id": "lab-02-prompt-lifecycle",
    "title": "Lab 2: Prompt lifecycle and structured output",
    "objective_ids": ["AIP-1.6", "AIP-5.1", "AIP-5.2"],
    "cost_class": "low",
    "regions": ["us-east-1"],
    "scenario": (
        "A downstream service needs the model to return strict JSON matching a "
        "fixed schema. Edits to the prompt keep causing silent breakage. You "
        "will treat the prompt as a versioned artifact, enforce structured "
        "output, and gate changes on a small regression set."
    ),
    "architecture": (
        "A versioned prompt plus a JSON schema is sent to a Bedrock model. "
        "Outputs are validated against the schema; a small regression set runs "
        "on every prompt change before promotion."
    ),
    "prerequisites": (
        "Lab 1 completed or Bedrock access confirmed; a text model enabled in "
        "us-east-1; a JSON schema for the target output."
    ),
    "objectives_text": (
        "Version prompts and gate on evaluation (AIP-1.6), enforce schema-valid "
        "output (AIP-5.1), and detect regressions before promotion (AIP-5.2)."
    ),
    "region_note": "us-east-1 for model availability; no cross-Region calls.",
    "recall_prompt": (
        "What two controls together prevent a prompt edit from silently " "lowering output quality?"
    ),
    "cleanup": (
        "No persistent AWS resources are created. If you saved prompts in "
        "Bedrock Prompt Management, confirm you intend to keep them or delete "
        "the test versions."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Define the target JSON schema (required keys, types) and write "
                "prompt version v1 that instructs the model to return only that "
                "JSON. Save v1 as your baseline."
            ),
            "prediction_prompt": (
                "Predict which schema field the model is most likely to omit or "
                "mistype on a messy input."
            ),
            "mandatory": True,
            "reflection": (
                "Which field actually failed first? Note whether the prompt or "
                "the schema wording caused it."
            ),
            "hints": [
                "Structured output is a contract; the schema is the contract, "
                "the prompt is how you ask for it.",
                "Bedrock Prompt Management can store and version prompts; a repo "
                "file works too.",
                "State the schema explicitly in the prompt and add one example "
                "of a valid object.",
                "Pin v1: schema with required keys and types, a prompt that says "
                "'return only JSON matching this schema', and one worked example. "
                "Save it as the baseline you will diff against.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "Build a small regression set of 5-8 representative inputs "
                "(including two messy edge cases). Run v1 and validate each "
                "output against the schema; record pass/fail per input."
            ),
            "prediction_prompt": (
                "How many of your edge cases do you expect v1 to pass on the " "first run?"
            ),
            "mandatory": True,
            "reflection": (
                "Did the edge cases fail validation or just quality? Distinguish "
                "a schema violation from a wrong-but-valid answer."
            ),
            "hints": [
                "A regression set makes quality measurable instead of anecdotal.",
                "Validate with a JSON schema validator, not by eyeballing output.",
                "Log the exact validation error for each failing input.",
                "Record a pass/fail table: input -> schema-valid? -> correct? Keep "
                "it; it becomes the gate for every future prompt edit.",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Create prompt version v2 to fix a failure from v1. Re-run the "
                "full regression set and only 'promote' v2 if it is strictly "
                "better and introduces no new failures."
            ),
            "prediction_prompt": (
                "Predict whether your v2 fix will cause any previously-passing " "input to regress."
            ),
            "mandatory": True,
            "reflection": (
                "Did v2 fix the target without regressing others? Note how the "
                "gate caught (or would have caught) a bad change."
            ),
            "hints": [
                "A fix that breaks a passing case is a regression, not an " "improvement.",
                "Keep v1 and v2 side by side; never edit in place.",
                "Promote only when v2 >= v1 on every input and strictly better on " "at least one.",
                "The lifecycle: version -> evaluate on the regression set -> "
                "promote only on a non-regressing improvement. This is the gate "
                "that stops silent quality loss.",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-schema-baseline",
            "label": "Schema and v1 baseline defined",
            "step_id": "s1",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-regression-run",
            "label": "Regression set run and recorded",
            "step_id": "s2",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c3-promotion-decision",
            "label": "v2 evaluated and promotion decided",
            "step_id": "s3",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": False,
        },
    ],
}

# --- Lab 3: Knowledge Base baseline RAG -----------------------------------

_LAB_3: dict[str, Any] = {
    "lab_id": "lab-03-knowledge-base-rag",
    "title": "Lab 3: Knowledge Base baseline RAG",
    "objective_ids": ["AIP-1.3", "AIP-1.4", "AIP-1.5"],
    "cost_class": "medium",
    "regions": ["us-east-1"],
    "scenario": (
        "You must ground an assistant in a small internal document set so it "
        "answers from your sources with citations. You will build a Bedrock "
        "Knowledge Base over an S3 bucket, ingest documents, and verify that "
        "retrieval returns relevant, cited passages."
    ),
    "architecture": (
        "Documents land in an S3 bucket; a Bedrock Knowledge Base ingests and "
        "chunks them into a managed vector store. Queries retrieve top matches "
        "with citations that are passed to the model for grounded answers."
    ),
    "prerequisites": (
        "Bedrock access and an embeddings model enabled in us-east-1; "
        "permission to create an S3 bucket and a Bedrock Knowledge Base; a "
        "handful of small source documents."
    ),
    "objectives_text": (
        "Prepare and ingest source data (AIP-1.3), stand up a managed vector "
        "store (AIP-1.4), and evaluate retrieval relevance and citations "
        "(AIP-1.5)."
    ),
    "region_note": (
        "This lab creates billable resources (S3 storage, embeddings, a vector "
        "store). Stay in us-east-1 and complete cleanup."
    ),
    "recall_prompt": (
        "What are the three stages between a raw document in S3 and a cited "
        "answer from the assistant?"
    ),
    "cleanup": (
        "Delete the Knowledge Base (and its managed vector store), then empty "
        "and delete the S3 bucket. Confirm the bucket no longer appears before "
        "marking cleanup verified."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Create an S3 bucket in us-east-1 and upload 3-5 small, "
                "self-contained documents (e.g., policy or FAQ text). Keep each "
                "document focused on one topic."
            ),
            "prediction_prompt": (
                "Predict how document structure (one topic per file vs. mixed) "
                "will affect retrieval relevance later."
            ),
            "mandatory": True,
            "reflection": (
                "Note whether any document mixed unrelated topics; that will "
                "show up as noisy retrieval in step 3."
            ),
            "hints": [
                "Clean, single-topic documents retrieve more coherently than " "mixed ones.",
                "Use the S3 console to create the bucket and upload objects in " "us-east-1.",
                "Name the bucket uniquely and tag it with your study-session tag "
                "for easy cleanup.",
                "Create one S3 bucket, tag it (study-session, owner), and upload "
                "3-5 single-topic documents. This bucket is the KB data source.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "Create a Bedrock Knowledge Base pointing at the bucket, choose "
                "an embeddings model and a managed vector store, and run "
                "ingestion/sync. Wait for ingestion to complete."
            ),
            "prediction_prompt": (
                "Predict how chunk size will trade off against retrieval "
                "precision for your short documents."
            ),
            "mandatory": True,
            "reflection": (
                "Did ingestion report any skipped or failed documents? Note what "
                "caused it (format, size, encoding)."
            ),
            "hints": [
                "Ingestion = extract text, chunk, embed, index into the vector " "store.",
                "Bedrock Knowledge Bases offer a managed vector store so you do "
                "not run your own cluster.",
                "Start with default chunking; change it only if retrieval later "
                "cuts across topics.",
                "Create the KB with the S3 bucket as source, pick an embeddings "
                "model and the managed vector store, then run Sync and wait for "
                "'Completed'.",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Use the Knowledge Base test/query panel to ask 3-4 questions "
                "answerable from your documents. Confirm answers are grounded "
                "and show citations back to the right source."
            ),
            "prediction_prompt": (
                "Predict which question will retrieve the wrong passage, and why."
            ),
            "mandatory": True,
            "reflection": (
                "Were citations pointing at the correct source document? Note any "
                "query that retrieved an unrelated chunk."
            ),
            "hints": [
                "Grounded means the answer is supported by a retrieved, cited "
                "passage, not model memory.",
                "The KB test panel shows retrieved chunks and their source for " "each query.",
                "Ask one question whose answer appears in only one document to " "test precision.",
                "Verify each answer cites the correct source chunk. If a query "
                "retrieves an unrelated passage, that signals a chunking or "
                "document-structure problem to revisit.",
            ],
        },
        {
            "step_id": "s4",
            "display_order": 4,
            "instruction": (
                "Clean up: delete the Knowledge Base and its vector store, then "
                "empty and delete the S3 bucket. Re-list buckets to confirm it "
                "is gone."
            ),
            "prediction_prompt": ("Which resource is easiest to forget and keep incurring cost?"),
            "mandatory": True,
            "reflection": (
                "Did deletion of the KB also remove the managed vector store, or "
                "was it separate? Note the dependency order."
            ),
            "hints": [
                "A clicked delete button is not proof; absence is.",
                "Delete the Knowledge Base first, then the S3 bucket it read " "from.",
                "Empty the bucket (objects and versions) before deleting it.",
                "After deletion, re-list buckets and confirm yours is absent. The "
                "cleanup checkpoint only verifies on observed absence.",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-bucket-created",
            "label": "Source bucket present",
            "step_id": "s1",
            "validator_id": "s3-bucket-present",
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-retrieval-grounded",
            "label": "Grounded, cited retrieval confirmed",
            "step_id": "s3",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c3-bucket-removed",
            "label": "Source bucket removed",
            "step_id": "s4",
            "validator_id": "s3-bucket-absent",
            "is_cleanup": True,
            "mandatory": True,
        },
    ],
}

# --- Lab 4: Advanced retrieval --------------------------------------------

_LAB_4: dict[str, Any] = {
    "lab_id": "lab-04-advanced-retrieval",
    "title": "Lab 4: Advanced retrieval (chunking, hybrid, rerank)",
    "objective_ids": ["AIP-1.4", "AIP-1.5", "AIP-4.2", "AIP-5.1", "AIP-5.2"],
    "cost_class": "medium",
    "regions": ["us-east-1"],
    "scenario": (
        "Baseline RAG retrieval is good but misses exact-term queries and "
        "sometimes grounds on a weaker passage. You will run a controlled "
        "experiment varying chunking, hybrid search, and reranking, and measure "
        "which change actually improves retrieval on a fixed query set."
    ),
    "architecture": (
        "A fixed evaluation query set runs against retrieval configurations: "
        "baseline semantic, structure-aware chunking, hybrid (lexical + "
        "semantic), and hybrid + rerank. Each configuration's hit quality is "
        "measured and compared."
    ),
    "prerequisites": (
        "Lab 3 completed or an existing Knowledge Base with ingested documents; "
        "a fixed set of evaluation queries with known-good source passages."
    ),
    "objectives_text": (
        "Tune the vector store and retrieval (AIP-1.4), compare chunking/hybrid/"
        "rerank strategies (AIP-1.5), reason about cost/performance (AIP-4.2), "
        "and evaluate changes with a repeatable method (AIP-5.1/5.2)."
    ),
    "region_note": (
        "Reuses billable KB resources from Lab 3. Stay in us-east-1 and clean "
        "up any resources this lab adds."
    ),
    "recall_prompt": (
        "Which retrieval change gave the biggest measured gain on your query "
        "set, and what did it cost in latency?"
    ),
    "cleanup": (
        "Delete any extra Knowledge Base versions, indexes, or buckets created "
        "for this experiment. If you also finished with Lab 3's base resources, "
        "remove them and confirm absence."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Fix an evaluation set: 6-10 queries, each tagged with the "
                "source passage that should be retrieved. Include at least two "
                "exact-term queries (codes, part numbers)."
            ),
            "prediction_prompt": ("Predict which query type baseline semantic search will miss."),
            "mandatory": True,
            "reflection": (
                "Did you include enough exact-term queries to expose semantic "
                "search's blind spot? Note the mix."
            ),
            "hints": [
                "You cannot compare retrieval strategies without a fixed, labeled " "query set.",
                "Label each query with the document/passage that is the correct " "hit.",
                "Add exact-term queries specifically to stress lexical matching.",
                "Freeze the query set now: queries + expected source passages. "
                "Every configuration is scored against this same set.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "Run the baseline (semantic-only) retrieval against the query "
                "set and record, per query, whether the expected passage was in "
                "the top results. Capture latency."
            ),
            "prediction_prompt": ("Predict your baseline hit rate and which queries will fail."),
            "mandatory": True,
            "reflection": (
                "Which queries failed and were they the exact-term ones you "
                "expected? Record the baseline numbers."
            ),
            "hints": [
                "A baseline measurement is the control for the whole experiment.",
                "Use the KB query/test panel and record top-k hits per query.",
                "Score a hit as 1 if the expected passage appears in top-k, else " "0.",
                "Record baseline hit rate and median latency. These are the "
                "numbers every later configuration must beat.",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Change one variable at a time: (a) structure-aware chunking, "
                "(b) hybrid lexical+semantic search, (c) add reranking. Re-run "
                "the same query set after each change and record hits and "
                "latency."
            ),
            "prediction_prompt": (
                "Predict which single change will most help the exact-term " "queries."
            ),
            "mandatory": True,
            "reflection": (
                "Did any change improve hit rate but worsen latency? Capture the "
                "trade-off per configuration."
            ),
            "hints": [
                "Changing one variable at a time keeps the result attributable.",
                "Hybrid search blends lexical and semantic; reranking reorders "
                "retrieved candidates.",
                "Hybrid typically fixes exact-term misses; rerank fixes ordering "
                "of relevant results.",
                "Build a table: configuration -> hit rate -> latency. One row per "
                "change, same query set, so each delta is isolated and "
                "attributable.",
            ],
        },
        {
            "step_id": "s4",
            "display_order": 4,
            "instruction": (
                "Pick the configuration with the best hit rate that still meets "
                "your latency/cost budget, and write a one-paragraph rationale "
                "citing the measured numbers."
            ),
            "prediction_prompt": (
                "Will the highest-hit-rate configuration also be the one you "
                "ship? Why or why not?"
            ),
            "mandatory": True,
            "reflection": (
                "Was the best-quality configuration worth its added latency/cost? "
                "State the trade-off you accepted."
            ),
            "hints": [
                "The best retrieval setup is the one that meets the budget, not "
                "the absolute top score.",
                "Weigh hit-rate gain against added latency and per-query cost.",
                "Reject a change whose cost outweighs its measured quality gain.",
                "Defensible choice: 'Config C raised hit rate from X to Y within "
                "the latency budget at cost Z, so we select it.' Cite the actual "
                "numbers from your table.",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-eval-set-fixed",
            "label": "Evaluation query set fixed and labeled",
            "step_id": "s1",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-experiment-recorded",
            "label": "Baseline and variant results recorded",
            "step_id": "s3",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c3-selection-rationale",
            "label": "Configuration selected with rationale",
            "step_id": "s4",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": False,
        },
    ],
}


# --- Lab 6: Bounded tool-using agent --------------------------------------

_LAB_6: dict[str, Any] = {
    "lab_id": "lab-06-bounded-agent",
    "title": "Lab 6: Bounded tool-using agent",
    "objective_ids": ["AIP-2.1", "AIP-3.1", "AIP-4.3", "AIP-5.1"],
    "cost_class": "medium",
    "regions": ["us-east-1"],
    "scenario": (
        "You will build a small agent that calls one AWS tool (a Lambda "
        "function) under strict bounds: a typed tool schema, a least-privilege "
        "IAM role, a timeout, a correlation trace, and a human-escalation path. "
        "Then you will inject an unsafe tool call and prove the agent rejects "
        "it rather than executing it."
    ),
    "architecture": (
        "The agent plans, validates tool arguments against a schema, invokes a "
        "least-privilege Lambda tool with a timeout, emits a correlation ID on "
        "every step, and escalates to a human for any out-of-policy action."
    ),
    "prerequisites": (
        "Permission to create an IAM role and a Lambda function in us-east-1; "
        "Bedrock access for the agent's model; CloudWatch Logs enabled."
    ),
    "objectives_text": (
        "Design a bounded agent with typed tools and limits (AIP-2.1), enforce "
        "least privilege and safe failure (AIP-3.1), diagnose from traces "
        "(AIP-4.3), and evaluate the safety behavior (AIP-5.1)."
    ),
    "region_note": (
        "Creates a Lambda function and IAM role (low cost). Stay in us-east-1 "
        "and complete cleanup."
    ),
    "recall_prompt": (
        "Name the five bounds every tool-using agent in this lab enforced "
        "before any tool call executed."
    ),
    "cleanup": (
        "Delete the Lambda function and the IAM role created for the agent. "
        "Re-list functions to confirm the tool function is gone before marking "
        "cleanup verified."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Create a minimal Lambda 'tool' function and a least-privilege "
                "IAM role that grants only the single action the tool needs. "
                "Attach the role to the function."
            ),
            "prediction_prompt": (
                "Predict which permission the tool truly needs, and which you "
                "might over-grant by habit."
            ),
            "mandatory": True,
            "reflection": (
                "Did the role end up broader than the one action required? Note "
                "what you trimmed to reach least privilege."
            ),
            "hints": [
                "Least privilege means the role grants only the actions the tool "
                "actually calls.",
                "Create the IAM role first, then the Lambda, then attach the role "
                "in the console.",
                "Start from an empty policy and add exactly one action; avoid "
                "wildcard resources.",
                "Create a Lambda tool and a role whose policy lists only the one "
                "needed action on the specific resource. This bounds what a "
                "misbehaving agent can do.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "Define a typed tool schema (name, parameters, types) and wire "
                "the agent to validate arguments against it before calling, with "
                "a per-call timeout and a correlation ID logged on each step."
            ),
            "prediction_prompt": (
                "Predict what the agent should do when the model proposes "
                "arguments that fail schema validation."
            ),
            "mandatory": True,
            "reflection": (
                "Did a malformed argument get rejected at the schema boundary "
                "before any AWS call? Note where the rejection happened."
            ),
            "hints": [
                "The tool schema is the contract; validation happens before the "
                "call, not after.",
                "Set a Lambda/client timeout and generate a correlation ID per " "agent run.",
                "Log the correlation ID on plan, validate, call, and result " "steps.",
                "Validate every argument against the schema first; on failure, "
                "reject the call and log it with the correlation ID. Enforce a "
                "timeout so a slow tool cannot hang the run.",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Inject an unsafe/out-of-policy tool call (e.g., an action the "
                "role does not permit, or arguments outside the schema). Confirm "
                "the agent rejects it with a bounded failure and escalates "
                "rather than executing."
            ),
            "prediction_prompt": (
                "Predict whether the failure will come from schema validation, "
                "the IAM boundary, or both."
            ),
            "mandatory": True,
            "reflection": (
                "Was the unsafe call stopped by your validation, by IAM, or both "
                "(defense in depth)? Capture the sanitized evidence."
            ),
            "hints": [
                "A safe agent fails closed on an out-of-policy action, never open.",
                "The IAM role should deny the action even if validation were " "bypassed.",
                "Capture the sanitized denial from CloudWatch using the " "correlation ID.",
                "Prove defense in depth: schema validation rejects the bad "
                "arguments and the least-privilege role denies the action. "
                "Record the sanitized trace as evidence of safe failure.",
            ],
        },
        {
            "step_id": "s4",
            "display_order": 4,
            "instruction": (
                "Clean up: delete the Lambda function and the IAM role. Re-list "
                "functions to confirm the tool function no longer exists."
            ),
            "prediction_prompt": (
                "Which resource, left behind, would keep an unused permission " "alive?"
            ),
            "mandatory": True,
            "reflection": (
                "Did you remove both the function and the role? Note the order "
                "and any dependency you hit."
            ),
            "hints": [
                "A clicked delete is not proof; confirm absence.",
                "Delete the Lambda function, then the IAM role it used.",
                "Detach the role from the function before deleting the role if " "required.",
                "After deletion, re-list functions and confirm the tool function "
                "is absent. The cleanup checkpoint verifies only on observed "
                "absence.",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-tool-function-present",
            "label": "Agent tool (Lambda) created",
            "step_id": "s1",
            "validator_id": "lambda-function-present",
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-unsafe-call-rejected",
            "label": "Unsafe tool call rejected (defense in depth)",
            "step_id": "s3",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c3-tool-function-removed",
            "label": "Agent tool (Lambda) removed",
            "step_id": "s4",
            "validator_id": "lambda-function-absent",
            "is_cleanup": True,
            "mandatory": True,
        },
    ],
}

# --- Lab 7: Resilient streaming/async API integration ----------------------

_LAB_7: dict[str, Any] = {
    "lab_id": "lab-07-resilient-api",
    "title": "Lab 7: Resilient streaming and async API integration",
    "objective_ids": ["AIP-2.3", "AIP-2.4", "AIP-2.5"],
    "cost_class": "medium",
    "regions": ["us-east-1"],
    "scenario": (
        "You will put an API Gateway + Lambda in front of a Bedrock model, add "
        "streaming for responsiveness, an asynchronous/queued path for "
        "long-running work, bounded retries with backoff, and model routing. "
        "Then you will inject throttling and prove a bounded fallback with "
        "correlated traces."
    ),
    "architecture": (
        "Clients call API Gateway, which invokes a Lambda that either streams a "
        "synchronous Bedrock response or enqueues long work for async "
        "processing. Retries use bounded backoff; a routing policy chooses the "
        "model; traces correlate every hop."
    ),
    "prerequisites": (
        "Permission to create API Gateway, Lambda, and a queue in us-east-1; "
        "Bedrock access; CloudWatch and X-Ray (or equivalent) enabled."
    ),
    "objectives_text": (
        "Integrate via managed API boundaries (AIP-2.3), implement streaming "
        "and resilient API patterns (AIP-2.4), and add async/routing/trace "
        "handling with bounded failure (AIP-2.5)."
    ),
    "region_note": (
        "Creates API Gateway, Lambda, and a queue (low-to-medium cost). Stay in "
        "us-east-1 and complete cleanup."
    ),
    "recall_prompt": (
        "When the model was throttled, what bounded behavior kept the API from "
        "a retry storm or a false success?"
    ),
    "cleanup": (
        "Delete the API, the Lambda, and the queue created for this lab. "
        "Re-list APIs to confirm the API is gone before marking cleanup "
        "verified."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Create an API Gateway endpoint fronting a Lambda that calls a "
                "Bedrock model synchronously, and stream tokens back to the "
                "caller as they are generated."
            ),
            "prediction_prompt": (
                "Predict how streaming changes perceived latency versus a " "buffered response."
            ),
            "mandatory": True,
            "reflection": (
                "Did first-token time improve noticeably with streaming? Note "
                "the perceived vs. total latency difference."
            ),
            "hints": [
                "Streaming improves perceived latency without changing total " "generation time.",
                "Put API Gateway in front of a Lambda; do not expose the model " "directly.",
                "Use the model's streaming response API and forward chunks to " "the client.",
                "Create API Gateway -> Lambda -> Bedrock (streaming). Forward "
                "tokens as they arrive so the client sees output immediately.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "Add an asynchronous path: for long-running requests, enqueue "
                "the work and return a job handle, processing it off the "
                "synchronous request path."
            ),
            "prediction_prompt": (
                "Predict which requests should take the async path instead of "
                "streaming synchronously."
            ),
            "mandatory": True,
            "reflection": (
                "Did the async path keep the synchronous endpoint responsive "
                "under long jobs? Note the handoff mechanism."
            ),
            "hints": [
                "Long-running work should not block a synchronous request " "thread.",
                "Use a queue to decouple submission from processing.",
                "Return a job id immediately; process the work asynchronously.",
                "Enqueue long jobs and return a handle; a worker processes them "
                "off the request path so the sync endpoint stays responsive.",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Add bounded exponential backoff with jitter and a max-attempt "
                "cap, plus a routing policy that sends simple requests to a "
                "cheaper model and hard ones to a stronger model with a safe "
                "fallback."
            ),
            "prediction_prompt": (
                "Predict what should happen when the router cannot confidently "
                "classify a request."
            ),
            "mandatory": True,
            "reflection": (
                "Did your retry policy have a hard attempt cap, and did routing "
                "define a no-route fallback? Note both."
            ),
            "hints": [
                "Unbounded or synchronized retries create storms; backoff with "
                "jitter avoids them.",
                "A routing policy needs explicit criteria and a defined fallback.",
                "Cap attempts and classify which errors are even retryable.",
                "Add backoff+jitter with a max-attempt cap, and a routing policy "
                "with explicit criteria plus a safe default when classification "
                "is unclear.",
            ],
        },
        {
            "step_id": "s4",
            "display_order": 4,
            "instruction": (
                "Inject throttling against the model and confirm the API returns "
                "a bounded fallback or explicit error (never a false success), "
                "with correlated traces across API Gateway, Lambda, and the "
                "model call."
            ),
            "prediction_prompt": (
                "Predict whether a partial/throttled call could slip through as " "an HTTP 200."
            ),
            "mandatory": True,
            "reflection": (
                "Could you reconstruct the throttled request end to end from the "
                "correlation ID? Note any missing trace hop."
            ),
            "hints": [
                "A throttled or partial result must be an explicit error or safe "
                "fallback, not a 200.",
                "Correlate traces with one ID across API Gateway, Lambda, and the " "model call.",
                "Verify the retry cap engaged and the fallback fired under " "throttling.",
                "Prove bounded failure: under throttling the API falls back or "
                "errors explicitly, retries stay capped, and the correlation ID "
                "reconstructs the whole request. No false success.",
            ],
        },
        {
            "step_id": "s5",
            "display_order": 5,
            "instruction": (
                "Clean up: delete the API, the Lambda, and the queue. Re-list "
                "APIs to confirm the API no longer exists."
            ),
            "prediction_prompt": ("Which resource keeps billing if forgotten after this lab?"),
            "mandatory": True,
            "reflection": (
                "Did you remove all three resources? Note the deletion order and " "any dependency."
            ),
            "hints": [
                "A clicked delete is not proof; confirm absence.",
                "Delete the API first, then the Lambda, then the queue.",
                "Check for any stage/deployment that keeps the API reachable.",
                "After deletion, re-list APIs and confirm yours is absent. The "
                "cleanup checkpoint verifies only on observed absence.",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-api-present",
            "label": "API endpoint created",
            "step_id": "s1",
            "validator_id": "apigateway-api-present",
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-throttle-fallback",
            "label": "Bounded fallback under throttling proven",
            "step_id": "s4",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c3-api-removed",
            "label": "API endpoint removed",
            "step_id": "s5",
            "validator_id": "apigateway-api-absent",
            "is_cleanup": True,
            "mandatory": True,
        },
    ],
}


# --- Lab 5: Guardrails and adversarial testing -----------------------------

_LAB_5: dict[str, Any] = {
    "lab_id": "lab-05-guardrails-adversarial",
    "title": "Lab 5: Guardrails and adversarial testing",
    "objective_ids": ["AIP-3.1", "AIP-3.4", "AIP-5.1"],
    "cost_class": "low",
    "regions": ["us-east-1"],
    "scenario": (
        "You will put layered guardrails around a Bedrock model (input "
        "filtering, grounding, output filtering), build an adversarial test set "
        "including prompt-injection attempts, and measure the block rate and "
        "false-positive rate so safety is evidence-based rather than assumed."
    ),
    "architecture": (
        "Requests pass through input guardrails, the model (grounded where "
        "applicable), then output guardrails. An adversarial test set drives "
        "the system and block/false-positive rates are recorded."
    ),
    "prerequisites": (
        "Bedrock access in us-east-1; a guardrail capability (e.g., Bedrock "
        "Guardrails) or an equivalent input/output filter you can configure; a "
        "small labeled attack set and a benign set."
    ),
    "objectives_text": (
        "Design layered safety controls and defend against injection (AIP-3.1), "
        "document the safety posture (AIP-3.4), and evaluate guardrails with a "
        "repeatable method (AIP-5.1)."
    ),
    "region_note": "us-east-1 for model/guardrail availability; no cross-Region calls.",
    "recall_prompt": (
        "Name the three guardrail layers you used and the two rates you measured " "to judge them."
    ),
    "cleanup": (
        "If you created a managed guardrail resource, delete it; otherwise no "
        "persistent resources are created. Confirm no test guardrail remains "
        "attached to a production alias."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Configure layered guardrails: an input filter (deny-listed "
                "topics / injection patterns), grounding where applicable, and "
                "an output filter for harmful content."
            ),
            "prediction_prompt": (
                "Predict which layer will catch an indirect prompt-injection "
                "attempt carried in retrieved text."
            ),
            "mandatory": True,
            "reflection": (
                "Which layer actually caught injection in testing? Note whether "
                "one layer alone would have sufficed."
            ),
            "hints": [
                "Defense in depth means no single layer is the only thing "
                "standing between a bypass and harm.",
                "Bedrock Guardrails can enforce denied topics and content "
                "filters at input and output.",
                "Treat retrieved/user content as untrusted and keep it separate "
                "from instructions.",
                "Configure input filtering, grounding, and output filtering so a "
                "miss in one layer is caught by another. Isolate untrusted "
                "content from the instruction channel.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "Build an adversarial test set (direct and indirect injection, "
                "data-exfiltration attempts, harmful requests) plus a benign set "
                "of legitimate requests."
            ),
            "prediction_prompt": (
                "Predict your false-positive rate on the benign set before " "running it."
            ),
            "mandatory": True,
            "reflection": (
                "Was the benign set large and varied enough to expose false "
                "positives? Note any gap."
            ),
            "hints": [
                "You cannot measure guardrails without both attacks and benign " "traffic.",
                "Cover direct injection, indirect (retrieved) injection, and "
                "exfiltration prompts.",
                "Label each case so you can score blocks and false positives.",
                "Assemble a labeled attack set and a benign set; the benign set "
                "is what reveals over-blocking (false positives).",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Run both sets through the guarded system and record the block "
                "rate on attacks and the false-positive rate on benign requests. "
                "Document an acceptable balance and remaining risk."
            ),
            "prediction_prompt": (
                "Predict whether tightening the filter to raise the block rate "
                "will raise false positives."
            ),
            "mandatory": True,
            "reflection": (
                "What balance did you accept, and what residual risk remains "
                "documented for stakeholders?"
            ),
            "hints": [
                "Safety is a measured trade-off between blocking harm and "
                "blocking legitimate use.",
                "Report both the attack block rate and the benign false-positive " "rate.",
                "Record residual risk the guardrails do not cover.",
                "Produce a table: block rate, false-positive rate, chosen "
                "threshold, and documented residual risk. This is the safety "
                "evidence a system card references.",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-guardrails-configured",
            "label": "Layered guardrails configured",
            "step_id": "s1",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-adversarial-measured",
            "label": "Block and false-positive rates recorded",
            "step_id": "s3",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
    ],
}

# --- Lab 8: Secure multi-tenant RAG ----------------------------------------

_LAB_8: dict[str, Any] = {
    "lab_id": "lab-08-secure-multitenant-rag",
    "title": "Lab 8: Secure multi-tenant RAG",
    "objective_ids": ["AIP-3.3", "AIP-1.4", "AIP-2.3", "AIP-3.2"],
    "cost_class": "medium",
    "regions": ["us-east-1"],
    "scenario": (
        "You will build a RAG knowledge base holding documents for two tenants "
        "and prove that identity-aware, server-side authorization lets each "
        "tenant retrieve only its own documents, with an audit trail of who "
        "accessed what."
    ),
    "architecture": (
        "Tenant-tagged documents live in S3 and are indexed into a vector "
        "store. Each query carries a tenant identity; retrieval applies "
        "server-side authorization and metadata filtering, and access is "
        "logged for audit."
    ),
    "prerequisites": (
        "Permission to create an S3 bucket and a Bedrock Knowledge Base in "
        "us-east-1; the ability to tag documents by tenant; a way to pass a "
        "tenant identity with each query."
    ),
    "objectives_text": (
        "Enforce identity-aware access and tenant isolation (AIP-3.3), build a "
        "scoped vector store (AIP-1.4), apply secure integration boundaries "
        "(AIP-2.3), and keep an auditable access record (AIP-3.2)."
    ),
    "region_note": (
        "Creates billable S3 + Knowledge Base resources. Stay in us-east-1 and " "complete cleanup."
    ),
    "recall_prompt": (
        "Where was tenant isolation enforced, and why is a prompt instruction "
        "or client-side filter not enough?"
    ),
    "cleanup": (
        "Delete the Knowledge Base and its vector store, then empty and delete "
        "the S3 bucket. Re-list buckets to confirm absence before marking "
        "cleanup verified."
    ),
    "steps": [
        {
            "step_id": "s1",
            "display_order": 1,
            "instruction": (
                "Create an S3 bucket and upload documents for two tenants, each "
                "object tagged with its tenant ID. Keep tenant A and tenant B "
                "content clearly separated."
            ),
            "prediction_prompt": (
                "Predict what happens if tenant metadata is missing on even one " "object."
            ),
            "mandatory": True,
            "reflection": (
                "Did every object get a tenant tag? Note how a missing tag could " "become a leak."
            ),
            "hints": [
                "Isolation depends on reliable tenant metadata on every object.",
                "Use S3 object metadata/tags to carry the tenant ID.",
                "An untagged object cannot be safely filtered by tenant.",
                "Create one bucket, upload tenant-A and tenant-B documents, and "
                "tag every object with its tenant ID. Missing tags are future "
                "leaks.",
            ],
        },
        {
            "step_id": "s2",
            "display_order": 2,
            "instruction": (
                "Index the documents into a Knowledge Base vector store, then "
                "configure retrieval so each query is scoped by the caller's "
                "tenant identity using server-side metadata filtering."
            ),
            "prediction_prompt": (
                "Predict whether a prompt instruction alone could enforce the " "tenant boundary."
            ),
            "mandatory": True,
            "reflection": (
                "Was the tenant filter applied before retrieval (server-side) "
                "rather than after? Note where it runs."
            ),
            "hints": [
                "Authorization must happen at retrieval time, server-side, not "
                "in the prompt or client.",
                "Metadata filtering scopes retrieval to the caller's tenant.",
                "The identity must come from an authenticated caller, not from "
                "user-supplied text.",
                "Index the docs, then enforce a server-side metadata filter keyed "
                "on the authenticated tenant identity so disallowed documents "
                "are never fetched.",
            ],
        },
        {
            "step_id": "s3",
            "display_order": 3,
            "instruction": (
                "Test isolation: as tenant A, query for content that exists only "
                "in tenant B. Confirm it is never retrieved. Record an audit "
                "entry (identity, resource, timestamp) for each access."
            ),
            "prediction_prompt": (
                "Predict whether any phrasing as tenant A could surface tenant " "B's document."
            ),
            "mandatory": True,
            "reflection": (
                "Did any query cross the tenant boundary? Capture the audit "
                "entries proving who accessed what."
            ),
            "hints": [
                "A leak test must actively try to retrieve the other tenant's " "data.",
                "The audit log must tie identity to the specific resource and " "time.",
                "Try several phrasings as tenant A to probe the boundary.",
                "Confirm tenant A never retrieves tenant B content across "
                "phrasings, and record identity+resource+timestamp audit entries "
                "as proof of controlled access.",
            ],
        },
        {
            "step_id": "s4",
            "display_order": 4,
            "instruction": (
                "Clean up: delete the Knowledge Base and vector store, then "
                "empty and delete the S3 bucket. Re-list buckets to confirm it "
                "is gone."
            ),
            "prediction_prompt": ("Which resource, if left, could still expose tenant data?"),
            "mandatory": True,
            "reflection": (
                "Did deletion remove both the index and the bucket? Note the " "dependency order."
            ),
            "hints": [
                "A clicked delete is not proof; absence is.",
                "Delete the Knowledge Base first, then the S3 bucket.",
                "Empty the bucket (objects and versions) before deleting it.",
                "After deletion, re-list buckets and confirm absence. The cleanup "
                "checkpoint verifies only on observed absence.",
            ],
        },
    ],
    "checkpoints": [
        {
            "checkpoint_id": "c1-tenant-bucket-present",
            "label": "Tenant-tagged source bucket present",
            "step_id": "s1",
            "validator_id": "s3-bucket-present",
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c2-isolation-proven",
            "label": "Cross-tenant isolation and audit proven",
            "step_id": "s3",
            "validator_id": None,
            "is_cleanup": False,
            "mandatory": True,
        },
        {
            "checkpoint_id": "c3-tenant-bucket-removed",
            "label": "Tenant source bucket removed",
            "step_id": "s4",
            "validator_id": "s3-bucket-absent",
            "is_cleanup": True,
            "mandatory": True,
        },
    ],
}


_AUTHORED_LABS: tuple[dict[str, Any], ...] = (
    _LAB_1,
    _LAB_2,
    _LAB_3,
    _LAB_4,
    _LAB_5,
    _LAB_6,
    _LAB_7,
    _LAB_8,
)


def build_authored_labs() -> list[dict[str, Any]]:
    """Return the authored labs in ingestion shape."""
    return [dict(lab) for lab in _AUTHORED_LABS]


def build_lab_curriculum_items(start_order: int) -> list[dict[str, Any]]:
    """Return curriculum rail entries for the authored labs.

    Args:
        start_order: display order for the first lab; labs follow sequentially.
    """
    items: list[dict[str, Any]] = []
    for offset, lab in enumerate(_AUTHORED_LABS):
        items.append(
            {
                "item_id": lab["lab_id"],
                "item_type": "lab",
                "title": lab["title"],
                "display_order": start_order + offset,
                "objective_ids": list(lab["objective_ids"]),
                "prerequisites": [],
                "content_ref": lab["lab_id"],
            }
        )
    return items


def lab_count() -> int:
    """Return the number of authored labs."""
    return len(_AUTHORED_LABS)
