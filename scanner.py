"""
Module: scanner.py
Description: OSINT Discovery Engine with Smart Filtering
"""
from duckduckgo_search import DDGS
import time

def find_business_url(name, location):
    """
    Finds the official website, skipping Social Media and Wikipedia.
    """
    # Broader query works better than "official site" sometimes
    query = f"{name} {location} official website"
    print(f"[*] Radar: Searching for {query}...")
    
    # List of sites to IGNORE (The "Noise" Filter)
    skip_list = [
        'facebook.com', 'instagram.com', 'linkedin.com', 
        'wikipedia.org', 'yelp.com', 'tripadvisor.com', 
        'yellowpages.com', 'youtube.com', 'tiktok.com',
        'glassdoor.com', 'bloomberg.com'
    ]
    
    try:
        # Get top 5 results to look through
        results = DDGS().text(query, max_results=5)
        
        if results:
            for r in results:
                url = r['href']
                # If the URL does NOT contain any word from our skip list, it's likely the real site
                if not any(skip in url for skip in skip_list):
                    print(f"[*] Found valid site: {url}")
                    return url
                    
            # If we looped through all 5 and they were ALL social media, return the first one as a backup
            # (Or return None if you prefer strict mode)
            print("[!] Only found social/directory links.")
            return None
            
    except Exception as e:
        print(f"[!] Radar Error: {e}")
    return None

def find_competitors(industry, location, user_domain, limit=2):
    """
    Automated Market Radar: Finds top competitors in the area.
    """
    query = f"top rated {industry} in {location}"
    print(f"[*] Radar: Scanning market for '{query}'...")
    
    competitors = []
    try:
        # Fetch more results to filter effectively
        results = DDGS().text(query, max_results=10)
        
        for r in results:
            url = r['href']
            title = r['title']
            
            # FILTERS:
            # 1. Skip the user's own website
            if user_domain in url:
                continue
            # 2. Skip directory sites (Reuse the skip logic if needed, but simplified here)
            skip_list = ['yelp', 'yellowpages', 'facebook', 'instagram', 'linkedin', 'tripadvisor', 'wikipedia']
            if any(x in url for x in skip_list):
                continue
                
            competitors.append({"name": title, "url": url})
            
            if len(competitors) >= limit:
                break
                
    except Exception as e:
        print(f"[!] Competitor Scan Error: {e}")
        
    return competitors