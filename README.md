# VC & Accelerator Portfolio Aggregator

A full-stack web application that fetches, normalizes, and aggregates startup portfolio data from VC firms into a single searchable SQLite database.

## Architecture
- **Backend**: FastAPI + SQLite (FTS5 enabled) + Playwright + Claude-3.5-Sonnet
- **Frontend**: Next.js 14 App Router + Tailwind CSS + shadcn/ui
- **Scheduler**: APScheduler running weekly

## Local Development
1. **Backend**:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
    python database/seed_sources.py
    python dummy_seed_companies.py # Run to seed UI locally
    uvicorn main:app --reload
    ```
2. **Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## Docker Deployment

To deploy this using Docker Compose:

1. Create a `.env` file containing `ANTHROPIC_API_KEY=your_key_here`.
2. Run `docker compose up --build -d`.

### `docker-compose.yml` example

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./backend/aggregator.db:/app/aggregator.db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api
```
