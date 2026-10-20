"""Authored Domain 3 (AIP-C01) ordering and matching questions.

See content/domain1_ordering_matching.py for the ordering/matching dict shapes.
Domain 3 covers AI safety, security, and governance. All AWS services referenced
here are in-scope for AIP-C01; keyed answers never use out-of-scope services.
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = []

QUESTIONS.extend(
    [
        {
            "question_id": "d3o-layered-guardrail-flow",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A chat assistant must apply defense-in-depth so that both the user "
                "input and the model output pass through safety controls. Place the "
                "steps in the correct order."
            ),
            "scenario_constraint": "Request must flow input-side checks before output-side checks.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Apply the Amazon Bedrock Guardrails input policy to the user prompt."),
                ("b", "Invoke the foundation model to generate a candidate response."),
                ("c", "Apply the Amazon Bedrock Guardrails output policy to the response."),
                ("d", "Return the filtered response to the user."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The input guardrail screens the prompt first, the model generates "
                "only after input passes, the output guardrail filters the generation, "
                "and the user receives the response last."
            ),
            "rationales": {
                "a": (True, "Input filtering must happen before invoking the model."),
                "b": (True, "Generation follows a clean input and precedes output filtering."),
                "c": (True, "The output policy screens the generated text before delivery."),
                "d": (True, "Delivery is last, only after output filtering."),
            },
        },
        {
            "question_id": "d3o-pii-redaction-pipeline",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "An intake pipeline must remove personal data from documents before "
                "they are embedded for retrieval. Place the steps in the correct order."
            ),
            "scenario_constraint": "PII must be detected and redacted before downstream use.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Detect PII entities in the raw text with Amazon Comprehend."),
                ("b", "Redact or mask the detected PII spans."),
                ("c", "Embed and index the redacted text for retrieval."),
                ("d", "Write an audit log entry recording the redaction."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Detection identifies the spans, redaction removes them, the clean text "
                "is then indexed, and the redaction is logged for audit."
            ),
            "rationales": {
                "a": (True, "Detection must precede redaction."),
                "b": (True, "Redaction follows detection and precedes indexing."),
                "c": (True, "Only redacted text should be embedded and indexed."),
                "d": (True, "The audit entry records the completed redaction."),
            },
        },
        {
            "question_id": "d3o-safety-incident-response",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Monitoring flags that a deployed assistant produced harmful output in "
                "production. Place the incident-response steps in the correct order."
            ),
            "scenario_constraint": "Containment precedes diagnosis and permanent fixes.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Detect the harmful output from CloudWatch alarms on safety metrics."),
                ("b", "Contain impact by tightening the Amazon Bedrock Guardrails policy."),
                ("c", "Investigate root cause using CloudTrail and model invocation logs."),
                ("d", "Deploy a validated fix and update the model card."),
                ("e", "Conduct a post-incident review and record lessons learned."),
            ],
            "correct_sequence": ["a", "b", "c", "d", "e"],
            "correct_option_ids": [],
            "explanation": (
                "Detection triggers the response, containment limits blast radius first, "
                "investigation finds the cause, a validated fix is deployed with updated "
                "governance artifacts, and the review closes the loop."
            ),
            "rationales": {
                "a": (True, "An incident starts with detection."),
                "b": (True, "Containment limits harm before deeper diagnosis."),
                "c": (True, "Root-cause analysis follows containment."),
                "d": (True, "The permanent fix and documentation come after diagnosis."),
                "e": (True, "The retrospective is the final step."),
            },
        },
        {
            "question_id": "d3o-multitenant-access-setup",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "You are securing a multi-tenant retrieval service so each tenant only "
                "sees its own documents. Place the steps in the correct order."
            ),
            "scenario_constraint": "Isolation must be enforced before any tenant query runs.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Define per-tenant IAM policies scoped to that tenant's data."),
                (
                    "b",
                    "Register tenant data in AWS Lake Formation with row-level permissions.",
                ),
                ("c", "Authenticate the caller and resolve the tenant identity."),
                ("d", "Execute the retrieval query under the tenant-scoped permissions."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "IAM policies and Lake Formation permissions establish enforced isolation "
                "first; at request time the tenant identity is resolved and the query runs "
                "within those server-side boundaries."
            ),
            "rationales": {
                "a": (True, "Scoped IAM policies are defined before requests arrive."),
                "b": (
                    True,
                    "Lake Formation row-level permissions complete the enforced isolation.",
                ),
                "c": (True, "Identity resolution happens at request time, after controls exist."),
                "d": (True, "The query runs last under the enforced tenant scope."),
            },
        },
        {
            "question_id": "d3o-prompt-injection-defense",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A RAG assistant ingests untrusted web content and must resist prompt "
                "injection hidden in that content. Place the steps in the correct order."
            ),
            "scenario_constraint": "Untrusted input must be screened before it reaches the model.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Sanitize retrieved passages to strip embedded instructions."),
                ("b", "Classify the combined prompt for injection and jailbreak patterns."),
                ("c", "Invoke the model with the retrieved context under a strict system policy."),
                ("d", "Validate the model output against the expected JSON Schema."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Sanitization removes injected instructions, classification catches residual "
                "attacks, the model is invoked under enforced constraints, and output "
                "validation confirms the response is well-formed."
            ),
            "rationales": {
                "a": (True, "Sanitizing the untrusted passages comes first."),
                "b": (
                    True,
                    "Injection classification runs on the assembled prompt before generation.",
                ),
                "c": (True, "Generation happens after input defenses."),
                "d": (True, "Schema validation of output is the last gate."),
            },
        },
        {
            "question_id": "d3o-encryption-at-rest-setup",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "You must encrypt a knowledge base's source bucket with a customer-managed "
                "key and control who can decrypt. Place the steps in the correct order."
            ),
            "scenario_constraint": "The key and its policy must exist before data is protected.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Create a customer-managed key in AWS KMS."),
                ("b", "Attach a key policy granting decrypt only to the retrieval role."),
                ("c", "Enable default encryption on the Amazon S3 bucket with that key."),
                ("d", "Confirm new objects are encrypted with the managed key."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The KMS key is created, its policy restricts decrypt, the bucket is "
                "configured to use the key, and encryption of new objects is verified."
            ),
            "rationales": {
                "a": (True, "The key must exist before any policy or bucket references it."),
                "b": (True, "The key policy is set before the bucket relies on it."),
                "c": (True, "Bucket default encryption follows key setup."),
                "d": (True, "Verification confirms the control is active."),
            },
        },
        {
            "question_id": "d3o-guardrail-denied-topics",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A regulated assistant must refuse specified off-limits subjects. Place the "
                "steps to configure and verify this with Amazon Bedrock Guardrails in the "
                "correct order."
            ),
            "scenario_constraint": "Policy must be defined and attached before it can be tested.",
            "difficulty": "easy",
            "question_format": "ordering",
            "options": [
                ("a", "Define the denied topics with examples in a guardrail."),
                ("b", "Attach the guardrail to the model invocation."),
                ("c", "Send test prompts covering the denied topics."),
                ("d", "Confirm the assistant refuses and logs the blocked requests."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The denied topics are defined, the guardrail is attached to invocations, "
                "test prompts exercise it, and the refusals plus logs are confirmed."
            ),
            "rationales": {
                "a": (True, "Defining denied topics is the first configuration step."),
                "b": (True, "Attaching the guardrail activates it on invocations."),
                "c": (True, "Testing follows configuration."),
                "d": (True, "Confirming refusals and logging closes the task."),
            },
        },
        {
            "question_id": "d3o-model-card-governance",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Before releasing a customized model, your governance process must produce "
                "an approved model card. Place the steps in the correct order."
            ),
            "scenario_constraint": "Documentation and review precede release.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                (
                    "a",
                    "Record intended use and evaluation results in an Amazon SageMaker model card.",
                ),
                ("b", "Attach fairness metrics from Amazon SageMaker Clarify to the card."),
                ("c", "Submit the model card for governance review and approval."),
                ("d", "Release the model with the approved card linked in the registry."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The card captures intended use and results, fairness metrics are attached, "
                "the card is reviewed and approved, and release references the approved card."
            ),
            "rationales": {
                "a": (True, "Authoring the card content comes first."),
                "b": (True, "Fairness metrics enrich the card before review."),
                "c": (True, "Review and approval precede release."),
                "d": (True, "Release is gated on the approved card."),
            },
        },
        {
            "question_id": "d3o-responsible-ai-attribution",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "An assistant must show users which sources support an answer and how "
                "confident it is. Place the steps in the correct order."
            ),
            "scenario_constraint": "Sources and confidence are derived before they can be shown.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Retrieve supporting passages from the knowledge base."),
                ("b", "Generate the answer grounded in the retrieved passages."),
                ("c", "Emit a confidence signal to CloudWatch for the response."),
                ("d", "Display the answer with source attribution and the confidence indicator."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Passages are retrieved, the grounded answer is generated, a confidence "
                "signal is recorded, and the UI shows the answer with attribution and "
                "confidence."
            ),
            "rationales": {
                "a": (True, "Retrieval provides the sources to attribute."),
                "b": (True, "Generation is grounded in the retrieved passages."),
                "c": (True, "Confidence is emitted before presentation."),
                "d": (True, "The attributed, confidence-labeled answer is shown last."),
            },
        },
        {
            "question_id": "d3o-text-to-sql-guardrails",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A text-to-SQL feature must prevent destructive or out-of-scope queries. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "Validation must occur before any query executes.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Generate a candidate SQL statement from the natural-language request."),
                (
                    "b",
                    "Validate the statement against a read-only operation and table allowlist.",
                ),
                ("c", "Execute the validated query with a least-privilege database role."),
                ("d", "Return only the permitted result rows to the user."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The candidate SQL is generated, validated against a read-only allowlist, "
                "executed under least privilege, and only permitted rows are returned."
            ),
            "rationales": {
                "a": (True, "Generation produces the candidate to validate."),
                "b": (True, "Allowlist validation must precede execution."),
                "c": (True, "Execution uses an enforced least-privilege role."),
                "d": (True, "Returning permitted rows is the final step."),
            },
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3o-macie-pii-discovery",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "You must discover and remediate unprotected personal data in a training "
                "data bucket. Place the steps in the correct order."
            ),
            "scenario_constraint": "Discovery precedes classification-based remediation.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Run an Amazon Macie sensitive-data discovery job on the Amazon S3 bucket."),
                ("b", "Review the findings to locate buckets holding PII."),
                ("c", "Apply masking to the affected objects and tighten the bucket policy."),
                ("d", "Re-scan to confirm no unprotected PII remains."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Macie discovers sensitive data, findings are reviewed, remediation masks "
                "and restricts access, and a re-scan verifies the fix."
            ),
            "rationales": {
                "a": (True, "Discovery runs first to surface sensitive data."),
                "b": (True, "Findings are reviewed before acting."),
                "c": (True, "Remediation follows the review."),
                "d": (True, "A re-scan confirms remediation."),
            },
        },
        {
            "question_id": "d3o-contextual-grounding-check",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "To reduce hallucinations, an assistant must verify answers are grounded in "
                "retrieved context before replying. Place the steps in the correct order."
            ),
            "scenario_constraint": "Grounding is checked before the answer is released.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Assemble retrieved context and the user question."),
                ("b", "Generate a grounded answer with the foundation model."),
                (
                    "c",
                    "Run the Amazon Bedrock Guardrails contextual grounding check on the answer.",
                ),
                ("d", "Suppress or flag the answer if the grounding score is below threshold."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Context is assembled, the answer is generated, the grounding check scores "
                "it, and low-grounding answers are suppressed or flagged."
            ),
            "rationales": {
                "a": (True, "Context assembly precedes generation."),
                "b": (True, "Generation produces the answer to check."),
                "c": (True, "The grounding check evaluates the generated answer."),
                "d": (True, "Enforcement on the score is the final gate."),
            },
        },
        {
            "question_id": "d3o-drift-monitoring-loop",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "You must continuously monitor a deployed model for behavioral drift and act "
                "on it. Place the steps in the correct order."
            ),
            "scenario_constraint": "A baseline must exist before drift can be measured.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Establish a quality and behavior baseline for the model."),
                (
                    "b",
                    "Configure Amazon SageMaker Model Monitor to compare traffic to the baseline.",
                ),
                ("c", "Raise a CloudWatch alarm when drift crosses the threshold."),
                ("d", "Trigger review and retraining in response to the alarm."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "A baseline is established, Model Monitor compares live traffic to it, a "
                "CloudWatch alarm fires on drift, and review or retraining responds."
            ),
            "rationales": {
                "a": (True, "Drift is measured relative to a baseline."),
                "b": (True, "Monitoring compares production to the baseline."),
                "c": (True, "Alarming follows detected drift."),
                "d": (True, "Remediation responds to the alarm."),
            },
        },
        {
            "question_id": "d3o-llm-judge-safety-eval",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "You need an automated safety evaluation of candidate responses using a "
                "judge model. Place the steps in the correct order."
            ),
            "scenario_constraint": "Candidates must be produced before they are judged.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Generate candidate responses to a safety test set."),
                ("b", "Score each response with an Amazon Bedrock LLM-as-a-judge prompt."),
                ("c", "Aggregate the judge scores into a safety metric."),
                ("d", "Gate the release on the aggregated safety metric."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Candidates are generated, the judge scores them, scores are aggregated into "
                "a metric, and release is gated on that metric."
            ),
            "rationales": {
                "a": (True, "Responses must exist before judging."),
                "b": (True, "The judge scores the generated responses."),
                "c": (True, "Aggregation turns scores into a metric."),
                "d": (True, "The gate uses the aggregated metric."),
            },
        },
        {
            "question_id": "d3o-vpc-private-bedrock",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "An application must call Amazon Bedrock without traversing the public "
                "internet. Place the steps in the correct order."
            ),
            "scenario_constraint": "The private path must exist before traffic can use it.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Create an interface VPC endpoint for Amazon Bedrock."),
                (
                    "b",
                    "Restrict the endpoint policy and security group to the application subnets.",
                ),
                ("c", "Route the application's Bedrock calls through the VPC endpoint."),
                ("d", "Verify traffic stays private using VPC flow logs."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The endpoint is created, its policy and security group are scoped, the app "
                "routes calls through it, and flow logs confirm private traffic."
            ),
            "rationales": {
                "a": (True, "The endpoint must exist first."),
                "b": (True, "Scoping the endpoint precedes routing traffic."),
                "c": (True, "The app routes through the scoped endpoint."),
                "d": (True, "Verification confirms the private path."),
            },
        },
        {
            "question_id": "d3o-data-lineage-catalog",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "An auditor needs to trace where a training dataset originated. Place the "
                "steps to establish lineage in the correct order."
            ),
            "scenario_constraint": "Sources must be cataloged before lineage can be traced.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Crawl the source datasets and register them in the AWS Glue Data Catalog."),
                ("b", "Capture transformation lineage as AWS Glue jobs process the data."),
                ("c", "Tag the resulting dataset with its lineage metadata."),
                ("d", "Produce a lineage report answering the auditor's query."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Sources are cataloged, transformation lineage is captured, the output is "
                "tagged with lineage metadata, and a report answers the audit question."
            ),
            "rationales": {
                "a": (True, "Cataloging sources is the foundation of lineage."),
                "b": (True, "Transformation lineage builds on cataloged sources."),
                "c": (True, "Tagging records the lineage on the output."),
                "d": (True, "The report is produced from the captured lineage."),
            },
        },
        {
            "question_id": "d3o-retention-lifecycle",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Conversation transcripts must be deleted after a fixed retention period. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "A retention policy must be defined before automated deletion.",
            "difficulty": "easy",
            "question_format": "ordering",
            "options": [
                ("a", "Define the required retention period from the compliance policy."),
                ("b", "Store transcripts in a dedicated Amazon S3 prefix."),
                (
                    "c",
                    "Configure an S3 Lifecycle rule to expire objects after the retention period.",
                ),
                ("d", "Confirm aged objects are deleted on schedule."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The retention period is defined, transcripts are stored in a dedicated "
                "prefix, a lifecycle rule expires them, and deletion is confirmed."
            ),
            "rationales": {
                "a": (True, "The policy defines the retention period first."),
                "b": (True, "A dedicated prefix is the lifecycle rule's target."),
                "c": (True, "The lifecycle rule enforces expiration."),
                "d": (True, "Confirming deletion verifies the control."),
            },
        },
        {
            "question_id": "d3o-defense-in-depth-moderation",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A content pipeline layers multiple moderation stages around the model. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "Pre-model checks run before post-model checks.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Pre-screen the user input with Amazon Comprehend for toxicity."),
                ("b", "Apply the Amazon Bedrock model with its built-in guardrail."),
                ("c", "Post-validate the generation with a Lambda moderation function."),
                ("d", "Filter the final response at API Gateway before it leaves."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Comprehend pre-screens input, the guarded model generates, a Lambda "
                "function post-validates, and API Gateway applies the final filter at the "
                "edge."
            ),
            "rationales": {
                "a": (True, "Input pre-screening is the first layer."),
                "b": (True, "The guarded model runs after input screening."),
                "c": (True, "Post-validation inspects the generation."),
                "d": (True, "Edge filtering is the last layer before delivery."),
            },
        },
        {
            "question_id": "d3o-agent-trace-review",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "To audit an agent's decision, a reviewer must reconstruct its reasoning and "
                "tool calls. Place the steps in the correct order."
            ),
            "scenario_constraint": "Tracing must be enabled before a trace can be reviewed.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Enable Amazon Bedrock agent tracing for the agent."),
                ("b", "Run the agent on the scenario under review."),
                ("c", "Collect the reasoning and tool-call trace."),
                ("d", "Review the trace to confirm the decision was justified."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Tracing is enabled, the agent runs, the trace is collected, and the reviewer "
                "evaluates the captured reasoning and tool calls."
            ),
            "rationales": {
                "a": (True, "Tracing must be on before a run produces a trace."),
                "b": (True, "The agent run generates the trace data."),
                "c": (True, "The trace is collected after the run."),
                "d": (True, "Review of the trace is the final step."),
            },
        },
        {
            "question_id": "d3o-secrets-rotation-flow",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "A model gateway must use a rotating API credential without hardcoding it. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "The secret must be stored before the app retrieves it.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Store the credential in AWS Secrets Manager."),
                ("b", "Grant the gateway's IAM role read access to that secret."),
                ("c", "Retrieve the secret at runtime instead of reading a hardcoded value."),
                ("d", "Enable automatic rotation on the secret."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The secret is stored, the role is granted read access, the app retrieves it "
                "at runtime, and rotation is enabled for ongoing hygiene."
            ),
            "rationales": {
                "a": (True, "The secret must exist before it can be referenced."),
                "b": (True, "Access is granted before retrieval can succeed."),
                "c": (True, "Runtime retrieval replaces hardcoded values."),
                "d": (True, "Rotation is enabled once retrieval works."),
            },
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3o-adversarial-testing",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Before launch, a team must adversarially test an assistant's safety "
                "controls. Place the steps in the correct order."
            ),
            "scenario_constraint": "Attacks are designed before they are executed and fixed.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Compile an adversarial prompt set covering jailbreaks and injection."),
                ("b", "Run the prompts against the guarded assistant."),
                ("c", "Measure how many attacks bypassed the guardrails."),
                ("d", "Strengthen the guardrail policy for the bypasses and re-test."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The attack set is compiled, run against the assistant, bypass rate is "
                "measured, and the policy is strengthened and re-tested."
            ),
            "rationales": {
                "a": (True, "Designing the attack set comes first."),
                "b": (True, "Execution follows design."),
                "c": (True, "Measurement follows execution."),
                "d": (True, "Hardening and re-testing close the loop."),
            },
        },
        {
            "question_id": "d3o-output-schema-enforcement",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A downstream system requires strictly structured model output. Place the "
                "steps in the correct order."
            ),
            "scenario_constraint": "A schema must be defined before output can be validated.",
            "difficulty": "easy",
            "question_format": "ordering",
            "options": [
                ("a", "Define the required JSON Schema for the response."),
                ("b", "Instruct the model to produce output matching the schema."),
                ("c", "Validate the generated output against the schema."),
                ("d", "Reject or repair output that fails validation."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The schema is defined, the model is prompted to match it, output is "
                "validated, and failing output is rejected or repaired."
            ),
            "rationales": {
                "a": (True, "The schema must exist before validation."),
                "b": (True, "The model is prompted against the defined schema."),
                "c": (True, "Validation checks output against the schema."),
                "d": (True, "Enforcement handles validation failures."),
            },
        },
        {
            "question_id": "d3o-fairness-assessment",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "You must assess a model for bias across demographic groups before release. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "Groups must be defined before fairness metrics are computed.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Define the sensitive attributes and comparison groups."),
                ("b", "Compute fairness metrics across the groups with Amazon SageMaker Clarify."),
                ("c", "Compare the metrics against the acceptable fairness thresholds."),
                ("d", "Document the results in the model card and decide on release."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Groups are defined, Clarify computes metrics, the metrics are compared to "
                "thresholds, and the results drive the documented release decision."
            ),
            "rationales": {
                "a": (True, "Defining groups precedes metric computation."),
                "b": (True, "Clarify computes the fairness metrics."),
                "c": (True, "Comparison against thresholds follows computation."),
                "d": (True, "Documentation and the decision come last."),
            },
        },
        {
            "question_id": "d3o-token-redaction-logging",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Governance requires logging model interactions without storing sensitive "
                "content. Place the steps in the correct order."
            ),
            "scenario_constraint": "Sensitive tokens must be redacted before logs persist.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Capture the request and response in the application layer."),
                ("b", "Redact sensitive tokens and PII from the captured text."),
                ("c", "Write the redacted record to CloudWatch Logs."),
                ("d", "Retain the governance log under the defined retention policy."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The interaction is captured, sensitive tokens are redacted, the redacted "
                "record is logged, and it is retained per policy."
            ),
            "rationales": {
                "a": (True, "Capture happens before redaction."),
                "b": (True, "Redaction must precede persistence."),
                "c": (True, "Only redacted records are written to logs."),
                "d": (True, "Retention governs the stored log."),
            },
        },
        {
            "question_id": "d3o-human-review-escalation",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Low-confidence or sensitive responses must be escalated to a human before "
                "release. Place the steps in the correct order."
            ),
            "scenario_constraint": "The confidence signal must be evaluated before routing.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Generate a response and its confidence estimate."),
                ("b", "Evaluate the confidence and sensitivity against the escalation policy."),
                ("c", "Route flagged responses to an Amazon Augmented AI (A2I) human review."),
                ("d", "Release only responses that pass review or clear the threshold."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "A response and confidence are produced, the policy evaluates them, flagged "
                "items go to A2I human review, and only passing items are released."
            ),
            "rationales": {
                "a": (True, "Generation produces the signal to evaluate."),
                "b": (True, "Policy evaluation precedes routing."),
                "c": (True, "Flagged items are routed to human review."),
                "d": (True, "Release is gated on review or threshold."),
            },
        },
        {
            "question_id": "d3o-least-privilege-fm-access",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "A service account should invoke only one approved foundation model. Place "
                "the steps in the correct order."
            ),
            "scenario_constraint": "The scoped policy must exist before it can be enforced.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Write an IAM policy allowing invocation of only the approved model."),
                ("b", "Attach the policy to the service role."),
                ("c", "Attempt to invoke a non-approved model and confirm it is denied."),
                ("d", "Review IAM Access Analyzer findings to confirm no broader access remains."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The scoped policy is written and attached, a denial test confirms "
                "enforcement, and Access Analyzer confirms no unintended broad access."
            ),
            "rationales": {
                "a": (True, "The scoped policy is authored first."),
                "b": (True, "Attaching the policy activates enforcement."),
                "c": (True, "A denial test validates the restriction."),
                "d": (True, "Access Analyzer confirms least privilege holds."),
            },
        },
        {
            "question_id": "d3o-misuse-monitoring",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "You must continuously detect and respond to misuse of a public assistant. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "Signals must be defined before they can be alarmed on.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Define misuse signals such as repeated blocked requests per user."),
                ("b", "Emit those signals as CloudWatch metrics from the application."),
                ("c", "Configure CloudWatch alarms and anomaly detection on the signals."),
                ("d", "Throttle or suspend offending identities when an alarm fires."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Misuse signals are defined, emitted as metrics, alarmed on with anomaly "
                "detection, and enforced against when alarms fire."
            ),
            "rationales": {
                "a": (True, "Signal definition comes first."),
                "b": (True, "Emitting metrics follows definition."),
                "c": (True, "Alarms are configured on the emitted metrics."),
                "d": (True, "Enforcement responds to alarms."),
            },
        },
        {
            "question_id": "d3o-compliance-check-gate",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "Each agent action must pass a compliance check before it executes. Place "
                "the steps in the correct order."
            ),
            "scenario_constraint": "The check runs before the side-effecting action.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "The agent proposes a concrete action to take."),
                ("b", "A Lambda compliance check validates the action against policy."),
                ("c", "Execute the action only if the check passes."),
                ("d", "Record the decision and outcome for the audit trail."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The agent proposes an action, the Lambda check validates it, execution "
                "proceeds only on success, and the decision is recorded for audit."
            ),
            "rationales": {
                "a": (True, "A proposed action is the input to the check."),
                "b": (True, "The compliance check runs before execution."),
                "c": (True, "Execution is gated on the check passing."),
                "d": (True, "Recording the outcome supports audit."),
            },
        },
        {
            "question_id": "d3o-anonymization-analytics",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Conversation data must be anonymized before analysts query it. Place the "
                "steps in the correct order."
            ),
            "scenario_constraint": "Identifiers are removed before analytics access is granted.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Identify direct and quasi-identifiers in the dataset."),
                ("b", "Apply masking and anonymization to those fields."),
                ("c", "Store the anonymized dataset in a separate analytics location."),
                ("d", "Grant analysts access only to the anonymized dataset."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Identifiers are found, masked and anonymized, the clean dataset is stored "
                "separately, and analyst access is limited to that dataset."
            ),
            "rationales": {
                "a": (True, "Identifier discovery precedes anonymization."),
                "b": (True, "Masking removes the identifiers."),
                "c": (True, "The anonymized data is isolated for analytics."),
                "d": (True, "Access is granted only to the anonymized copy."),
            },
        },
        {
            "question_id": "d3o-uncertainty-surfacing",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "A clinical-support assistant must flag uncertain answers for clinician "
                "attention. Place the steps in the correct order."
            ),
            "scenario_constraint": "Uncertainty is measured before it is displayed.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Generate the answer and an uncertainty estimate."),
                ("b", "Emit the uncertainty value to CloudWatch for monitoring."),
                ("c", "Compare the uncertainty to the clinical threshold."),
                ("d", "Display a caution banner on answers above the threshold."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The answer and uncertainty are produced, the value is monitored, compared "
                "to the threshold, and a caution banner is shown when warranted."
            ),
            "rationales": {
                "a": (True, "Generation yields the uncertainty estimate."),
                "b": (True, "Emitting the metric supports monitoring."),
                "c": (True, "The comparison determines the display decision."),
                "d": (True, "The banner is the user-facing final step."),
            },
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3o-guardrail-pii-masking",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "An assistant must block personal data from appearing in its responses. "
                "Place the steps to configure this with Amazon Bedrock Guardrails in the "
                "correct order."
            ),
            "scenario_constraint": "The PII policy is set before output is filtered.",
            "difficulty": "easy",
            "question_format": "ordering",
            "options": [
                ("a", "Select the PII entity types to block or mask in a guardrail."),
                ("b", "Attach the guardrail to the assistant's model invocation."),
                ("c", "Generate a response that would otherwise include PII."),
                ("d", "Confirm the response has the PII masked or blocked."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "PII entity types are selected, the guardrail is attached, a response is "
                "generated, and masking or blocking is confirmed."
            ),
            "rationales": {
                "a": (True, "Choosing PII types is the first config step."),
                "b": (True, "Attaching the guardrail enforces the policy."),
                "c": (True, "A test generation exercises the policy."),
                "d": (True, "Confirming the mask validates the control."),
            },
        },
        {
            "question_id": "d3o-grounding-confidence-verify",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A knowledge assistant must only answer when it can cite grounded, "
                "high-confidence sources. Place the steps in the correct order."
            ),
            "scenario_constraint": "Grounding and confidence are established before answering.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Retrieve candidate passages for the query."),
                ("b", "Score semantic relevance and confidence of the passages."),
                ("c", "Generate an answer only from passages above the confidence threshold."),
                ("d", "Return a safe fallback when no passage clears the threshold."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Passages are retrieved and scored, an answer is generated only from "
                "confident sources, and a safe fallback covers the low-confidence case."
            ),
            "rationales": {
                "a": (True, "Retrieval provides candidate passages."),
                "b": (True, "Scoring determines which passages qualify."),
                "c": (True, "Generation uses only confident passages."),
                "d": (True, "The fallback handles the no-confident-source case."),
            },
        },
        {
            "question_id": "d3o-dsar-deletion",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "A user exercises their right to erasure and all their stored data must be "
                "removed. Place the steps in the correct order."
            ),
            "scenario_constraint": "Records are located before deletion and verification.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Locate all stored records tied to the user's identifier."),
                ("b", "Delete the records across the data stores in one controlled operation."),
                ("c", "Verify the deletion across every affected store."),
                ("d", "Record a tamper-evident deletion confirmation in the audit log."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Records are located, deleted, verified as gone across stores, and the "
                "confirmed deletion is logged for audit."
            ),
            "rationales": {
                "a": (True, "Locating records precedes deletion."),
                "b": (True, "Deletion follows discovery."),
                "c": (True, "Verification confirms records are gone."),
                "d": (True, "The audit confirmation records completion."),
            },
        },
        {
            "question_id": "d3o-bias-monitoring-production",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "After launch, a lending assistant must be monitored for emerging bias. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "A baseline bias profile precedes ongoing comparison.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Capture a launch-time bias baseline with Amazon SageMaker Clarify."),
                ("b", "Feed production predictions and group labels into SageMaker Model Monitor."),
                ("c", "Emit bias drift metrics to CloudWatch."),
                ("d", "Alarm and trigger governance review when bias drift exceeds the limit."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "A baseline is captured, production data is monitored against it, drift "
                "metrics flow to CloudWatch, and alarms trigger governance review."
            ),
            "rationales": {
                "a": (True, "The baseline anchors drift measurement."),
                "b": (True, "Monitoring compares production to the baseline."),
                "c": (True, "Drift metrics are emitted for alarming."),
                "d": (True, "Alarms drive the governance response."),
            },
        },
        {
            "question_id": "d3o-encryption-sdk-fields",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Specific sensitive fields must be encrypted at the application layer with a "
                "managed key. Place the steps in the correct order."
            ),
            "scenario_constraint": "The key and data key must exist before encryption.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Provision a KMS key for field-level encryption."),
                ("b", "Use the AWS Encryption SDK to request a data key under the KMS key."),
                ("c", "Encrypt the sensitive fields with the data key."),
                ("d", "Persist the ciphertext and encrypted data key together."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The KMS key is provisioned, the Encryption SDK derives a data key, fields "
                "are encrypted, and ciphertext with the wrapped key is persisted."
            ),
            "rationales": {
                "a": (True, "The KMS key underpins the data key."),
                "b": (True, "The data key is derived before encrypting."),
                "c": (True, "Encryption uses the data key."),
                "d": (True, "Storing ciphertext with the wrapped key is last."),
            },
        },
        {
            "question_id": "d3o-jailbreak-classifier-chain",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A high-risk assistant layers a dedicated classifier ahead of the model to "
                "catch jailbreaks. Place the steps in the correct order."
            ),
            "scenario_constraint": "Classification gates the model, not the other way around.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Receive the user prompt at the application boundary."),
                ("b", "Score the prompt with the jailbreak-detection classifier."),
                ("c", "Block or sanitize prompts the classifier flags."),
                ("d", "Forward only cleared prompts to the guarded model."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The prompt is received, scored by the classifier, flagged prompts are "
                "blocked or sanitized, and only cleared prompts reach the model."
            ),
            "rationales": {
                "a": (True, "Receiving the prompt is the entry point."),
                "b": (True, "Classification runs before the model."),
                "c": (True, "Enforcement handles flagged prompts."),
                "d": (True, "Only cleared prompts proceed."),
            },
        },
        {
            "question_id": "d3o-governance-framework-rollout",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "An organization is standardizing GenAI governance across teams. Place the "
                "rollout steps in the correct order."
            ),
            "scenario_constraint": "Standards are defined before they can be enforced and audited.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Define the governance policy and required model-card fields."),
                ("b", "Publish reusable guardrail and tagging standards via Service Catalog."),
                ("c", "Require teams to adopt the standards for new deployments."),
                ("d", "Audit adoption using CloudTrail and the Glue Data Catalog."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Policy and card fields are defined, reusable standards are published, teams "
                "adopt them, and adoption is audited."
            ),
            "rationales": {
                "a": (True, "Policy definition is the foundation."),
                "b": (True, "Reusable standards operationalize the policy."),
                "c": (True, "Adoption follows publication."),
                "d": (True, "Auditing verifies adoption."),
            },
        },
        {
            "question_id": "d3o-reasoning-display-flow",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "A regulated assistant must show its reasoning and supporting evidence to "
                "users. Place the steps in the correct order."
            ),
            "scenario_constraint": "Reasoning is captured before it can be displayed safely.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Capture the model's reasoning trace during generation."),
                ("b", "Redact any sensitive content from the reasoning trace."),
                ("c", "Attach the cited sources to the final answer."),
                ("d", "Display the answer with the sanitized reasoning and sources."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Reasoning is captured, sensitive content is redacted, sources are attached, "
                "and the sanitized reasoning with sources is shown."
            ),
            "rationales": {
                "a": (True, "Capturing reasoning is the first step."),
                "b": (True, "Redaction precedes any display."),
                "c": (True, "Sources are attached before presentation."),
                "d": (True, "The sanitized display is final."),
            },
        },
        {
            "question_id": "d3o-lake-formation-grant",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "A data team must grant a GenAI pipeline fine-grained read access to curated "
                "tables. Place the steps in the correct order."
            ),
            "scenario_constraint": "Data must be registered before permissions can be granted.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Register the data location with AWS Lake Formation."),
                ("b", "Define the tables and columns in the Glue Data Catalog."),
                ("c", "Grant the pipeline role column-level read permissions."),
                ("d", "Validate that the role reads only the permitted columns."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The location is registered, tables and columns are cataloged, the role is "
                "granted column-level reads, and access is validated."
            ),
            "rationales": {
                "a": (True, "Registration precedes cataloging and grants."),
                "b": (True, "Catalog definitions back the grants."),
                "c": (True, "Grants follow cataloging."),
                "d": (True, "Validation confirms fine-grained access."),
            },
        },
        {
            "question_id": "d3o-canary-safety-rollout",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "A new guardrail policy must be rolled out safely to production traffic. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "A limited canary precedes full rollout.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Deploy the new guardrail policy to a small canary slice of traffic."),
                ("b", "Monitor safety and quality metrics for the canary in CloudWatch."),
                ("c", "Compare the canary metrics against the current policy."),
                ("d", "Promote the policy to all traffic once metrics hold."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The policy is deployed to a canary, metrics are monitored and compared, and "
                "the policy is promoted only after the canary holds."
            ),
            "rationales": {
                "a": (True, "A canary limits blast radius first."),
                "b": (True, "Monitoring the canary follows deployment."),
                "c": (True, "Comparison informs the promotion decision."),
                "d": (True, "Full promotion is last."),
            },
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3o-enforced-over-prompt",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "A team wants to stop an assistant from revealing an internal pricing tool, "
                "and must choose the most reliable enforcement path. Place the steps in the "
                "correct order."
            ),
            "scenario_constraint": "Enforced controls are preferred over prompt instructions.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Remove the pricing tool from the agent's allowed tool set via IAM."),
                ("b", "Add a denied-topic rule for pricing in an Amazon Bedrock guardrail."),
                ("c", "Add a system-prompt note asking the model not to discuss pricing."),
                (
                    "d",
                    "Test that pricing requests are refused even when the prompt is adversarial.",
                ),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "Enforced controls come first: the IAM tool restriction and the guardrail "
                "denied topic do the real work, the system-prompt note is a weak supplement, "
                "and adversarial testing confirms the enforced controls hold."
            ),
            "rationales": {
                "a": (True, "Server-side IAM removal of the tool is the strongest control."),
                "b": (True, "The guardrail denied topic is the next enforced layer."),
                "c": (True, "The system-prompt note is a weak, last supplement."),
                "d": (True, "Adversarial testing validates the enforced controls."),
            },
        },
        {
            "question_id": "d3o-cross-region-residency",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Regulated data must stay within an approved Region when calling a model. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "Region constraints are enforced before invocation.",
            "difficulty": "hard",
            "question_format": "ordering",
            "options": [
                ("a", "Confirm the approved Region from the data-residency policy."),
                ("b", "Restrict model invocation to that Region with an IAM condition."),
                ("c", "Route requests to the in-Region Amazon Bedrock endpoint."),
                ("d", "Audit CloudTrail to confirm no out-of-Region invocations occurred."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The approved Region is confirmed, an IAM condition enforces it, requests "
                "route in-Region, and CloudTrail confirms compliance."
            ),
            "rationales": {
                "a": (True, "Policy defines the approved Region first."),
                "b": (True, "The IAM condition enforces the Region."),
                "c": (True, "Routing follows the enforced constraint."),
                "d": (True, "Auditing verifies residency held."),
            },
        },
        {
            "question_id": "d3o-waf-abuse-protection",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "A public GenAI endpoint must be protected from automated abuse at the edge. "
                "Place the steps in the correct order."
            ),
            "scenario_constraint": "Rules are defined before enforcement and tuning.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Define rate-based and bot-control rules in AWS WAF."),
                ("b", "Associate the WAF web ACL with the API Gateway endpoint."),
                ("c", "Monitor blocked-request metrics in CloudWatch."),
                ("d", "Tune the rules to reduce false positives."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "WAF rules are defined, associated with the endpoint, monitored, and tuned "
                "to balance protection and false positives."
            ),
            "rationales": {
                "a": (True, "Rules are authored first."),
                "b": (True, "Association activates enforcement."),
                "c": (True, "Monitoring follows enforcement."),
                "d": (True, "Tuning refines the active rules."),
            },
        },
        {
            "question_id": "d3o-output-filter-lambda-apigw",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Final responses must be scrubbed of disallowed content before leaving the "
                "service. Place the steps in the correct order."
            ),
            "scenario_constraint": "Model output is filtered before it reaches the client.",
            "difficulty": "easy",
            "question_format": "ordering",
            "options": [
                ("a", "Receive the model's generated response in the service."),
                ("b", "Run a Lambda post-processor to redact disallowed content."),
                ("c", "Apply an API Gateway response filter as a final check."),
                ("d", "Deliver the scrubbed response to the client."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The response is received, a Lambda post-processor redacts it, API Gateway "
                "applies a final filter, and the scrubbed response is delivered."
            ),
            "rationales": {
                "a": (True, "Receiving the response is the entry point."),
                "b": (True, "Lambda post-processing runs before the edge filter."),
                "c": (True, "The API Gateway filter is the final check."),
                "d": (True, "Delivery is last."),
            },
        },
        {
            "question_id": "d3o-golden-dataset-hallucination",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "A team monitors hallucination rate against a trusted reference set. Place "
                "the steps in the correct order."
            ),
            "scenario_constraint": "The golden dataset exists before responses are compared.",
            "difficulty": "medium",
            "question_format": "ordering",
            "options": [
                ("a", "Curate a golden dataset of questions with verified answers."),
                ("b", "Run the assistant over the golden dataset."),
                ("c", "Diff the assistant's answers against the verified answers."),
                ("d", "Publish the hallucination rate to a CloudWatch dashboard."),
            ],
            "correct_sequence": ["a", "b", "c", "d"],
            "correct_option_ids": [],
            "explanation": (
                "The golden dataset is curated, the assistant is run over it, answers are "
                "diffed against the verified answers, and the hallucination rate is "
                "published."
            ),
            "rationales": {
                "a": (True, "The golden dataset must exist first."),
                "b": (True, "Running the assistant produces answers to compare."),
                "c": (True, "Diffing yields the hallucination signal."),
                "d": (True, "Publishing the metric is the final step."),
            },
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3m-control-to-threat",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each safety control to the threat it primarily mitigates. Each "
                "threat is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map safety controls to the threat they address.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Amazon Bedrock Guardrails contextual grounding check"),
                ("p2", "Prompt-injection classifier on retrieved content"),
                ("p3", "Guardrails PII filter on output"),
                ("p4", "JSON Schema validation of output"),
            ],
            "match_responses": [
                ("r1", "Hallucinated, ungrounded answers"),
                ("r2", "Hidden instructions in untrusted context"),
                ("r3", "Leakage of personal data in responses"),
                ("r4", "Malformed output breaking a downstream system"),
                ("r5", "Model latency spikes"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Grounding checks counter hallucination, injection classifiers counter "
                "hidden instructions, PII filters prevent data leakage, and schema "
                "validation prevents malformed output; latency is a performance concern, "
                "not a safety control target here."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-service-to-governance",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each AWS service to the governance capability it provides. Each "
                "capability is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map services to governance capabilities.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Amazon SageMaker model cards"),
                ("p2", "AWS CloudTrail"),
                ("p3", "AWS Glue Data Catalog"),
                ("p4", "Amazon SageMaker Model Monitor"),
            ],
            "match_responses": [
                ("r1", "Documenting intended use and limitations"),
                ("r2", "Immutable audit log of API activity"),
                ("r3", "Centralized metadata and data lineage"),
                ("r4", "Continuous drift detection in production"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Model cards document use and limits, CloudTrail provides the audit log, the "
                "Glue Data Catalog centralizes metadata and lineage, and Model Monitor "
                "detects drift."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-responsible-ai-artifact",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "Match each responsible-AI practice to the artifact or service that supports "
                "it. Each option is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map responsible-AI practices to supporting artifacts.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Fairness assessment across groups"),
                ("p2", "Automated quality scoring of responses"),
                ("p3", "Transparency about intended use and limits"),
                ("p4", "Auditable record of agent decisions"),
            ],
            "match_responses": [
                ("r1", "Amazon SageMaker Clarify"),
                ("r2", "Amazon Bedrock LLM-as-a-judge"),
                ("r3", "Model card"),
                ("r4", "Amazon Bedrock agent tracing"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Clarify assesses fairness, an LLM-as-a-judge scores quality, the model card "
                "conveys transparency, and agent tracing records decisions for audit."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-pii-tool-to-role",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each data-protection service to its role. Each role is used once. "
                "Match each item to the correct option."
            ),
            "scenario_constraint": "Map data-protection services to their roles.",
            "difficulty": "easy",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Amazon Macie"),
                ("p2", "Amazon Comprehend"),
                ("p3", "AWS KMS"),
                ("p4", "AWS Secrets Manager"),
            ],
            "match_responses": [
                ("r1", "Discover sensitive data in Amazon S3"),
                ("r2", "Detect PII entities in text"),
                ("r3", "Manage encryption keys"),
                ("r4", "Store and rotate credentials"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Macie discovers sensitive data in S3, Comprehend detects PII in text, KMS "
                "manages keys, and Secrets Manager stores and rotates credentials."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-guardrail-policy-type",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each Amazon Bedrock Guardrails policy to what it filters. Each option "
                "is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map guardrail policy types to their effect.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Denied topics"),
                ("p2", "Content filters"),
                ("p3", "Sensitive information filters"),
                ("p4", "Contextual grounding check"),
            ],
            "match_responses": [
                ("r1", "Block specified off-limits subjects"),
                ("r2", "Reduce hate, violence, and similar categories"),
                ("r3", "Mask or block PII in text"),
                ("r4", "Flag answers not supported by provided context"),
                ("r5", "Compress prompts to save tokens"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Denied topics block subjects, content filters reduce harmful categories, "
                "sensitive information filters handle PII, and the grounding check flags "
                "unsupported answers; token compression is unrelated."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-enforced-vs-advisory",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each mechanism to whether it is an enforced control or an advisory "
                "measure. Responses may be reused. Match each item to the correct option."
            ),
            "scenario_constraint": "Distinguish enforced controls from advisory measures.",
            "difficulty": "hard",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "IAM policy denying a tool invocation"),
                ("p2", "System-prompt note asking the model to avoid a topic"),
                ("p3", "Amazon Bedrock Guardrails denied topic"),
                ("p4", "A politeness request embedded in the user prompt"),
            ],
            "match_responses": [
                ("r1", "Enforced control"),
                ("r2", "Advisory measure"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r1", "p4": "r2"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "IAM denials and guardrail denied topics are server-side enforced controls, "
                "while prompt-level notes and embedded requests are advisory and can be "
                "overridden."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-log-source-to-use",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each logging source to its governance use. Each use is used once. "
                "Match each item to the correct option."
            ),
            "scenario_constraint": "Map log sources to their governance use.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "AWS CloudTrail"),
                ("p2", "Amazon Bedrock Model Invocation Logs"),
                ("p3", "CloudWatch Logs"),
                ("p4", "VPC flow logs"),
            ],
            "match_responses": [
                ("r1", "Who called which API and when"),
                ("r2", "Prompt and completion records for model calls"),
                ("r3", "Application-level redacted interaction logs"),
                ("r4", "Network traffic path verification"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "CloudTrail records API activity, Bedrock Model Invocation Logs capture "
                "prompts and completions, CloudWatch Logs hold application logs, and VPC "
                "flow logs verify network paths."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-defense-layer-placement",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each defense-in-depth component to where it runs in the request path. "
                "Each placement is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map moderation components to their placement.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Amazon Comprehend toxicity pre-screen"),
                ("p2", "Amazon Bedrock model with guardrail"),
                ("p3", "Lambda post-validation"),
                ("p4", "API Gateway response filter"),
            ],
            "match_responses": [
                ("r1", "On the input before the model"),
                ("r2", "At the generation step"),
                ("r3", "On the output after the model"),
                ("r4", "At the edge before delivery"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Comprehend pre-screens input, the guarded model generates, Lambda "
                "post-validates output, and API Gateway filters at the edge."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-privacy-technique-to-goal",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each privacy technique to its goal. Each goal is used once. Match "
                "each item to the correct option."
            ),
            "scenario_constraint": "Map privacy techniques to their goals.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Masking PII fields"),
                ("p2", "S3 Lifecycle expiration"),
                ("p3", "VPC endpoint for Bedrock"),
                ("p4", "KMS encryption at rest"),
            ],
            "match_responses": [
                ("r1", "Hide identifiers in stored or returned data"),
                ("r2", "Delete data after its retention period"),
                ("r3", "Keep model traffic off the public internet"),
                ("r4", "Protect stored data with managed keys"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Masking hides identifiers, lifecycle rules enforce retention deletion, VPC "
                "endpoints keep traffic private, and KMS protects data at rest."
            ),
            "rationales": {},
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3m-metric-to-dashboard",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each monitored safety signal to what it indicates. Each indication is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map safety signals to what they indicate.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Rising hallucination rate against the golden dataset"),
                ("p2", "Increasing blocked-request count per user"),
                ("p3", "Growing bias drift metric"),
                ("p4", "Falling grounding-check pass rate"),
            ],
            "match_responses": [
                ("r1", "Answer quality is degrading"),
                ("r2", "Possible abuse by specific identities"),
                ("r3", "Fairness is shifting over time"),
                ("r4", "Answers are becoming less supported by context"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Hallucination rate tracks quality, blocked-request spikes suggest abuse, "
                "bias drift tracks fairness shifts, and grounding pass rate tracks "
                "context support."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-identity-service-role",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each identity and access service to its function. Each function is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map identity services to their function.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Amazon Cognito"),
                ("p2", "AWS IAM"),
                ("p3", "IAM Identity Center"),
                ("p4", "IAM Access Analyzer"),
            ],
            "match_responses": [
                ("r1", "Authenticate application end users"),
                ("r2", "Define resource and action permissions"),
                ("r3", "Centralize workforce single sign-on"),
                ("r4", "Surface unintended access paths"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Cognito authenticates end users, IAM defines permissions, Identity Center "
                "centralizes workforce SSO, and Access Analyzer surfaces unintended access."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-attack-to-defense",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each attack type to its primary defense. Each defense is used once. "
                "Match each item to the correct option."
            ),
            "scenario_constraint": "Map attacks to their primary defense.",
            "difficulty": "hard",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Prompt injection via retrieved content"),
                ("p2", "Jailbreak attempt in the user prompt"),
                ("p3", "Attempted PII exfiltration in output"),
                ("p4", "Destructive text-to-SQL request"),
            ],
            "match_responses": [
                ("r1", "Sanitize untrusted context before use"),
                ("r2", "Jailbreak-detection classifier before the model"),
                ("r3", "Guardrails PII output filter"),
                ("r4", "Read-only allowlist validation of generated SQL"),
                ("r5", "Provisioned throughput"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Sanitization defends against injected context, a classifier catches "
                "jailbreaks, a PII output filter stops exfiltration, and SQL allowlisting "
                "blocks destructive queries; provisioned throughput is a capacity feature."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-objective-to-focus",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each Domain 3 focus area to the service most associated with it. Each "
                "service is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map Domain 3 focus areas to their service.",
            "difficulty": "easy",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Input and output safety filtering"),
                ("p2", "Sensitive-data discovery"),
                ("p3", "Model documentation and review"),
                ("p4", "Fairness and bias metrics"),
            ],
            "match_responses": [
                ("r1", "Amazon Bedrock Guardrails"),
                ("r2", "Amazon Macie"),
                ("r3", "Amazon SageMaker model cards"),
                ("r4", "Amazon SageMaker Clarify"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Guardrails handle safety filtering, Macie discovers sensitive data, model "
                "cards document models, and Clarify computes fairness metrics."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-encryption-scope",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each encryption mechanism to its scope. Each scope is used once. "
                "Match each item to the correct option."
            ),
            "scenario_constraint": "Map encryption mechanisms to their scope.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "S3 default encryption with a KMS key"),
                ("p2", "AWS Encryption SDK field encryption"),
                ("p3", "TLS to the Bedrock endpoint"),
                ("p4", "KMS key policy"),
            ],
            "match_responses": [
                ("r1", "Protect whole objects at rest"),
                ("r2", "Protect specific fields at the application layer"),
                ("r3", "Protect data in transit"),
                ("r4", "Control who may use the key"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "S3 default encryption protects objects at rest, the Encryption SDK protects "
                "fields, TLS protects data in transit, and the key policy controls key use."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-eval-target-to-metric",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "Match each responsible-AI evaluation target to its metric. Each metric is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map evaluation targets to their metrics.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Toxicity in generated text"),
                ("p2", "Disparity across demographic groups"),
                ("p3", "Answer support by sources"),
                ("p4", "Model confidence in a response"),
            ],
            "match_responses": [
                ("r1", "Toxicity score"),
                ("r2", "Fairness disparity metric"),
                ("r3", "Grounding score"),
                ("r4", "Confidence estimate"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Toxicity scores measure harmful text, fairness disparity measures group "
                "differences, grounding scores measure source support, and confidence "
                "estimates measure response certainty."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-governance-artifact-owner",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each governance artifact to the question it answers. Each question is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map governance artifacts to the question they answer.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Model card"),
                ("p2", "Glue data lineage"),
                ("p3", "CloudTrail log"),
                ("p4", "Metadata tags"),
            ],
            "match_responses": [
                ("r1", "What is this model for and where does it fall short?"),
                ("r2", "Where did this dataset come from?"),
                ("r3", "Who performed this action and when?"),
                ("r4", "How is this resource classified and owned?"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Model cards describe purpose and limits, lineage traces data origin, "
                "CloudTrail answers who-did-what-when, and tags record classification and "
                "ownership."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-pii-stage-to-tool",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each stage of PII handling to the service used. Each service is used "
                "once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map PII-handling stages to their service.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Find PII in free text"),
                ("p2", "Find sensitive objects across S3"),
                ("p3", "Encrypt the redacted records"),
                ("p4", "Record the redaction event"),
            ],
            "match_responses": [
                ("r1", "Amazon Comprehend"),
                ("r2", "Amazon Macie"),
                ("r3", "AWS KMS"),
                ("r4", "CloudWatch Logs"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Comprehend finds PII in text, Macie scans S3, KMS encrypts the records, and "
                "CloudWatch Logs records the redaction event."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-safety-term-to-definition",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each safety term to its definition. Each definition is used once. "
                "Match each item to the correct option."
            ),
            "scenario_constraint": "Map safety terms to their definitions.",
            "difficulty": "easy",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Prompt injection"),
                ("p2", "Jailbreak"),
                ("p3", "Grounding"),
                ("p4", "Defense in depth"),
            ],
            "match_responses": [
                ("r1", "Hidden instructions that hijack the model's behavior"),
                ("r2", "Coaxing the model past its safety constraints"),
                ("r3", "Tying answers to supporting source content"),
                ("r4", "Layering multiple independent controls"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Injection hijacks behavior with hidden instructions, jailbreaks bypass "
                "safety constraints, grounding ties answers to sources, and defense in depth "
                "layers controls."
            ),
            "rationales": {},
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3m-responsible-practice-service",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "Match each responsible-AI practice to the AWS capability enabling it. Each "
                "capability is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map responsible-AI practices to AWS capabilities.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Show the agent's reasoning and tool calls"),
                ("p2", "A/B test prompt variants for responsible outcomes"),
                ("p3", "Score candidate answers for quality"),
                ("p4", "Enforce a per-action compliance check"),
            ],
            "match_responses": [
                ("r1", "Amazon Bedrock agent tracing"),
                ("r2", "Amazon Bedrock Prompt Flows"),
                ("r3", "Amazon Bedrock LLM-as-a-judge"),
                ("r4", "Lambda compliance check"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Agent tracing exposes reasoning, Prompt Flows support A/B variants, an "
                "LLM-as-a-judge scores answers, and a Lambda check enforces compliance."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-network-control-purpose",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each network control to its purpose. Each purpose is used once. Match "
                "each item to the correct option."
            ),
            "scenario_constraint": "Map network controls to their purpose.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Interface VPC endpoint"),
                ("p2", "AWS PrivateLink"),
                ("p3", "Security group"),
                ("p4", "AWS WAF"),
            ],
            "match_responses": [
                ("r1", "Reach a service without the public internet"),
                ("r2", "Expose a service privately across accounts"),
                ("r3", "Restrict instance-level inbound and outbound traffic"),
                ("r4", "Filter malicious web requests at the edge"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "VPC endpoints give private service reach, PrivateLink exposes services "
                "across accounts, security groups restrict instance traffic, and WAF filters "
                "web requests."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-sql-safety-step",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each text-to-SQL safety measure to the risk it reduces. Each risk is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map text-to-SQL measures to the risk they reduce.",
            "difficulty": "hard",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Read-only operation allowlist"),
                ("p2", "Table and column allowlist"),
                ("p3", "Least-privilege database role"),
                ("p4", "Row-limit on results"),
            ],
            "match_responses": [
                ("r1", "Prevent destructive writes or deletes"),
                ("r2", "Prevent access to out-of-scope data"),
                ("r3", "Contain damage if validation is bypassed"),
                ("r4", "Prevent oversized data exfiltration"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Operation allowlists stop writes, table/column allowlists limit scope, "
                "least privilege contains bypass damage, and row limits curb exfiltration."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-monitoring-tool-signal",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each monitoring tool to the signal it is best suited to track. Each "
                "signal is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map monitoring tools to their best-fit signal.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "CloudWatch anomaly detection"),
                ("p2", "SageMaker Model Monitor"),
                ("p3", "Bedrock Model Invocation Logs"),
                ("p4", "CloudTrail"),
            ],
            "match_responses": [
                ("r1", "Unexpected spikes in a safety metric"),
                ("r2", "Statistical drift from a baseline"),
                ("r3", "Exact prompts and completions"),
                ("r4", "API caller and action history"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Anomaly detection catches metric spikes, Model Monitor catches drift, "
                "invocation logs hold prompts and completions, and CloudTrail records API "
                "history."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-pii-entity-example",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each data item to whether it is PII that should be redacted. "
                "Responses may be reused. Match each item to the correct option."
            ),
            "scenario_constraint": "Classify data items as PII or not.",
            "difficulty": "easy",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "A customer's full name and home address"),
                ("p2", "A social security number"),
                ("p3", "An aggregate count of total users"),
                ("p4", "A public product SKU"),
            ],
            "match_responses": [
                ("r1", "Redact as PII"),
                ("r2", "Not PII"),
            ],
            "match_key": {"p1": "r1", "p2": "r1", "p3": "r2", "p4": "r2"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Names with addresses and social security numbers are PII and must be "
                "redacted, while aggregate counts and public SKUs are not personal data."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-compliance-control-regime",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each compliance need to the control that satisfies it. Each control "
                "is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map compliance needs to their control.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Prove when data was deleted"),
                ("p2", "Prove who accessed the model"),
                ("p3", "Prove the training data's origin"),
                ("p4", "Prove intended use was documented"),
            ],
            "match_responses": [
                ("r1", "S3 Lifecycle plus audit log entry"),
                ("r2", "CloudTrail access records"),
                ("r3", "Glue data lineage"),
                ("r4", "Approved model card"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Lifecycle plus logs prove deletion, CloudTrail proves access, lineage "
                "proves data origin, and the model card proves documented intent."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-guardrail-vs-alternative",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each safety requirement to the most reliable approach. Each approach "
                "is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Prefer enforced controls over prompt-only approaches.",
            "difficulty": "hard",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Guarantee a banned topic is never discussed"),
                ("p2", "Guarantee a tool is never callable"),
                ("p3", "Guarantee PII never appears in output"),
                ("p4", "Encourage a friendlier tone"),
            ],
            "match_responses": [
                ("r1", "Guardrails denied topic"),
                ("r2", "IAM restriction on the tool"),
                ("r3", "Guardrails PII output filter"),
                ("r4", "System-prompt wording"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Hard guarantees need enforced controls (denied topic, IAM, PII filter); "
                "only the soft tone preference is appropriately handled by prompt wording."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-clarify-vs-monitor",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "Match each bias task to the right service and timing. Each option is used "
                "once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map bias tasks to service and timing.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Pre-release fairness assessment"),
                ("p2", "Ongoing bias drift in production"),
                ("p3", "Documenting fairness results"),
                ("p4", "Alerting on a drift threshold breach"),
            ],
            "match_responses": [
                ("r1", "Amazon SageMaker Clarify"),
                ("r2", "Amazon SageMaker Model Monitor"),
                ("r3", "Model card"),
                ("r4", "CloudWatch alarm"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Clarify assesses fairness pre-release, Model Monitor tracks drift in "
                "production, the model card documents results, and a CloudWatch alarm fires "
                "on threshold breaches."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-safety-eval-stage",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "Match each safety evaluation activity to its stage. Each stage is used "
                "once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map safety evaluation activities to their stage.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Adversarial red-teaming"),
                ("p2", "Canary deployment of a new policy"),
                ("p3", "Golden-dataset hallucination check"),
                ("p4", "Post-incident review"),
            ],
            "match_responses": [
                ("r1", "Pre-release testing"),
                ("r2", "Controlled rollout"),
                ("r3", "Continuous monitoring"),
                ("r4", "After an incident"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Red-teaming is pre-release, canaries are controlled rollout, golden-dataset "
                "checks are continuous monitoring, and reviews follow incidents."
            ),
            "rationales": {},
        },
    ]
)

QUESTIONS.extend(
    [
        {
            "question_id": "d3m-retention-action",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each retention requirement to the mechanism that satisfies it. Each "
                "mechanism is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map retention requirements to their mechanism.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Auto-delete transcripts after 90 days"),
                ("p2", "Keep an immutable record that deletion happened"),
                ("p3", "Encrypt retained data"),
                ("p4", "Restrict who can read retained data"),
            ],
            "match_responses": [
                ("r1", "S3 Lifecycle expiration rule"),
                ("r2", "CloudTrail and audit log"),
                ("r3", "KMS encryption"),
                ("r4", "IAM read policy"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Lifecycle rules auto-delete, audit logs prove deletion, KMS encrypts "
                "retained data, and IAM restricts read access."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-grounding-failure-response",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each grounding-check outcome to the appropriate response. Each "
                "response is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map grounding outcomes to responses.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "High grounding score"),
                ("p2", "Low grounding score"),
                ("p3", "No supporting passage retrieved"),
                ("p4", "Borderline score on a sensitive topic"),
            ],
            "match_responses": [
                ("r1", "Return the answer with citations"),
                ("r2", "Suppress the answer and ask to rephrase"),
                ("r3", "Return a safe fallback message"),
                ("r4", "Escalate to human review"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "High grounding returns cited answers, low grounding suppresses, no passage "
                "yields a fallback, and borderline sensitive cases escalate to a human."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-tag-to-governance-value",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each metadata tag to the governance value it supports. Each value is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map metadata tags to governance value.",
            "difficulty": "easy",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "data-classification=confidential"),
                ("p2", "owner=risk-team"),
                ("p3", "retention=90d"),
                ("p4", "environment=production"),
            ],
            "match_responses": [
                ("r1", "Drive access and handling rules"),
                ("r2", "Establish accountability"),
                ("r3", "Drive lifecycle expiration"),
                ("r4", "Scope change controls"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Classification tags drive handling, owner tags establish accountability, "
                "retention tags drive lifecycle, and environment tags scope change control."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-human-review-trigger",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each response condition to whether it should trigger human review. "
                "Responses may be reused. Match each item to the correct option."
            ),
            "scenario_constraint": "Decide which conditions warrant human review.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Low confidence on a medical question"),
                ("p2", "A guardrail flagged the response"),
                ("p3", "High confidence on a routine FAQ"),
                ("p4", "A clearly grounded factual answer"),
            ],
            "match_responses": [
                ("r1", "Route to human review"),
                ("r2", "Release automatically"),
            ],
            "match_key": {"p1": "r1", "p2": "r1", "p3": "r2", "p4": "r2"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Low-confidence sensitive answers and guardrail-flagged responses need human "
                "review, while high-confidence routine and clearly grounded answers can be "
                "released automatically."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-incident-phase-action",
            "objective_ids": ["AIP-3.3"],
            "prompt": (
                "Match each incident-response phase to its action. Each action is used once. "
                "Match each item to the correct option."
            ),
            "scenario_constraint": "Map incident-response phases to actions.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Detection"),
                ("p2", "Containment"),
                ("p3", "Investigation"),
                ("p4", "Recovery"),
            ],
            "match_responses": [
                ("r1", "CloudWatch alarm on a safety metric"),
                ("r2", "Tighten the guardrail policy"),
                ("r3", "Trace root cause via CloudTrail and invocation logs"),
                ("r4", "Deploy a validated fix and update the model card"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Detection is the alarm, containment tightens guardrails, investigation "
                "traces root cause, and recovery deploys a fix with updated documentation."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-output-control-layer",
            "objective_ids": ["AIP-3.1"],
            "prompt": (
                "Match each output-side control to what it guarantees. Each guarantee is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map output controls to their guarantee.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "JSON Schema validation"),
                ("p2", "Guardrails content filter on output"),
                ("p3", "Guardrails PII filter on output"),
                ("p4", "Lambda business-rule check"),
            ],
            "match_responses": [
                ("r1", "Output is well-formed and parseable"),
                ("r2", "Output avoids harmful categories"),
                ("r3", "Output contains no personal data"),
                ("r4", "Output respects domain-specific rules"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Schema validation guarantees well-formed output, content filters avoid "
                "harmful categories, PII filters remove personal data, and a Lambda check "
                "enforces business rules."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-access-concept-definition",
            "objective_ids": ["AIP-3.2"],
            "prompt": (
                "Match each access-control concept to its definition. Each definition is "
                "used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map access-control concepts to definitions.",
            "difficulty": "easy",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "Least privilege"),
                ("p2", "Role-based access control"),
                ("p3", "Identity federation"),
                ("p4", "Row-level security"),
            ],
            "match_responses": [
                ("r1", "Grant only the permissions needed"),
                ("r2", "Assign permissions by role"),
                ("r3", "Use an external identity provider for sign-in"),
                ("r4", "Restrict visibility to specific data rows"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "Least privilege grants only what is needed, RBAC assigns by role, "
                "federation uses an external IdP, and row-level security limits row "
                "visibility."
            ),
            "rationales": {},
        },
        {
            "question_id": "d3m-service-to-domain3-skill",
            "objective_ids": ["AIP-3.4"],
            "prompt": (
                "Match each service to the Domain 3 responsible-AI skill it supports. Each "
                "skill is used once. Match each item to the correct option."
            ),
            "scenario_constraint": "Map services to responsible-AI skills.",
            "difficulty": "medium",
            "question_format": "matching",
            "match_prompts": [
                ("p1", "CloudWatch"),
                ("p2", "Amazon SageMaker Clarify"),
                ("p3", "Amazon Bedrock Prompt Management"),
                ("p4", "Amazon Augmented AI (A2I)"),
            ],
            "match_responses": [
                ("r1", "Track confidence and uncertainty signals"),
                ("r2", "Measure fairness across groups"),
                ("r3", "Version and A/B test prompts responsibly"),
                ("r4", "Insert human review of flagged outputs"),
            ],
            "match_key": {"p1": "r1", "p2": "r2", "p3": "r3", "p4": "r4"},
            "options": [],
            "correct_option_ids": [],
            "explanation": (
                "CloudWatch tracks confidence signals, Clarify measures fairness, Prompt "
                "Management versions and tests prompts, and A2I inserts human review."
            ),
            "rationales": {},
        },
    ]
)


def question_count() -> int:
    """Return the number of authored Domain 3 ordering/matching questions."""
    return len(QUESTIONS)
