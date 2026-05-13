from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List

ROOT = Path(__file__).resolve().parent.parent


def _read_json(rel: str) -> Any:
    path = ROOT / rel
    return json.loads(path.read_text(encoding="utf-8"))


def load_site() -> dict[str, Any]:
    return _read_json("data/site.json")


def load_projects_raw() -> list[dict[str, Any]]:
    data = _read_json("data/projects.json")
    projects = data.get("projects")
    if not isinstance(projects, list):
        raise ValueError("data/projects.json must contain a 'projects' array.")
    return projects


def compact_for_ai(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Minimal fields sent to the model (URLs must match exactly for linking)."""
    out: list[dict[str, Any]] = []
    for p in projects:
        out.append(
            {
                "name": p["name"],
                "url": p["url"],
                "category": p["category"],
                "tagline": p["tagline"],
                "tags": p.get("tags", []),
                "featured": bool(p.get("featured", False)),
            }
        )
    return out


def unique_categories(projects: Iterable[dict[str, Any]]) -> List[str]:
    seen: set[str] = set()
    ordered: List[str] = []
    for p in projects:
        c = str(p.get("category", "")).strip()
        if not c or c in seen:
            continue
        seen.add(c)
        ordered.append(c)
    return ordered


def _haystack(p: dict[str, Any]) -> str:
    tags = p.get("tags") or []
    if not isinstance(tags, list):
        tags = []
    parts = [str(p.get("name", "")), str(p.get("category", "")), str(p.get("tagline", ""))]
    parts.extend(str(t) for t in tags)
    return " ".join(parts).lower()


def matches_search(p: dict[str, Any], query: str) -> bool:
    q = (query or "").strip().lower()
    if not q:
        return True
    tokens = [t for t in q.split() if t]
    if not tokens:
        return True
    hay = _haystack(p)
    return all(tok in hay for tok in tokens)


def sort_projects(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(p: dict[str, Any]) -> tuple:
        featured = 1 if p.get("featured") else 0
        order = int(p.get("order", 999))
        name = str(p.get("name", "")).lower()
        return (-featured, order, name)

    return sorted(projects, key=key)


def filter_projects(
    projects: list[dict[str, Any]],
    *,
    query: str,
    category: str,
    featured_only: bool,
) -> list[dict[str, Any]]:
    cat = (category or "All").strip()
    out: list[dict[str, Any]] = []
    for p in projects:
        if featured_only and not p.get("featured"):
            continue
        if cat != "All" and str(p.get("category", "")).strip() != cat:
            continue
        if not matches_search(p, query):
            continue
        out.append(p)
    return sort_projects(out)


def featured_projects(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sort_projects([p for p in projects if p.get("featured")])
