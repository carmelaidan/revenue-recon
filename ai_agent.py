"""
Module: ai_agent.py
Description: Uses Gemini 1.5 Flash (Faster & Cheaper)
"""
import google.generativeai as genai
import os
import streamlit as st

# Configure Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    pass # Handle missing secrets gracefully in UI

def generate_audit_narrative(business_name, url, score, ssl, ports, seo, tech):
    # CHANGED: 'gemini-pro' -> 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-1.5-flash')
    
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
        return f"AI Error: {e}"

def generate_seo_fixes(url, current_title, current_desc, industry, location):
    # CHANGED: 'gemini-pro' -> 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-1.5-flash')
    
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