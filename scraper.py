import requests
from bs4 import BeautifulSoup
import datetime
import os
from supabase import create_client

# Configuration : récupérer les clés depuis GitHub Secrets
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def scrape_scholarshipportal():
    url = "https://www.scholarshipportal.com/scholarships"
    r = requests.get(url, headers={"User-Agent": "ZenithCapBot/1.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for item in soup.select("a[href*='/scholarship/']")[:5]:  # limite 5 résultats
        title = item.get_text(strip=True)
        link = "https://www.scholarshipportal.com" + item["href"]
        results.append({
            "title": title,
            "application_link": link,
            "deadline": None,
            "country": None,
            "level": None,
            "source": "ScholarshipPortal",
            "verified": False,
            "fetched_at": datetime.datetime.utcnow().isoformat()
        })
    return results

if __name__ == "__main__":
    data = scrape_scholarshipportal()
    for d in data:
        supabase.table("scholarships").insert(d).execute()
    print(f"{len(data)} bourses ajoutées à Supabase.")
