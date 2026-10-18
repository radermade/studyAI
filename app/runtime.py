"""Per-session runtime accessor for the Streamlit app.

Builds one `StudyRuntime` per browser session and caches it in session state.
Credentials and answer material never enter session state; only the service
handles (which read committed SQLite data) are cached.
"""

from __future__ import annotations

from typing import Any

import streamlit as st
from content.aip_c01 import BLUEPRINT_VERSION
from study_core.bootstrap import StudyRuntime, build_runtime
from study_core.settings import Settings

_RUNTIME_KEY = "_sa_runtime"
DEFAULT_LEARNER_ID = "local-learner"


def get_runtime() -> StudyRuntime:
    """Return the session's runtime, building it on first use.

    The read-only AWS validator is attached lazily; offline sessions still work
    for every non-lab view.
    """
    cached: Any = st.session_state.get(_RUNTIME_KEY)
    if cached is not None:
        return cached  # type: ignore[no-any-return]
    validator = _build_validator()
    runtime = build_runtime(
        Settings.from_env(), blueprint_version=BLUEPRINT_VERSION, validator=validator
    )
    st.session_state[_RUNTIME_KEY] = runtime
    return runtime


def _build_validator() -> Any:
    """Build the read-only AWS validator, tolerating a missing boto3/AWS setup."""
    try:
        from study_aws.validators import AwsReadOnlyValidator

        return AwsReadOnlyValidator()
    except Exception:
        return None


def learner_id() -> str:
    """Return the active learner ID for this local session."""
    return DEFAULT_LEARNER_ID
