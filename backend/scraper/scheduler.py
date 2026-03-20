from apscheduler.schedulers.background import BackgroundScheduler
from api.routes import run_scrape_task
from database.connection import SessionLocal
from database.models import Investor
import asyncio

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    def scrape_all():
        db = SessionLocal()
        investors = db.query(Investor).all()
        for inv in investors:
            asyncio.run(run_scrape_task(inv.id))
        db.close()
        
    # Run once a week at midnight Sunday
    scheduler.add_job(scrape_all, 'cron', day_of_week='sun', hour=0, minute=0)
    scheduler.start()
