from __future__ import annotations


def inject_global_css(*, dark: bool) -> str:
    """Return a <style> block tuned for light or dark theme."""
    if dark:
        bg = "#0b1220"
        panel = "#0f172a"
        card = "#111c2e"
        text = "#e5e7eb"
        muted = "rgba(229,231,235,0.72)"
        faint = "rgba(229,231,235,0.55)"
        border = "rgba(255,255,255,0.10)"
        border_hover = "rgba(255,255,255,0.22)"
        tag_bg = "rgba(255,255,255,0.06)"
        btn = "#e5e7eb"
        btn_text = "#0b1220"
        btn_hover_bg = "#cbd5e1"
        section_muted = "rgba(229,231,235,0.60)"
        browse_fg = "#93c5fd"
        browse_bg = "rgba(59, 130, 246, 0.18)"
        browse_bd = "rgba(147, 197, 253, 0.42)"
    else:
        bg = "#ffffff"
        panel = "#f7f8fa"
        card = "#ffffff"
        text = "#111827"
        muted = "rgba(17,24,39,0.72)"
        faint = "rgba(17,24,39,0.55)"
        border = "rgba(17,24,39,0.10)"
        border_hover = "rgba(17,24,39,0.35)"
        tag_bg = "rgba(17,24,39,0.04)"
        btn = "#111827"
        btn_text = "#ffffff"
        btn_hover_bg = "#1f2937"
        section_muted = "rgba(17,24,39,0.60)"
        browse_fg = "#1d4ed8"
        browse_bg = "rgba(37, 99, 235, 0.10)"
        browse_bd = "rgba(37, 99, 235, 0.30)"

    return f"""
<style>
/* Room under Streamlit's fixed header so primary tabs stay visible */
.ah-top-spacer {{
  min-height: calc(4.5rem + env(safe-area-inset-top, 0px));
  height: calc(4.5rem + env(safe-area-inset-top, 0px));
  width: 100%;
  flex-shrink: 0;
}}

.block-container {{
  padding-top: 0.85rem;
  padding-bottom: 2.5rem;
  max-width: 1200px;
}}

section[data-testid="stMain"] > div {{
  padding-top: 0 !important;
}}

.stApp {{
  background-color: {bg};
  color: {text};
}}

section[data-testid="stSidebar"] {{
  background-color: {panel};
  border-right: 1px solid {border};
}}

section[data-testid="stSidebar"] * {{
  color: {text};
}}

h1, h2, h3 {{
  letter-spacing: -0.02em;
  color: {text};
}}

.stCaption, [data-testid="stCaptionContainer"] {{
  color: {faint} !important;
}}

div[data-testid="stMetricValue"] {{
  color: {text};
  overflow: visible !important;
  text-overflow: clip !important;
  white-space: normal !important;
  line-height: 1.2 !important;
  overflow-wrap: anywhere;
  padding: 0.2rem 0 0.45rem 0 !important;
  font-size: clamp(1.45rem, 2.8vw, 1.85rem) !important;
}}

[data-testid="stMetric"] {{
  overflow: visible !important;
  min-height: 4.5rem;
  padding: 0.35rem 0 0.85rem 0 !important;
  align-items: flex-start !important;
}}

[data-testid="stMetric"] > div {{
  overflow: visible !important;
}}

[data-testid="stMetricLabel"] {{
  white-space: normal !important;
  overflow: visible !important;
  padding-bottom: 0.2rem !important;
}}

.ah-hero {{
  border: 1px solid {border};
  border-radius: 16px;
  padding: 1.25rem 1.35rem 1.1rem 1.35rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, {panel} 0%, {bg} 55%);
}}

.ah-hero-title {{
  font-size: 2.05rem;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 0.35rem 0;
  color: {text};
}}

.ah-hero-sub {{
  font-size: 1.02rem;
  color: {muted};
  margin: 0 0 0.75rem 0;
  max-width: 52rem;
}}

.ah-section-label {{
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: {section_muted};
  margin: 1.1rem 0 0.45rem 0;
}}

.ah-section-label.ah-section-browse {{
  display: inline-block;
  color: {browse_fg} !important;
  background: {browse_bg} !important;
  border: 1px solid {browse_bd} !important;
  border-radius: 8px !important;
  padding: 0.45rem 0.8rem !important;
  margin: 1.25rem 0 0.55rem 0 !important;
  letter-spacing: 0.11em !important;
}}

.ah-card {{
  border: 1px solid {border};
  border-radius: 14px;
  background: {card};
  padding: 16px 16px 12px 16px;
  height: 100%;
  box-shadow: 0 1px 0 rgba(0,0,0,0.03);
}}
.ah-card:hover {{ border-color: {border_hover}; }}

.ah-badge {{
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 0.22rem 0.5rem;
  border-radius: 999px;
  border: 1px solid {border};
  color: {faint};
  margin-bottom: 0.55rem;
}}

.ah-title {{
  font-size: 1.05rem;
  font-weight: 800;
  color: {text};
  margin-bottom: 0.25rem;
}}

.ah-tagline {{
  font-size: 0.92rem;
  color: {muted};
  margin-bottom: 0.6rem;
  line-height: 1.35;
}}

.ah-meta {{
  font-size: 0.80rem;
  color: {faint};
  margin-bottom: 0.55rem;
}}

.ah-tag {{
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 650;
  padding: 0.16rem 0.45rem;
  border-radius: 999px;
  border: 1px solid {border};
  background: {tag_bg};
  margin-right: 0.35rem;
  margin-bottom: 0.35rem;
  color: {text};
}}

div.stLinkButton > a {{
  background-color: {btn} !important;
  color: {btn_text} !important;
  border-radius: 10px !important;
  font-weight: 800 !important;
  padding: 0.52rem 0.95rem !important;
  border: 1px solid {btn} !important;
}}
div.stLinkButton > a:hover {{
  background-color: {btn_hover_bg} !important;
  border-color: {btn_hover_bg} !important;
}}

div[data-testid="stMarkdownContainer"] > p {{ margin-bottom: 0.25rem; }}

.ah-headshot-wrap img {{
  border-radius: 999px;
  border: 1px solid {border};
}}

[data-testid="stTabs"] {{
  margin-top: 0 !important;
  padding-top: 0 !important;
  position: relative;
  z-index: 200;
}}

[data-testid="stTabs"] [data-baseweb="tab-list"] {{
  gap: 10px;
  padding: 10px 12px !important;
  flex-wrap: wrap;
  background: {panel} !important;
  border: 1px solid {border} !important;
  border-radius: 12px !important;
}}

[data-testid="stTabs"] button {{
  padding: 0.55rem 1.05rem !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  color: {muted} !important;
  border-radius: 8px !important;
}}

[data-testid="stTabs"] button[aria-selected="true"] {{
  color: {text} !important;
  background: {card} !important;
  border: 1px solid {border} !important;
}}

[data-testid="stTabs"] button p {{
  color: inherit !important;
}}

[data-testid="stTabs"] button:hover {{
  color: {text} !important;
}}

/* Primary & form submit — theme primaryColor + BaseWeb vary by Streamlit version */
[data-testid="baseButton-primary"],
[data-testid="stBaseButton-primary"],
[data-testid="stFormSubmitButton"] button,
[data-testid="stFormSubmitButton"] [data-baseweb="button"],
div[data-testid="stForm"] button[type="submit"],
div[data-testid="stForm"] [data-baseweb="button"][kind="primary"],
button[kind="primary"] {{
  background-color: {btn} !important;
  background-image: none !important;
  color: {btn_text} !important;
  -webkit-text-fill-color: {btn_text} !important;
  border: 1px solid {btn} !important;
  font-weight: 700 !important;
}}
[data-testid="baseButton-primary"]:hover,
[data-testid="stBaseButton-primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover:not(:disabled),
[data-testid="stFormSubmitButton"] [data-baseweb="button"]:hover:not(:disabled),
div[data-testid="stForm"] button[type="submit"]:hover:not(:disabled),
button[kind="primary"]:hover:not(:disabled) {{
  background-color: {btn_hover_bg} !important;
  background-image: none !important;
  color: {btn_text} !important;
  -webkit-text-fill-color: {btn_text} !important;
  border-color: {btn_hover_bg} !important;
}}
[data-testid="baseButton-primary"]:disabled,
[data-testid="stBaseButton-primary"]:disabled,
[data-testid="stFormSubmitButton"] button:disabled,
[data-testid="stFormSubmitButton"] [data-baseweb="button"]:disabled,
div[data-testid="stForm"] button[type="submit"]:disabled,
button[kind="primary"]:disabled {{
  opacity: 0.5 !important;
  cursor: not-allowed !important;
}}
[data-testid="baseButton-primary"] p,
[data-testid="baseButton-primary"] span,
[data-testid="stBaseButton-primary"] p,
[data-testid="stBaseButton-primary"] span,
[data-testid="stFormSubmitButton"] button p,
[data-testid="stFormSubmitButton"] button span,
[data-testid="stFormSubmitButton"] [data-baseweb="button"] p,
[data-testid="stFormSubmitButton"] [data-baseweb="button"] span,
div[data-testid="stForm"] button[type="submit"] p,
button[kind="primary"] p,
button[kind="primary"] span {{
  color: {btn_text} !important;
  -webkit-text-fill-color: {btn_text} !important;
}}
</style>
""".strip()
