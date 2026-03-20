from fastapi import FastAPI
from database.connection import init_db
from api.routes import router

app = FastAPI(title="VC & Accelerator Portfolio Aggregator")

from sqlite_utils import Database
import os
from database.seed_sources import seed_db

@app.on_event("startup")
def on_startup():
    init_db()
    
    # Automatically seed the investors table if it's empty on a fresh deployment
    try:
        seed_db()
    except Exception as e:
        print("Seed error:", e)

    # Enable FTS5
    db_path = os.getenv("DATABASE_URL", "sqlite:///aggregator.db").replace("sqlite:///", "")
    if db_path.startswith("./"):
        db_path = db_path[2:]

    try:
        db = Database(db_path)
        if "companies_fts" not in db.table_names():
            db["companies"].enable_fts(["name", "description", "sector"], create_triggers=True)
    except Exception as e:
        print("FTS init error:", e)

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "VC Aggregator API running"}
