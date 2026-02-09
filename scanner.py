"""
Module: scanner.py
Description: Hybrid OSINT Engine (DuckDuckGo + Google Backup)
"""
from duckduckgo_search import DDGS
try:
    from googlesearch import search as google_search
except ImportError:
    google_search = None
import time

def find_business_url(name, location):
    """
    Finds the official website using a Hybrid approach (DDG -> Google).
    """
    query = f"{name} {location} official website"
    print(f"[*] Radar: Searching for {query}...")
    
    # List of sites to IGNORE (The "Noise" Filter)
    skip_list = [
        'facebook.com', 'instagram.com', 'linkedin.com', 
        'wikipedia.org', 'yelp.com', 'tripadvisor.com', 
        'yellowpages.com', 'youtube.com', 'tiktok.com',
        'glassdoor.com', 'bloomberg.com', 'crunchbase.com'
    ]

    # --- ATTEMPT 1: DUCKDUCKGO ---
    try:
        print("[*] Trying DuckDuckGo...")
        results = DDGS().text(query, max_results=5)
        if results:
            for r in results:
                url = r['href']
                if not any(skip in url for skip in skip_list):
                    return url
    except Exception as e:
        print(f"[!] DDG Failed: {e}")

    # --- ATTEMPT 2: GOOGLE (BACKUP) ---
    if google_search:
        try:
            print("[*] DDG failed/blocked. Switching to Google Backup...")
            # Google search yields URLs directly
            for url in google_search(query, num_results=5):
                if not any(skip in url for skip in skip_list):
                    return url
        except Exception as e:
            print(f"[!] Google Backup Failed: {e}")

    return None

def find_competitors(industry, location, user_domain, limit=3):
    """
    Automated Market Radar: Finds top competitors using Hybrid Search.
    """
    query = f"top rated {industry} in {location}"
    competitors = []
    
    # Common filters for competitor search
    skip_list = ['yelp', 'yellowpages', 'facebook', 'instagram', 'linkedin', 'tripadvisor', 'wikipedia']

    # --- ATTEMPT 1: DUCKDUCKGO ---
    try:
        results = DDGS().text(query, max_results=10)
        for r in results:
            url = r['href']
            title = r['title']
            
            if user_domain in url: continue
            if any(x in url for x in skip_list): continue
                
            competitors.append({"name": title, "url": url})
            if len(competitors) >= limit: return competitors
            
    except Exception as e:
        print(f"[!] DDG Competitor Scan Error: {e}")

    # --- ATTEMPT 2: GOOGLE (BACKUP) ---
    # Note: google_search only returns URLs, not Titles, so we guess the title from the URL
    if not competitors and google_search:
        try:
            for url in google_search(query, num_results=10):
                if user_domain in url: continue
                if any(x in url for x in skip_list): continue
                
                # Create a pretty name from the domain (e.g., www.smile.com -> Smile)
                name = url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0].title()
                
                competitors.append({"name": name, "url": url})
                if len(competitors) >= limit: return competitors
        except Exception as e:
            print(f"[!] Google Competitor Scan Error: {e}")

    return competitors