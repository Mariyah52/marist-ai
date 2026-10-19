# Marist — IMADI Tech AI Technology Consultant

Marist is being rebuilt as a multilingual AI consultant for IMADI Tech. The first foundation supports:

- Persistent users, conversations and messages
- AI responses with language adaptation
- Business-problem and lead capture records
- Proposed-solution records
- WhatsApp webhook + outgoing message service
- A browser voice MVP using speech recognition/synthesis
- Docker deployment

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# or cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API and `web/index.html` for the voice MVP (serve the web directory from the same host in production).

## Architecture direction

Voice/chat → conversation manager → intent/problem understanding → Imadi knowledge → solution reasoning → response → lead + solution records → human follow-up.

The current voice UI is deliberately an MVP. For production-quality multilingual, interruptible voice, replace browser speech recognition/synthesis with a dedicated streaming STT/TTS or realtime voice provider while keeping the `/api/voice/turn` contract and conversation database.

## Current build: V1 + Lead Intelligence

Marist is an IMADI Tech AI technology consultant foundation. It supports persistent conversations, multilingual language tagging, AI responses, business-opportunity detection, lead records, proposed-solution records, WhatsApp webhook handling, a browser voice MVP, and a protected admin dashboard.

### Local run

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open `/voice` for the voice MVP and `/admin/` for the lead dashboard. Set `ADMIN_API_KEY` in `.env` before using the dashboard. Set `ANTHROPIC_API_KEY` for live Claude responses.

### Production voice

The current `/voice` page uses browser speech recognition/synthesis as a development MVP. The backend is deliberately provider-neutral so a production realtime STT/TTS provider can be connected without changing the conversation, lead, solution, or database layers.

## Website chat (portfolio)

`POST /api/chat/turn` with `{"session_id": "...", "message": "..."}` returns `{"reply": "..."}`.
The portfolio's chat box (`assets/marist-chat.js`) calls it. To switch it on:

1. Deploy this server and set these environment variables:
   - `ANTHROPIC_API_KEY` (required for live replies — without it the server tries a local Ollama model)
   - `ANTHROPIC_MODEL` (default `claude-haiku-5-5`)
   - `ALLOWED_ORIGINS` = the portfolio's address(es), comma separated
   - `DATABASE_URL` = a PostgreSQL URL (SQLite on Render is wiped on every redeploy)
   - `ADMIN_API_KEY` for the dashboard at `/admin/`
   - WhatsApp: `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_VERIFY_TOKEN`, and `WHATSAPP_APP_SECRET`
2. Put the server's URL in the portfolio's `assets/marist-chat.js` (`window.MARIST_API_URL`).

Each visitor can send `CHAT_RATE_LIMIT` messages per `CHAT_RATE_WINDOW_SECONDS` (default 20 per 10 minutes).
