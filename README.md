# Analytics Hub (Streamlit)

Single **portfolio hub** that lists every deployed Streamlit app, supports **light/dark** themes (defaults to **dark**), optional **OpenAI-powered** “which app should I open?” guidance, and keeps data in **`data/projects.json`** so URLs stay consistent (including the GitHub wake workflow).

## Run locally

```bash
cd "C:\Users\jhaab\OneDrive - UW\Desktop\Cursor\03. Portfolio\01. portfolio_all_projects"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Configure profile and links

Edit **`data/site.json`**:

- `linkedin_url` — replace with your real profile URL.
- `headshot_path` — path relative to repo root (for example `assets/headshot.jpg`). Drop an image file there, or change the path.

## OpenAI (optional)

**Streamlit Community Cloud:** App settings → Secrets → TOML:

```toml
OPENAI_API_KEY = "sk-..."
```

**Cost-efficient models only:** the hub defaults to **`gpt-4o-mini`**. Optionally set `OPENAI_MODEL` to another **allowed** id: any **`gpt-4o-mini`** snapshot or **`gpt-3.5-turbo`** variant. Premium models (e.g. full `gpt-4o`) are **not** used — the app falls back to `gpt-4o-mini`.

**Local shell:** set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL` within the allowlist above).

If no key is set, **Get suggestions** stays disabled; the rest of the hub works normally.

## Data model

- **`data/projects.json`** — canonical list (`name`, `url`, `category`, `tagline`, `tags`, `featured`, `order`).
- **`content/about.md`** — About tab (markdown).

After you deploy this hub to a new Streamlit URL, add that URL to **`wake_extra_urls`** in `data/site.json` so the scheduled workflow also keeps the hub warm.

## Keep-alive workflow

`.github/workflows/keep_alive.yml` runs every **10 hours** (and on demand). It executes **`scripts/wake_from_data.py`**, which loads all `url` values from `data/projects.json` plus any strings in `site.json → wake_extra_urls`.

## Archive

Earlier snapshots and `Apps_link.xlsx` live under **`initial_data/`**.
