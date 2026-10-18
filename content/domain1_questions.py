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
]


def question_count() -> int:
    """Return the number of authored Domain 1 questions."""
    return len(QUESTIONS)
