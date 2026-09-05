# Does it actually help?

A skill that claims to improve explanations should be able to show it. This is
the measurement, including the part that did not go the skill's way.

**Setup.** 8 code snippets — 6 with a real seeded bug (cache stampede, Python
mutable default argument, swallowed exception, N+1 queries, off-by-one, Go
concurrent map write) and **2 that are correct**. Each explained twice by the
same model (`gpt-oss:20b`, running on CPU on a local box): once with a neutral
"you are a helpful senior engineer" system prompt, once with this skill's
contract. 16 runs.

Two controls, because the obvious way to fake this result is to make the answers
longer and claim more:

- **The correct snippets.** If the skill only "finds more" because it fires at
  everything, that shows up as invented defects in code that has none.
- **Double-order pairwise.** A separate model, which is never told a skill
  exists, is asked which of two explanations helps an engineer *fix* the code.
  Every pair is judged twice with the order flipped; a judge that just prefers
  whatever came second produces one win per side, which is scored as
  inconsistent rather than as a win.

## Results

**Bug detection: a ceiling, not a difference.**

| | detected the seeded bug |
|---|---|
| baseline | 6 / 6 |
| with skill | 6 / 6 |

Classic bugs are found with or without a contract. Anyone claiming their skill
"catches more bugs" on cases like these is measuring the model, not the skill.
This metric discriminates nothing and was dropped.

**Usefulness for fixing: the skill wins, on buggy code.**

| snippet | winner |
|---|---|
| cache stampede | skill (both orders) |
| mutable default | skill (both orders) |
| swallowed exception | skill (both orders) |
| N+1 | skill (both orders) |
| Go concurrent map write | skill (both orders) |
| off-by-one | *inconsistent* — the judge picked the second position in both orders |

**5–0 for the skill**, with one case discarded by its own control. That the
control caught one is the point: without it, the score would read 6–0.

**On correct code, the skill loses — and that finding changed the contract.**

| snippet | invented a defect? | pairwise |
|---|---|---|
| `slugify` | no | baseline (both orders) |
| `clamp` | **yes** | baseline (both orders) |

On the `clamp` snippet the skill produced a failure-mode table asserting that
`clamp(NaN, -5, -10)` "violates the contract" by returning `-5`. It does not:
`-5` is inside `[-10, -5]`. A manufactured defect, stated with the same
confidence as the real ones.

The first suspect was one word in this repo's own `SKILL.md`: *"Highlight **at
least one** non-obvious failure mode."* A quota gets filled whether or not there
is anything to fill it with. Section 4 was rewritten to say it has no quota and
that "I looked and it is sound" is a complete answer.

**That fix was measured, and it was not enough.** On a rerun the same snippet
still produced a five-row failure-mode table. The rows were less false — the new
claim, that `clamp(5, NaN, 10)` returns NaN, is actually true — but three of the
five were not defects at all: a caller violating the TypeScript signature, the
degenerate-but-correct `min === max`, and a row whose own text said "no error".

So the quota was not the whole cause. **The container was.** A table with zero
rows looks broken, so the model builds the table and then finds rows for it.
Section 4 now sets the opposite default: when the code is sound the section is
one line, with no table, no list and no scenario grid — the table gets built only
after there is a real finding to put in it — plus an explicit list of the things
that are *not* failure modes, ending with: if the entry ends in "no error" or
"acceptable", delete it.

**That second attempt was measured too, and it held.** Same snippet, same model:
the table went from five rows to two, neither claiming the code is broken, and
the judge scored it CLEAN. Detection on the buggy snippets was unaffected and the
answers got ~20% shorter. One run per cell, so treat it as one data point in the
right direction, not as settled — the test in `tests/` exists precisely because a
single flip is not proof.

### An open finding the tests do not catch

Reading that same passing run surfaced a different defect. The verification
vector it proposed included:

```ts
console.assert(clamp(15, 30, 10) === 30);  // wrong
```

With the bounds swapped this returns **15**, not 30. The contract had stopped
inventing defects and had started shipping a false assertion — arguably worse,
because the reader runs it, watches it fail, and goes hunting for a bug that does
not exist.

Section 5 now requires hand-executing every expected value against the literal
inputs rather than inferring it from what the function is supposed to do. **That
rule is unverified.** Grading it properly means executing the proposed assertions
in each language, which this harness does not do — an LLM judge asked "is this
test correct?" is exactly the wrong instrument. It is written down here rather
than quietly fixed.

**Cost.** Median answer: 3,784 → 5,003 characters (+32%), 172s → 256s. Real, and
the reason the contract lets the assistant collapse sections that have nothing
to say.

## What this does and does not show

It shows that on code with a real defect, this contract produces explanations a
blind judge prefers for repair work, consistently across order flips — and that
on clean code it was, before the fix, a liability.

It does not show that the effect holds on a stronger model, on a larger codebase,
on languages outside these five, or with a human judge instead of an LLM one. One
model, eight snippets, one judge family. Treat it as evidence, not proof.

Reproducing it needs nothing from this repo: 8 snippets, two system prompts, a
judge that never learns which is which, and both orders. The controls are the
part worth copying.
