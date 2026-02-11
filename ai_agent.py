"""
Module: ai_agent.py
Description: Debug Edition - Tells you exactly why the API is failing.
"""
import google.generativeai as genai
import os
import streamlit as st

def configure_gemini():
    # 1. Try Streamlit Secrets
    api_key = st.secrets.get("GEMINI_API_KEY")
    source = "Streamlit Secrets"
    
    # 2. Try Local Environment
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
        source = "Local .env"

    # 3. Debug Output
    if not api_key:
        return False, "❌ Error: GEMINI_API_KEY is missing from both Secrets and .env"
    
    try:
        genai.configure(api_key=api_key)
        return True, f"✅ Key found in {source}"
    except Exception as e:
        return False, f"❌ Configuration Error: {str(e)}"

# Run configuration immediately
is_configured, config_status = configure_gemini()

def generate_with_fallback(prompt):
    if not is_configured:
        return f"AI Error: {config_status}"

    # Try standard model first
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback to Pro
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e2:
            return f"AI Connection Failed. \nError 1 (Flash): {e} \nError 2 (Pro): {e2}"

def generate_audit_narrative(business_name, url, score, ssl, ports, seo, tech):
    prompt = f"Write a 3-paragraph executive summary for {business_name} ({url}). Score: {score}/100."
    return generate_with_fallback(prompt)

def generate_seo_fixes(url, title, desc, industry, loc):
    prompt = f"Write 3 SEO meta tags for {url} in {industry}."
    return generate_with_fallback(prompt)