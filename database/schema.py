from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    ticker: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    sector: Mapped[str] = mapped_column(String(100))


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    document_type: Mapped[str] = mapped_column(String(50), default="annual_report")
    filename: Mapped[str] = mapped_column(String(255))
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analysis"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    positive: Mapped[float] = mapped_column(Float, default=0.0)
    negative: Mapped[float] = mapped_column(Float, default=0.0)
    neutral: Mapped[float] = mapped_column(Float, default=0.0)
    polarity: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    ai_mentions: Mapped[int] = mapped_column(Integer, default=0)
    inflation_mentions: Mapped[int] = mapped_column(Integer, default=0)
    expansion_mentions: Mapped[int] = mapped_column(Integer, default=0)
    capex_mentions: Mapped[int] = mapped_column(Integer, default=0)
    risk_mentions: Mapped[int] = mapped_column(Integer, default=0)
