"""Authored Domain 1 (AIP-C01) scenario questions with answers and explanations.

These are original, scenario-style multiple-choice questions written to test
architecture reasoning for the AWS Certified Generative AI Developer exam.
Each question has a decisive constraint, four distinct options, one correct
answer, per-option rationales, and a teaching explanation. No proprietary exam
content is reproduced.

Shape per question:
    {
      "question_id", "objective_ids", "prompt", "scenario_constraint",
      "difficulty", "source_ids",
      "options": [(option_id, text), ...],
      "correct_option_ids": [...],
      "explanation": "...",
      "rationales": {option_id: (is_correct, rationale)},
    }
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    {
        "question_id": "d1-bedrock-vs-sagemaker",
        "objective_ids": ["AIP-1.1", "AIP-1.2"],
        "prompt": (
            "A team needs a chat assistant that uses leading third-party "
            "foundation models with pay-per-use pricing, no infrastructure to "
            "manage, and the fastest path to production. Which approach best "
            "fits these constraints?"
        ),
        "scenario_constraint": "Fastest path, no infra management, pay-per-use, third-party FMs.",
        "difficulty": "medium",
        "options": [
            ("a", "Call foundation models through Amazon Bedrock on-demand."),
            ("b", "Fine-tune and host a model on Amazon SageMaker real-time endpoints."),
            ("c", "Run an open-weights model on self-managed EC2 GPU instances."),
            ("d", "Deploy a model to an EKS cluster with a custom inference server."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Amazon Bedrock gives serverless, pay-per-use access to multiple "
            "third-party and Amazon foundation models with no infrastructure to "
            "manage, which is the fastest path when you do not need custom "
            "hosting. SageMaker, EC2, and EKS all add provisioning, scaling, and "
            "operational burden you were explicitly told to avoid."
        ),
        "rationales": {
            "a": (
                True,
                "Serverless, multi-model, pay-per-use, no infra: matches every constraint.",
            ),
            "b": (
                False,
                "SageMaker endpoints mean managing hosting/scaling and usually custom models.",
            ),
            "c": (False, "Self-managed EC2 GPUs are the most operational-heavy option."),
            "d": (False, "EKS plus a custom server adds the most management overhead."),
        },
    },
    {
        "question_id": "d1-fallback-cross-region",
        "objective_ids": ["AIP-1.2"],
        "prompt": (
            "Your production application calls one Bedrock model, but that model "
            "is occasionally throttled in your primary Region, causing user-"
            "facing failures. You must improve resilience with minimal code "
            "change. What is the most appropriate design?"
        ),
        "scenario_constraint": "Improve resilience to throttling with minimal code change.",
        "difficulty": "medium",
        "options": [
            ("a", "Add retries with exponential backoff plus a cross-Region inference fallback."),
            ("b", "Immediately switch all traffic to a self-hosted model."),
            ("c", "Increase the request timeout so throttled calls eventually succeed."),
            ("d", "Cache every response indefinitely to avoid calling the model."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Bounded retries with exponential backoff absorb transient "
            "throttling, and a cross-Region inference fallback keeps the app "
            "serving when a model is constrained in one Region, all without a "
            "major rewrite. Longer timeouts do not fix throttling, indefinite "
            "caching breaks correctness, and self-hosting is a large change."
        ),
        "rationales": {
            "a": (True, "Backoff plus cross-Region fallback is the standard resilience pattern."),
            "b": (False, "Self-hosting is a major change, not minimal, and adds operational load."),
            "c": (False, "A longer timeout does not resolve throttling; it just delays failure."),
            "d": (False, "Indefinite caching returns stale/incorrect answers for dynamic prompts."),
        },
    },
    {
        "question_id": "d1-chunking-long-docs",
        "objective_ids": ["AIP-1.5"],
        "prompt": (
            "Retrieval quality is poor for a knowledge base of long, well-"
            "structured policy documents: retrieved passages often cut across "
            "unrelated sections. Which change most directly improves retrieval "
            "relevance?"
        ),
        "scenario_constraint": "Long structured documents; retrieved chunks mix unrelated sections.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Use structure-aware (hierarchical/semantic) chunking that respects section boundaries.",
            ),
            ("b", "Increase the number of results (top-k) returned for every query."),
            ("c", "Switch to a larger foundation model for generation."),
            ("d", "Remove metadata from the index to simplify retrieval."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Chunks that respect document structure keep semantically coherent "
            "passages together, which directly fixes retrieval that currently "
            "spans unrelated sections. Raising top-k adds noise, a bigger "
            "generation model does not fix retrieval inputs, and removing "
            "metadata reduces the filtering you need."
        ),
        "rationales": {
            "a": (
                True,
                "Structure-aware chunking preserves coherent passages and fixes the root cause.",
            ),
            "b": (False, "More results add noise without fixing incoherent chunks."),
            "c": (False, "Generation model size does not change what retrieval returns."),
            "d": (False, "Metadata improves filtering; removing it hurts relevance."),
        },
    },
    {
        "question_id": "d1-tenant-isolation-rag",
        "objective_ids": ["AIP-1.4"],
        "prompt": (
            "A multi-tenant RAG application must ensure one tenant can never "
            "retrieve another tenant's documents. Where should tenant isolation "
            "be enforced?"
        ),
        "scenario_constraint": "Hard guarantee: no cross-tenant document retrieval.",
        "difficulty": "hard",
        "options": [
            (
                "a",
                "Enforce tenant filtering with metadata/authorization at retrieval time, server-side.",
            ),
            ("b", "Add a sentence to the prompt telling the model not to mix tenants."),
            ("c", "Rely on the foundation model to infer tenant boundaries from context."),
            ("d", "Store all tenants together and de-duplicate results after generation."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Isolation must be a server-side authorization and metadata filter "
            "applied during retrieval, so disallowed documents are never fetched. "
            "Prompt instructions and model inference are not security controls, "
            "and post-generation de-duplication means sensitive data was already "
            "retrieved and possibly exposed."
        ),
        "rationales": {
            "a": (True, "Retrieval-time, server-side authorization is the only hard guarantee."),
            "b": (False, "Prompt instructions are not a security boundary and can be bypassed."),
            "c": (False, "Model inference cannot be trusted to enforce access control."),
            "d": (False, "Post-hoc filtering means the data was already retrieved."),
        },
    },
    {
        "question_id": "d1-prompt-regression",
        "objective_ids": ["AIP-1.6"],
        "prompt": (
            "A team keeps editing a production prompt and occasionally ships a "
            "change that quietly lowers answer quality. What practice most "
            "directly prevents these silent regressions?"
        ),
        "scenario_constraint": "Prevent silent quality regressions from prompt edits.",
        "difficulty": "medium",
        "options": [
            ("a", "Version prompts and gate changes on an evaluation test set before promotion."),
            ("b", "Let any engineer edit the live prompt and watch user complaints."),
            ("c", "Make prompts longer so they cover more cases."),
            ("d", "Store prompts only in application code comments."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Treating prompts as versioned artifacts and running them against an "
            "evaluation set before promotion catches regressions before users do. "
            "Reacting to complaints is after-the-fact, longer prompts are not "
            "inherently better, and comments are not a managed lifecycle."
        ),
        "rationales": {
            "a": (
                True,
                "Versioning plus an evaluation gate is the governed, regression-safe lifecycle.",
            ),
            "b": (False, "Watching complaints detects regressions only after users are harmed."),
            "c": (False, "Length does not equal quality and can add confusion."),
            "d": (False, "Comments provide no versioning, review, or evaluation."),
        },
    },
    {
        "question_id": "d1-multimodal-ingest",
        "objective_ids": ["AIP-1.3"],
        "prompt": (
            "An ingestion pipeline must accept scanned PDFs, images, and audio "
            "and prepare them for a text-based retrieval system. Which approach "
            "correctly prepares this mixed input?"
        ),
        "scenario_constraint": "Mixed media must become retrievable text for a text RAG system.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Extract text per modality (OCR for scans/images, transcription for audio), then validate and index.",
            ),
            ("b", "Store the raw binary files directly in the vector index."),
            ("c", "Send raw audio bytes to a text embedding model."),
            ("d", "Skip validation and index whatever each file produces."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Each modality needs the right extraction step (OCR for scanned "
            "images, transcription for audio) to produce clean text, which is "
            "then validated and indexed. Raw binaries and raw audio cannot be "
            "embedded as text, and skipping validation lets malformed input "
            "corrupt retrieval."
        ),
        "rationales": {
            "a": (
                True,
                "Modality-appropriate extraction plus validation yields clean, retrievable text.",
            ),
            "b": (False, "A text vector index cannot use raw binary files."),
            "c": (False, "A text embedding model cannot consume raw audio bytes."),
            "d": (False, "Skipping validation lets malformed content degrade retrieval."),
        },
    },
    {
        "question_id": "d1-poc-evaluation",
        "objective_ids": ["AIP-1.1"],
        "prompt": (
            "Before committing to a full build, you must prove a GenAI feature "
            "delivers business value. What makes the proof-of-concept most "
            "credible?"
        ),
        "scenario_constraint": "Demonstrate business value before full-scale investment.",
        "difficulty": "easy",
        "options": [
            (
                "a",
                "Define success metrics tied to the business outcome and measure the PoC against them.",
            ),
            ("b", "Show the demo works once on a hand-picked happy-path input."),
            ("c", "Pick the model with the most parameters and assume it is best."),
            ("d", "Measure only latency and ignore answer quality."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A credible PoC states measurable success criteria linked to the "
            "business outcome and evaluates against them. A single happy-path "
            "demo, raw model size, or latency-only measurement do not establish "
            "real value."
        ),
        "rationales": {
            "a": (True, "Outcome-linked metrics make the PoC's value measurable and defensible."),
            "b": (False, "One cherry-picked input does not demonstrate reliable value."),
            "c": (False, "Parameter count is not a proxy for business value."),
            "d": (False, "Latency alone ignores whether answers are correct or useful."),
        },
    },
    {
        "question_id": "d1-embedding-choice",
        "objective_ids": ["AIP-1.5"],
        "prompt": (
            "You must choose an embedding model for semantic search over a "
            "domain-specific corpus with a tight storage and latency budget. "
            "Which consideration should drive the choice?"
        ),
        "scenario_constraint": "Domain fit under a tight storage and latency budget.",
        "difficulty": "hard",
        "options": [
            (
                "a",
                "Balance retrieval quality on your domain against embedding dimensionality, latency, and cost.",
            ),
            ("b", "Always choose the highest-dimension embedding available."),
            ("c", "Choose whichever model has the most downloads."),
            ("d", "Use the same model that generates answers, for consistency."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Embedding selection is a trade-off: higher dimensionality can raise "
            "quality but costs more storage and latency, so you evaluate domain "
            "retrieval quality against your budget. Max dimensionality, "
            "popularity, and reusing the generation model are not grounded in "
            "your constraints."
        ),
        "rationales": {
            "a": (
                True,
                "Quality-versus-dimensionality/latency/cost trade-off fits the stated budget.",
            ),
            "b": (False, "Highest dimensionality ignores the storage and latency budget."),
            "c": (False, "Download count does not predict domain retrieval quality."),
            "d": (False, "A good generation model is not necessarily a good embedding model."),
        },
    },
    # --- AIP-1.1 additional ------------------------------------------------
    {
        "question_id": "d1-wa-genai-lens",
        "objective_ids": ["AIP-1.1"],
        "prompt": (
            "Your team is designing a production GenAI workload and wants a "
            "structured way to review it for reliability, security, cost, and "
            "operational excellence specific to generative AI. What should you use?"
        ),
        "scenario_constraint": "Need a structured, GenAI-specific architecture review.",
        "difficulty": "easy",
        "options": [
            ("a", "The AWS Well-Architected Framework with the Generative AI Lens."),
            ("b", "A one-page internal checklist written from memory."),
            ("c", "Only a cost calculator spreadsheet."),
            ("d", "A post-launch retrospective after the first outage."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "The Well-Architected Framework plus the Generative AI Lens gives a "
            "structured, GenAI-specific review across the pillars before launch. "
            "An ad hoc checklist, a cost-only view, or a post-incident review do "
            "not provide that coverage proactively."
        ),
        "rationales": {
            "a": (True, "Well-Architected + GenAI Lens is the structured, GenAI-specific review."),
            "b": (False, "An informal checklist misses pillars and is not GenAI-specific."),
            "c": (False, "Cost is one pillar; this ignores reliability, security, and ops."),
            "d": (False, "Reviewing only after an outage is reactive, not a design review."),
        },
    },
    {
        "question_id": "d1-latency-budget-design",
        "objective_ids": ["AIP-1.1"],
        "prompt": (
            "A customer-facing assistant must respond within a strict latency "
            "budget, but the best-quality model is too slow for every request. "
            "Which design best balances the business constraint?"
        ),
        "scenario_constraint": "Strict latency budget vs. a slow high-quality model.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Route simple requests to a fast model and reserve the slow model for cases that need it.",
            ),
            ("b", "Always use the slowest, highest-quality model for every request."),
            ("c", "Remove the latency budget because quality matters more."),
            ("d", "Cache one generic answer and return it for all requests."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Tiered routing by request complexity meets the latency budget while "
            "preserving quality where it matters. Using the slow model always "
            "breaks the budget, dropping the budget ignores the business "
            "constraint, and one cached answer destroys correctness."
        ),
        "rationales": {
            "a": (
                True,
                "Complexity-based routing balances latency and quality against the budget.",
            ),
            "b": (False, "Always using the slow model violates the stated latency budget."),
            "c": (False, "Discarding the constraint ignores the business requirement."),
            "d": (False, "A single cached answer is wrong for most inputs."),
        },
    },
    # --- AIP-1.2 additional ------------------------------------------------
    {
        "question_id": "d1-provisioned-throughput",
        "objective_ids": ["AIP-1.2", "AIP-2.2"],
        "prompt": (
            "A workload has steady, high-volume Bedrock traffic and needs "
            "predictable throughput and cost rather than per-request on-demand "
            "pricing. Which option fits best?"
        ),
        "scenario_constraint": "Steady high volume; predictable throughput and cost.",
        "difficulty": "medium",
        "options": [
            ("a", "Amazon Bedrock Provisioned Throughput for the model."),
            ("b", "On-demand invocation scaled by hope."),
            ("c", "A single Lambda with a fixed concurrency of one."),
            ("d", "Switching models randomly to spread load."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Provisioned Throughput gives predictable capacity and cost for "
            "steady, high-volume workloads. On-demand is better for spiky or low "
            "volume, a single-concurrency Lambda bottlenecks throughput, and "
            "random model switching does not address capacity."
        ),
        "rationales": {
            "a": (True, "Provisioned Throughput suits steady high volume with predictable cost."),
            "b": (False, "Unmanaged on-demand gives neither predictable throughput nor cost."),
            "c": (False, "Concurrency of one throttles a high-volume workload."),
            "d": (False, "Random switching does not provide capacity guarantees."),
        },
    },
    {
        "question_id": "d1-finetune-vs-rag",
        "objective_ids": ["AIP-1.2"],
        "prompt": (
            "You must ground an assistant in a large, frequently changing "
            "internal knowledge base while keeping answers current with minimal "
            "retraining. Which customization approach fits best?"
        ),
        "scenario_constraint": "Frequently changing knowledge; minimize retraining.",
        "difficulty": "medium",
        "options": [
            ("a", "Retrieval Augmented Generation over the knowledge base."),
            ("b", "Fine-tune the model nightly on the entire knowledge base."),
            ("c", "Hard-code the knowledge into the system prompt."),
            ("d", "Train a model from scratch on the documents."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "RAG keeps answers current by retrieving fresh content at query time "
            "with no retraining as the knowledge base changes. Nightly "
            "fine-tuning is costly and lags changes, prompt hard-coding does not "
            "scale to a large corpus, and training from scratch is unjustified."
        ),
        "rationales": {
            "a": (True, "RAG grounds on changing content with no retraining."),
            "b": (False, "Frequent fine-tuning is expensive and still lags updates."),
            "c": (False, "A large corpus will not fit or stay current in a prompt."),
            "d": (False, "From-scratch training is wasteful and unnecessary here."),
        },
    },
    # --- AIP-1.3 additional ------------------------------------------------
    {
        "question_id": "d1-data-quality-gate",
        "objective_ids": ["AIP-1.3"],
        "prompt": (
            "Low-quality input records are degrading model responses. You want "
            "to catch bad data before it reaches the model and track quality "
            "over time. Which approach fits best?"
        ),
        "scenario_constraint": "Catch bad input before inference; monitor quality.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Validate inputs against quality rules in the pipeline and emit quality metrics.",
            ),
            ("b", "Send all records to the model and inspect complaints later."),
            ("c", "Delete any record you are unsure about without logging."),
            ("d", "Assume upstream systems always produce clean data."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A validation stage with explicit quality rules plus emitted metrics "
            "catches bad input before inference and makes quality observable. "
            "Reacting to complaints is after the fact, silent deletion loses "
            "signal, and assuming clean data ignores the observed problem."
        ),
        "rationales": {
            "a": (True, "Pre-inference validation plus metrics is the quality gate."),
            "b": (False, "Inspecting complaints later does not prevent bad outputs."),
            "c": (False, "Silent deletion removes data and auditability."),
            "d": (False, "The scenario shows upstream data is not clean."),
        },
    },
    {
        "question_id": "d1-pii-before-model",
        "objective_ids": ["AIP-1.3", "AIP-3.2"],
        "prompt": (
            "Incoming support tickets may contain personal data that should not "
            "be sent to the model verbatim. Where should detection and redaction "
            "happen?"
        ),
        "scenario_constraint": "PII must not reach the model verbatim.",
        "difficulty": "medium",
        "options": [
            ("a", "In the ingestion/preprocessing stage, before the model call."),
            ("b", "After the model has already generated a response."),
            ("c", "Nowhere; rely on the model to ignore personal data."),
            ("d", "Only in quarterly manual audits of logs."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Detecting and redacting personal data in preprocessing ensures it "
            "never reaches the model. Post-generation is too late, trusting the "
            "model is not a control, and quarterly audits do not prevent exposure "
            "at request time."
        ),
        "rationales": {
            "a": (True, "Redaction before the model call prevents verbatim exposure."),
            "b": (False, "Post-generation redaction means PII already reached the model."),
            "c": (False, "Model behavior is not a privacy control."),
            "d": (False, "Periodic audits do not prevent real-time exposure."),
        },
    },
    # --- AIP-1.4 additional ------------------------------------------------
    {
        "question_id": "d1-vector-store-choice",
        "objective_ids": ["AIP-1.4"],
        "prompt": (
            "You want a managed way to stand up a RAG knowledge base on AWS "
            "without operating your own vector database cluster. Which option "
            "fits best?"
        ),
        "scenario_constraint": "Managed RAG; avoid running a vector DB cluster.",
        "difficulty": "easy",
        "options": [
            ("a", "Amazon Bedrock Knowledge Bases with a managed vector store."),
            ("b", "Self-hosted vector database on EC2 you patch and scale."),
            ("c", "A plain relational table with LIKE queries."),
            ("d", "Store embeddings in flat files on local disk."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Bedrock Knowledge Bases provide a managed vector store and retrieval "
            "pipeline without operating a cluster. Self-hosting adds ops burden, "
            "a relational LIKE query is not semantic search, and flat files do "
            "not scale or support vector search."
        ),
        "rationales": {
            "a": (True, "Managed Knowledge Bases avoid running your own vector cluster."),
            "b": (False, "Self-hosting is exactly the ops burden you wanted to avoid."),
            "c": (False, "LIKE queries are keyword matching, not semantic retrieval."),
            "d": (False, "Flat files do not provide scalable vector search."),
        },
    },
    {
        "question_id": "d1-vector-freshness",
        "objective_ids": ["AIP-1.4"],
        "prompt": (
            "Source documents behind a knowledge base change throughout the day, "
            "and stale retrievals are causing wrong answers. Which approach keeps "
            "retrieval current?"
        ),
        "scenario_constraint": "Documents change through the day; avoid stale retrieval.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Incrementally sync/re-index changed documents so the vector store stays current.",
            ),
            ("b", "Re-index the entire corpus once a year."),
            ("c", "Never update the index after the first load."),
            ("d", "Delete the index whenever an answer is wrong."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Incremental synchronization and re-indexing of changed documents "
            "keeps the vector store aligned with sources. Annual or never "
            "re-indexing guarantees staleness, and deleting the index on each "
            "wrong answer is destructive and does not address freshness."
        ),
        "rationales": {
            "a": (True, "Incremental change detection and re-indexing keeps retrieval current."),
            "b": (False, "Annual re-indexing leaves the index stale for most of the year."),
            "c": (False, "Never updating guarantees stale retrieval."),
            "d": (False, "Dropping the index is destructive and misses the real cause."),
        },
    },
    # --- AIP-1.5 additional ------------------------------------------------
    {
        "question_id": "d1-hybrid-search",
        "objective_ids": ["AIP-1.5"],
        "prompt": (
            "Semantic search misses results that users find by exact keyword "
            "(part numbers, error codes), while keyword search misses conceptual "
            "matches. Which retrieval approach addresses both?"
        ),
        "scenario_constraint": "Need both exact-term and conceptual matches.",
        "difficulty": "medium",
        "options": [
            ("a", "Hybrid search combining keyword and semantic retrieval, then rerank."),
            ("b", "Keyword search only."),
            ("c", "Semantic search only."),
            ("d", "Return the whole document and let the model find the answer."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Hybrid search blends lexical and semantic signals and reranks to "
            "capture both exact terms and concepts. Either method alone misses "
            "one case, and returning whole documents overflows context and buries "
            "the answer."
        ),
        "rationales": {
            "a": (True, "Hybrid + rerank captures exact terms and conceptual matches."),
            "b": (False, "Keyword-only misses conceptual matches."),
            "c": (False, "Semantic-only misses exact-term matches like codes."),
            "d": (False, "Dumping whole documents wastes context and hides answers."),
        },
    },
    {
        "question_id": "d1-reranking",
        "objective_ids": ["AIP-1.5"],
        "prompt": (
            "Your retriever returns relevant passages but often not in the best "
            "order, so the model sometimes grounds on a weaker passage. Which "
            "technique most directly improves which passages the model uses?"
        ),
        "scenario_constraint": "Relevant results retrieved but poorly ordered.",
        "difficulty": "hard",
        "options": [
            ("a", "Add a reranking model to reorder retrieved passages by relevance."),
            ("b", "Increase temperature on the generation model."),
            ("c", "Return fewer total characters at random."),
            ("d", "Disable retrieval and rely on model memory."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A reranker reorders candidates so the strongest passages are "
            "prioritized for grounding. Temperature affects generation "
            "randomness not retrieval order, random truncation can drop the best "
            "passage, and disabling retrieval removes grounding entirely."
        ),
        "rationales": {
            "a": (True, "Reranking reorders passages so the model grounds on the best ones."),
            "b": (False, "Temperature changes randomness, not retrieval ordering."),
            "c": (False, "Random truncation may discard the most relevant passage."),
            "d": (False, "Removing retrieval loses grounding on current data."),
        },
    },
    # --- AIP-1.6 additional ------------------------------------------------
    {
        "question_id": "d1-prompt-versioning",
        "objective_ids": ["AIP-1.6"],
        "prompt": (
            "Multiple engineers edit shared prompts and you need approvals, an "
            "audit trail, and the ability to roll back a bad change. Which "
            "capability best supports this governance?"
        ),
        "scenario_constraint": "Shared prompts need approval, audit, and rollback.",
        "difficulty": "medium",
        "options": [
            ("a", "Amazon Bedrock Prompt Management with versioned, governed prompts."),
            ("b", "Pasting prompts into chat messages ad hoc."),
            ("c", "Keeping the only copy in one engineer's notebook."),
            ("d", "Editing the live prompt directly with no record."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Prompt Management provides versioning, approval workflow, audit, and "
            "rollback for shared prompts. Ad hoc messages, a single private copy, "
            "or editing live with no record provide none of those governance "
            "controls."
        ),
        "rationales": {
            "a": (True, "Prompt Management gives versioning, approval, audit, and rollback."),
            "b": (False, "Ad hoc chat prompts have no governance or history."),
            "c": (False, "A private notebook is not shared, audited, or recoverable."),
            "d": (False, "Editing live with no record prevents rollback and audit."),
        },
    },
    {
        "question_id": "d1-structured-output",
        "objective_ids": ["AIP-1.6"],
        "prompt": (
            "A downstream system requires the model's output to be valid JSON "
            "matching a fixed schema, and malformed output currently breaks it. "
            "Which approach best enforces reliable structure?"
        ),
        "scenario_constraint": "Downstream needs schema-valid JSON; malformed output breaks it.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Constrain output to a JSON schema and validate it, rejecting or repairing invalid responses.",
            ),
            ("b", "Ask politely in the prompt and hope for valid JSON."),
            ("c", "Parse free-form text with brittle string splitting."),
            ("d", "Let the downstream system crash and retry forever."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Enforcing a JSON schema plus validation (and handling invalid "
            "responses) gives reliable structured output. A hopeful prompt is "
            "not a guarantee, brittle parsing fails on variation, and unbounded "
            "crash-retry is not a fix."
        ),
        "rationales": {
            "a": (True, "Schema constraint plus validation reliably enforces structure."),
            "b": (False, "A prompt request alone does not guarantee valid JSON."),
            "c": (False, "String splitting breaks on normal output variation."),
            "d": (False, "Crash-and-retry does not produce valid output."),
        },
    },
    # --- Evening-out additions (one more each for 1.2, 1.3, 1.4, 1.6) ------
    {
        "question_id": "d1-model-eval-selection",
        "objective_ids": ["AIP-1.2"],
        "prompt": (
            "You must choose between several candidate foundation models for a "
            "summarization feature and need a defensible selection rather than a "
            "gut feel. Which approach best supports the decision?"
        ),
        "scenario_constraint": "Pick among candidate FMs with a defensible, measured rationale.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Evaluate candidates on a representative dataset for quality, latency, and cost, then choose.",
            ),
            ("b", "Pick the newest model announced in a blog post."),
            ("c", "Choose the model with the largest context window regardless of task fit."),
            ("d", "Select whichever model a teammate used on a different project."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A structured evaluation on representative data across quality, "
            "latency, and cost yields a defensible model choice. Recency, raw "
            "context size, and unrelated prior use are not evidence that a model "
            "fits this task."
        ),
        "rationales": {
            "a": (
                True,
                "Measured evaluation on representative data is the defensible selection method.",
            ),
            "b": (False, "Newest-announced is not evidence of task fit."),
            "c": (False, "A large context window alone does not mean better summaries."),
            "d": (False, "Fit on a different project does not transfer to this task."),
        },
    },
    {
        "question_id": "d1-dedup-ingestion",
        "objective_ids": ["AIP-1.3"],
        "prompt": (
            "Your ingestion pipeline pulls from several overlapping sources, so "
            "near-duplicate documents inflate the index and skew retrieval toward "
            "repeated content. Which step best addresses this during ingestion?"
        ),
        "scenario_constraint": "Overlapping sources create near-duplicates that skew retrieval.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Deduplicate near-identical content during ingestion before indexing.",
            ),
            ("b", "Index everything and raise top-k to compensate."),
            ("c", "Randomly drop half of all documents to shrink the index."),
            ("d", "Trust retrieval to ignore duplicates at query time."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Detecting and removing near-duplicate content during ingestion keeps "
            "the index clean and prevents retrieval from over-weighting repeated "
            "passages. Raising top-k adds more duplicates, random dropping loses "
            "real content, and retrieval does not inherently suppress duplicates."
        ),
        "rationales": {
            "a": (True, "Ingestion-time deduplication fixes the skew at its source."),
            "b": (False, "More results surface even more duplicates."),
            "c": (False, "Random dropping discards unique content, not just duplicates."),
            "d": (False, "Retrieval does not automatically collapse duplicate passages."),
        },
    },
    {
        "question_id": "d1-metadata-filtering",
        "objective_ids": ["AIP-1.4"],
        "prompt": (
            "Users in different departments must only retrieve documents for "
            "their own department, and queries also need to scope by document "
            "type. Which knowledge-base capability supports this directly?"
        ),
        "scenario_constraint": "Scope retrieval by department and document type.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Attach metadata to documents and apply metadata filters at retrieval time.",
            ),
            ("b", "Create a separate foundation model per department."),
            ("c", "Add the department name to the end of the user's question text."),
            ("d", "Return all documents and let the model decide what applies."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Document metadata plus retrieval-time metadata filters scope results "
            "by department and type precisely. A model per department is wasteful "
            "and does not scope data, appending text to the query is unreliable, "
            "and returning everything defeats scoping and risks exposure."
        ),
        "rationales": {
            "a": (True, "Metadata filtering is the direct mechanism for scoped retrieval."),
            "b": (False, "A model per department does not control which documents are retrieved."),
            "c": (False, "Query-text hints are not an enforced retrieval filter."),
            "d": (False, "Returning everything removes the scoping the scenario requires."),
        },
    },
    {
        "question_id": "d1-few-shot-prompting",
        "objective_ids": ["AIP-1.6"],
        "prompt": (
            "A classification prompt is inconsistent on edge cases, and you want "
            "to steer the model toward the correct label format without "
            "fine-tuning. Which prompt-engineering technique fits best?"
        ),
        "scenario_constraint": "Improve consistency on edge cases without fine-tuning.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Add a few representative labeled examples (few-shot) that cover the edge cases.",
            ),
            ("b", "Remove all instructions and let the model infer the task."),
            ("c", "Repeat the same instruction several times in a row."),
            ("d", "Raise the temperature to encourage more varied answers."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Few-shot examples that cover the tricky cases demonstrate the "
            "expected label and format, improving consistency without training. "
            "Removing instructions increases ambiguity, repetition adds no new "
            "signal, and higher temperature makes outputs less consistent."
        ),
        "rationales": {
            "a": (
                True,
                "Edge-case few-shot examples steer format and consistency without training.",
            ),
            "b": (False, "Removing instructions makes the task more ambiguous."),
            "c": (False, "Repeating the same instruction adds no new guidance."),
            "d": (False, "Higher temperature reduces consistency, worsening the problem."),
        },
    },
]


def question_count() -> int:
    """Return the number of authored Domain 1 questions."""
    return len(QUESTIONS)
