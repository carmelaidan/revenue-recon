"""
Module: app.py
Description: The "Auto-Consultant" Dashboard with Debug Mode & Smart Fallback
"""
import streamlit as st
import pandas as pd
import re
from duckduckgo_search import DDGS # Imported directly for Debug Mode
from scanner import find_business_url, find_competitors
from analyzer import check_ssl, check_seo, detect_tech_stack
from network_scanner import scan_common_ports
from ai_agent import generate_audit_narrative, generate_seo_fixes
from reporter import save_audit_report

# --- HELPER: IMPROVED GOOGLE MAPS PARSER ---
def extract_location_from_maps(url):
    """
    Extracts the city/area from a Google Maps URL.
    Handles standard URLs and tries to parse 'place/' segments.
    """
    if not url:
        return ""
    
    try:
        # 1. Look for the standard 'place/City+Name' pattern
        match = re.search(r'place/([^/]+)', url)
        if match:
            # Replace '+' with spaces and remove any trailing coordinates
            clean_loc = match.group(1).replace('+', ' ')
            return clean_loc.split(',')[0] # Return just the city/area name
            
        # 2. Fallback: If it's a short link or weird format, we might need a backup
    except:
        pass
    return ""

# --- PAGE CONFIG ---
st.set_page_config(page_title="RevenueRecon", page_icon="🚀", layout="wide")
st.title("🚀 RevenueRecon: Automated Growth Engine")
st.markdown("---")

# --- SIDEBAR ---
with st.sidebar:
    mode = st.radio("Select Operation Mode", ["🏢 Business Search (Auto-Discovery)", "🔗 Self-Audit (Direct URL)"])
    st.info("💡 **Pro Tip:** If the Auto-Discovery fails, paste the URL manually to unlock the audit.")

# --- INPUT VARIABLES ---
target_name = ""
maps_link = ""
direct_url = ""
run_scan = False
location_query = "" # This will hold the extracted location

# --- MODE 1: BUSINESS SEARCH ---
if mode == "🏢 Business Search (Auto-Discovery)":
    c1, c2 = st.columns(2)
    with c1:
        target_name = st.text_input("Business Name", placeholder="e.g. Dr. Smile Dental")
    with c2:
        maps_link = st.text_input("Google Maps Link", placeholder="Paste the full maps link here...")
    
    # Auto-extract location if link is provided
    if maps_link:
        location_query = extract_location_from_maps(maps_link)
        if location_query:
            st.success(f"📍 Detected Location: **{location_query}**")
        else:
            st.warning("⚠️ Could not read location from Map Link. (Scan will still proceed)")
            # Optional: Allow manual override for location if parsing fails
            location_query = st.text_input("Enter City/Area manually (if Map Link failed):", placeholder="e.g. Manila")
    
    if st.button("🚀 Launch Scan"):
        run_scan = True

# --- MODE 2: SELF AUDIT ---
elif mode == "🔗 Self-Audit (Direct URL)":
    direct_url = st.text_input("Enter Website URL", placeholder="https://www.example.com")
    location_query = st.text_input("Target Location (For Competitor Comparison)", placeholder="e.g. Chicago")
    if st.button("🔍 Run Audit"):
        run_scan = True
        target_name = "Direct Client"

# --- MAIN LOGIC ---
if run_scan:
    
    # 1. FIND THE URL (With Debugging & Manual Override)
    user_url = None
    
    if direct_url:
        user_url = direct_url
    else:
        if not target_name:
            st.error("Please enter a Business Name.")
            st.stop()
        
        search_loc = location_query if location_query else ""
        
        # --- DEBUG SECTION START ---
        # We run a raw search here to see what the server sees
        with st.expander(f"🕵️ Debugging Search for: {target_name}...", expanded=True):
            try:
                query = f"{target_name} {search_loc} official website"
                st.write(f"**Query:** `{query}`")
                
                # Direct call to DDGS to see raw results
                raw_results = list(DDGS().text(query, max_results=5))
                
                if not raw_results:
                    st.error("❌ DuckDuckGo returned 0 results.")
                else:
                    st.success(f"✅ Found {len(raw_results)} raw results.")
                    for i, r in enumerate(raw_results):
                        st.write(f"**Result {i+1}:** [{r['title']}]({r['href']})")
                        
                        # Simulating the filter logic
                        skip_list = ['facebook', 'instagram', 'linkedin', 'wikipedia', 'yelp', 'yellowpages']
                        if not any(skip in r['href'] for skip in skip_list):
                            if not user_url:
                                user_url = r['href']
                                st.write(f"🎉 **Auto-Selected:** {user_url}")
            except Exception as e:
                st.error(f"⚠️ Search Error: {e}")
        # --- DEBUG SECTION END ---

        # If the debug loop didn't find it, try the scanner module (backup)
        if not user_url:
             with st.spinner(f"📡 Retrying via Scanner Module..."):
                user_url = find_business_url(target_name, search_loc)

        # --- THE SMART FALLBACK FIX ---
        if not user_url:
            st.warning(f"⚠️ We couldn't auto-detect a website for '{target_name}'.")
            st.info("They might not have one (This is a sales opportunity!), or the search failed.")
            
            # The Manual Override Input
            manual_override = st.text_input("👇 If they have a website, paste it here to continue:", placeholder="https://...")
            
            if manual_override:
                user_url = manual_override
                st.success(f"✅ Manual Override Accepted. Scanning {user_url}...")
            else:
                st.error("❌ No website found or provided. Cannot proceed with Audit.")
                st.stop()
        else:
            st.success(f"✅ Target Locked: {user_url}")

    # 2. COMPETITOR RADAR
    comp_data = []
    # Only run if we have a valid location to search in
    if location_query:
        # Guess industry from name (Simple heuristic: takes last word)
        industry_guess = target_name.split(' ')[-1] 
        
        with st.spinner(f"⚔️ Radar Active: Scanning for top-rated competitors in {location_query}..."):
            # Clean domain for filtering
            domain_clean = user_url.replace("https://", "").replace("http://", "").split("/")[0]
            competitors = find_competitors(industry_guess, location_query, domain_clean)
            
            # Lite Scan on Competitors
            for comp in competitors:
                c_ssl = check_ssl(comp['url'])
                c_tech = detect_tech_stack(comp['url'])
                c_score = 90 if c_ssl else 40 # Simple score for speed
                comp_data.append({
                    "Name": comp['name'],
                    "URL": comp['url'],
                    "Score": c_score,
                    "Tech": len(c_tech),
                    "SSL": "✅" if c_ssl else "❌"
                })

    # 3. DEEP USER SCAN
    progress = st.progress(0, text="Deep Audit in progress...")
    
    ssl = check_ssl(user_url)
    progress.progress(30, text="Checking Security Protocols...")
    seo = check_seo(user_url)
    progress.progress(60, text="Analyzing Content Strategy...")
    tech = detect_tech_stack(user_url)
    ports = scan_common_ports(user_url)
    progress.progress(100, text="Analysis Complete.")

    # Scoring
    score = 100
    if not ssl: score -= 30
    if not seo.get('description'): score -= 15
    if "Risk" in str(ports): score -= 20
    if score < 0: score = 0

    # --- DISPLAY: BATTLEFIELD ---
    if comp_data:
        st.subheader("⚔️ Market Battlefield")
        # Add User
        all_data = [{"Name": f"{target_name} (You)", "URL": user_url, "Score": score, "Tech": len(tech), "SSL": "✅" if ssl else "❌"}] + comp_data
        df = pd.DataFrame(all_data)
        st.dataframe(df.style.highlight_max(axis=0, subset=['Score'], color='#d4edda'), use_container_width=True)

    st.divider()

    # --- DISPLAY: SEO AUTO-FIXER (The "Consultant" Feature) ---
    st.subheader("🛠️ Automated SEO Fixer")
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Current Meta Data")
        if not seo.get('title'):
             st.error("Title Tag: Missing ❌")
        else:
             st.info(f"Title: {seo.get('title')}")
             
        if not seo.get('description'):
             st.error("Description: Missing ❌")
        else:
             st.info(f"Desc: {seo.get('description')}")
    
    with col2:
        st.caption("AI Optimization")
        if st.button("✨ Generate Google-Ranking Tags"):
            with st.spinner("Rewriting content for Google dominance..."):
                # Call the AI function
                fixed_content = generate_seo_fixes(user_url, seo.get('title'), seo.get('description'), target_name, location_query)
                st.success("Optimization Complete!")
                st.code(fixed_content, language="markdown")

    st.divider()

    # --- EXECUTIVE REPORT ---
    with st.spinner("Drafting PDF Report..."):
        ai_summary = generate_audit_narrative(target_name, user_url, score, ssl, ports, seo, tech)
        
    st.info(ai_summary)
    
    # Save PDF (Simplified placeholder)
    # pdf_file = save_audit_report(target_name, user_url, score, ai_summary, ssl, seo, ports, {}, False, tech, [], [])
    # with open(pdf_file, "rb") as f:
    #    st.download_button("Download Executive PDF", f, file_name=pdf_file)