from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from app.core.ratelimit import check_rate_limit
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.conversation import get_or_create_conversation, recent_history
from app.services.ai import generate_reply
from app.services.analysis import save_opportunity
from app.models import Message
from app.services.language import detect_language

router = APIRouter(prefix="/api/voice", tags=["voice"])
class VoiceTurn(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    transcript: str = Field(min_length=1, max_length=1000)

@router.post("/turn")
def voice_turn(payload: VoiceTurn, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request)
    user, conversation = get_or_create_conversation(db, f"web:{payload.session_id}")
    language = detect_language(payload.transcript)
    user.preferred_language = language
    db.add(Message(conversation_id=conversation.id, direction="inbound", message_type="voice", content=payload.transcript, language=language))
    db.flush()
    history = recent_history(db, conversation.id)
    reply = generate_reply(history)
    db.add(Message(conversation_id=conversation.id, direction="outbound", message_type="voice", content=reply, ai_generated=True, language=language))
    save_opportunity(db, conversation, payload.transcript, reply)
    db.commit()
    return {"reply": reply, "conversation_id": conversation.id}
