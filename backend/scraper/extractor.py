import json
import anthropic
from config import ANTHROPIC_API_KEY
from bs4 import BeautifulSoup

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a data extraction engine. You will receive HTML from a vc or accelerator portfolio page.
Extract ALL companies/startups listed on this page into a JSON array.
Fields:
- name (required)
- website_url
- description
- sector
- stage
- location
- founded_year
- logo_url
- status (active, acquired, dead, ipo)

Rules:
- Return ONLY valid JSON array. No markdown wraps like ```json
- Omit fields if not available
- Normalize empty/none to string where possible or just omit
"""

def extract_companies_from_html(html_content: str) -> list:
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style", "svg", "nav", "footer"]):
        script.decompose()
    clean_html = str(soup)

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": clean_html}]
        )
        txt = response.content[0].text.strip()
        if txt.startswith("```json"): txt = txt[7:]
        if txt.endswith("```"): txt = txt[:-3]
        return json.loads(txt.strip())
    except Exception as e:
        print(f"Extraction error: {e}")
        raise e
