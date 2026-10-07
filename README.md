# Marist — Imadi Technologies AI Technology Consultant

Marist is being rebuilt as a multilingual AI consultant for Imadi Technologies. The first foundation supports:

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

Marist is an Imadi Technologies AI technology consultant foundation. It supports persistent conversations, multilingual language tagging, AI responses, business-opportunity detection, lead records, proposed-solution records, WhatsApp webhook handling, a browser voice MVP, and a protected admin dashboard.

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
