from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.services.conversation import get_or_create_conversation, recent_history
from app.services.ai import generate_reply
from app.services.analysis import save_opportunity
from app.services.whatsapp import send_text
from app.models import Message
from app.services.language import detect_language

router = APIRouter(tags=["whatsapp"])

@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == settings.whatsapp_verify_token and challenge:
        return int(challenge)
    raise HTTPException(status_code=403, detail="Forbidden")

@router.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    try:
        value = data["entry"][0]["changes"][0]["value"]
        msg = value["messages"][0]
        if msg.get("type") != "text": return {"status":"ignored"}
        external_id = msg.get("id")
        if external_id and db.query(Message).filter(Message.external_message_id == external_id).first():
            return {"status":"duplicate"}
        phone = msg["from"]
        text = msg["text"]["body"]
        language = detect_language(text)
        user, conversation = get_or_create_conversation(db, phone)
        user.preferred_language = language
        db.add(Message(conversation_id=conversation.id, direction="inbound", content=text, external_message_id=external_id, language=language))
        db.flush()
        reply = generate_reply(recent_history(db, conversation.id))
        db.add(Message(conversation_id=conversation.id, direction="outbound", content=reply, ai_generated=True, language=language))
        save_opportunity(db, conversation, text, reply)
        db.commit()
        send_text(phone, reply)
        return {"status":"ok"}
    except (KeyError, IndexError, TypeError):
        return {"status":"ignored"}
