from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def now(): return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    preferred_language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), default="AI_ACTIVE")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="conversation", cascade="all, delete-orphan")
    solutions = relationship("SolutionOpportunity", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    direction: Mapped[str] = mapped_column(String(16))
    message_type: Mapped[str] = mapped_column(String(32), default="text")
    content: Mapped[str] = mapped_column(Text)
    external_message_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    conversation = relationship("Conversation", back_populates="messages")

class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), default="NEW")
    priority: Mapped[str] = mapped_column(String(16), default="MEDIUM")
    industry: Mapped[str | None] = mapped_column(String(150), nullable=True)
    company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    contact_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    conversation = relationship("Conversation", back_populates="leads")

class SolutionOpportunity(Base):
    __tablename__ = "solution_opportunities"
    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    business_problem: Mapped[str] = mapped_column(Text)
    current_process: Mapped[str | None] = mapped_column(Text, nullable=True)
    proposed_solution: Mapped[str] = mapped_column(Text)
    solution_category: Mapped[str | None] = mapped_column(String(150), nullable=True)
    technologies: Mapped[str | None] = mapped_column(Text, nullable=True)
    business_benefits: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    conversation = relationship("Conversation", back_populates="solutions")
