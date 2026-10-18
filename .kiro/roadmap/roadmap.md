# AWS Generative AI Developer Study Platform Roadmap

**Target certification:** AWS Certified Generative AI Developer – Professional (AIP-C01)  
**Roadmap status:** Proposed  
**Blueprint baseline:** AWS exam guide accessed 2026-10-18  
**Primary outcome:** Build and use a local-first study system that produces measurable exam readiness and genuine AWS implementation experience.

## 1. Product objective

Create a focused study cockpit that combines:

- Adaptive Socratic grilling and timed exam questions.
- KodeKloud-inspired lesson and hands-on lab workflows.
- Guided AWS Console walkthroughs with prediction, verification, troubleshooting, and cleanup.
- A curated, source-attributed local knowledge base.
- Durable progress, misconception, confidence, and spaced-review tracking.
- Kiro skills for coaching and a local MCP server for deterministic state.

The platform must cover every task in all five current AIP-C01 content domains. It complements—not replaces—the AWS official pretest, Skill Builder, Builder Labs, Cloud Quest, Jam, SimuLearn, and official practice exam.

### 1.1 Study modes

The learner-facing product is organized around three modes plus hands-on labs:

1. **Grill (practice).** One question at a time with immediate, explained feedback and adaptive selection. No score pressure. Primary daily-practice loop.
2. **Scored Session (exam simulation).** A timed, officially weighted set of questions that mirrors the AIP-C01 scoring mechanics, withholds feedback until submission, and reports a transparent scaled-score estimate and pass/fail. Supports multiple sessions, reset, and history.
3. **Review.** Resurfaces exactly what the learner is missing — the incorrect/unanswered items from scored sessions and spaced-repetition items from grill history — so weaknesses can be studied and closed.
4. **Labs.** Guided, learner-operated AWS Console walkthroughs with read-only validation (unchanged from the lab matrix in section 7).

### 1.2 Scored-session scoring model (official AIP-C01 mechanics)

A full scored session mirrors the official exam as documented in the AWS exam guide:

- **75 questions total: 65 scored, 10 unscored.** Unscored items are mixed in, unmarked, and do not affect the score (they model AWS pretest items).
- **Question types:** multiple choice (one correct of four) and multiple response (two or more correct of five or more). Multiple response is **all-or-nothing** — every correct option must be selected, with no partial credit.
- **Unanswered questions are scored as incorrect. There is no penalty for guessing.**
- **Scaled score 100–1000, pass at 750.** The platform computes a transparent internal estimate from the raw correct count and labels it clearly as an internal estimate, not an official AWS scaled score (AWS's scaling is proprietary and form-specific).
- **Compensatory scoring:** the overall result determines pass/fail. Per-domain results are shown only as informational strengths/weaknesses, never as per-domain pass gates.

**Scored-session selection:** the scored questions are a random subslice weighted by the official domain percentages (31/26/20/12/11) using largest-remainder rounding, with no repeats within a session, and the 10 unscored items drawn from the pool at randomized unmarked positions.

**Scaling to available content:** the selection engine always targets the official weighting, but a session may be scoped to the domains that currently have authored questions ("all available" by default, or a chosen subset). Within the available/selected domains the official relative weighting is preserved, the session is clearly labeled "not full-length" until all five domains and the full 75-item structure can be met, and the unscored-item count is 0 until the pool is large enough for 65 scored + 10 unscored to be meaningful. No code change is needed for a true full-length session once content exists; only more authored questions.

## 2. Guiding constraints

1. **Study before platform polish.** Deliver a useful quiz and lab loop quickly; defer optional sophistication.
2. **Hands-on means learner-operated.** Guide AWS Console actions, but do not automate away the learning objective.
3. **Local-first state.** SQLite is authoritative for learner state; chat history is not persistence.
4. **Primary-source grounding.** Prefer current AWS documentation and record source URL plus retrieval date.
5. **No exam dumps.** Questions must be original, licensed, or supplied by legitimate official resources.
6. **Least privilege and cost safety.** AWS validation is read-only by default; every chargeable lab has cost and cleanup gates.
7. **Original interface.** Reproduce useful learning interaction patterns, not KodeKloud branding, proprietary text, assets, or exact trade dress.
8. **Blueprint drift is expected.** Keep objectives in data so a future exam-guide update does not require application rewrites.

## 3. Definition of success

The project is successful when the learner can:

- Complete diagnostic, grill, review, lab, and mock-exam sessions from one local UI.
- Trace every question and lab to one or more AIP-C01 tasks.
- Demonstrate coverage of every task listed in section 5.
- Complete all required labs, including cleanup verification.
- Explain architecture trade-offs without notes, not merely identify service names.
- Sustain at least 80% on fresh scenario questions in every domain and at least 85% overall across two timed mocks.
- Keep confidence calibration within 10 percentage points of observed accuracy.
- Resolve all high-priority misconceptions and pass delayed recall checks.
- Complete the official AWS practice exam as the final external readiness signal.

These thresholds are internal readiness targets, not claims about AWS scoring or a guaranteed exam result.

## 4. Current exam blueprint

| Domain | Weight | Roadmap emphasis |
|---|---:|---:|
| 1. Foundation Model Integration, Data Management, and Compliance | 31% | 31% |
| 2. Implementation and Integration | 26% | 26% |
| 3. AI Safety, Security, and Governance | 20% | 20% |
| 4. Operational Efficiency and Optimization for GenAI Applications | 12% | 12% |
| 5. Testing, Validation, and Troubleshooting | 11% | 11% |

Domain weighting controls question distribution, but **no domain may be skipped**. Lower-weight domains remain mandatory readiness gates.

## 5. Required knowledge-domain specification

The following coverage contract paraphrases the current official AIP-C01 task and skill scope. Content records, questions, and labs must reference stable task IDs such as `AIP-1.4`.

### Domain 1 — Foundation Model Integration, Data Management, and Compliance (31%)

#### AIP-1.1 Analyze requirements and design GenAI solutions

Required knowledge and abilities:

- Translate business outcomes, risk, latency, scale, data, regional, and cost constraints into an architecture.
- Select appropriate foundation-model capabilities, integration styles, and deployment patterns.
- Build proof-of-concept experiments that validate feasibility, performance, and business value.
- Standardize reusable components using AWS Well-Architected guidance and the Generative AI Lens.

Required evidence: an architecture decision record, a constrained model-selection scenario, and a proof-of-concept evaluation plan.

#### AIP-1.2 Select and configure foundation models

Required knowledge and abilities:

- Compare models by capability, modality, context, quality, responsibility, latency, throughput, availability, customization, and cost.
- Decouple applications from providers and support dynamic model selection without application rewrites.
- Design fallback, circuit-breaker, cross-Region inference, and graceful-degradation behavior.
- Explain customization choices including prompting, retrieval augmentation, fine-tuning, LoRA/adapters, deployment, versioning, rollback, and retirement.
- Understand where Amazon Bedrock, SageMaker AI, Lambda, API Gateway, AppConfig, Step Functions, and Model Registry fit.

Required evidence: Lab 1 model comparison and Lab 10 resilience/model-routing exercise.

#### AIP-1.3 Implement data validation and processing pipelines for FM consumption

Required knowledge and abilities:

- Define and monitor input data quality with Glue Data Quality, Data Wrangler, Lambda, and CloudWatch patterns.
- Process text, image, audio, and tabular inputs with modality-appropriate services.
- Format requests and conversation data for model-specific Bedrock and SageMaker interfaces.
- Normalize, enrich, classify, and extract entities to improve model input quality.

Required evidence: multimodal ingestion design plus malformed-input troubleshooting scenario.

#### AIP-1.4 Design and implement vector-store solutions

Required knowledge and abilities:

- Compare Bedrock Knowledge Bases, OpenSearch Service, Aurora PostgreSQL/pgvector, and other supported metadata/vector patterns.
- Design metadata for source, author, time, tenant, access policy, domain, and lifecycle filtering.
- Plan sharding, specialized indexes, hierarchical organization, and performance at scale.
- Integrate document repositories, internal wikis, data systems, and knowledge sources.
- Keep vector stores fresh through incremental updates, change detection, synchronization, refresh, and deletion workflows.

Required evidence: Lab 3 knowledge base and a multi-tenant vector architecture review.

#### AIP-1.5 Design retrieval mechanisms for FM augmentation

Required knowledge and abilities:

- Select fixed, semantic, recursive, and hierarchical chunking based on content structure.
- Select embedding models and dimensions based on domain fit, quality, storage, latency, and cost.
- Deploy vector retrieval with OpenSearch, Aurora pgvector, or managed Bedrock Knowledge Bases.
- Implement keyword, semantic, hybrid, metadata-filtered, and reranked search.
- Apply query expansion, decomposition, rewriting, and transformation.
- Expose retrieval through stable APIs, function tools, or MCP-compatible interfaces.

Required evidence: Labs 3 and 4, including a retrieval comparison with measured relevance and latency.

#### AIP-1.6 Implement prompt engineering strategies and governance

Required knowledge and abilities:

- Define roles, instructions, examples, variables, output schemas, constraints, and guardrails.
- Manage multi-turn context, clarification, intent, and conversation state.
- Version, approve, audit, log, and roll back prompts using Prompt Management and supporting AWS services.
- Build prompt tests, edge cases, regression checks, and quality gates.
- Refine prompts systematically using structured inputs, output contracts, and feedback loops.
- Build chained and conditional prompt workflows with reusable preprocessing and postprocessing.

Required evidence: Lab 2 prompt lifecycle and a regression exercise.

### Domain 2 — Implementation and Integration (26%)

#### AIP-2.1 Implement agentic AI solutions and tool integrations

Required knowledge and abilities:

- Design agent memory, state, sessions, tool selection, and single- versus multi-agent boundaries.
- Apply structured reasoning and orchestration patterns such as ReAct without treating hidden reasoning as an application contract.
- Enforce stopping conditions, timeouts, IAM boundaries, circuit breakers, and bounded autonomy.
- Coordinate specialized models and aggregate outputs when appropriate.
- Add human review, approval, escalation, and feedback steps.
- Define, validate, observe, retry, and safely fail tool calls.
- Understand Strands Agents, AWS Agent Squad, Step Functions, Lambda, ECS, and MCP server/client patterns.

Required evidence: Lab 6 tool-using agent plus an unsafe-tool-call failure drill.

#### AIP-2.2 Implement model deployment strategies

Required knowledge and abilities:

- Choose on-demand invocation, provisioned throughput, batch/asynchronous approaches, or SageMaker endpoints by workload.
- Account for LLM memory, accelerator, model-loading, token-processing, container, and scaling characteristics.
- Use smaller or specialized models, cascading, and hybrid deployment where they improve the quality/resource balance.

Required evidence: deployment decision matrix and capacity scenario.

#### AIP-2.3 Design and implement enterprise integration architectures

Required knowledge and abilities:

- Integrate GenAI into legacy, API-based, event-driven, and synchronized enterprise systems.
- Use API Gateway, Lambda, EventBridge, queues, and workflow orchestration appropriately.
- Apply federation, role-based access, least privilege, and model/data authorization.
- Handle on-premises, edge, cross-environment, regional, and jurisdictional requirements.
- Build CI/CD with security scans, automated evaluation, quality gates, rollback, centralized gateways, and observability.

Required evidence: Lab 7 enterprise integration and CI/CD design review.

#### AIP-2.4 Implement FM API integrations

Required knowledge and abilities:

- Implement synchronous and asynchronous Bedrock interactions through AWS SDKs and queues.
- Deliver streaming responses through suitable protocols and application layers.
- Handle quotas, throttling, retries with jitter/backoff, idempotency, timeout, fallback, validation, and tracing.
- Route requests by content, complexity, model capability, policy, quality, latency, or cost.

Required evidence: Lab 7 streaming API plus throttling and fallback exercise.

#### AIP-2.5 Implement application integration patterns and development tools

Required knowledge and abilities:

- Design GenAI APIs for streaming, token limits, long-running requests, validation, and model failures.
- Build accessible application interfaces and API-first/no-code integration patterns.
- Integrate document workflows and business systems, including Bedrock Data Automation use cases.
- Use Amazon Q Developer appropriately for development, refactoring, testing, and troubleshooting.
- Implement prompt chains and AWS-native agent orchestration patterns.
- Diagnose applications using CloudWatch Logs Insights, X-Ray, and GenAI-specific failure patterns.

Required evidence: working local app integration and an observability-based debugging drill.

### Domain 3 — AI Safety, Security, and Governance (20%)

#### AIP-3.1 Implement input and output safety controls

Required knowledge and abilities:

- Filter harmful input and output using Bedrock Guardrails and layered custom moderation.
- Reduce hallucination with grounding, verification, confidence signals, semantic checks, and structured schemas.
- Design defense in depth across preprocessing, model controls, tool controls, postprocessing, and API boundaries.
- Detect and mitigate prompt injection, jailbreaks, adversarial inputs, unsafe tool parameters, and indirect injection.
- Explain why prompt instructions alone are not a security control.

Required evidence: Lab 5 guardrails and adversarial testing lab.

#### AIP-3.2 Implement data security and privacy controls

Required knowledge and abilities:

- Apply IAM, VPC endpoints, network isolation, encryption, Lake Formation, logging, and least-privilege data access.
- Detect, mask, redact, anonymize, and govern PII with services such as Comprehend, Macie, Guardrails, and S3 lifecycle controls.
- Separate tenant identity, authorization, retrieval filters, context, memory, logs, and outputs.
- Understand model-provider data handling and retention implications.

Required evidence: Lab 8 secure multi-tenant RAG threat model and implementation review.

#### AIP-3.3 Implement AI governance and compliance mechanisms

Required knowledge and abilities:

- Produce model/system cards, lineage, metadata, source attribution, and decision logs.
- Track sources with Glue Data Catalog, tagging, citations, and CloudTrail audit records.
- Map technical controls to organizational policy, regulation, and responsible-AI requirements.
- Continuously monitor misuse, policy violations, drift, bias, redaction, access, and response behavior.

Required evidence: governance control matrix and audit-trail exercise.

#### AIP-3.4 Implement responsible AI principles

Required knowledge and abilities:

- Communicate uncertainty, evidence, source attribution, and suitable user-facing explanations.
- Evaluate fairness and disparate behavior with systematic test sets and comparison workflows.
- Document intended use, limitations, exclusions, and human-oversight requirements.
- Enforce policy through guardrails and automated compliance checks.

Required evidence: responsible-AI report for a capstone system.

### Domain 4 — Operational Efficiency and Optimization (12%)

#### AIP-4.1 Implement cost optimization and resource efficiency

Required knowledge and abilities:

- Measure and reduce input/output tokens through pruning, compression, retrieval precision, and response controls.
- Route by complexity and compare price-to-performance rather than price alone.
- Apply batching, capacity planning, autoscaling, provisioned throughput, and utilization analysis.
- Use prompt, semantic, exact-match, and edge caching safely; define invalidation and privacy boundaries.

Required evidence: Lab 10 cost experiment with quality guardrails.

#### AIP-4.2 Optimize application performance

Required knowledge and abilities:

- Balance latency, quality, throughput, availability, and cost using streaming, precomputation, parallelism, and optimized models.
- Optimize retrieval indexes, query preprocessing, hybrid scoring, and reranking.
- Manage concurrency, token throughput, batch inference, model parameters, and capacity.
- Profile end-to-end service communication and vector/model bottlenecks.

Required evidence: performance benchmark and bottleneck-remediation report.

#### AIP-4.3 Implement monitoring systems for GenAI applications

Required knowledge and abilities:

- Monitor operational, model, retrieval, tool, quality, business, safety, and cost signals.
- Use CloudWatch, Bedrock Model Invocation Logging, X-Ray/traces, dashboards, alerts, and anomaly detection.
- Preserve privacy while enabling forensic traceability and auditability.
- Observe agent tools and multi-agent coordination.
- Monitor vector-store freshness, index behavior, quality, and reliability.
- Diagnose hallucination, drift, inconsistency, retrieval failure, and reasoning/workflow failure with golden datasets and traces.

Required evidence: Lab 9 observability dashboard and incident drill.

### Domain 5 — Testing, Validation, and Troubleshooting (11%)

#### AIP-5.1 Implement evaluation systems for GenAI

Required knowledge and abilities:

- Evaluate relevance, correctness, groundedness, factuality, consistency, fluency, safety, and business outcome.
- Use Bedrock Model Evaluations, offline test sets, A/B tests, canaries, multi-model comparison, and cost/latency-quality analysis.
- Gather human ratings and annotations and understand their limitations.
- Build continuous evaluation, regression tests, deployment quality gates, and reporting.
- Combine deterministic checks, model-based evaluation, LLM-as-a-judge, and human review appropriately.
- Evaluate retrieval relevance/recall/latency and agent task completion/tool effectiveness.
- Detect semantic drift and validate model or prompt updates with synthetic workflows.

Required evidence: Lab 11 evaluation harness and release-gate decision.

#### AIP-5.2 Troubleshoot GenAI applications

Required knowledge and abilities:

- Diagnose context overflow, truncation, missing content, and chunking problems.
- Diagnose API request, response, schema, permission, quota, timeout, and integration failures.
- Isolate prompt regressions through versions, repeatable test sets, and systematic refinement.
- Diagnose retrieval failures involving preprocessing, embeddings, drift, indexing, filtering, ranking, and latency.
- Use logs, traces, schema validation, output comparison, and controlled reproduction instead of random prompt changes.

Required evidence: Lab 12 multi-fault troubleshooting challenge.

## 6. Phased delivery roadmap

### Phase 0 — Baseline, safety, and blueprint lock

**Goal:** Establish scope and prevent unsafe or untraceable study content.

Deliverables:

- Machine-readable objective manifest containing all task IDs in section 5.
- Source registry with official AWS exam guide and per-domain pages.
- Learner profile: exam date, weekly capacity, AWS experience, target Region, account type, and lab budget.
- AWS lab safety policy: dedicated profile, least privilege, budget alerts, region allowlist, resource tags, and cleanup rules.
- Baseline official pretest or local diagnostic.

Exit gate:

- Every current official task is represented in the manifest.
- No lab can begin without prerequisites, expected cost class, and cleanup procedure.
- Baseline strengths, weaknesses, and confidence calibration are recorded.

### Phase 1 — Local study core MVP

**Goal:** Make adaptive study useful before building advanced UI or content automation.

Deliverables:

- Python project and pinned dependency manifest.
- SQLite schema and numbered migrations.
- Study-core services for objectives, attempts, misconceptions, spaced review, source search, and sessions.
- Local MCP tools: `start_session`, `next_question`, `grade_and_record`, `get_due_reviews`, `get_progress`, and `search_local_material`.
- Initial Kiro skills: `/aip-grill` and `/aip-review`.
- Curated seed material and at least two original scenario prompts per task.

Exit gate:

- A complete grill session survives process restart with no lost attempt data.
- Questions cannot be selected without objective and source metadata.
- Answer keys are not returned with unanswered questions.

### Phase 2 — KodeKloud-inspired learning UI

**Goal:** Create a fast, focused course-and-lab workflow without copying KodeKloud intellectual property.

Deliverables:

- Streamlit app with Today, Learn, Grill, Labs, Review, Mock, Knowledge, and Progress views.
- Persistent curriculum rail showing domains, modules, labs, completion, and due-review badges.
- Lesson player with concept content, architecture visuals, checkpoints, notes, and linked practice.
- Desktop lab workspace with resizable instruction and workspace/verification panes.
- AWS Console companion mode: open Console in a separate tab, keep steps/checkpoints visible locally, and validate through read-only tools.
- Hint ladder, “check” action, explanation panel, progress bar, elapsed time, and explicit cleanup state.
- Original visual tokens and accessible keyboard/responsive behavior.

Exit gate:

- A learner can move from lesson to associated grill questions and lab without losing context.
- Refreshing the app does not lose current session or lab progress.
- The UI clearly distinguishes verified, self-reported, failed, and not-yet-checked steps.
- No KodeKloud logos, copied screenshots, proprietary wording, or cloned brand styling are present.

**Delivery note (revised):** The workspace shipped and was then refocused per learner
direction to a four-view app — **Grill, Labs, Review, Progress** — dropping Today, Learn,
Mock, Knowledge, and the curriculum rail. The lesson-authoring workflow is deferred; the
daily loop is practice (Grill) and hands-on (Labs), with Review and Progress as adaptive
support. Thread-safe SQLite access and launch-path resolution were added so the app runs
reliably under `streamlit run`.

### Phase 2.5 — Scored sessions, scoring, and session management

**Goal:** Give the learner AWS-style scored sessions now — officially weighted question
selection, exam-accurate scoring mechanics, a transparent scaled-score estimate, review of
missed items, and full session reset/history — pulled forward from Phase 8 so it is usable
with the content that exists today and scales automatically as content grows.

Deliverables:

- **Scored-session engine** implementing the section 1.2 scoring model: official
  31/26/20/12/11 largest-remainder selection, multiple-choice and all-or-nothing
  multiple-response grading, unanswered-as-incorrect, no guessing penalty, and the
  65-scored/10-unscored structure (unscored count scales from 0 up with the pool).
- **Transparent scaled-score estimate** (raw correct, percentage, 100–1000 linear estimate,
  pass/fail at a 750 equivalent) explicitly labeled an internal estimate, not an AWS score.
- **Compensatory result** with per-domain informational breakdown, never per-domain gates.
- **Domain scope picker** defaulting to "all available domains," preserving official
  relative weighting within the selected/available domains and labeling non-full-length
  sessions clearly.
- **Delayed feedback:** no correctness, answer, or explanation shown until submission.
- **Single-session, non-accumulating state:** scored-session results are temporary and
  measurable, not an archive. At most one scored session exists at a time; starting or
  resetting a session clears the prior one. The in-progress session is persisted only so a
  browser refresh does not lose it mid-exam. There is no long-term session history.
- **Review integration:** Review surfaces the specific missed/unanswered items and weak
  objectives from the single most recent scored session, in addition to spaced-repetition
  items.
- **Original terminal/ASCII aesthetic:** a monospace, lightly colorful "hackeresque" score
  readout and session banner that remains WCAG-accessible (status is text+icon, not color
  alone) and uses original art, not copied trade dress.

Exit gate:

- A scored session selects questions by official weighting (scaled to available domains),
  grades MC and MR correctly with all-or-nothing MR and unanswered-as-incorrect, and
  reports a transparent scaled-score estimate and pass/fail labeled as an internal estimate.
- Feedback is withheld until submission; after submission the learner can review every
  missed item with its explanation.
- The learner can reset the active session; starting or resetting clears the prior session
  so only one scored session's data exists at a time (no accumulating history).
- The in-progress session survives a browser refresh.
- Review lists the missed items and weak objectives from the single most recent scored
  session.
- Per-domain results are informational only; overall pass/fail uses compensatory scoring.

### Phase 3 — Domain 1 mastery: models, data, RAG, and prompts

**Goal:** Complete the largest exam domain and establish the knowledge architecture used by later phases.

Deliverables:

- Full source coverage and question bank for AIP-1.1 through AIP-1.6.
- Lab 1: model selection and inference comparison.
- Lab 2: prompt management, structured output, versions, and regression.
- Lab 3: Bedrock Knowledge Base ingestion and baseline RAG.
- Lab 4: chunking, metadata, hybrid retrieval, reranking, freshness, and tenant filtering.
- Architecture scenarios covering Bedrock versus SageMaker, customization choices, fallback, and data processing.

Exit gate:

- All Domain 1 tasks have concept, scenario, troubleshooting, and hands-on evidence.
- At least 80% accuracy on fresh Domain 1 scenarios after a delayed review.
- Learner can explain retrieval failures and model-selection trade-offs without prompts.

Status: Implemented. The exit gate is enforced by the `MasteryEvaluator`
(`study_core/mastery.py`) and surfaced in the Progress view. It evaluates, from
committed evidence, these criteria for Domain 1: every objective practiced
(coverage), grill accuracy >= 80% (threshold exposed), no open misconceptions,
at least one Domain 1 lab completed (independent vs. assisted shown), and an
informational latest-scored-session accuracy. The result is labeled a
transparent internal study gate, not an AWS score prediction. Question bank:
24 authored Domain 1 questions (4 per task); Labs 1-4 authored.

### Phase 4 — Domain 2 mastery: agents, APIs, deployment, and enterprise integration

**Goal:** Build production integration competence rather than isolated prompt demos.

Deliverables:

- Full source coverage and question bank for AIP-2.1 through AIP-2.5.
- Lab 6: bounded tool-using agent with validation, timeout, least privilege, trace, and human escalation.
- Lab 7: streaming API, asynchronous path, retry/backoff, routing, and enterprise event integration.
- CI/CD design with evaluation gates, security scan, canary, and rollback.
- Deployment strategy and capacity exercises.

Exit gate:

- Learner can identify unsafe autonomy and integration designs.
- Agent and API failure drills are completed from logs/traces.
- At least 80% accuracy on fresh Domain 2 scenarios.

Status: Implemented. 20 authored Domain 2 questions (4 per task, AIP-2.1-2.5)
cover agents/tools, deployment/capacity, enterprise integration, FM-API
resilience, and async/routing/observability, including unsafe-autonomy and
failure-handling scenarios. Labs 6 (bounded tool-using agent: typed schema,
least-privilege IAM, timeout, trace, human escalation, unsafe-call failure
drill) and 7 (streaming + async + bounded retries + routing + throttle
fallback with correlated traces) are authored as data-driven walkthroughs. The
per-domain `MasteryEvaluator` enforces the Domain 2 exit gate (coverage,
>= 80% grill accuracy, no open misconceptions, hands-on lab completion;
informational scored-session accuracy), surfaced in the Progress view. A lab
lifecycle fix lets mandatory validator-less reasoning checkpoints complete via
committed self-report while still requiring validator evidence for Verified and
proven absence for Cleaned up.

### Phase 5 — Domain 3 mastery: safety, security, privacy, and governance

**Goal:** Make security and responsible AI architectural concerns, not final-layer filters.

Deliverables:

- Full source coverage and question bank for AIP-3.1 through AIP-3.4.
- Lab 5: input/output guardrails and adversarial testing.
- Lab 8: secure multi-tenant RAG with identity-aware retrieval and auditability.
- Threat model covering prompt injection, indirect injection, data exfiltration, tool misuse, and poisoned retrieval.
- Governance matrix, data lifecycle, lineage, model/system card, fairness test, and human-oversight plan.

Exit gate:

- Learner demonstrates defense in depth and least privilege.
- Security controls are validated at identity, data, retrieval, model, tool, output, and audit layers.
- At least 80% accuracy on fresh Domain 3 scenarios.

Status: Implemented. 16 authored Domain 3 questions (4 per task, AIP-3.1-3.4)
cover layered guardrails and prompt-injection defense, privacy/PII/residency,
identity-aware access and tenant isolation, and governance (system cards,
fairness, human oversight, lineage). Labs 5 (layered guardrails + adversarial
test set with measured block/false-positive rates) and 8 (secure multi-tenant
RAG with server-side identity-aware retrieval and an audit trail) are authored
as data-driven walkthroughs. The per-domain `MasteryEvaluator` enforces the
Domain 3 exit gate, surfaced in the Progress view; its hands-on criterion now
counts a lab for every domain it touches (not just the primary), so
multi-domain security labs register correctly.

### Phase 6 — Domain 4 mastery: operations, performance, and cost

**Goal:** Operate GenAI applications against explicit service-level and business objectives.

Deliverables:

- Full source coverage and question bank for AIP-4.1 through AIP-4.3.
- Lab 9: invocation logging, traces, quality/cost metrics, dashboards, and incident response.
- Lab 10: token reduction, routing, caching, streaming, concurrency, throughput, and retrieval optimization.
- Quality-latency-cost benchmark and optimization decision record.

Exit gate:

- Optimization never lowers quality or safety below an explicit threshold.
- Learner can identify the bottleneck from evidence before selecting a remedy.
- At least 80% accuracy on fresh Domain 4 scenarios.

Status: Implemented. 12 authored Domain 4 questions (4 per task, AIP-4.1-4.3)
cover operations/monitoring/incident response, performance optimization
(caching, token reduction, concurrency, quality-floor protection), and cost
optimization (routing, batch, attribution, provisioned vs. on-demand). Labs 9
(observability + evidence-led incident response) and 10 (cost/performance
benchmark with a before/after decision record that holds the quality
threshold) are authored as data-driven walkthroughs. The per-domain
`MasteryEvaluator` enforces the Domain 4 exit gate, surfaced in the Progress
view. Note: a placeholder-suppression fix now treats an objective as authored
only when it is the PRIMARY objective of an authored question, so a secondary
tag (e.g. a Domain 4 question also tagged AIP-5.2) no longer suppresses an
un-authored objective's grill placeholders.

### Phase 7 — Domain 5 mastery: evaluation and troubleshooting

**Goal:** Validate and repair GenAI systems systematically.

Deliverables:

- Full source coverage and question bank for AIP-5.1 and AIP-5.2.
- Lab 11: golden dataset, deterministic metrics, model-based evaluation, human feedback, and release quality gate.
- Lab 12: hidden multi-fault challenge spanning prompt, context, retrieval, IAM/API, schema, and latency issues.
- Evaluation report with limitations and stakeholder-facing comparison.

Exit gate:

- Learner uses controlled evidence rather than ad hoc prompt editing.
- Learner isolates every Lab 12 fault and proposes the narrowest justified remediation.
- At least 80% accuracy on fresh Domain 5 scenarios.

Status: Implemented. 8 authored Domain 5 questions (4 per task, AIP-5.1-5.2)
cover evaluation (golden datasets, deterministic vs. judge metrics, judge
calibration, release gates) and troubleshooting (variable isolation, retrieval
vs. generation, reproduce-before-fix, validate-recovery). Labs 11 (evaluation +
release gate with a documented go/no-go) and 12 (hidden multi-fault
troubleshooting across prompt/context/retrieval/IAM/schema/latency) are
authored as data-driven walkthroughs. The per-domain `MasteryEvaluator`
enforces the Domain 5 exit gate, surfaced in the Progress view.

**Milestone:** With all five domains authored (80 questions, 12 labs, 20/20
objectives covered), a scored session now draws the full exam structure — 65
scored + 10 unscored = 75 questions, full_length=True, no excluded domains —
entirely from authored content.

### Phase 8 — Exam simulation and readiness closure

**Goal:** Convert domain knowledge into reliable timed scenario performance and make a
defensible go/no-go decision before sitting the exam.

**Relationship to Phase 2.5:** Phase 8 reuses the Phase 2.5 scored-session engine
(selection, grading, scaled-score estimate, session history). Phase 8 adds the heavier
**readiness-gate** layer on top: fresh-form reservation, two full-length mocks, misconception
closure, the required lab matrix, and the official-practice/residual-risk review. Phase 2.5
answers "run a scored session now"; Phase 8 answers "am I ready for the real exam."

Deliverables:

- `/aip-mock` skill and timed full-length mock UI built on the Phase 2.5 engine.
- Blueprint-weighted full 75-question sessions (65 scored + 10 unscored) once all five
  domains have sufficient authored questions.
- At least two fresh full mocks with no immediate feedback and non-overlapping items.
- Weakness-directed review plan based on errors, confidence, speed, and lab evidence.
- Official AWS practice exam and final gap analysis.

Exit gate:

- At least 85% overall on two fresh internal full-length timed mocks (per-domain shown as
  informational strengths/weaknesses, consistent with the exam's compensatory scoring).
- No unresolved high-priority misconception.
- Required lab matrix is complete and cleanup is verified.
- Official practice result and remaining risk are reviewed before scheduling or sitting the exam.

### Phase 9 — Optional enhancements after demonstrated need

Potential additions:

- Local speech-to-text and oral answer mode.
- Hybrid lexical/vector retrieval if FTS5 quality is insufficient.
- Source freshness automation.
- Screenshot-assisted checkpoint evidence.
- Local question-drafting pipeline with independent review.
- Calendar integration and forecasted readiness date.
- **Multi-subject support.** Generalize the platform from a single AIP-C01 blueprint to multiple study subjects (other certifications or topics).

These are not MVP requirements and must not delay hands-on study.

#### Multi-subject support — assessment and migration path

The study loop itself (grill, scored session, review, labs, scoring, state machines, persistence) is subject-agnostic and portable. Two deliberate single-subject lock-ins would need to become per-subject configuration before a second subject can be added cleanly:

1. **`study_core/common.py: TASK_ID_PATTERN = r"^AIP-([1-5])\.([1-9])$"`** — hardcodes the AIP objective ID shape (5 domains, 9 tasks max). This must become a per-subject validator derived from the subject's blueprint, not a module-level constant.
2. **The global blueprint constants in `study_core/common.py`** — `DOMAIN_WEIGHTS`, `_DOMAIN_TASK_COUNTS`, and `ALL_TASK_IDS` encode the AIP-C01 domain weighting (31/26/20/12/11) and objective inventory. These must move behind a `Subject`/`Blueprint` entity rather than living as AWS-specific module globals.

Migration path when a measured need arises:

- Promote **subject/blueprint to a first-class entity** (table + Pydantic model) carrying its own ID, domain weights, objective inventory, and ID pattern.
- Make `TASK_ID_PATTERN` and `DOMAIN_WEIGHTS` **per-subject configuration** resolved from the active subject rather than imported constants.
- Extend the existing `blueprint_version` column toward a `subject_id` foreign key so objectives, questions, attempts, sessions, and labs are scoped to a subject.
- Keep subject facts in `content/` and configuration — never as constants inside `study_core`, preserving the inward dependency rule.

No code changes are made now; this records the shape of the work so the current AWS-specific constants are a known, contained boundary rather than a scattered assumption.

## 7. Required hands-on lab matrix

| Lab | Primary task coverage | Required proof |
|---|---|---|
| 1. Bedrock model comparison | 1.1, 1.2, 2.2, 4.1 | Recorded quality/latency/cost comparison and selection rationale |
| 2. Prompt lifecycle and structured output | 1.6, 5.1, 5.2 | Versioned prompt, schema checks, regression result |
| 3. Knowledge Base baseline RAG | 1.3, 1.4, 1.5 | Ingestion, retrieval, citations, freshness check |
| 4. Advanced retrieval | 1.4, 1.5, 4.2, 5.1, 5.2 | Chunk/search/rerank experiment with measured results |
| 5. Guardrails and adversarial inputs | 3.1, 3.4, 5.1 | Attack set, layered controls, false-positive analysis |
| 6. Bounded tool-using agent | 2.1, 3.1, 4.3, 5.1 | Tool schema, IAM boundary, timeout, trace, escalation |
| 7. Production API integration | 2.3, 2.4, 2.5 | Streaming, async path, retries, routing, traces |
| 8. Secure multi-tenant RAG | 1.4, 2.3, 3.2, 3.3 | Identity-aware retrieval tests and audit evidence |
| 9. Observability and incident response | 2.5, 4.3, 5.2 | Dashboard, alert, trace-led diagnosis |
| 10. Cost/performance optimization | 1.2, 2.2, 2.4, 4.1, 4.2 | Before/after benchmark preserving quality threshold |
| 11. Evaluation and release gate | 1.6, 3.4, 5.1 | Golden set, metrics, judge calibration, deployment decision |
| 12. Multi-fault troubleshooting | 4.3, 5.2 | Evidence-based root causes and minimal remediations |

Every lab must include prerequisites, learning objectives, architecture, estimated cost class, Region assumptions, stepwise instructions, prediction prompts, validation, failure injection, reflection questions, cleanup, and delayed recall.

## 8. UI experience specification

### Course mode

- Left rail: domain/module tree, progress, locks/prerequisites, lab and review indicators.
- Main canvas: short lesson sections with diagrams, examples, checkpoints, and “practice this” actions.
- Utility area: notes, glossary, cited sources, and objective IDs.
- Persistent header: current path, completion, due reviews, and resume action.

### Lab mode

- Left curriculum rail may collapse.
- Center instruction pane contains one active task, objective, rationale, hints, checks, and cleanup.
- Right workspace pane contains validation output, architecture/context, notes, and optional local terminal views.
- AWS Console opens in a dedicated browser tab because embedding is unreliable and can weaken security boundaries.
- Panes are resizable; active step and evidence persist across refreshes.
- Checkpoints expose `Not started`, `In progress`, `Self-reported`, `Verified`, `Failed`, and `Cleaned up` states.
- Hints are progressive: conceptual nudge, service-area hint, procedural hint, then solution with a learning penalty marker.

### Grill, scored-session, and mock modes

- Distraction-free question canvas with objective hidden during scored sessions and mocks.
- Confidence and elapsed time recorded before grading.
- Grill feedback shows result, missing concept, correct reasoning, distractor analysis, source, and next question.
- Scored sessions and mocks withhold all feedback until submission, then show the score
  readout and a review of every missed item.

### Visual aesthetic (terminal / ASCII)

- The workspace uses an original, lightly colorful "hackeresque" terminal aesthetic:
  monospace score readouts, an original ASCII-art banner, and bordered terminal-style
  panes for score summaries and session results.
- The aesthetic is decorative only and must never carry meaning by color or art alone:
  every status still pairs an icon and text, WCAG 2.2 AA contrast is preserved, and the
  ASCII banner has an accessible text equivalent.
- All art and styling are original; no copied logos, palettes, or trade dress.

### Originality and accessibility

- Use original product name, typography, color tokens, icons, copy, and component styling.
- Do not copy KodeKloud source code, screenshots, exact layouts, lesson text, or protected assets.
- Meet WCAG 2.2 AA contrast and keyboard expectations where Streamlit permits.
- Never encode status by color alone.

## 9. Content and question acceptance criteria

Every content unit must have:

- One or more exact objective IDs.
- Primary source URL, title, publisher, retrieval date, and freshness status.
- A concise explanation, architecture trade-offs, failure modes, and verification method.
- Clear distinction between AWS-documented fact, project recommendation, and learner note.

Every graded question must have:

- Objective IDs, difficulty, format, source references, answer/rubric, distractor rationales, and review status.
- A scenario constraint that matters to the answer.
- An explanation for why each option is appropriate or inappropriate.
- No unsupported absolute claims such as “always” or “never.”
- Independent review before use in readiness scoring.

## 10. Platform quality and security gates

- SQLite writes are transactional and schema migrations are versioned.
- AWS credentials are never stored in the repository or database.
- AWS validators use explicit allowlisted, read-only operations by default.
- Chargeable resources carry study-session tags and cleanup checks.
- Logs redact prompts, PII, credentials, tokens, and sensitive retrieved content.
- MCP tool contracts use validated structured inputs and outputs.
- The model cannot claim that progress, verification, or cleanup was recorded unless the corresponding tool succeeds.
- Generated content cannot enter the scored bank without source checks and review.

## 11. Source baseline

Primary blueprint sources:

- [AWS AIP-C01 exam overview](https://docs.aws.amazon.com/aws-certification/latest/examguides/ai-professional-01.html)
- [Domain 1](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01-domain1.html)
- [Domain 2](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01-domain2.html)
- [Domain 3](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01-domain3.html)
- [Domain 4](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01-domain4.html)
- [Domain 5](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01-domain5.html)
- [AWS certification page and official preparation path](https://aws.amazon.com/certification/certified-generative-ai-developer-professional)

Interaction-pattern reference:

- [KodeKloud Labs Introduction](https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Linux-Basics/Labs-Introduction)

Content based on web sources has been summarized and rephrased. Revalidate the blueprint before major content releases and again before the exam date.
