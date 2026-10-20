"""Question-bank quality audit: length bias and distractor repetition.

The authored banks must not be gameable by surface tells. This check measures,
per domain and overall:

* **Length bias** — how often the correct option is the longest among
  single-answer questions. Random is ~25% for 4-option items; a high value means
  a test-taker can score by picking the longest answer.
* **Distractor repetition** — how often the exact same wrong-option text is
  reused across the bank, which trains the learner to dismiss a concept on sight.

Usage:
    python -m scripts.audit_questions            # report
    python -m scripts.audit_questions --check    # exit 1 if thresholds exceeded

Thresholds (``--check``): correct-is-longest share <= 40% per domain, and no
single distractor text reused more than 3 times across the whole bank. Service
NAMES legitimately recur as plausible wrong services; the repetition check
targets full option sentences, and short option texts (<= 24 chars, typically a
bare service name) are excluded from the repetition cap.
"""

from __future__ import annotations

import importlib
import sys
from collections import Counter
from typing import Any

_DOMAINS = range(1, 6)
_LONGEST_SHARE_MAX = 0.40
_DISTRACTOR_REUSE_MAX = 3
_SHORT_OPTION_CHARS = 24

# Out-of-scope AWS services per the official exam guide appendix. A keyed-correct
# answer or teaching explanation must never rely on one of these. Matched as
# word-boundary substrings against option/explanation text.
_OUT_OF_SCOPE_SERVICES: tuple[str, ...] = (
    "Amazon MQ",
    "AWS Clean Rooms",
    "AWS Data Exchange",
    "Amazon DataZone",
    "Amazon FinSpace",
    "Amazon Managed Blockchain",
    "Alexa for Business",
    "Amazon Chime",
    "AWS Wickr",
    "Amazon WorkDocs",
    "Amazon WorkMail",
    "AWS Budgets",
    "AWS Cost and Usage Report",
    "AWS Savings Plans",
    "AWS Batch",
    "Amazon EC2 Image Builder",
    "AWS Elastic Beanstalk",
    "Amazon Lightsail",
    "AWS Serverless Application Repository",
    "AWS App2Container",
    "AWS Copilot",
    "Amazon SES",
)

# Modules that hold authored multiple-choice/response questions (the ones with
# an options + correct_option_ids shape the service check can inspect).
_QUESTION_MODULES = tuple(f"content.domain{d}_questions" for d in _DOMAINS)


def _load(domain: int) -> list[dict[str, Any]]:
    module = importlib.import_module(f"content.domain{domain}_questions")
    return list(module.QUESTIONS)


def _out_of_scope_hits() -> list[tuple[str, str]]:
    """Return (question_id, service) where a correct answer/explanation uses an
    out-of-scope service. Only the keyed-correct options and the explanation are
    checked; a plausible out-of-scope *distractor* is acceptable."""
    hits: list[tuple[str, str]] = []
    for module_name in _QUESTION_MODULES:
        module = importlib.import_module(module_name)
        for q in module.QUESTIONS:
            correct = set(q.get("correct_option_ids", ()))
            texts = [t for oid, t in q.get("options", ()) if oid in correct]
            texts.append(str(q.get("explanation", "")))
            blob = " ".join(texts)
            for svc in _OUT_OF_SCOPE_SERVICES:
                if svc.lower() in blob.lower():
                    hits.append((str(q["question_id"]), svc))
    return hits


def _single_answer(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        q for q in questions if q.get("question_format", "multiple_choice") == "multiple_choice"
    ]


def _longest_share(questions: list[dict[str, Any]]) -> tuple[int, int, int, int]:
    """Return (longest_count, total, avg_correct_len, avg_wrong_len)."""
    sa = _single_answer(questions)
    longest = 0
    corr_lens: list[int] = []
    wrong_lens: list[int] = []
    for q in sa:
        lengths = {oid: len(text) for oid, text in q["options"]}
        cid = q["correct_option_ids"][0]
        corr_lens.append(lengths[cid])
        wrong_lens.extend(length for oid, length in lengths.items() if oid != cid)
        if lengths[cid] == max(lengths.values()):
            longest += 1
    avg_c = sum(corr_lens) // len(corr_lens) if corr_lens else 0
    avg_w = sum(wrong_lens) // len(wrong_lens) if wrong_lens else 0
    return longest, len(sa), avg_c, avg_w


def _distractor_counts(all_questions: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for q in all_questions:
        for oid, text in q["options"]:
            if oid in q["correct_option_ids"]:
                continue
            norm = text.strip().lower()
            if len(norm) <= _SHORT_OPTION_CHARS:
                continue  # bare service names may legitimately recur
            counts[norm] += 1
    return counts


def main(argv: list[str]) -> int:
    """Report the audit; with --check, fail on threshold violations."""
    check = "--check" in argv
    all_questions: list[dict[str, Any]] = []
    violations: list[str] = []

    print("Length bias (single-answer: how often correct is the longest option):")
    for domain in _DOMAINS:
        questions = _load(domain)
        all_questions.extend(questions)
        longest, total, avg_c, avg_w = _longest_share(questions)
        share = longest / total if total else 0.0
        flag = "  <-- OVER" if share > _LONGEST_SHARE_MAX else ""
        print(
            f"  D{domain}: {longest}/{total} longest = {share:.0%}  "
            f"(avg correct {avg_c} vs wrong {avg_w} chars){flag}"
        )
        if share > _LONGEST_SHARE_MAX:
            violations.append(
                f"D{domain} correct-is-longest {share:.0%} > {_LONGEST_SHARE_MAX:.0%}"
            )

    distractors = _distractor_counts(all_questions)
    overused = {t: c for t, c in distractors.items() if c > _DISTRACTOR_REUSE_MAX}
    print(f"\nDistractor repetition (full option sentences, > {_SHORT_OPTION_CHARS} chars):")
    for text, count in distractors.most_common(12):
        if count > 1:
            marker = "  <-- OVER" if count > _DISTRACTOR_REUSE_MAX else ""
            print(f"  {count}x  {text[:66]}{marker}")
    if overused:
        violations.append(f"{len(overused)} distractor(s) reused > {_DISTRACTOR_REUSE_MAX} times")

    hits = _out_of_scope_hits()
    print("\nOut-of-scope services in a keyed answer or explanation:")
    if hits:
        for qid, svc in hits:
            print(f"  {qid}: {svc}  <-- OVER")
        violations.append(f"{len(hits)} keyed answer(s) reference an out-of-scope service")
    else:
        print("  none")

    print(f"\nTotal questions: {len(all_questions)}")
    if check:
        if violations:
            print("\nAUDIT FAILED:")
            for v in violations:
                print(f"  - {v}")
            return 1
        print("\nAUDIT PASSED: no length bias or distractor-reuse violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
