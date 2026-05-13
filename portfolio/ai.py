from __future__ import annotations

import json
from typing import Any

from openai import OpenAI


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
    )
    choice = resp.choices[0].message.content
    if not choice:
        return "_No response from the model._"
    return choice.strip()
