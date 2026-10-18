"""Original visual tokens and status helpers.

No KodeKloud branding, palette, or trade dress is used. Status is always paired
with an icon and text, never color alone.
"""

from __future__ import annotations

from enum import StrEnum

# Original semantic color tokens (dark professional workspace).
TOKENS: dict[str, str] = {
    "background": "#10151c",
    "surface": "#18202b",
    "border": "#2a3645",
    "text": "#e6edf3",
    "muted": "#9fb0c0",
    "action": "#4c8bf5",
    "success": "#3fb27f",
    "warning": "#d6ab4e",
    "danger": "#e06c75",
    "focus": "#8ab4ff",
}

PRODUCT_NAME = "studyAI Workspace"

BASE_CSS = """
<style>
:root {
  --sa-bg: #10151c;
  --sa-surface: #18202b;
  --sa-border: #2a3645;
  --sa-text: #e6edf3;
  --sa-muted: #9fb0c0;
}
.sa-rail-item { padding: 2px 0; }
.sa-badge {
  display: inline-block; padding: 1px 8px; border-radius: 6px;
  border: 1px solid var(--sa-border); font-size: 0.8rem;
}
.sa-pane {
  border: 1px solid var(--sa-border); border-radius: 8px; padding: 12px;
  background: var(--sa-surface);
}
button:focus-visible, a:focus-visible { outline: 2px solid #8ab4ff; }
</style>
"""


class StatusTone(StrEnum):
    """Status tones paired with an icon and text (never color alone)."""

    NEUTRAL = "neutral"
    PROGRESS = "progress"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"


_ICONS: dict[StatusTone, str] = {
    StatusTone.NEUTRAL: "[ ]",
    StatusTone.PROGRESS: "[~]",
    StatusTone.SUCCESS: "[x]",
    StatusTone.WARNING: "[!]",
    StatusTone.DANGER: "[-]",
}


def status_label(tone: StatusTone, text: str) -> str:
    """Return a text+icon status label (accessible without color)."""
    return f"{_ICONS[tone]} {text}"
