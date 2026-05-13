"""Wake every Streamlit URL listed in data/projects.json plus optional data/site.json extras."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def collect_urls() -> list[str]:
    projects_path = ROOT / "data" / "projects.json"
    site_path = ROOT / "data" / "site.json"
    data = json.loads(projects_path.read_text(encoding="utf-8"))
    projects = data.get("projects", [])
    urls: list[str] = []
    seen: set[str] = set()
    for p in projects:
        u = str(p.get("url", "")).strip()
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    if site_path.is_file():
        site = json.loads(site_path.read_text(encoding="utf-8"))
        for u in site.get("wake_extra_urls") or []:
            u = str(u).strip()
            if u and u not in seen:
                seen.add(u)
                urls.append(u)
    return urls


async def _wake() -> int:
    from playwright.async_api import async_playwright

    urls = collect_urls()
    if not urls:
        print("No URLs found; exiting.", file=sys.stderr)
        return 1

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            for url in urls:
                print(f"Wake: {url}")
                context = await browser.new_context()
                page = await context.new_page()
                try:
                    await page.goto(url, wait_until="networkidle", timeout=90000)
                    await asyncio.sleep(8)
                    print(f"OK: {url}")
                except Exception as exc:
                    print(f"WARN: {url} -> {exc}", file=sys.stderr)
                finally:
                    await page.close()
                    await context.close()
        finally:
            await browser.close()
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(_wake()))


if __name__ == "__main__":
    main()
