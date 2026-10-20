"""Transactional ingestion of the Phase 0 handoff and seed content into SQLite.

Ingestion validates the handoff envelope, then writes blueprint, objectives,
sources, profile, safety, baseline, questions, and the FTS index. Public
question data and private answer material are written to separate tables.
Re-ingesting an identical blueprint version is idempotent.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any

from study_core.artifacts import ArtifactEnvelope
from study_core.db import DbConnection, immediate_transaction


def ingest_handoff(
    conn: DbConnection,
    handoff: ArtifactEnvelope,
    *,
    now_iso: str,
    answer_material: Mapping[str, Mapping[str, Any]] | None = None,
    question_options: Mapping[str, Sequence[tuple[str, str]]] | None = None,
    content_units: Sequence[Mapping[str, Any]] | None = None,
    curriculum: Sequence[Mapping[str, Any]] | None = None,
    labs: Sequence[Mapping[str, Any]] | None = None,
    rich_questions: Sequence[Mapping[str, Any]] | None = None,
) -> None:
    """Ingest an accepted Phase 0 handoff into the database idempotently.

    Args:
        conn: an open connection with foreign keys enabled.
        handoff: the verified Phase0Handoff envelope.
        now_iso: UTC ISO timestamp for provenance fields.
        answer_material: optional map of question_id -> {correct_option_ids,
            rubric}. Private grading material lives only in `answer_material`.
    """
    handoff.verify()
    payload = handoff.payload
    blueprint_version = str(payload["blueprint_version"])
    manifest = payload["manifest"]
    registry = payload["source_registry"]
    profile = payload["learner_profile"]
    safety = payload["lab_safety_policy"]
    baseline = payload["baseline_summary"]
    seed = payload["seed_admission"]

    with immediate_transaction(conn):
        conn.execute(
            "INSERT OR IGNORE INTO blueprints (blueprint_version, created_at) VALUES (?, ?)",
            (blueprint_version, now_iso),
        )
        _ingest_domains(conn, manifest["domains"], blueprint_version)
        _ingest_objectives(conn, manifest["objectives"], blueprint_version)
        _ingest_sources(conn, registry["sources"], blueprint_version)
        _ingest_profile(conn, profile, now_iso)
        _ingest_safety(conn, safety, now_iso)
        _ingest_baseline(conn, baseline, now_iso)
        _ingest_questions(conn, seed, now_iso, answer_material or {}, question_options or {})
        _ingest_rich_questions(conn, rich_questions or (), now_iso)
        _ingest_content(conn, content_units or (), now_iso)
        _ingest_curriculum(conn, curriculum or ())
        _ingest_labs(conn, labs or ())


def _ingest_domains(conn: DbConnection, domains: Sequence[Mapping[str, Any]], version: str) -> None:
    for domain in domains:
        conn.execute(
            "INSERT OR IGNORE INTO domains (domain_id, blueprint_version, title, weight_percent) "
            "VALUES (?, ?, ?, ?)",
            (
                int(domain["domain_id"]),
                version,
                str(domain["title"]),
                int(domain["weight_percent"]),
            ),
        )


def _ingest_objectives(
    conn: DbConnection, objectives: Sequence[Mapping[str, Any]], version: str
) -> None:
    for objective in objectives:
        conn.execute(
            "INSERT OR IGNORE INTO objectives (objective_id, blueprint_version, domain_id, "
            "title, status) VALUES (?, ?, ?, ?, ?)",
            (
                str(objective["objective_id"]),
                version,
                int(objective["domain_id"]),
                str(objective["title"]),
                str(objective["status"]),
            ),
        )


def _ingest_sources(conn: DbConnection, sources: Sequence[Mapping[str, Any]], version: str) -> None:
    for source in sources:
        conn.execute(
            "INSERT OR IGNORE INTO sources (source_id, blueprint_version, url, title, "
            "publisher, retrieved_at, source_type, freshness) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                str(source["source_id"]),
                version,
                str(source["url"]),
                str(source["title"]),
                str(source["publisher"]),
                str(source["retrieved_at"]),
                str(source["source_type"]),
                str(source["freshness"]),
            ),
        )


def _ingest_profile(conn: DbConnection, profile: Mapping[str, Any], now_iso: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO learner_profiles (learner_id, profile_version, weekly_hours, "
        "experience, target_region, account_type, lab_budget_usd, exam_date, "
        "exam_date_undecided, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            str(profile["learner_id"]),
            str(profile["profile_version"]),
            int(profile["weekly_hours"]),
            str(profile["experience"]),
            str(profile["target_region"]),
            str(profile["account_type"]),
            float(profile["lab_budget_usd"]),
            profile.get("exam_date"),
            1 if profile["exam_date_undecided"] else 0,
            str(profile.get("updated_at", now_iso)),
        ),
    )


def _ingest_safety(conn: DbConnection, safety: Mapping[str, Any], now_iso: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO safety_policies (policy_version, payload_json, ingested_at) "
        "VALUES (?, ?, ?)",
        (str(safety["policy_version"]), json.dumps(safety, sort_keys=True), now_iso),
    )


def _ingest_baseline(conn: DbConnection, baseline: Mapping[str, Any], now_iso: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO baseline_summaries (run_id, learner_id, complete, "
        "answered_count, unanswered_count, mean_confidence, ingested_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            str(baseline["run_id"]),
            str(baseline["learner_id"]),
            1 if baseline["complete"] else 0,
            int(baseline["answered_count"]),
            int(baseline["unanswered_count"]),
            float(baseline["mean_confidence"]),
            now_iso,
        ),
    )


def _ingest_questions(
    conn: DbConnection,
    seed: Sequence[Mapping[str, Any]],
    now_iso: str,
    answer_material: Mapping[str, Mapping[str, Any]],
    question_options: Mapping[str, Sequence[tuple[str, str]]],
) -> None:
    for prompt in seed:
        question_id = str(prompt["question_id"])
        # Skip placeholder prompts whose options were suppressed (their objective
        # now has authored questions). A selectable question must have options.
        if question_id not in question_options:
            continue
        source_ids = list(prompt["source_ids"])
        conn.execute(
            "INSERT OR IGNORE INTO questions (question_id, prompt, scenario_constraint, "
            "difficulty, question_format, source_ids, review_status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                question_id,
                str(prompt["prompt"]),
                str(prompt["scenario_constraint"]),
                str(prompt["difficulty"]),
                str(prompt["question_format"]),
                json.dumps(source_ids),
                str(prompt["review_status"]),
                now_iso,
            ),
        )
        for objective_id in prompt["objective_ids"]:
            conn.execute(
                "INSERT OR IGNORE INTO question_objectives (question_id, objective_id) "
                "VALUES (?, ?)",
                (question_id, str(objective_id)),
            )
        for option_id, text in question_options.get(question_id, ()):
            conn.execute(
                "INSERT OR IGNORE INTO question_options (question_id, option_id, text) "
                "VALUES (?, ?, ?)",
                (question_id, option_id, text),
            )
        material = answer_material.get(question_id)
        if material is not None:
            conn.execute(
                "INSERT OR IGNORE INTO answer_material "
                "(question_id, correct_option_ids, rubric, explanation) "
                "VALUES (?, ?, ?, ?)",
                (
                    question_id,
                    json.dumps(list(material["correct_option_ids"])),
                    str(material["rubric"]),
                    str(material.get("explanation", "")),
                ),
            )
            for option_id, (is_correct, rationale) in material.get("rationales", {}).items():
                conn.execute(
                    "INSERT OR IGNORE INTO option_rationales "
                    "(question_id, option_id, is_correct, rationale) VALUES (?, ?, ?, ?)",
                    (question_id, str(option_id), 1 if is_correct else 0, str(rationale)),
                )


def _ingest_rich_questions(
    conn: DbConnection, questions: Sequence[Mapping[str, Any]], now_iso: str
) -> None:
    """Ingest authored questions with options, answer keys, and explanations."""
    for question in questions:
        question_id = str(question["question_id"])
        conn.execute(
            "INSERT OR IGNORE INTO questions (question_id, prompt, scenario_constraint, "
            "difficulty, question_format, source_ids, review_status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, 'reviewed', ?)",
            (
                question_id,
                str(question["prompt"]),
                str(question["scenario_constraint"]),
                str(question["difficulty"]),
                str(question.get("question_format", "multiple_choice")),
                json.dumps(list(question.get("source_ids", ["aip-c01-domain-1"]))),
                now_iso,
            ),
        )
        for objective_id in question["objective_ids"]:
            conn.execute(
                "INSERT OR IGNORE INTO question_objectives (question_id, objective_id) "
                "VALUES (?, ?)",
                (question_id, str(objective_id)),
            )
        for option_id, text in question.get("options", ()):
            conn.execute(
                "INSERT OR IGNORE INTO question_options (question_id, option_id, text) "
                "VALUES (?, ?, ?)",
                (question_id, str(option_id), str(text)),
            )
        conn.execute(
            "INSERT OR IGNORE INTO answer_material "
            "(question_id, correct_option_ids, rubric, explanation, correct_sequence) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                question_id,
                json.dumps(list(question.get("correct_option_ids", []))),
                str(question["explanation"]),
                str(question["explanation"]),
                json.dumps(list(question.get("correct_sequence", []))),
            ),
        )
        for option_id, (is_correct, rationale) in question.get("rationales", {}).items():
            conn.execute(
                "INSERT OR IGNORE INTO option_rationales "
                "(question_id, option_id, is_correct, rationale) VALUES (?, ?, ?, ?)",
                (question_id, str(option_id), 1 if is_correct else 0, str(rationale)),
            )
        # Matching questions carry prompts, responses, and a private pairing key.
        for order, (prompt_id, text) in enumerate(question.get("match_prompts", ())):
            conn.execute(
                "INSERT OR IGNORE INTO match_prompts (question_id, prompt_id, display_order, "
                "text) VALUES (?, ?, ?, ?)",
                (question_id, str(prompt_id), order, str(text)),
            )
        for order, (response_id, text) in enumerate(question.get("match_responses", ())):
            conn.execute(
                "INSERT OR IGNORE INTO match_responses (question_id, response_id, "
                "display_order, text) VALUES (?, ?, ?, ?)",
                (question_id, str(response_id), order, str(text)),
            )
        for prompt_id, response_id in question.get("match_key", {}).items():
            conn.execute(
                "INSERT OR IGNORE INTO match_answer_keys (question_id, prompt_id, response_id) "
                "VALUES (?, ?, ?)",
                (question_id, str(prompt_id), str(response_id)),
            )


def _ingest_content(
    conn: DbConnection, content_units: Sequence[Mapping[str, Any]], now_iso: str
) -> None:
    for unit in content_units:
        content_id = str(unit["content_id"])
        objective_ids = list(unit["objective_ids"])
        existing = conn.execute(
            "SELECT 1 FROM content_units WHERE content_id = ?", (content_id,)
        ).fetchone()
        if existing is not None:
            continue
        conn.execute(
            "INSERT INTO content_units (content_id, title, body, source_ids, freshness, "
            "created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                content_id,
                str(unit["title"]),
                str(unit["body"]),
                json.dumps(list(unit["source_ids"])),
                str(unit["freshness"]),
                now_iso,
            ),
        )
        for objective_id in objective_ids:
            conn.execute(
                "INSERT OR IGNORE INTO content_objectives (content_id, objective_id) "
                "VALUES (?, ?)",
                (content_id, str(objective_id)),
            )
        conn.execute(
            "INSERT INTO material_fts (content_id, title, body, objective_ids, freshness) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                content_id,
                str(unit["title"]),
                str(unit["body"]),
                json.dumps(objective_ids),
                str(unit["freshness"]),
            ),
        )


def _ingest_curriculum(conn: DbConnection, items: Sequence[Mapping[str, Any]]) -> None:
    for item in items:
        conn.execute(
            "INSERT OR IGNORE INTO curriculum_items (item_id, item_type, title, display_order, "
            "objective_ids, prerequisites, content_ref) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(item["item_id"]),
                str(item["item_type"]),
                str(item["title"]),
                int(item["display_order"]),
                json.dumps(list(item["objective_ids"])),
                json.dumps(list(item["prerequisites"])),
                item.get("content_ref"),
            ),
        )


def _ingest_labs(conn: DbConnection, labs: Sequence[Mapping[str, Any]]) -> None:
    for lab in labs:
        lab_id = str(lab["lab_id"])
        conn.execute(
            "INSERT OR IGNORE INTO lab_definitions (lab_id, title, objective_ids, cost_class, "
            "regions, architecture, cleanup, scenario, prerequisites, objectives_text, "
            "region_note, recall_prompt) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                lab_id,
                str(lab["title"]),
                json.dumps(list(lab["objective_ids"])),
                str(lab["cost_class"]),
                json.dumps(list(lab["regions"])),
                str(lab["architecture"]),
                str(lab["cleanup"]),
                str(lab.get("scenario", "")),
                str(lab.get("prerequisites", "")),
                str(lab.get("objectives_text", "")),
                str(lab.get("region_note", "")),
                str(lab.get("recall_prompt", "")),
            ),
        )
        for step in lab.get("steps", ()):
            conn.execute(
                "INSERT OR IGNORE INTO lab_steps (lab_id, step_id, display_order, instruction, "
                "prediction_prompt, mandatory, hints_json, reflection) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    lab_id,
                    str(step["step_id"]),
                    int(step["display_order"]),
                    str(step["instruction"]),
                    str(step["prediction_prompt"]),
                    1 if step["mandatory"] else 0,
                    json.dumps([str(h) for h in step.get("hints", ())]),
                    str(step.get("reflection", "")),
                ),
            )
        for checkpoint in lab.get("checkpoints", ()):
            conn.execute(
                "INSERT OR IGNORE INTO lab_checkpoints (lab_id, checkpoint_id, validator_id, "
                "is_cleanup, mandatory, label, step_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    lab_id,
                    str(checkpoint["checkpoint_id"]),
                    checkpoint.get("validator_id"),
                    1 if checkpoint["is_cleanup"] else 0,
                    1 if checkpoint["mandatory"] else 0,
                    str(checkpoint.get("label", "")),
                    str(checkpoint.get("step_id", "")),
                ),
            )
