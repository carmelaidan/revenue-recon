"""
Module: ai_agent.py
Description: smart AI Agent for Strategy (Branch B) and Executive Audits (Branch A).
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_available_model(api_key):
    """Dynamically finds a working model name."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models = response.json().get('models', [])
            for model in models:
                if 'generateContent' in model['supportedGenerationMethods'] and 'gemini' in model['name']:
                    return model['name']
    except:
        pass
    return "models/gemini-pro"

def query_gemini(prompt):
    """Helper function to send raw requests to Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return "Error: No API Key."
    
    model_name = get_available_model(api_key)
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text prompt": prompt}]}]} # Fixed key name
    
    # Correct payload structure for Gemini API
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"AI Error: {response.text}"
    except Exception as e:
        return f"Connection Error: {e}"

# --- BRANCH B: STRATEGY (No Website) ---
def generate_website_strategy(business_name, location, reviews):
    prompt = f"""
    You are a Senior Digital Strategist. A business named '{business_name}' in '{location}' has no website.
    Reviews: "{reviews}"
    
    Write a Website Proposal. Format exactly like this:
    1. PROPOSED DOMAIN: (Name)
    2. HERO HEADLINE: (One sentence)
    3. STRATEGY SUMMARY: (3 sentences on how a website will solve their specific problems based on reviews)
    4. KEY SELLING POINT: (The main hook)
    """
    return query_gemini(prompt)

# --- BRANCH A: EXECUTIVE AUDIT (Website Exists) ---
def generate_audit_narrative(business_name, url, score, ssl, ports, seo, tech_stack):
    """
    Analyzes technical scan data and writes a professional executive summary.
    """
    prompt = f"""
    You are a Cyber Security & Marketing Consultant. You just ran an audit on: {business_name} ({url}).
    
    DATA FINDINGS:
    - Overall Risk Score: {score}/100 (Lower is worse)
    - SSL Certificate: {"Secure" if ssl else "CRITICAL FAIL (Not Secure)"}
    - Open Ports: {ports}
    - SEO Meta Description: {"Present" if seo.get('description') else "MISSING (Invisible to Google)"}
    - Tech Stack: {tech_stack}
    
    TASK:
    Write a professional Executive Summary (max 150 words).
    Do NOT just list the data again. Interpret it.
    
    Structure:
    1. **Security Posture**: Evaluate their risk level. Mention the SSL and ports implications.
    2. **Digital Presence**: Critique their SEO and tech stack. Are they modern or outdated?
    3. **Strategic Recommendation**: Give 1 actionable next step.
    
    Tone: Professional, direct, and authoritative.
    """
    return query_gemini(prompt)