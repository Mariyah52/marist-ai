from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.database import Base, engine
from app.models import User, Conversation, Message, Lead, SolutionOpportunity
from app.api.health import router as health_router
from app.api.voice import router as voice_router
from app.api.webhook import router as webhook_router
from app.api.admin import router as admin_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Marist AI Technology Consultant", version="0.1.0")
app.include_router(health_router)
app.include_router(voice_router)
app.include_router(webhook_router)
app.include_router(admin_router)
app.mount("/voice", StaticFiles(directory="web", html=True), name="voice")
app.mount("/admin", StaticFiles(directory="web", html=True), name="admin")

@app.get("/")
def root():
    return {"name":"Marist","description":"Imadi Technologies AI voice and WhatsApp consultant","status":"running"}
