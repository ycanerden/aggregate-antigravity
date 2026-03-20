import asyncio
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from database.models import Company, Investor, ScrapeLog
from api.schemas import CompanyRes, InvestorRes
from scraper.engine import fetch_portfolio_html
from scraper.extractor import extract_companies_from_html
from scraper.normalizer import normalize_and_save

router = APIRouter()

@router.get("/api/companies", response_model=List[CompanyRes])
def get_companies(
    q: str = Query(None),
    sector: str = Query(None),
    stage: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Company)
    if q:
        # FTS5 match
        query = query.filter(Company.id.in_(
            db.query(Company.id).from_statement(db.text("SELECT rowid as id FROM companies_fts WHERE companies_fts MATCH :q")).params(q=f"{q}*")
        ))
    if sector:
        query = query.filter(Company.sector == sector)
    if stage:
        query = query.filter(Company.stage == stage)
    return query.limit(50).all()

@router.get("/api/companies/{slug}", response_model=CompanyRes)
def get_company_by_slug(slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == slug).first()
    if not company: raise HTTPException(status_code=404, detail="Not found")
    return company

@router.get("/api/investors", response_model=List[InvestorRes])
def get_investors(db: Session = Depends(get_db)):
    return db.query(Investor).all()

async def run_scrape_task(investor_id: int):
    db = next(get_db())
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor: return
    log = ScrapeLog(investor_id=investor.id, status="started")
    db.add(log)
    db.commit()
    try:
        html = await fetch_portfolio_html(investor.portfolio_url)
        extracted = extract_companies_from_html(html)
        normalize_and_save(db, investor.id, extracted, log)
    except Exception as e:
        log.status = "failed"
        log.error_message = str(e)
        investor.scrape_status = "failed"
        db.commit()

@router.post("/api/scrape/{investor_id}")
def scrape_investor(investor_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(run_scrape_task, investor_id)
    return {"message": f"Scrape initiated for investor {investor_id}"}

@router.get("/api/logs")
def get_scrape_logs(db: Session = Depends(get_db)):
    return db.query(ScrapeLog).order_by(ScrapeLog.id.desc()).limit(20).all()
