"""
Module: scanner.py
Description: Serper.dev API with Social Media OSINT
"""
import requests
import json
import streamlit as st

def serper_search(query, num_results=5):
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

def find_business_url(name, location):
    query = f"{name} {location} official website"
    results = serper_search(query)
    skip = ['facebook', 'instagram', 'linkedin', 'yelp', 'tripadvisor', 'youtube', 'tiktok']
    for r in results:
        link = r.get('link', '')
        if not any(x in link for x in skip):
            return link
    return None

def find_social_links(name, location):
    """
    New: specifically hunts for social footprints.
    """
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

def find_competitors(industry, location, user_domain):
    query = f"top rated {industry} in {location}"
    competitors = []
    results = serper_search(query, num_results=8)
    skip = ['yelp', 'tripadvisor', 'facebook', 'linkedin']
    
    for r in results:
        link = r.get('link', '')
        title = r.get('title', 'Unknown')
        if user_domain in link or any(x in link for x in skip): continue
        competitors.append({"name": title, "url": link})
        if len(competitors) >= 3: break
    return competitors