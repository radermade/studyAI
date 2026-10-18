"""Transport-independent domain logic for the studyAI platform.

`study_core` must not import Streamlit, FastMCP, or boto3. It owns the Phase 0
blueprint, source, profile, safety, baseline, and seed-admission rules plus the
deterministic handoff and acceptance evaluation.
"""
