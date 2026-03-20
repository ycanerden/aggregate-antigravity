import json
import sys
from pathlib import Path

# Add backend directory to sys.path so we can run this directly if needed
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.connection import SessionLocal, init_db
from database.models import Investor

SEED_DATA = [
    {"name": "Y Combinator", "type": "accelerator", "portfolio_url": "https://www.ycombinator.com/companies", "location": "San Francisco, CA"},
    {"name": "Techstars", "type": "accelerator", "portfolio_url": "https://www.techstars.com/portfolio", "location": "Boulder, CO"},
    {"name": "500 Global", "type": "accelerator", "portfolio_url": "https://500.co/portfolio", "location": "San Francisco, CA"},
    {"name": "Sequoia Capital", "type": "vc", "portfolio_url": "https://www.sequoiacap.com/our-companies/", "location": "Menlo Park, CA"},
    {"name": "a16z", "type": "vc", "portfolio_url": "https://a16z.com/portfolio/", "location": "Menlo Park, CA"},
    {"name": "Accel", "type": "vc", "portfolio_url": "https://www.accel.com/portfolio", "location": "Palo Alto, CA"},
    {"name": "Benchmark", "type": "vc", "portfolio_url": "https://www.benchmark.com/portfolio", "location": "San Francisco, CA"},
    {"name": "First Round Capital", "type": "vc", "portfolio_url": "https://firstround.com/companies/", "location": "San Francisco, CA"},
    {"name": "Greylock", "type": "vc", "portfolio_url": "https://greylock.com/portfolio/", "location": "Menlo Park, CA"},
    {"name": "Lightspeed Venture Partners", "type": "vc", "portfolio_url": "https://lsvp.com/portfolio/", "location": "Menlo Park, CA"},
    {"name": "Founders Fund", "type": "vc", "portfolio_url": "https://foundersfund.com/portfolio/", "location": "San Francisco, CA"},
    {"name": "Bessemer Venture Partners", "type": "vc", "portfolio_url": "https://www.bvp.com/portfolio", "location": "San Francisco, CA"},
    {"name": "NEA", "type": "vc", "portfolio_url": "https://www.nea.com/portfolio", "location": "Menlo Park, CA"},
    {"name": "Index Ventures", "type": "vc", "portfolio_url": "https://www.indexventures.com/companies/", "location": "London, UK"},
    {"name": "GV (Google Ventures)", "type": "vc", "portfolio_url": "https://www.gv.com/portfolio/", "location": "Mountain View, CA"},
    {"name": "Kleiner Perkins", "type": "vc", "portfolio_url": "https://www.kleinerperkins.com/portfolio", "location": "Menlo Park, CA"},
    {"name": "Union Square Ventures", "type": "vc", "portfolio_url": "https://www.usv.com/portfolio/", "location": "New York, NY"},
    {"name": "Antler", "type": "accelerator", "portfolio_url": "https://www.antler.co/portfolio", "location": "Singapore"},
    {"name": "Entrepreneur First", "type": "accelerator", "portfolio_url": "https://www.joinef.com/companies/", "location": "London, UK"},
    {"name": "Plug and Play", "type": "accelerator", "portfolio_url": "https://www.plugandplaytechcenter.com/portfolio/", "location": "Sunnyvale, CA"}
]

def seed_db():
    init_db()
    db = SessionLocal()
    
    # Check if already seeded
    existing = db.query(Investor).count()
    if existing > 0:
        print(f"Database already contains {existing} investors. Skipping seed.")
        db.close()
        return

    added = 0
    for vc in SEED_DATA:
        investor = Investor(
            name=vc["name"],
            type=vc["type"],
            portfolio_url=vc["portfolio_url"],
            location=vc["location"],
        )
        db.add(investor)
        added += 1

    db.commit()
    print(f"Successfully seeded {added} investors.")
    db.close()

if __name__ == "__main__":
    seed_db()
