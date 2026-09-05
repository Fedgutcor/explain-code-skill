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

There is no test suite — the artifact is prose. What there is, is a way to check
you didn't make things worse:

1. Pick three snippets, at least one with a real bug and one that is genuinely
   trivial.
2. Get an explanation with the current `SKILL.md` and with your edited one.
3. Ask: did the bug get named more precisely? Did the trivial snippet get
   *longer* without getting clearer?

The second question is the one people skip. A contract change that improves hard
cases while padding easy ones is usually a net loss, because easy cases are most
of them.
