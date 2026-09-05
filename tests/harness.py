"""Runs the contract against a model and grades the output.

Provider-agnostic on purpose: it speaks to an OpenAI-compatible `/chat/completions`
endpoint, which covers Ollama, llama.cpp, vLLM, OpenAI, Groq, OpenRouter and most
gateways. Configure with environment variables:

    EXPLAIN_EVAL_BASE_URL   default http://localhost:11434/v1
    EXPLAIN_EVAL_MODEL      default gpt-oss:20b
    EXPLAIN_EVAL_API_KEY    default "ollama" (ignored by local servers)

    EXPLAIN_JUDGE_BASE_URL / EXPLAIN_JUDGE_MODEL / EXPLAIN_JUDGE_API_KEY
        The grader. Defaults to the same endpoint, but SET IT TO A DIFFERENT
        MODEL when you can: a model grading its own output is a weaker check.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent

BASELINE_SYSTEM = "You are a helpful senior software engineer. Explain code clearly when asked."
PROMPT = "Explain how this {lang} code works:\n\n```{lang}\n{code}\n```"


def contract() -> str:
    """The body of SKILL.md, without the YAML frontmatter."""
    return (ROOT / "SKILL.md").read_text().split("---", 2)[2].strip()


def _chat(base_url: str, api_key: str, model: str, system: str, prompt: str,
          max_tokens: int = 2048, timeout: int = 900) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read())
    return (data["choices"][0]["message"].get("content") or "").strip()


def explain(code: str, lang: str, *, with_contract: bool) -> str:
    return _chat(
        os.environ.get("EXPLAIN_EVAL_BASE_URL", "http://localhost:11434/v1"),
        os.environ.get("EXPLAIN_EVAL_API_KEY", "ollama"),
        os.environ.get("EXPLAIN_EVAL_MODEL", "gpt-oss:20b"),
        contract() if with_contract else BASELINE_SYSTEM,
        PROMPT.format(lang=lang, code=code),
    )


def _grade(rubric: str, valid: tuple[str, ...]) -> str:
    base = os.environ.get("EXPLAIN_JUDGE_BASE_URL") or os.environ.get("EXPLAIN_EVAL_BASE_URL", "http://localhost:11434/v1")
    key = os.environ.get("EXPLAIN_JUDGE_API_KEY") or os.environ.get("EXPLAIN_EVAL_API_KEY", "ollama")
    model = os.environ.get("EXPLAIN_JUDGE_MODEL") or os.environ.get("EXPLAIN_EVAL_MODEL", "gpt-oss:20b")
    for _ in range(3):
        raw = _chat(base, key, model, "You are a strict grader. Answer with one word.",
                    rubric, max_tokens=512).upper()
        m = re.search(r"\b(" + "|".join(valid) + r")\b", raw)
        if m:
            return m.group(1)
    return "UNPARSED"


DETECT_RUBRIC = """You are grading whether a code explanation identifies a specific defect.

THE DEFECT THAT EXISTS IN THE CODE:
{bug}

THE EXPLANATION TO GRADE:
---
{answer}
---

Does the explanation identify THIS defect as a problem? Different wording is fine;
the mechanism must match, and it must be presented as a problem rather than
mentioned in passing.

Answer with exactly one word: YES or NO."""

INVENTION_RUBRIC = """You are grading whether a code explanation invents defects that do not exist.

THE CODE IS CORRECT. It has no bug.

THE EXPLANATION TO GRADE:
---
{answer}
---

Does the explanation claim the code has a bug, defect, or incorrect behaviour?

Suggestions for improvement, performance notes, hardening ideas and stylistic
remarks are NOT invented defects. Only count claims that the code behaves
incorrectly, is broken, or will fail.

Answer with exactly one word: CLEAN or INVENTED."""


def detects_bug(answer: str, bug: str) -> bool:
    return _grade(DETECT_RUBRIC.format(bug=bug, answer=answer), ("YES", "NO")) == "YES"


def invents_defect(answer: str) -> bool:
    return _grade(INVENTION_RUBRIC.format(answer=answer), ("CLEAN", "INVENTED")) == "INVENTED"
