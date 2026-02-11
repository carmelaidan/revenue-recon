"""
Module: ai_agent.py
Description: Uses Gemini with automatic fallback to older models to prevent 404s.
"""
import os
from typing import List, Optional, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed

import google.generativeai as genai
import streamlit as st

# --- Configure Gemini ---
_api_key = None
_key_source = None

try:
    # 1. Streamlit secrets (.streamlit/secrets.toml)
    try:
        if hasattr(st, "secrets") and st.secrets is not None:
            _api_key = st.secrets.get("GEMINI_API_KEY", None)
            if _api_key:
                _key_source = "st.secrets"
    except Exception:
        pass
    # 2. Environment variable (.env via python-dotenv, or shell)
    if not _api_key:
        _api_key = os.getenv("GEMINI_API_KEY")
        if _api_key:
            _key_source = "os.getenv / .env"

    if _api_key:
        genai.configure(api_key=_api_key)
    _config_error = None
except Exception as e:
    _config_error = str(e)


def _write_debug_to_sidebar(key_set: bool, key_source: Optional[str], errors: List[Tuple[str, str]]):
    """Write AI debug info to Streamlit sidebar for troubleshooting."""
    with st.sidebar.expander("🔧 AI Debug Info", expanded=True):
        st.caption("Diagnostics for Gemini connection failures")
        st.write("**API Key Status:**", "✅ Set" if key_set else "❌ Missing or empty")
        if key_source:
            st.write("**Source:**", key_source)
        if _config_error:
            st.error(f"**Config Error:** {_config_error}")

        if errors:
            st.write("**Model attempts:**")
            for model_name, err_msg in errors:
                st.code(f"{model_name}: {err_msg}", language=None)
            last_err = errors[-1][1]
            if "403" in last_err or "PERMISSION_DENIED" in last_err:
                st.warning("403 / PERMISSION_DENIED: Check API key validity & quotas.")
            elif "404" in last_err or "NOT_FOUND" in last_err:
                st.warning("404 / NOT_FOUND: Model may be deprecated or unavailable.")
            elif "API key" in last_err.lower() or "invalid" in last_err.lower():
                st.warning("Key may be invalid or revoked.")


def generate_with_fallback(prompt: str) -> str:
    """
    Tries multiple model versions to find one that works.
    On failure, writes detailed error info to the Streamlit sidebar.
    """
    models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    errors: List[Tuple[str, str]] = []

    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err_msg = f"{type(e).__name__}: {str(e)}"
            errors.append((model_name, err_msg))
            continue

    # All models failed — write debug info to sidebar
    _write_debug_to_sidebar(
        key_set=bool(_api_key),
        key_source=_key_source,
        errors=errors
    )

    fallback_msg = "AI Unavailable: Could not connect to any Gemini model."
    if errors:
        fallback_msg += f" Last error: {errors[-1][1][:120]}..."
    return fallback_msg


def generate_audit_narrative(business_name, url, score, ssl, ports, seo, tech):
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
    return generate_with_fallback(prompt)


def generate_seo_fixes(url, current_title, current_desc, industry, location):
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
    return generate_with_fallback(prompt)
