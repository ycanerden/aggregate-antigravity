from fastapi import FastAPI
from database.connection import init_db
from api.routes import router

app = FastAPI(title="VC & Accelerator Portfolio Aggregator")

from sqlite_utils import Database
import os

@app.on_event("startup")
def on_startup():
    init_db()
    # Enable FTS5
    db_path = os.getenv("DATABASE_URL", "sqlite:///backend/aggregator.db").replace("sqlite:///", "")
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
