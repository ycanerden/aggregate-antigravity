import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from database.connection import SessionLocal
from database.models import Company, Investment, Investor, ScrapeLog
from scraper.normalizer import normalize_and_save

def add_dummies():
    db = SessionLocal()
    
    antler = db.query(Investor).filter(Investor.name == "Antler").first()
    yc = db.query(Investor).filter(Investor.name == "Y Combinator").first()
    sequoia = db.query(Investor).filter(Investor.name == "Sequoia Capital").first()
    
    if not antler or not yc or not sequoia:
        print("Seed investors not found.")
        return

    yc_c = [{"name": "Stripe", "website_url": "https://stripe.com", "description": "Payment processing software", "sector": "fintech", "stage": "ipo", "location": "San Francisco", "founded_year": 2010, "status": "active"}, {"name": "Airbnb", "website_url": "https://airbnb.com", "description": "Vacation rentals", "sector": "marketplace", "stage": "ipo", "location": "San Francisco", "founded_year": 2008, "status": "active"}, {"name": "Brex", "website_url": "https://brex.com", "description": "Corporate cards for startups", "sector": "fintech", "stage": "growth", "location": "San Francisco", "founded_year": 2017, "status": "active"}]
    seq_c = [{"name": "Stripe", "website_url": "https://stripe.com", "description": "Payment processing software", "sector": "fintech", "stage": "ipo", "location": "San Francisco", "founded_year": 2010, "status": "active"}, {"name": "Linear", "website_url": "https://linear.app", "description": "Issue tracking tool", "sector": "saas", "stage": "series-b", "location": "San Francisco", "founded_year": 2019, "status": "active"}, {"name": "Vercel", "website_url": "https://vercel.com", "description": "Frontend hosting platform", "sector": "devtools", "stage": "series-d", "location": "San Francisco", "founded_year": 2015, "status": "active"}]
    ant_c = [{"name": "Scribe", "website_url": "https://scribe.com", "description": "AI documentation", "sector": "ai", "stage": "seed", "location": "New York", "founded_year": 2022, "status": "active"}]
    
    l1 = ScrapeLog(investor_id=yc.id, status="started")
    db.add(l1)
    normalize_and_save(db, yc.id, yc_c, l1)
    
    l2 = ScrapeLog(investor_id=sequoia.id, status="started")
    db.add(l2)
    normalize_and_save(db, sequoia.id, seq_c, l2)
    
    l3 = ScrapeLog(investor_id=antler.id, status="started")
    db.add(l3)
    normalize_and_save(db, antler.id, ant_c, l3)
    
    print("Dummy startup data seeded!")

if __name__ == "__main__":
    add_dummies()
