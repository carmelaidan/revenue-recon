"""
Module: ai_agent.py
Description: Self-Healing AI with Industry Classification
"""
import google.generativeai as genai
import os
import streamlit as st

# --- 1. CONFIGURATION ---
def configure_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key: return False
    try:
        genai.configure(api_key=api_key)
        return True
    except:
        return False

is_configured = configure_gemini()

# --- 2. DYNAMIC MODEL FINDER ---
def get_working_model():
    if not is_configured: return None
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name.lower():
                return genai.GenerativeModel(m.name)
        return genai.GenerativeModel('models/gemini-pro')
    except: return None

# --- 3. INTELLIGENCE FUNCTIONS ---

def identify_industry(business_name):
    """
    New Feature: Asks AI to categorize the business name into a searchable industry string.
    Example: "Solaire Resort North" -> "Casino Hotel"
    """
    model = get_working_model()
    if not model: return business_name.split(' ')[-1] # Fallback to old "dumb" logic

    prompt = f"""
    Identify the specific market industry for the business "{business_name}".
    Reply with ONLY the 2-3 word industry category. Do not add punctuation.
    Example Input: Jollibee -> Example Output: Fast Food Restaurant
    Example Input: Accenture -> Example Output: IT Consulting
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return business_name  # Fail safe

def generate_audit_narrative(business_name, url, score, ssl, ports, seo, tech):
    model = get_working_model()
    if not model: return "AI Unavailable."
    
    prompt = f"""
    You are a Senior Cyber Security Strategist.
    Write a 3-paragraph executive summary for '{business_name}' ({url}).
    
    DATA: Score: {score}/100, SSL: {ssl}, SEO: {seo}
    TONE: Urgent but professional.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error: {e}"

def generate_seo_fixes(url, current_title, current_desc, industry, location):
    model = get_working_model()
    if not model: return "AI Unavailable."
    
    prompt = f"""
    Act as an SEO Expert. Rewrite meta tags for {url} ({industry} in {location}).
    CURRENT: Title: {current_title}, Desc: {current_desc}
    Provide 3 better options.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error: {e}"