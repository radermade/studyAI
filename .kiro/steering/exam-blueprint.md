# AIP-C01 authoritative blueprint (from the official AWS exam guide)

Source of truth: `./.kiro/steering/AWS-Certified-Generative-AI-Developer-Pro_Exam-Guide.pdf`
(AWS Certified Generative AI Developer – Professional, Exam Guide v1.0). Extracted
2026 from the official PDF. When authoring or reviewing questions, defer to this
file over any secondary site or model recollection.

## Exam mechanics (official)

- 65 scored questions + 10 unscored (unmarked) = 75 total. 180 minutes.
- Scaled score 100–1000; pass at 750; compensatory (overall pass/fail, no
  per-domain gate). Unanswered = incorrect; no guessing penalty.

## Question types (official — AIP-C01 uses these four)

1. **Multiple choice** — 1 correct of 4.
2. **Multiple response** — 2+ correct of 5+; must select all correct for credit.
3. **Ordering** — place 3–6 responses into the correct order (dropdown). Some
   questions use ALL responses, others only SOME; the instructions state how
   many. Must select the right responses AND order them correctly for credit
   (all-or-nothing).
4. **Matching** — match a list of 3–6 prompts to responses (dropdown). Responses
   may be used once, multiple times, or not at all; the instructions state how.
   Must get EVERY pair correct for credit (all-or-nothing).

Scoring and placement (per the AWS Training & Certification blog on new question
types): every ordering/matching question has the SAME scoring value as a
multiple-choice or multiple-response question — ordering is NOT weighted more
despite requiring a correct sequence. All types are mixed throughout the exam
and drawn from any domain, so distribute them across domains by the normal
31/26/20/12/11 weighting.

Case study (a shared scenario with 2+ separately-scored sub-questions) is a
program-wide new type but is NOT listed in the AIP-C01 exam guide's question-
types section, so treat it as out of scope for this exam unless AWS updates the
guide.

Status in our bank: multiple_choice and multiple_response are implemented and
authored. **Ordering and matching are NOT yet implemented** (no data model,
grading, UI, or authored questions). This is a known gap to close.

## Domains and weightings (official)

| Domain | Title | Weight |
|---|---|---|
| 1 | Foundation Model Integration, Data Management, and Compliance | 31% |
| 2 | Implementation and Integration | 26% |
| 3 | AI Safety, Security, and Governance | 20% |
| 4 | Operational Efficiency and Optimization for GenAI Applications | 12% |
| 5 | Testing, Validation, and Troubleshooting | 11% |

## Tasks and skills (official wording — author questions to these)

Domain 1: 1.1 analyze requirements & design (WA GenAI Lens, PoC via Bedrock);
1.2 select/configure FMs (benchmarks, dynamic routing via Lambda/API Gateway/
AppConfig, resilience via Step Functions circuit breakers + Bedrock Cross-Region
Inference, customization via SageMaker + LoRA/adapters + Model Registry);
1.3 data validation/processing (Glue Data Quality, SageMaker Data Wrangler,
multimodal via Bedrock + SageMaker Processing + Transcribe, JSON formatting,
Comprehend entity extraction); 1.4 vector stores (Bedrock Knowledge Bases,
OpenSearch Neural plugin, RDS+S3, DynamoDB, metadata frameworks, sharding/
multi-index, freshness/sync); 1.5 retrieval (chunking incl. hierarchical, Titan
embeddings, OpenSearch/Aurora pgvector/Knowledge Bases, hybrid search +
reranker, query expansion/decomposition via Lambda/Step Functions, function
calling + MCP access); 1.6 prompt engineering/governance (Bedrock Prompt
Management + Guardrails, Step Functions clarification, Comprehend intent,
DynamoDB history, CloudTrail/CloudWatch Logs, QA via Lambda/Step Functions/
CloudWatch, chain-of-thought, Prompt Flows chains/branching).

Domain 2: 2.1 agentic AI (Strands Agents, AWS Agent Squad, MCP, Step Functions
ReAct, stopping conditions/timeouts/IAM boundaries/circuit breakers, model
ensembles, human review via Step Functions/API Gateway, Strands API custom
tools + Lambda validation, Lambda stateless MCP servers + ECS complex MCP
servers); 2.2 deployment (Lambda on-demand, Bedrock provisioned throughput,
SageMaker endpoints, container memory/GPU/token patterns, smaller models +
API-based model cascading); 2.3 enterprise integration (API-based legacy +
event-driven loose coupling, API Gateway microservices + Lambda webhooks +
EventBridge, identity federation + RBAC + least-privilege FM access, Outposts/
Wavelength for jurisdiction, CodePipeline/CodeBuild CI/CD + GenAI gateway);
2.4 FM API integration (Bedrock sync APIs + SDKs + SQS async + API Gateway
validation, streaming APIs + WebSockets/SSE + chunked transfer, SDK exponential
backoff + API Gateway rate limiting + fallback + X-Ray, routing via static/Step
Functions dynamic/metric-based/API Gateway); 2.5 app integration/dev tools
(API Gateway streaming + token limits + retries, Amplify UI + OpenAPI + Prompt
Flows no-code, Lambda CRM + Step Functions doc processing + Q Business +
Bedrock Data Automation, Q Developer productivity, Strands/Agent Squad + Step
Functions orchestration + Bedrock prompt chaining, CloudWatch Logs Insights +
X-Ray + Q Developer troubleshooting).

Domain 3: 3.1 input/output safety (Bedrock Guardrails filter in/out, Step
Functions/Lambda moderation, specialized eval for toxicity, text-to-SQL
determinism, Knowledge Base grounding + confidence/semantic verification + JSON
Schema, defense-in-depth Comprehend pre + Bedrock model + Lambda post + API
Gateway filter, prompt-injection/jailbreak detection + sanitization + classifiers
+ adversarial testing); 3.2 data security/privacy (VPC endpoints + IAM + Lake
Formation + CloudWatch, Comprehend + Macie PII, Bedrock native privacy +
Guardrails + S3 Lifecycle retention, masking/anonymization); 3.3 governance/
compliance (SageMaker model cards, Glue data lineage + Glue Data Catalog +
metadata tagging + CloudTrail audit, org governance frameworks, continuous
misuse/drift/bias monitoring + token redaction + output filters); 3.4 responsible
AI (reasoning displays + CloudWatch confidence/uncertainty + source attribution +
Bedrock agent tracing, fairness metrics in CloudWatch + Prompt Management/Flows
A/B + Bedrock LLM-as-a-judge, Guardrails by policy + model cards + Lambda
compliance checks).

Domain 4: 4.1 cost (token estimation/tracking + context-window optimization +
prompt compression/pruning + response limiting, cost-capability tradeoff + tiered
FM by complexity + price-performance, batching + capacity planning + auto-scaling
+ provisioned throughput, semantic caching + result fingerprinting + edge/prompt
caching); 4.2 performance (pre-computation + latency-optimized Bedrock models +
parallel requests + streaming + benchmarking, index optimization + query
preprocessing + hybrid search, token processing + batch inference + concurrency,
model-specific params + A/B + temperature/top-k/top-p, capacity/utilization +
auto-scaling, API profiling + vector query optimization + LLM latency reduction);
4.3 monitoring (operational/performance/FM-interaction tracing + business metrics
+ dashboards, CloudWatch token usage/prompt effectiveness/hallucination rates/
response quality + anomaly detection + Bedrock Model Invocation Logs + cost
anomaly, observability dashboards + audit logging + behavior tracking, tool-call
observability + multi-agent coordination, vector store monitoring + index
optimization, golden datasets for hallucination + output diffing + reasoning-path
tracing).

Domain 5: 5.1 evaluation (relevance/accuracy/consistency/fluency metrics, Bedrock
Model Evaluations + A/B + canary + multi-model + cost-performance, feedback/
rating/annotation, continuous eval + regression + quality gates, RAG evaluation +
LLM-as-a-Judge + human feedback, retrieval relevance/context-match/latency,
agent task-completion + tool-usage + Bedrock Agent evaluations + reasoning
quality, reporting/visualization, deployment validation via synthetic workflows +
hallucination/semantic-drift checks); 5.2 troubleshooting (context-window overflow
+ dynamic chunking + truncation analysis, API integration error logging/validation,
prompt testing frameworks + version comparison, retrieval relevance + embedding
diagnostics + drift + vectorization + chunking remediation + vector search tuning,
template testing + CloudWatch Logs prompt-confusion + X-Ray observability +
schema validation).

## In-scope AWS services (author only from these)

Analytics: Athena, EMR, Glue, Kinesis, OpenSearch Service, QuickSight, MSK.
Application Integration: AppFlow, AppConfig, EventBridge, SNS, SQS, Step Functions.
Compute: App Runner, EC2, Lambda, Lambda@Edge, Outposts, Wavelength.
Containers: ECR, ECS, EKS, Fargate.
Customer Engagement: Amazon Connect.
Database: Aurora, DocumentDB, DynamoDB, DynamoDB Streams, ElastiCache, Neptune, RDS.
Developer Tools: Amplify, CDK, CLI, CloudFormation, CodeArtifact, CodeBuild,
CodeDeploy, CodePipeline, Tools and SDKs, X-Ray.
Machine Learning: Augmented AI (A2I), Bedrock, Bedrock AgentCore, Bedrock
Knowledge Bases, Bedrock Prompt Management, Bedrock Prompt Flows, Comprehend,
Kendra, Lex, Q Business, Q Business Apps, Q Developer, Rekognition, SageMaker AI,
SageMaker Clarify, SageMaker Data Wrangler, SageMaker Ground Truth, SageMaker
JumpStart, SageMaker Model Monitor, SageMaker Model Registry, SageMaker Neo,
SageMaker Processing, SageMaker Unified Studio, Textract, Titan, Transcribe.
Management/Governance: Auto Scaling, Chatbot, CloudTrail, CloudWatch, CloudWatch
Logs, CloudWatch Synthetics, Cost Anomaly Detection, Cost Explorer, Managed
Grafana, Service Catalog, Systems Manager, Well-Architected Tool.
Migration/Transfer: DataSync, Transfer Family.
Networking/Content Delivery: API Gateway, AppSync, CloudFront, ELB, Global
Accelerator, PrivateLink, Route 53, VPC.
Security/Identity/Compliance: Cognito, Encryption SDK, IAM, IAM Access Analyzer,
IAM Identity Center, KMS, Macie, Secrets Manager, WAF.
Storage: EBS, EFS, S3, S3 Intelligent-Tiering, S3 Lifecycle policies, S3 Cross-Region
Replication.

## Notable OUT-of-scope services (must NOT be the keyed answer / preferably avoid)

Amazon MQ; Clean Rooms, Data Exchange, DataZone, FinSpace; Managed Blockchain;
Alexa for Business, Chime, Wickr, WorkDocs, WorkMail; AWS Budgets, Cost and Usage
Report, Reserved Instance reports, Savings Plans; Batch, EC2 Image Builder, ECS/EKS
Anywhere, Elastic Beanstalk, Lightsail, Local Zones, Serverless Application
Repository; App2Container, Copilot, ROSA; Amazon SES. (List is non-exhaustive; see
the PDF appendix.)

## Authoring guidance derived from the guide

- Use official short service names (e.g. "Amazon SNS", "Amazon API Gateway").
- Keep questions scenario-based and decision-oriented (AWS's own samples are long
  scenarios asking for the BEST design under constraints), not recall.
- Prefer the services AWS names in the relevant skill statement as the keyed
  answer; use other in-scope services as plausible distractors.
- Do not key an answer to an out-of-scope service.
- Known gap: author Ordering and Matching items once those formats are supported.
