from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

# Default and allowlist keep portfolio suggestions cheap (short JSON + small replies).
DEFAULT_AI_MODEL = "gpt-4o-mini"


def resolve_cost_efficient_model(requested: str | None) -> tuple[str, bool]:
    """
    Return (model_id, overridden).

    Allows gpt-4o-mini (any dated snapshot) and gpt-3.5-turbo variants.
    Anything else falls back to DEFAULT_AI_MODEL.
    """
    r = (requested or "").strip()
    if not r:
        return DEFAULT_AI_MODEL, False
    lower = r.lower()
    if lower == DEFAULT_AI_MODEL.lower():
        return DEFAULT_AI_MODEL, False
    if lower.startswith("gpt-4o-mini"):
        return r, False
    if lower.startswith("gpt-3.5-turbo"):
        return r, False
    return DEFAULT_AI_MODEL, True


def _message_text(content: Any) -> str:
    """Normalize OpenAI message.content (str, None, or rare list/shape) to plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text" and isinstance(block.get("text"), str):
                    parts.append(block["text"])
                elif isinstance(block.get("text"), str):
                    parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts)
    return str(content)


def suggest_apps(
    user_message: str,
    projects: list[dict[str, Any]],
    *,
    api_key: str,
    model: str,
) -> str:
    """Return markdown guidance with links; raises on API/auth errors."""
    client = OpenAI(api_key=api_key)
    payload = json.dumps(projects, ensure_ascii=False)
    system = (
        "You are an assistant for Abhishek Jha's analytics portfolio hub. "
        "You receive a JSON array of apps with fields: name, url, category, tagline, tags, featured. "
        "Help the user pick the best apps to open. Be concise and practical. "
        "Recommend up to three apps when possible, fewer if the question is narrow. "
        "For each recommendation, include a markdown link using the exact url from JSON, e.g. "
        "[App name](exact_url). Do not invent URLs. "
        "If the question is broad (examples: market research, strategy, pricing, forecasting, GenAI), "
        "still pick the closest matches from the JSON and explain briefly why—do not reply with an empty list. "
        "For market research / competitive intelligence, prioritize Market Intelligence apps when present. "
        "If the question is not about choosing apps, answer briefly and still suggest relevant apps if any. "
        "Do not claim private or unverifiable facts about the author beyond the provided metadata."
    )
    user = f"User question:\n{user_message}\n\nApps JSON:\n{payload}"
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
        max_tokens=700,
    )
    choice = _message_text(resp.choices[0].message.content)
    out = choice.strip()
    if not out:
        return (
            "_The model returned an empty reply. Try rephrasing, or check your API key and model access._"
        )
    return out
