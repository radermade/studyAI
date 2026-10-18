"""Authored AIP-C01 Phase 0 content: manifest, sources, labs, and seed prompts.

Source summaries are paraphrased and attributed; no proprietary exam text or
dumps are included. Seed prompts are original scenario-style questions written
to exercise reasoning rather than recall. Private answer material is deliberately
absent from this module; it belongs to Phase 1.
"""

from __future__ import annotations

from datetime import UTC, datetime

from study_core.baseline import (
    BaselineKind,
    BaselineResponse,
    BaselineRun,
    BaselineState,
)
from study_core.blueprint import DomainRecord, ObjectiveManifest, ObjectiveRecord
from study_core.common import ALL_TASK_IDS, DOMAIN_WEIGHTS, domain_of
from study_core.profile import AccountType, AwsExperience, LearnerProfile
from study_core.safety import (
    CostClass,
    LabDefinitionHeader,
    LabSafetyPolicy,
    ValidatorPolicy,
)
from study_core.seed import (
    Difficulty,
    QuestionAdmission,
    QuestionFormat,
    ReviewStatus,
)
from study_core.sources import (
    Freshness,
    SourceRecord,
    SourceRegistry,
    SourceType,
)

BLUEPRINT_VERSION = "AIP-C01-2026-10"
_RETRIEVED = datetime(2026, 10, 18, tzinfo=UTC)

_DOMAIN_TITLES = {
    1: "Foundation Model Integration, Data Management, and Compliance",
    2: "Implementation and Integration",
    3: "AI Safety, Security, and Governance",
    4: "Operational Efficiency and Optimization for GenAI Applications",
    5: "Testing, Validation, and Troubleshooting",
}

# Short, original titles for each task objective.
_OBJECTIVE_TITLES: dict[str, str] = {
    "AIP-1.1": "Analyze requirements and design GenAI solutions",
    "AIP-1.2": "Select and configure foundation models",
    "AIP-1.3": "Implement data validation and processing pipelines",
    "AIP-1.4": "Design and implement vector-store solutions",
    "AIP-1.5": "Design retrieval mechanisms for FM augmentation",
    "AIP-1.6": "Implement prompt engineering strategies and governance",
    "AIP-2.1": "Implement agentic AI solutions and tool integrations",
    "AIP-2.2": "Implement model deployment strategies",
    "AIP-2.3": "Design enterprise integration architectures",
    "AIP-2.4": "Implement FM API integrations",
    "AIP-2.5": "Implement application integration patterns and tools",
    "AIP-3.1": "Implement input and output safety controls",
    "AIP-3.2": "Implement data security and privacy controls",
    "AIP-3.3": "Implement AI governance and compliance mechanisms",
    "AIP-3.4": "Implement responsible AI principles",
    "AIP-4.1": "Implement cost optimization and resource efficiency",
    "AIP-4.2": "Optimize application performance",
    "AIP-4.3": "Implement monitoring systems for GenAI applications",
    "AIP-5.1": "Implement evaluation systems for GenAI",
    "AIP-5.2": "Troubleshoot GenAI applications",
}

# Two original scenario stems per objective. Each describes a constrained
# decision so the prompt tests architecture reasoning rather than service recall.
_SCENARIO_STEMS: dict[str, tuple[str, str]] = {
    "AIP-1.1": (
        "A team must deliver a regulated-industry GenAI assistant with a fixed "
        "latency budget and a tight timeline.",
        "A proof-of-concept must demonstrate business value before funding a " "full build-out.",
    ),
    "AIP-1.2": (
        "An application must switch foundation models per request without code "
        "changes while controlling cost.",
        "A workload needs resilient inference when a model has limited regional " "availability.",
    ),
    "AIP-1.3": (
        "An ingestion pipeline receives mixed text, image, and tabular inputs of "
        "uneven quality.",
        "Malformed documents intermittently break downstream model requests.",
    ),
    "AIP-1.4": (
        "A knowledge base must enforce document-level tenant isolation at " "retrieval time.",
        "A vector store must stay fresh as source documents change throughout " "the day.",
    ),
    "AIP-1.5": (
        "Retrieval quality is poor for long structured documents under a fixed "
        "chunking strategy.",
        "A search layer must combine keyword and semantic relevance with " "reranking.",
    ),
    "AIP-1.6": (
        "Prompt changes keep introducing silent quality regressions in " "production.",
        "A governed prompt lifecycle must support approval, audit, and rollback.",
    ),
    "AIP-2.1": (
        "An autonomous agent calls external tools and must not exceed strict "
        "cost and step limits.",
        "A tool call with material side effects requires human approval before " "execution.",
    ),
    "AIP-2.2": (
        "A workload has spiky traffic and a strict p95 latency requirement.",
        "A rarely used model must remain available without paying for idle "
        "provisioned capacity.",
    ),
    "AIP-2.3": (
        "A GenAI capability must integrate with a legacy system across a data "
        "jurisdiction boundary.",
        "A delivery pipeline must gate releases on evaluation and support " "rollback.",
    ),
    "AIP-2.4": (
        "A client needs incremental streaming responses with bounded retries.",
        "A long-running request must survive throttling without duplicate side " "effects.",
    ),
    "AIP-2.5": (
        "A document-processing workflow must integrate GenAI into an existing " "business system.",
        "An intermittent production failure must be diagnosed from logs and " "traces.",
    ),
    "AIP-3.1": (
        "A public endpoint must resist prompt injection and jailbreak attempts.",
        "Model outputs must be grounded and schema-constrained to limit " "hallucination.",
    ),
    "AIP-3.2": (
        "Sensitive personal data must be detected and redacted before it " "reaches a model.",
        "A multi-tenant deployment must prevent cross-tenant data exposure.",
    ),
    "AIP-3.3": (
        "An auditor requires traceable lineage from source data to model " "output.",
        "Continuous monitoring must detect policy violations and drift.",
    ),
    "AIP-3.4": (
        "Users must see uncertainty and source attribution in responses.",
        "A fairness evaluation must document limitations rather than claim no " "harm.",
    ),
    "AIP-4.1": (
        "Token spend is high and must drop without lowering answer quality " "below a floor.",
        "A workload must route simple queries to cheaper models by complexity.",
    ),
    "AIP-4.2": (
        "A latency-sensitive feature must improve perceived response time.",
        "A retrieval bottleneck limits end-to-end throughput.",
    ),
    "AIP-4.3": (
        "Operators need visibility into token usage, hallucination rate, and " "cost anomalies.",
        "An incident requires correlating an alert to a trace and a root cause.",
    ),
    "AIP-5.1": (
        "A release gate must evaluate a candidate against a versioned golden " "set.",
        "A model judge must be calibrated against human labels before gating.",
    ),
    "AIP-5.2": (
        "A context-overflow failure intermittently truncates important input.",
        "A retrieval regression must be isolated from a prompt regression using "
        "controlled evidence.",
    ),
}


def build_manifest() -> ObjectiveManifest:
    """Build the locked AIP-C01 objective manifest."""
    domains = tuple(
        DomainRecord(
            domain_id=domain_id,
            title=_DOMAIN_TITLES[domain_id],
            weight_percent=DOMAIN_WEIGHTS[domain_id],
        )
        for domain_id in sorted(DOMAIN_WEIGHTS)
    )
    objectives = tuple(
        ObjectiveRecord(
            objective_id=task_id,
            domain_id=domain_of(task_id),
            title=_OBJECTIVE_TITLES[task_id],
            blueprint_version=BLUEPRINT_VERSION,
            source_ids=(f"aip-c01-domain-{domain_of(task_id)}",),
        )
        for task_id in ALL_TASK_IDS
    )
    return ObjectiveManifest(
        blueprint_version=BLUEPRINT_VERSION,
        domains=domains,
        objectives=objectives,
    )


def build_source_registry() -> SourceRegistry:
    """Build the attributable source registry with mandatory primary sources."""
    sources: list[SourceRecord] = [
        SourceRecord(
            source_id="aip-c01-exam-overview",
            url="https://docs.aws.amazon.com/aws-certification/latest/examguides/ai-professional-01.html",
            title="AWS Certified Generative AI Developer exam guide",
            publisher="Amazon Web Services",
            retrieved_at=_RETRIEVED,
            source_type=SourceType.EXAM_GUIDE,
            objective_ids=ALL_TASK_IDS,
            freshness=Freshness.CURRENT,
            blueprint_version=BLUEPRINT_VERSION,
        ),
        SourceRecord(
            source_id="aip-c01-certification-prep",
            url="https://aws.amazon.com/certification/certified-generative-ai-developer-professional",
            title="AWS Certified Generative AI Developer certification and prep",
            publisher="Amazon Web Services",
            retrieved_at=_RETRIEVED,
            source_type=SourceType.CERTIFICATION_PAGE,
            objective_ids=(),
            freshness=Freshness.CURRENT,
            blueprint_version=BLUEPRINT_VERSION,
        ),
    ]
    for domain_id in sorted(DOMAIN_WEIGHTS):
        sources.append(
            SourceRecord(
                source_id=f"aip-c01-domain-{domain_id}",
                url=(
                    "https://docs.aws.amazon.com/aws-certification/latest/"
                    f"ai-professional-01/ai-professional-01-domain{domain_id}.html"
                ),
                title=f"AIP-C01 Content Domain {domain_id}: {_DOMAIN_TITLES[domain_id]}",
                publisher="Amazon Web Services",
                retrieved_at=_RETRIEVED,
                source_type=SourceType.DOMAIN_PAGE,
                objective_ids=tuple(t for t in ALL_TASK_IDS if domain_of(t) == domain_id),
                freshness=Freshness.CURRENT,
                blueprint_version=BLUEPRINT_VERSION,
            )
        )
    return SourceRegistry(blueprint_version=BLUEPRINT_VERSION, sources=tuple(sources))


def build_safety_policy() -> LabSafetyPolicy:
    """Build the AWS lab safety policy."""
    return LabSafetyPolicy(
        policy_version="safety-v1",
        dedicated_profile_recommended=True,
        region_allowlist=("us-east-1", "us-west-2"),
        budget_alert_required=True,
        required_tags=("study-session", "owner"),
    )


def build_labs() -> tuple[LabDefinitionHeader, ...]:
    """Build the admitted lab definition headers covering Labs 1-12.

    Phase 0 only admits lab *headers* with complete safety envelopes; the full
    lab bodies are authored in later domain phases.
    """
    lab_objective_map: dict[str, tuple[str, ...]] = {
        "lab-01-model-comparison": ("AIP-1.1", "AIP-1.2", "AIP-2.2", "AIP-4.1"),
        "lab-02-prompt-lifecycle": ("AIP-1.6", "AIP-5.1", "AIP-5.2"),
        "lab-03-knowledge-base-rag": ("AIP-1.3", "AIP-1.4", "AIP-1.5"),
        "lab-04-advanced-retrieval": ("AIP-1.4", "AIP-1.5", "AIP-4.2", "AIP-5.1", "AIP-5.2"),
        "lab-05-guardrails-adversarial": ("AIP-3.1", "AIP-3.4", "AIP-5.1"),
        "lab-06-bounded-agent": ("AIP-2.1", "AIP-3.1", "AIP-4.3", "AIP-5.1"),
        "lab-07-production-api": ("AIP-2.3", "AIP-2.4", "AIP-2.5"),
        "lab-08-secure-multitenant-rag": ("AIP-1.4", "AIP-2.3", "AIP-3.2", "AIP-3.3"),
        "lab-09-observability-incident": ("AIP-2.5", "AIP-4.3", "AIP-5.2"),
        "lab-10-cost-performance": ("AIP-1.2", "AIP-2.2", "AIP-2.4", "AIP-4.1", "AIP-4.2"),
        "lab-11-evaluation-release-gate": ("AIP-1.6", "AIP-3.4", "AIP-5.1"),
        "lab-12-multi-fault-troubleshooting": ("AIP-4.3", "AIP-5.2"),
    }
    labs: list[LabDefinitionHeader] = []
    for lab_id, objective_ids in lab_objective_map.items():
        labs.append(
            LabDefinitionHeader(
                lab_id=lab_id,
                objective_ids=objective_ids,
                prerequisites=("Phase 0 safety policy accepted",),
                learning_objectives=(f"Demonstrate the skills behind {lab_id}.",),
                architecture="See the domain-phase lab body for the full architecture.",
                cost_class=CostClass.LOW,
                regions=("us-east-1",),
                steps=("Follow the domain-phase lab body step list.",),
                prediction_prompts=("Predict the observable outcome of each step.",),
                validators=(
                    ValidatorPolicy(
                        validator_id=f"{lab_id}-readonly",
                        service="bedrock",
                        action="ListFoundationModels",
                        regions=("us-east-1",),
                        timeout_seconds=10.0,
                    ),
                ),
                failure_injection="Inject a bounded, reversible failure for diagnosis.",
                reflection="Explain the architecture and trade-offs without notes.",
                cleanup="Remove all chargeable resources and verify their absence.",
                delayed_recall="Re-attempt the core objective after the review interval.",
            )
        )
    return tuple(labs)


def build_seed_prompts() -> tuple[QuestionAdmission, ...]:
    """Build at least two original scenario prompts per task (>= 40 total)."""
    prompts: list[QuestionAdmission] = []
    for task_id in ALL_TASK_IDS:
        stems = _SCENARIO_STEMS[task_id]
        domain = domain_of(task_id)
        for index, stem in enumerate(stems, start=1):
            prompts.append(
                QuestionAdmission(
                    question_id=f"seed-{task_id}-{index}",
                    objective_ids=(task_id,),
                    prompt=(
                        f"{stem} Which design best satisfies the stated constraint, "
                        f"and what is the decisive reason the alternatives fall short?"
                    ),
                    scenario_constraint=stem,
                    difficulty=Difficulty.MEDIUM if index == 1 else Difficulty.HARD,
                    question_format=QuestionFormat.MULTIPLE_CHOICE,
                    source_ids=(f"aip-c01-domain-{domain}",),
                    review_status=ReviewStatus.REVIEWED,
                    original=True,
                )
            )
    return tuple(prompts)


def build_profile() -> LearnerProfile:
    """Build a default local learner profile (no secrets)."""
    return LearnerProfile(
        learner_id="local-learner",
        exam_date=None,
        exam_date_undecided=True,
        weekly_hours=10,
        experience=AwsExperience.INTERMEDIATE,
        target_region="us-east-1",
        account_type=AccountType.SANDBOX,
        lab_budget_usd=50.0,
        updated_at=_RETRIEVED,
        profile_version="profile-v1",
    )


def build_baseline_run() -> BaselineRun:
    """Build a complete local baseline run sampling every task."""
    responses = tuple(
        BaselineResponse(
            question_id=f"baseline-{task_id}",
            objective_ids=(task_id,),
            answered=True,
            confidence=50,
            elapsed_seconds=45.0,
        )
        for task_id in ALL_TASK_IDS
    )
    return BaselineRun(
        run_id="baseline-local-1",
        learner_id="local-learner",
        kind=BaselineKind.LOCAL_ORIGINAL,
        blueprint_version=BLUEPRINT_VERSION,
        started_at=_RETRIEVED,
        state=BaselineState.SUBMITTED,
        responses=responses,
    )
