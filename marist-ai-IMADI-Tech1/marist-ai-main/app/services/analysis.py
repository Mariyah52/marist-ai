import re
from app.models import Lead, SolutionOpportunity

BUSINESS_TERMS = re.compile(r"\b(need|want|business|company|automation|website|app|software|erp|crm|whatsapp|dashboard|inventory|orders|invoice|data|ai|problem|system|workflow|integrat|saas|bot|excel|manual|customer|process|sales|support|document|ocr|report|analytics)\b", re.I)
INDUSTRIES = ["logistics", "retail", "ecommerce", "healthcare", "education", "real estate", "finance", "manufacturing", "restaurant", "hospitality", "fulfilment"]
CATEGORIES = {
    "whatsapp": "WhatsApp Automation", "erp": "ERP / Business Management", "crm": "CRM / Customer Management",
    "automation": "Business Automation", "website": "Custom Web Application", "app": "Custom Application",
    "software": "Custom Software", "saas": "SaaS / Digital Product", "ai": "AI Solution", "data": "Data / Analytics",
    "excel": "Workflow Automation", "manual": "Workflow Automation", "invoice": "Finance / Invoicing Automation",
    "inventory": "Inventory Management", "orders": "Order Management", "document": "AI Document Processing",
    "ocr": "AI Document Processing", "report": "Reporting & Insights"
}

def is_business_opportunity(text: str) -> bool:
    return bool(BUSINESS_TERMS.search(text or ""))

def infer_category(text: str) -> str | None:
    lower = (text or "").lower()
    hits = [(term, category) for term, category in CATEGORIES.items() if term in lower]
    return hits[0][1] if hits else None

def infer_industry(text: str) -> str | None:
    lower = (text or "").lower()
    return next((i.title() for i in INDUSTRIES if i in lower), None)

def save_opportunity(db, conversation, user_text, reply):
    if not is_business_opportunity(user_text):
        return None
    lead = db.query(Lead).filter(Lead.conversation_id == conversation.id).first()
    if not lead:
        lead = Lead(conversation_id=conversation.id, status="QUALIFYING", priority="MEDIUM")
        db.add(lead)
    lead.industry = lead.industry or infer_industry(user_text)
    category = infer_category(user_text)
    lower = user_text.lower()
    if any(x in lower for x in ["urgent", "asap", "hundreds", "thousands", "daily"]):
        lead.priority = "HIGH"
    solution_text = reply if reply else "Marist identified a potential technology opportunity; human review is required."
    solution = SolutionOpportunity(
        conversation_id=conversation.id,
        business_problem=user_text[:5000],
        current_process=user_text[:5000],
        proposed_solution=solution_text[:10000],
        solution_category=category,
        technologies=None,
        business_benefits=None,
        confidence=65 if category else 40,
    )
    db.add(solution)
    return lead
