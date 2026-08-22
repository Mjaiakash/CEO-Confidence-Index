from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    ticker: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    sector: Mapped[str | None] = mapped_column(String(200), nullable=True)


class Report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    year: Mapped[int] = mapped_column(index=True)
    report_type: Mapped[str] = mapped_column(String(100), default="annual_report")
    file_name: Mapped[str] = mapped_column(String(500), unique=True)
    extracted_text_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="downloaded")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analysis"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), unique=True, index=True)
    sentiment_label: Mapped[str] = mapped_column(String(30))
    sentiment_score: Mapped[float] = mapped_column(Float)
    positive_score: Mapped[float] = mapped_column(Float, default=0.0)
    negative_score: Mapped[float] = mapped_column(Float, default=0.0)
    ai_mentions: Mapped[int] = mapped_column(Integer, default=0)
    inflation_mentions: Mapped[int] = mapped_column(Integer, default=0)
    expansion_mentions: Mapped[int] = mapped_column(Integer, default=0)
    capex_mentions: Mapped[int] = mapped_column(Integer, default=0)
    risk_mentions: Mapped[int] = mapped_column(Integer, default=0)
    confidence_score: Mapped[float] = mapped_column(Float)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


def initialize_database(engine):
    Base.metadata.create_all(engine)
