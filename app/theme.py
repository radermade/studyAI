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


# Centralized CSS. Targets only stable app-owned `sa-` classes and generic,
# stable element selectors (never Streamlit's generated class names).
BASE_CSS = """
<style>
:root {
  --sa-bg: #10151c;
  --sa-surface: #18202b;
  --sa-border: #2a3645;
  --sa-text: #e6edf3;
  --sa-muted: #9fb0c0;
  --sa-action: #4c8bf5;
  --sa-success: #3fb27f;
  --sa-warning: #d6ab4e;
  --sa-danger: #e06c75;
  --sa-focus: #8ab4ff;
}
.sa-rail-item { padding: 2px 0; }
.sa-badge {
  display: inline-block; padding: 1px 8px; border-radius: 6px;
  border: 1px solid var(--sa-border); font-size: 0.8rem;
}
.sa-badge-success { border-color: var(--sa-success); color: var(--sa-success); }
.sa-badge-warning { border-color: var(--sa-warning); color: var(--sa-warning); }
.sa-badge-danger  { border-color: var(--sa-danger);  color: var(--sa-danger); }
.sa-badge-progress{ border-color: var(--sa-action);  color: var(--sa-action); }
.sa-badge-neutral { border-color: var(--sa-border);  color: var(--sa-muted); }
.sa-pane {
  border: 1px solid var(--sa-border); border-radius: 8px; padding: 12px;
  background: var(--sa-surface);
}
.sa-code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }

/* Visible focus for keyboard users wherever Streamlit renders real controls. */
button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
[role="radio"]:focus-visible,
[role="tab"]:focus-visible {
  outline: 3px solid var(--sa-focus);
  outline-offset: 2px;
}

/* Respect reduced-motion: never require animation to understand state. */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
}
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

# Human-readable status words, so meaning never depends on color or icon alone.
_WORDS: dict[StatusTone, str] = {
    StatusTone.NEUTRAL: "Not started",
    StatusTone.PROGRESS: "In progress",
    StatusTone.SUCCESS: "Done",
    StatusTone.WARNING: "Attention",
    StatusTone.DANGER: "Problem",
}


def status_label(tone: StatusTone, text: str) -> str:
    """Return a text+icon status label (meaning never depends on color alone)."""
    return f"{_ICONS[tone]} {text}"


def status_badge_html(tone: StatusTone, text: str) -> str:
    """Return an accessible status badge: color + icon + word + text.

    Uses a stable `sa-badge` class and an aria-label so assistive technology
    announces the status explicitly.
    """
    word = _WORDS[tone]
    icon = _ICONS[tone]
    return (
        f'<span class="sa-badge sa-badge-{tone.value}" '
        f'role="status" aria-label="{word}: {text}">{icon} {text}</span>'
    )


# Pane layout presets. Keyboard users choose a preset; pointer users can also
# drag the Streamlit column divider. A narrow screen falls back to stacked.
PANE_PRESETS: dict[str, tuple[int, int]] = {
    "Balanced": (1, 1),
    "Instructions wide": (3, 1),
    "Workspace wide": (1, 3),
}
DEFAULT_PANE_PRESET = "Instructions wide"
