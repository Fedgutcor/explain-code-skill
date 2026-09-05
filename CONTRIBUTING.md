# Contributing

This repo is a **contract**, not a library. That shapes what a good contribution
looks like.

## The bar for changing the contract

`SKILL.md` is short on purpose. Every line an assistant has to hold in context is
paid for by the reader, so a new rule has to earn its place by replacing a
failure that actually happens — not by covering a case that theoretically could.

A change to `SKILL.md` is much easier to accept when the issue or PR says:

1. **The failure.** A real explanation an assistant produced that the current
   contract permits and shouldn't. Paste it.
2. **The rule.** The smallest wording that would have prevented it.
3. **What it costs.** Which explanations get worse or longer because of the new
   rule. Everything has a cost; naming it is what makes the tradeoff reviewable.

Adding a sixth section is the change most likely to be declined. The contract
already leans on the edge of ceremony, which is why the assistant is explicitly
allowed to collapse sections that have nothing to say.

## Easier contributions, equally welcome

- **A worked example in another language.** `examples.md` is TypeScript. A pass
  over Python, Go, or Rust — with a real bug, not a toy — proves the contract
  isn't language-specific.
- **A counterexample.** Code where following the contract produces a *worse*
  explanation than a plain answer. That is more useful than a new rule, and it
  belongs in the issues.
- **A translation of `README.es.md` / `README.md`** into another language.
  Note that `SKILL.md` itself stays English-only, and deliberately: two
  translated copies of a contract diverge. This repo exists because exactly that
  happened — a published Spanish translation had silently dropped the triggers
  from the `description` field, producing a skill that never auto-activated.

## Forking is a legitimate outcome

If your team explains things differently, fork it and change the five parts. The
value here is *having* an explicit contract with failure criteria, not this
particular one. A fork that fits your codebase beats a compromise that fits
nobody.

## Testing a change

There is a regression gate: [`tests/`](tests). It needs a model — any
OpenAI-compatible endpoint, including a local Ollama — and it is skipped unless
you ask for it:

```bash
pip install pytest
export EXPLAIN_EVAL_ENABLED=1
export EXPLAIN_EVAL_BASE_URL=http://localhost:11434/v1
export EXPLAIN_EVAL_MODEL=gpt-oss:20b
export EXPLAIN_JUDGE_MODEL=<a different model, if you have one>
pytest tests -v
```

Three checks, and the first is the one that matters:

- `test_does_not_invent_defects` — on **correct** code, the contract must not
  manufacture a failure mode. This is a real defect this contract had, frozen as
  a test: section 4 used to demand "at least one" failure mode, and on a correct
  `clamp` the assistant filled the quota by asserting that `clamp(NaN, -5, -10)`
  "violates the contract" by returning `-5`. It does not. Run this before
  touching section 4.
- `test_still_finds_real_defects` — the guard against overcorrecting: a section
  allowed to say "nothing here" could learn to always say it.
- `test_baseline_is_clean_on_controls` — tests the probe, not the skill. If a
  plain assistant also calls the control snippet buggy, the snippet is at fault
  and the invention test proves nothing.

The measurement that produced these cases, including where the contract lost, is
in [EVAL.md](EVAL.md).

Two caveats. A language model is not deterministic, so a single flip is not a
regression — rerun before concluding. And these tests check that a change did not
break what is already known to matter; they cannot tell you a new rule is worth
its cost. That still needs the three questions above.
