from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User, Conversation, Message

def get_or_create_conversation(db: Session, phone: str):
    user = db.scalar(select(User).where(User.phone_number == phone))
    if not user:
        user = User(phone_number=phone)
        db.add(user); db.flush()
    conversation = db.scalar(select(Conversation).where(Conversation.user_id == user.id, Conversation.status != "CLOSED").order_by(Conversation.updated_at.desc()))
    if not conversation:
        conversation = Conversation(user_id=user.id)
        db.add(conversation); db.flush()
    return user, conversation

def recent_history(db: Session, conversation_id: int, limit=12):
    rows = db.scalars(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.desc()).limit(limit)).all()
    rows.reverse()
    return [{"role": "user" if m.direction == "inbound" else "assistant", "content": m.content} for m in rows]
