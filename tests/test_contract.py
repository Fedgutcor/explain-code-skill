"""Regression gate for the contract in SKILL.md.

These tests exist because of a defect the contract actually had. `SKILL.md`
used to say "Highlight **at least one** non-obvious failure mode" — a quota. On
a correct `clamp` function the assistant filled it by asserting that
`clamp(NaN, -5, -10)` "violates the contract" by returning `-5`, which it does
not: `-5` is inside `[-10, -5]`. A manufactured defect, stated as confidently as
a real one.

`test_does_not_invent_defects` is that failure, frozen. It fails on the old
wording and passes on the current one. Run it before changing section 4.

    pip install pytest
    EXPLAIN_EVAL_MODEL=... EXPLAIN_EVAL_BASE_URL=... pytest tests -v

Skipped by default: they need a model. Set EXPLAIN_EVAL_ENABLED=1 to run.
They are slow (a minute or more per case on local CPU inference) and, because a
language model is not deterministic, an isolated flip is not proof of a
regression — a real regression repeats.
"""
from __future__ import annotations

import os

import pytest

from cases import BUGGY, CONTROLS
from harness import detects_bug, explain, invents_defect

pytestmark = pytest.mark.skipif(
    os.environ.get("EXPLAIN_EVAL_ENABLED") != "1",
    reason="needs a model; set EXPLAIN_EVAL_ENABLED=1",
)


@pytest.mark.parametrize("case", CONTROLS, ids=lambda c: c.id)
def test_does_not_invent_defects(case):
    """On correct code the contract must not manufacture a failure mode.

    This is the control that a bug-finding test cannot provide: a contract that
    fires at everything scores 100% on buggy code and is still a liability.
    """
    answer = explain(case.code, case.lang, with_contract=True)
    assert not invents_defect(answer), (
        f"{case.id}: the contract claimed a defect in correct code.\n\n{answer}"
    )


@pytest.mark.parametrize("case", BUGGY, ids=lambda c: c.id)
def test_still_finds_real_defects(case):
    """Removing the quota must not cost real detection.

    Guards the obvious overcorrection: a section 4 that is allowed to say
    "nothing here" could learn to always say it.
    """
    answer = explain(case.code, case.lang, with_contract=True)
    assert detects_bug(answer, case.bug), (
        f"{case.id}: missed the seeded defect ({case.bug}).\n\n{answer}"
    )


@pytest.mark.parametrize("case", CONTROLS, ids=lambda c: c.id)
def test_baseline_is_clean_on_controls(case):
    """Sanity check on the probe itself, not on the skill.

    If a plain assistant also invents defects here, the control snippet is not
    as innocent as it looks and the invention test above proves nothing about
    the contract. This one failing means: fix the snippet, not SKILL.md.
    """
    answer = explain(case.code, case.lang, with_contract=False)
    assert not invents_defect(answer), (
        f"{case.id}: even the baseline calls this code buggy — the control "
        f"snippet is suspect.\n\n{answer}"
    )
