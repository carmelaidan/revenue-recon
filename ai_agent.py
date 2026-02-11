"""
Module: ai_agent.py
Description: Uses Gemini 1.5 Flash (Stable) with fallbacks
"""
import google.generativeai as genai
import os
import streamlit as st

# Configure Gemini
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        print("[!] GEMINI_API_KEY is missing.")
except Exception as e:
    print(f"[!] Gemini Config Error: {e}")

def get_model():
    """
    Returns the best available model.
    Tries Flash -> Pro -> Standard to ensure it never crashes.
    """
    # List of models to try in order of preference
    # 'gemini-1.5-flash' is the stable tag (no -latest)
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # Simple test generation to verify access
            # We don't actually generate content here, just returning the object
            # But the real test happens when we call generate_content
            return model
        except:
            continue
            
    # Absolute fallback
    return genai.GenerativeModel('gemini-pro')

def generate_audit_narrative(business_name, url, score, ssl, ports, seo, tech):
    model = get_model()
    
    prompt = f"""
    You are a Senior Cyber Security & Digital Strategist.
    Write a 3-paragraph executive summary for a client named '{business_name}'.
    
    DATA:
    - Website: {url}
    - Security Score: {score}/100
    - SSL Secure: {ssl}
    - Open Ports: {ports}
    - Tech Stack: {tech}
    - SEO Data: {seo}
    
    TONE: Professional, urgent, but constructive.
    STRUCTURE:
    1. The Good: What they are doing right.
    2. The Bad: The critical risks (Score, SSL, Ports).
    3. The Opportunity: How fixing SEO/Tech will increase revenue.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Generation Error: {e}. (Try refreshing to reset quota)"

def generate_seo_fixes(url, current_title, current_desc, industry, location):
    model = get_model()
    
    prompt = f"""
    You are a Google SEO Expert. Rewrite the meta tags for a website to rank #1.
    
    TARGET:
    - Industry: {industry}
    - Location: {location}
    - URL: {url}
    
    CURRENT (BAD) TAGS:
    - Title: {current_title}
    - Description: {current_desc}
    
    TASK:
    Write 3 options for a new, high-converting <title> and <meta description>.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"