"""
Module: scanner.py
Description: Official Google API Search (Fixes Cloud Blocking)
"""
import requests
import streamlit as st

def google_search_api(query, num_results=5):
    # Check if Secrets exist
    if "GOOGLE_API_KEY" not in st.secrets or "GOOGLE_CX" not in st.secrets:
        print("[!] ERROR: Missing Google API Secrets!")
        return []

    api_key = st.secrets["GOOGLE_API_KEY"]
    cx = st.secrets["GOOGLE_CX"]
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': api_key, 'cx': cx, 'q': query, 'num': num_results}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'items' in data:
            return data['items']
    except Exception as e:
        print(f"[!] API Error: {e}")
    return []

def find_business_url(name, location):
    query = f"{name} {location} official website"
    results = google_search_api(query)
    
    skip = ['facebook', 'instagram', 'linkedin', 'wikipedia', 'yelp']
    for r in results:
        link = r.get('link', '')
        if not any(x in link for x in skip):
            return link
    return None

def find_competitors(industry, location, user_domain, limit=3):
    query = f"top rated {industry} in {location}"
    competitors = []
    results = google_search_api(query, num_results=10)
    
    skip = ['yelp', 'facebook', 'instagram', 'linkedin', 'tripadvisor']
    for r in results:
        link = r.get('link', '')
        title = r.get('title', 'Unknown')
        
        if user_domain in link: continue
        if any(x in link for x in skip): continue
        
        competitors.append({"name": title, "url": link})
        if len(competitors) >= limit: break
            
    return competitors