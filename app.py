import streamlit as st
import time
from scanner import find_business_url
from analyzer import check_ssl, check_security_headers, check_email_security, check_seo, extract_emails, detect_tech_stack, extract_socials
from network_scanner import scan_common_ports
from ai_agent import generate_website_strategy, generate_audit_narrative # <-- NEW IMPORT
from reporter import save_audit_report, save_strategy_proposal

st.set_page_config(page_title="B2B Intel Suite", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ B2B Threat & Opportunity Intelligence Suite")
st.markdown("---")

# --- TABS ---
tab1, tab2 = st.tabs(["🏢 Business Search", "🔗 Self-Audit"])

target_name = ""
target_location = ""
direct_url = ""
run_scan = False
mode = ""

with tab1:
    col1, col2 = st.columns(2)
    with col1: target_name = st.text_input("Business Name", placeholder="e.g. Accenture")
    with col2: target_location = st.text_input("Location", placeholder="e.g. Manila")
    if st.button("🚀 Run OSINT Scan"):
        run_scan = True
        mode = "OSINT"

with tab2:
    direct_url = st.text_input("Enter Website URL", placeholder="https://www.example.com")
    if st.button("🔍 Run Self-Audit"):
        run_scan = True
        mode = "DIRECT"

# --- MAIN LOGIC ---
if run_scan:
    website_url = None
    if mode == "OSINT":
        if not target_name: st.stop()
        with st.spinner(f"Searching for {target_name}..."):
            website_url = find_business_url(target_name, target_location)
    elif mode == "DIRECT":
        if not direct_url: st.stop()
        website_url = direct_url
        target_name = "Target Business"

    # --- BRANCH A: WEBSITE FOUND ---
    if website_url:
        st.success(f"✅ Target Locked: {website_url}")
        my_bar = st.progress(0, text="Initiating Enterprise Scan...")

        # 1. RUN TECHNICAL SCANS
        with st.spinner("Running Deep Audit..."):
            ssl_valid = check_ssl(website_url)
            headers = check_security_headers(website_url)
            email_sec = check_email_security(website_url)
            ports = scan_common_ports(website_url)
            seo = check_seo(website_url)
            emails = extract_emails(website_url)
            tech = detect_tech_stack(website_url)
            my_bar.progress(60, text="Consulting AI Analyst...")

        # 2. CALCULATE SCORE
        score = 100
        if not ssl_valid: score -= 30
        if "Risk" in str(ports): score -= 20
        if not seo.get('description'): score -= 10
        if score < 0: score = 0

        # 3. RUN AI NARRATIVE GENERATION (NEW)
        with st.spinner("Drafting Executive Summary..."):
            ai_report = generate_audit_narrative(target_name, website_url, score, ssl_valid, ports, seo, tech)
            my_bar.progress(100, text="Complete")

        # --- DASHBOARD UI ---
        # KPI ROW
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Security Score", f"{score}/100", delta_color="normal" if score > 70 else "inverse")
        k2.metric("SSL Status", "Secure" if ssl_valid else "Vulnerable")
        k3.metric("Tech Stack", f"{len(tech)} Detected")
        k4.metric("Leads", f"{len(emails)} Emails")

        st.divider()

        # AI EXECUTIVE SUMMARY SECTION
        st.subheader("📝 Executive AI Analysis")
        st.info(ai_report) # Display the AI text prominently

        # DETAILED DATA
        with st.expander("See Raw Technical Data"):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Security Findings:**")
                st.json(ports)
                st.json(headers)
            with c2:
                st.write("**Marketing Findings:**")
                st.json(seo)
                st.write(tech)

        # GENERATE PDF (Pass the AI text to the PDF generator)
        pdf_file = save_audit_report(target_name, website_url, score, ai_report, ssl_valid, seo, ports)
        
        with open(pdf_file, "rb") as file:
            st.download_button("📥 Download Executive Report (PDF)", data=file, file_name=pdf_file, mime="application/pdf")

    # --- BRANCH B: NO WEBSITE ---
    else:
        st.warning("🔻 No Official Website Detected.")
        st.info("Generating Strategy...")
        reviews = "Customer service is great." 
        strategy = generate_website_strategy(target_name, target_location, reviews)
        st.markdown(strategy)
        
        pdf_file = save_strategy_proposal(target_name, strategy)
        with open(pdf_file, "rb") as file:
            st.download_button("📥 Download Strategy Proposal", data=file, file_name=pdf_file, mime="application/pdf")