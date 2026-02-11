"""
Module: scanner.py
Description: Serper.dev API (Web & Places Edition)
"""
import requests
import json
import streamlit as st

# --- 1. CORE SEARCH FUNCTIONS ---

def serper_search(query, num_results=5):
    """
    Standard Web Search (Articles, Blogs, Homepages)
    """
    if "SERPER_API_KEY" not in st.secrets:
        return []
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "num": num_results})
    headers = {'X-API-KEY': st.secrets["SERPER_API_KEY"], 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=payload)
        return response.json().get('organic', [])
    except:
        return []

def serper_places(query, num_results=5):
    """
    [NEW] Places Search (Google Maps Data)
    Returns actual businesses, not blog posts.
    """
    if "SERPER_API_KEY" not in st.secrets:
        return []
    url = "https://google.serper.dev/places"
    payload = json.dumps({"q": query, "num": num_results})
    headers = {'X-API-KEY': st.secrets["SERPER_API_KEY"], 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=payload)
        # Places results are in the 'places' key
        return response.json().get('places', [])
    except:
        return []

# --- 2. BUSINESS LOCATORS ---

def find_business_url(name, location):
    query = f"{name} {location} official website"
    results = serper_search(query)
    
    # Sites to ignore (Directories/Socials)
    skip = [
        'facebook', 'instagram', 'linkedin', 'yelp', 'tripadvisor', 
        'youtube', 'tiktok', 'wikipedia', 'glassdoor', 'agoda', 'booking.com'
    ]
    
    for r in results:
        link = r.get('link', '')
        # Return the first link that isn't a social media site
        if not any(x in link for x in skip):
            return link
    return None

def find_social_links(name, location):
    query = f"{name} {location} social media profile"
    results = serper_search(query, num_results=10)
    socials = {}
    targets = {
        "facebook.com": "Facebook",
        "instagram.com": "Instagram", 
        "linkedin.com": "LinkedIn",
        "twitter.com": "X (Twitter)",
        "tiktok.com": "TikTok",
        "youtube.com": "YouTube"
    }
    
    for r in results:
        link = r.get('link', '')
        for domain, platform in targets.items():
            if domain in link and platform not in socials:
                socials[platform] = link
    return socials

# --- 3. COMPETITOR FINDER (The Fix) ---

def find_competitors(industry, location, user_domain):
    """
    Uses the Places API to find real business entities.
    """
    # Query: "Casino Hotels in Quezon City"
    query = f"{industry} in {location}"
    print(f"[*] Searching Places for: {query}")
    
    places = serper_places(query, num_results=10)
    competitors = []
    
    for p in places:
        name = p.get('title', 'Unknown')
        website = p.get('website') # Places API returns a 'website' field!
        
        # 1. Skip if no website (we can't scan them)
        if not website: 
            continue
            
        # 2. Skip if it's the user's own business (fuzzy match)
        if user_domain in website or name.lower() in user_domain:
            continue
            
        # 3. Skip duplicates
        if any(c['url'] == website for c in competitors):
            continue

        competitors.append({"name": name, "url": website})
        
        # Stop after 3 good matches
        if len(competitors) >= 3: 
            break
            
    return competitors