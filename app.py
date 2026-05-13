from __future__ import annotations

import html
import os

import streamlit as st

from portfolio.ai import resolve_cost_efficient_model, suggest_apps
from portfolio.data import (
    ROOT,
    compact_for_ai,
    featured_projects,
    filter_projects,
    load_projects_raw,
    load_site,
    sort_projects,
    unique_categories,
)
from portfolio.styles import inject_global_css


st.set_page_config(
    page_title="Analytics Hub | Abhishek Jha",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _secret(name: str, default: str = "") -> str:
    env = (os.environ.get(name) or "").strip()
    if env:
        return env
    try:
        v = st.secrets[name]
        return str(v).strip() if v is not None else default
    except Exception:
        return default


def _render_project_card(p: dict, *, show_featured_badge: bool) -> None:
    tags = p.get("tags") or []
    if not isinstance(tags, list):
        tags = []
    tags_html = "".join(
        f"<span class='ah-tag'>{html.escape(str(t))}</span>" for t in tags
    )
    badge = ""
    if show_featured_badge and p.get("featured"):
        badge = "<div class='ah-badge'>Featured</div>"
    name = html.escape(str(p.get("name", "")))
    category = html.escape(str(p.get("category", "")))
    tagline = html.escape(str(p.get("tagline", "")))
    st.markdown(
        f"""
<div class="ah-card">
  {badge}
  <div class="ah-title">{name}</div>
  <div class="ah-meta">{category}</div>
  <div class="ah-tagline">{tagline}</div>
  <div>{tags_html}</div>
</div>
        """.strip(),
        unsafe_allow_html=True,
    )
    st.link_button("Open app", str(p.get("url", "#")), use_container_width=True)


if "theme" not in st.session_state:
    st.session_state.theme = "dark"

site = load_site()
projects = sort_projects(load_projects_raw())
categories = ["All"] + unique_categories(projects)

with st.sidebar:
    st.markdown("#### Appearance")
    is_dark = st.session_state.theme == "dark"
    theme_choice = st.radio(
        "Theme",
        options=["Light", "Dark"],
        index=1 if is_dark else 0,
        horizontal=True,
        key="theme_radio",
    )
    st.session_state.theme = "dark" if theme_choice == "Dark" else "light"
    if (st.session_state.theme == "dark") != is_dark:
        st.rerun()

    head_rel = str(site.get("headshot_path") or "").strip()
    head_path = (ROOT / head_rel) if head_rel else None
    if head_path and head_path.is_file():
        st.image(str(head_path), width=180)
    else:
        st.caption("_Add a headshot at the path in `data/site.json` → `headshot_path`_")

    st.markdown(f"### {site.get('profile_name', 'Your name')}")
    st.caption(site.get("role_line", ""))
    st.caption(site.get("focus_line", ""))
    st.markdown("---")
    st.markdown("**Links**")
    gh = site.get("github_url", "#")
    li = site.get("linkedin_url", "#")
    st.markdown(f"- [GitHub]({gh})")
    st.markdown(f"- [LinkedIn]({li})")

    st.markdown("---")
    st.markdown("**How to use**")
    st.caption(
        "Browse featured picks, search by keyword (all words must match), filter by category, "
        "then open any app in a new tab. Use **AI guide** for tailored recommendations."
    )

st.markdown(
    inject_global_css(dark=st.session_state.theme == "dark"),
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="ah-top-spacer" aria-hidden="true"></div>',
    unsafe_allow_html=True,
)
tab_apps, tab_about, tab_ai = st.tabs(["Apps", "About", "AI guide"])

with tab_apps:
    hero_title = site.get("hero_title", "Analytics Hub")
    st.markdown(
        f"""
<div class="ah-hero">
  <div class="ah-hero-title">{html.escape(str(hero_title))}</div>
  <div class="ah-hero-sub">{html.escape(str(site.get('hero_lead', '')))}</div>
</div>
        """.strip(),
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns([1.05, 1.05, 1.05, 1.35])
    with m1:
        st.metric("Apps", len(projects))
    with m2:
        st.metric("Categories", len(set(str(p.get("category", "")) for p in projects)))
    with m3:
        st.metric("Featured", sum(1 for p in projects if p.get("featured")))
    with m4:
        st.metric(
            "Experience",
            "Hands-on",
            help="Interactive Streamlit apps across forecasting, experimentation, pricing, GenAI, and data systems.",
        )

    feats = featured_projects(projects)
    if feats:
        st.markdown(
            "<div class='ah-section-label'>Featured</div>",
            unsafe_allow_html=True,
        )
        for i in range(0, len(feats), 3):
            row = feats[i : i + 3]
            cols = st.columns(3)
            for col, proj in zip(cols, row):
                with col:
                    _render_project_card(proj, show_featured_badge=False)

    st.markdown(
        "<div class='ah-section-label ah-section-browse'>Browse</div>",
        unsafe_allow_html=True,
    )
    left, mid, right = st.columns([1.25, 1.0, 0.95])
    with left:
        query = st.text_input(
            "Search",
            placeholder="Try: media mix pricing churn rag conjoint …",
        )
    with mid:
        category = st.selectbox("Category", options=categories, index=0)
    with right:
        featured_only = st.checkbox("Featured only", value=False)

    filtered = filter_projects(
        projects,
        query=query,
        category=str(category),
        featured_only=featured_only,
    )
    st.caption(f"Showing {len(filtered)} of {len(projects)} apps.")

    if not filtered:
        st.info("No matches. Try fewer keywords, clear **Featured only**, or switch category.")
    else:
        for i in range(0, len(filtered), 3):
            chunk = filtered[i : i + 3]
            cols = st.columns(3)
            for col, proj in zip(cols, chunk):
                with col:
                    _render_project_card(proj, show_featured_badge=True)

with tab_about:
    about_path = ROOT / "content" / "about.md"
    if about_path.is_file():
        st.markdown(about_path.read_text(encoding="utf-8"))
    else:
        st.warning("Missing `content/about.md`.")

with tab_ai:
    st.markdown(
        "Describe what you are looking for (role, domain, or method). "
        "The assistant recommends up to three apps using **only** the metadata in this hub."
    )
    api_key = _secret("OPENAI_API_KEY", "")
    model_raw = _secret("OPENAI_MODEL", "") or ""
    model, model_overridden = resolve_cost_efficient_model(model_raw or None)

    if api_key:
        if model_overridden and model_raw.strip():
            st.caption(
                f"Using **`{model}`** (cost-efficient). "
                f"`OPENAI_MODEL` was ignored for `{model_raw.strip()}` — only mini / 3.5-class models are allowed."
            )
        else:
            st.caption(f"Using **`{model}`** (cost-efficient).")

    user_q = st.text_area(
        "Your question",
        height=120,
        key="ai_question",
        placeholder="Example: I am hiring for a growth role focused on retention experiments and causal inference.",
    )
    if st.button("Get suggestions", type="primary", disabled=not api_key):
        q = (st.session_state.get("ai_question") or "").strip()
        if not q:
            st.warning("Enter a question first.")
        else:
            with st.spinner("Thinking…"):
                try:
                    answer = suggest_apps(
                        q,
                        compact_for_ai(projects),
                        api_key=api_key,
                        model=model,
                    )
                except Exception as exc:
                    answer = f"**Something went wrong.**\n\n`{type(exc).__name__}: {exc}`"
            st.session_state["ai_last_answer"] = answer

    last = st.session_state.get("ai_last_answer")
    if last is not None and str(last).strip() != "":
        st.markdown("---")
        st.markdown(str(last))
        if st.button("Clear AI response", key="ai_clear_btn"):
            st.session_state.pop("ai_last_answer", None)
            st.rerun()
    elif api_key:
        st.caption("Tip: click **Get suggestions** after you type your question.")

st.divider()
st.caption("© 2026 Abhishek Jha • Analytics & Decision Science")
