from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models import User, Conversation, Message, Lead, SolutionOpportunity

router = APIRouter(prefix="/api/admin", tags=["admin"])

def require_admin(x_admin_key: str | None = Header(default=None)):
    if not settings.admin_api_key or x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

def auth(x_admin_key: str | None = Header(default=None)):
    require_admin(x_admin_key)

def serialize_lead(db, lead):
    conversation = db.get(Conversation, lead.conversation_id)
    user = db.get(User, conversation.user_id) if conversation else None
    latest = db.scalar(select(Message).where(Message.conversation_id == lead.conversation_id).order_by(Message.created_at.desc()))
    return {"id": lead.id, "status": lead.status, "priority": lead.priority, "industry": lead.industry, "company": lead.company,
            "contact_name": lead.contact_name or (user.name if user else None), "phone": user.phone_number if user else None,
            "conversation_id": lead.conversation_id, "last_message": latest.content[:300] if latest else None,
            "created_at": lead.created_at.isoformat()}

@router.get("/stats", dependencies=[Depends(auth)])
def stats(db: Session = Depends(get_db)):
    return {"users": db.scalar(select(func.count(User.id))) or 0,
            "conversations": db.scalar(select(func.count(Conversation.id))) or 0,
            "messages": db.scalar(select(func.count(Message.id))) or 0,
            "leads": db.scalar(select(func.count(Lead.id))) or 0,
            "solutions": db.scalar(select(func.count(SolutionOpportunity.id))) or 0,
            "qualified_leads": db.scalar(select(func.count(Lead.id)).where(Lead.status.in_(["QUALIFIED", "HUMAN_REVIEW"]))) or 0}

@router.get("/leads", dependencies=[Depends(auth)])
def leads(db: Session = Depends(get_db), limit: int = 100):
    rows = db.scalars(select(Lead).order_by(Lead.created_at.desc()).limit(min(limit, 500))).all()
    return [serialize_lead(db, lead) for lead in rows]

@router.get("/conversations/{conversation_id}", dependencies=[Depends(auth)])
def conversation(conversation_id: int, db: Session = Depends(get_db)):
    conv = db.get(Conversation, conversation_id)
    if not conv: raise HTTPException(404, "Conversation not found")
    user = db.get(User, conv.user_id)
    messages = db.scalars(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())).all()
    solutions = db.scalars(select(SolutionOpportunity).where(SolutionOpportunity.conversation_id == conv.id).order_by(SolutionOpportunity.created_at.desc())).all()
    return {"conversation": {"id": conv.id, "status": conv.status, "summary": conv.summary, "user": {"phone": user.phone_number, "name": user.name, "language": user.preferred_language}},
            "messages": [{"id": m.id, "direction": m.direction, "type": m.message_type, "content": m.content, "created_at": m.created_at.isoformat()} for m in messages],
            "solutions": [{"id": s.id, "problem": s.business_problem, "solution": s.proposed_solution, "category": s.solution_category, "confidence": s.confidence, "created_at": s.created_at.isoformat()} for s in solutions]}

@router.get("/solutions", dependencies=[Depends(auth)])
def solutions(db: Session = Depends(get_db), limit: int = 100):
    rows = db.scalars(select(SolutionOpportunity).order_by(SolutionOpportunity.created_at.desc()).limit(min(limit, 500))).all()
    return [{"id": s.id, "conversation_id": s.conversation_id, "problem": s.business_problem, "current_process": s.current_process, "solution": s.proposed_solution, "category": s.solution_category, "technologies": s.technologies, "benefits": s.business_benefits, "confidence": s.confidence, "created_at": s.created_at.isoformat()} for s in rows]

@router.get("/analytics", dependencies=[Depends(auth)])
def analytics(db: Session = Depends(get_db)):
    from sqlalchemy import case
    categories = db.execute(select(SolutionOpportunity.solution_category, func.count(SolutionOpportunity.id)).group_by(SolutionOpportunity.solution_category).order_by(func.count(SolutionOpportunity.id).desc())).all()
    priorities = db.execute(select(Lead.priority, func.count(Lead.id)).group_by(Lead.priority)).all()
    statuses = db.execute(select(Lead.status, func.count(Lead.id)).group_by(Lead.status)).all()
    return {"solution_categories": [{"name": k or "Uncategorized", "count": v} for k, v in categories],
            "lead_priorities": [{"name": k, "count": v} for k, v in priorities],
            "lead_statuses": [{"name": k, "count": v} for k, v in statuses]}
