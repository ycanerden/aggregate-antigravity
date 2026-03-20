from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    slug: str
    website: Optional[str] = None
    description: Optional[str] = None
    sector: Optional[str] = None
    stage: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    logo_url: Optional[str] = None

class CompanyRes(CompanyBase):
    id: int
    model_config = {"from_attributes": True}

class InvestorBase(BaseModel):
    name: str
    type: str
    website: Optional[str] = None
    portfolio_url: str
    location: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None

class InvestorRes(InvestorBase):
    id: int
    last_scraped_at: Optional[datetime] = None
    scrape_status: Optional[str] = None
    model_config = {"from_attributes": True}
