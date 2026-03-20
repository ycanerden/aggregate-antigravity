import datetime
from sqlalchemy.orm import Session
from thefuzz import fuzz
from slugify import slugify
from database.models import Company, Investment, Investor, ScrapeLog

def normalize_and_save(db: Session, investor_id: int, extracted_data: list, log: ScrapeLog):
    investor = db.query(Investor).filter(Investor.id == investor_id).first()
    if not investor: return

    existing = db.query(Company).all()
    new_c, up_c = 0, 0

    for item in extracted_data:
        name = item.get("name", "").strip()
        if not name: continue
        website = item.get("website_url", "")
        
        matched = next((c for c in existing if c.website and c.website == website), None) if website else None
        if not matched:
            for c in existing:
                if fuzz.ratio(c.name.lower(), name.lower()) > 90:
                    matched = c; break
                    
        if not matched:
            slug_base = slugify(name)
            slug = slug_base
            c_idx = 1
            while next((c for c in existing if c.slug == slug), None):
                slug = f"{slug_base}-{c_idx}"; c_idx += 1
                
            matched = Company(name=name, slug=slug, website=website, description=item.get("description"), sector=item.get("sector"), stage=item.get("stage"), location=item.get("location"), status=item.get("status", "active"), logo_url=item.get("logo_url"))
            db.add(matched)
            db.flush()
            existing.append(matched)
            new_c += 1
        else:
            for k in ["description", "website", "sector", "stage", "location", "status", "logo_url"]:
                if item.get(k) and not getattr(matched, k): setattr(matched, k, item.get(k))
            up_c += 1
            
        inv = db.query(Investment).filter(Investment.investor_id == investor.id, Investment.company_id == matched.id).first()
        if not inv:
            inv = Investment(investor_id=investor.id, company_id=matched.id, round_type=item.get("stage"), source_url=investor.portfolio_url)
            db.add(inv)
        else:
            inv.last_confirmed_at = datetime.datetime.utcnow()

    log.companies_found = len(extracted_data)
    log.companies_new = new_c
    log.companies_updated = up_c
    log.status = "success"
    log.finished_at = datetime.datetime.utcnow()
    investor.last_scraped_at = datetime.datetime.utcnow()
    investor.scrape_status = "success"
    db.commit()
    return log
