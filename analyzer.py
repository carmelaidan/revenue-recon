"""
Module: analyzer.py
Description: SEO & Tech Analyzer with Anti-Blocking Headers
"""
import requests
from bs4 import BeautifulSoup

def get_headers():
    # This makes the request look like a real Chrome browser
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

def check_ssl(url):
    try:
        response = requests.get(url, headers=get_headers(), timeout=5)
        return True # If we can connect, SSL is likely working (requests fails on bad SSL by default)
    except:
        return False

def check_seo(url):
    seo_data = {"title": None, "description": None}
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if soup.title:
            seo_data["title"] = soup.title.string.strip()
            
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            seo_data["description"] = meta_desc.get("content").strip()
            
    except Exception as e:
        print(f"SEO Check Error: {e}")
        
    return seo_data

def detect_tech_stack(url):
    tech_stack = []
    try:
        response = requests.get(url, headers=get_headers(), timeout=5)
        text = response.text.lower()
        headers = str(response.headers).lower()
        
        # Simple signatures
        signatures = {
            "WordPress": ["wp-content", "wordpress"],
            "Shopify": ["shopify"],
            "Wix": ["wix.com", "_wix"],
            "Squarespace": ["squarespace"],
            "React": ["react"],
            "Bootstrap": ["bootstrap"],
            "Cloudflare": ["cloudflare"]
        }
        
        for tech, keywords in signatures.items():
            if any(k in text for k in keywords) or any(k in headers for k in keywords):
                tech_stack.append(tech)
                
    except:
        pass
    return tech_stack