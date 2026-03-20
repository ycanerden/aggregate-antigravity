from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "vc" | "accelerator" | "angel" | "corporate"
    website = Column(String)
    portfolio_url = Column(String, nullable=False)
    logo_url = Column(String)
    description = Column(String)
    location = Column(String)
    
    last_scraped_at = Column(DateTime)
    scrape_status = Column(String, default='pending')  # pending | success | failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to investments
    investments = relationship("Investment", back_populates="investor")
    logs = relationship("ScrapeLog", back_populates="investor")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    website = Column(String)
    description = Column(String)
    long_description = Column(String)
    sector = Column(String)
    stage = Column(String)
    founded_year = Column(Integer)
    location = Column(String)
    employee_count = Column(String)
    logo_url = Column(String)
    status = Column(String, default='active')  # active | acquired | dead | ipo
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to investments
    investments = relationship("Investment", back_populates="company")


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    investment_date = Column(String)
    round_type = Column(String)
    amount = Column(String)
    is_lead = Column(Boolean, default=False)
    source_url = Column(String)
    first_seen_at = Column(DateTime, default=datetime.utcnow)
    last_confirmed_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('investor_id', 'company_id', 'round_type', name='uq_investment'),
    )

    investor = relationship("Investor", back_populates="investments")
    company = relationship("Company", back_populates="investments")


class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    investor_id = Column(Integer, ForeignKey("investors.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    status = Column(String)  # success | failed | partial
    companies_found = Column(Integer, default=0)
    companies_new = Column(Integer, default=0)
    companies_updated = Column(Integer, default=0)
    error_message = Column(String)

    investor = relationship("Investor", back_populates="logs")
