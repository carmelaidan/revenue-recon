"""
Module: ai_agent.py
Description: Self-Healing AI - Automatically finds the correct model name for your account.
"""
import google.generativeai as genai
import os
import streamlit as st

# --- 1. CONFIGURATION ---
def configure_gemini():
    # Try Secret first, then Environment Variable
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is missing.")
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"❌ Config Error: {e}")
        return False

# Run config on load
is_configured = configure_gemini()

# --- 2. DYNAMIC MODEL FINDER ---
def get_working_model():
    """
    Asks Google: 'Which models can I use?' and picks the first one.
    This fixes the 404 error by never guessing a wrong name.
    """
    if not is_configured:
        return None

    try:
        # List all models available to your specific API Key
        for m in genai.list_models():
            # We only want models that can generate text (not image-only models)
            if 'generateContent' in m.supported_generation_methods:
                # Prefer Gemini models, avoiding 'vision' only legacy ones
                if 'gemini' in m.name.lower():
                    print(f"✅ Found working model: {m.name}")
                    return genai.GenerativeModel(m.name)
        
        # If list_models fails or is empty, try the absolute standard fallback
        return genai.GenerativeModel('models/gemini-pro')
        
    except Exception as e:
        print(f"❌ Model List Error: {e}")
        return None

# --- 3. GENERATION FUNCTIONS ---
def generate_audit_narrative(business_name, url, score, ssl, ports, seo, tech):
    model = get_working_model()
    if not model:
        return "AI Unavailable: Check API Key or Quota."

    prompt = f"""
    You are a Senior Cyber Security Strategist.
    Write a 3-paragraph executive summary for '{business_name}'.
    
    DATA:
    - URL: {url}
    - Score: {score}/100
    - SSL: {ssl}
    - SEO: {seo}
    
    Write clearly for a business owner.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Generation Failed: {str(e)}"

def generate_seo_fixes(url, current_title, current_desc, industry, location):
    model = get_working_model()
    if not model:
        return "AI Unavailable."

    prompt = f"""
    Act as an SEO Expert. Rewrite meta tags for {url} ({industry} in {location}).
    
    CURRENT:
    Title: {current_title}
    Desc: {current_desc}
    
    Provide 3 better options for Google Ranking.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"