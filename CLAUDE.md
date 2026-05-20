# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the IT Helpdesk API (main app)
python -m uvicorn api:app --reload

# Run the Streamlit price comparison app
streamlit run price_compare/app.py

# Run the matplotlib dashboard (requires API running first)
python practice/dashboard.py

# Test the API manually
# POST http://127.0.0.1:8000/ask  { "message": "...", "user_name": "..." }
# GET  http://127.0.0.1:8000/tickets
# GET  http://127.0.0.1:8000/stats
# Interactive docs: http://127.0.0.1:8000/docs
```

## Environment Variables

Requires a `.env` file in the project root:
```
ANTHROPIC_API_KEY=...
```

`price_compare/` has its own `.env` that also needs `SERPER_API_KEY` for the Google Shopping search via Serper.dev.

## Architecture

This repo contains two independent applications and a `practice/` folder of learning scripts.

### IT Helpdesk AI (`api.py`)
FastAPI service that accepts IT support questions, calls the Claude API (Haiku model), and returns structured JSON responses — categorized by type (硬體/軟體/網路/其他), severity (低/中/高), and solution steps. Every response is auto-saved as a JSON ticket under `tickets/`.

- `api.py` — the entire backend: FastAPI routes, Claude prompt, ticket I/O, and stats aggregation
- `tickets/` — JSON files, one per ticket, named by timestamp (`ticket_YYYYMMDDHHMMSS.json`)
- `practice/dashboard.py` — standalone script that calls the running API's `/stats` and `/tickets` endpoints and renders a 4-panel matplotlib chart

The system prompt forces Claude to return **only raw JSON** (no markdown fences). Parsing strips to the first `{...}` block as a safeguard.

### Price Comparison App (`price_compare/`)
Streamlit UI that searches Google Shopping via Serper.dev and optionally calls Claude (Haiku) to analyze and recommend products.

- `price_compare/search.py` — thin wrapper around the Serper API, runnable standalone
- `price_compare/app.py` — full Streamlit app; combines search, price filtering, and Claude analysis in one file

### Practice Scripts (`practice/`)
Standalone learning files covering pandas, numpy, matplotlib, seaborn, Streamlit, and prompt engineering. Not part of either application.

## Model Usage

Both apps use `claude-haiku-4-5-20251001`. The IT Helpdesk prompt is written in Traditional Chinese and constrains output to pure JSON. The price comparison prompt requests Traditional Chinese markdown output.

## 開發規範

- 變數命名使用 `snake_case`（如 `ticket_id`、`user_name`）
- 函式命名使用 `snake_case`（如 `get_tickets`、`save_ticket`）
- 程式碼註解一律使用繁體中文
- 字串格式優先使用 f-string
- 每個函式都要有繁體中文 docstring 說明用途

## 注意事項

- `tickets/` 資料夾內的 JSON 檔案**禁止修改或刪除**，這是系統的核心資料
- `.env` 檔案**禁止修改**，內含 API Key 等敏感資訊
- `.gitignore` 檔案**禁止修改**
- 修改 `api.py` 的 system prompt 時要特別小心，必須確保回傳格式仍為純 JSON
- 新增功能前先告知計畫，不要直接修改現有邏輯
