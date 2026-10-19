from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ratelimit import check_rate_limit
from app.models import Message
from app.services.ai import generate_reply
from app.services.analysis import save_opportunity
from app.services.conversation import get_or_create_conversation, recent_history
from app.services.language import detect_language

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatTurn(BaseModel):
    session_id: str = Field(min_length=8, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    message: str = Field(min_length=1, max_length=1000)


@router.post("/turn")
def chat_turn(payload: ChatTurn, request: Request, db: Session = Depends(get_db)):
    """Text chat for the website chat box. Same brain as WhatsApp and voice."""
    check_rate_limit(request)
    text = payload.message.strip()
    user, conversation = get_or_create_conversation(db, f"web:{payload.session_id}")
    language = detect_language(text)
    user.preferred_language = language
    db.add(Message(conversation_id=conversation.id, direction="inbound", message_type="web", content=text, language=language))
    db.flush()
    reply = generate_reply(recent_history(db, conversation.id))
    db.add(Message(conversation_id=conversation.id, direction="outbound", message_type="web", content=reply, ai_generated=True, language=language))
    save_opportunity(db, conversation, text, reply)
    db.commit()
    return {"reply": reply}
