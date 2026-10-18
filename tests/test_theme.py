"""Tests for accessible status rendering and pane presets."""

from __future__ import annotations

from app.theme import (
    DEFAULT_PANE_PRESET,
    PANE_PRESETS,
    StatusTone,
    status_badge_html,
    status_label,
)


def test_status_label_includes_icon_and_text() -> None:
    label = status_label(StatusTone.SUCCESS, "Verified")
    assert "Verified" in label
    assert label.startswith("[x]")  # icon, not color alone


def test_status_badge_has_role_and_aria_label() -> None:
    html = status_badge_html(StatusTone.DANGER, "Model access")
    # Status is conveyed by role, aria-label (word + text), icon, and class.
    assert 'role="status"' in html
    assert "aria-label=" in html
    assert "Problem" in html  # the word, so meaning never depends on color
    assert "sa-badge-danger" in html


def test_badge_covers_every_tone() -> None:
    for tone in StatusTone:
        html = status_badge_html(tone, "x")
        assert f"sa-badge-{tone.value}" in html


def test_pane_presets_are_complete() -> None:
    assert DEFAULT_PANE_PRESET in PANE_PRESETS
    assert set(PANE_PRESETS) == {"Balanced", "Instructions wide", "Workspace wide"}
    for weights in PANE_PRESETS.values():
        assert len(weights) == 2
        assert all(w > 0 for w in weights)
