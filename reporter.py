"""
Module: reporter.py
Description: Generates professional PDF reports with "Sanitized" text to prevent Unicode errors.
"""
from fpdf import FPDF
import datetime

def clean_text(text):
    """
    Sanitizes text to ensure it works with FPDF (Latin-1 encoding).
    Replaces smart quotes, emojis, and special symbols with standard ASCII.
    """
    if not isinstance(text, str):
        return str(text)
    
    # 1. Map common "fancy" characters to standard ones
    replacements = {
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u201c': '"',  # Left double quote
        '\u201d': '"',  # Right double quote
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2026': '...', # Ellipsis
        '\u2022': '*',  # Bullet point
        '–': '-',       # Another dash type
        '“': '"', 
        '”': '"'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
        
    # 2. Force encode to Latin-1, replacing unknown chars (like emojis) with '?'
    return text.encode('latin-1', 'replace').decode('latin-1')

def save_audit_report(name, url, score, ai_summary, ssl, seo, ports, headers, email_sec, tech, emails, socials):
    """
    Generates the Executive Audit PDF.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- HEADER ---
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, f"Security & Growth Audit: {clean_text(name)}", ln=True, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, f"Generated for: {clean_text(url)} | Date: {datetime.date.today()}", ln=True, align='C')
    pdf.ln(10)
    
    # --- EXECUTIVE SUMMARY ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "1. Executive Strategy Analysis", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 11)
    # Use clean_text() on the AI output
    pdf.multi_cell(0, 7, clean_text(ai_summary))
    pdf.ln(10)
    
    # --- TECHNICAL DATA APPENDIX ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "2. Technical Appendix", ln=True)
    pdf.ln(5)
    
    # Scores & SSL
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Overall Risk Score: {score}/100", ln=True)
    pdf.set_font("Arial", '', 11)
    ssl_status = "Secure (Valid HTTPS)" if ssl else "Vulnerable (No/Expired SSL)"
    pdf.cell(0, 7, f"SSL Status: {ssl_status}", ln=True)
    
    # Security Headers
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 7, "Security Headers:", ln=True)
    pdf.set_font("Arial", '', 10)
    for h, v in headers.items():
        pdf.cell(0, 6, f"{clean_text(h)}: {clean_text(str(v))}", ln=True)
        
    # Open Ports
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 7, "Open Ports (Risk Vectors):", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 6, clean_text(str(ports)))

    # Tech Stack
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 7, "Technology Stack:", ln=True)
    pdf.set_font("Arial", '', 10)
    for t in tech:
        pdf.cell(0, 6, f"- {clean_text(t)}", ln=True)

    # Emails & Socials
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 7, "Contact Data:", ln=True)
    pdf.set_font("Arial", '', 10)
    if emails:
        pdf.cell(0, 6, f"Emails Found: {clean_text(str(emails))}", ln=True)
    if socials:
        pdf.cell(0, 6, f"Social Links: {clean_text(str(socials))}", ln=True)

    # SAVE FILE
    filename = f"{clean_text(name).replace(' ', '_')}_Audit_Report.pdf"
    pdf.output(filename)
    return filename

def save_strategy_proposal(name, strategy_text):
    """
    Generates the Strategy Proposal PDF (No Website Found).
    """
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, f"Digital Strategy Proposal: {clean_text(name)}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 7, clean_text(strategy_text))
    
    filename = f"{clean_text(name).replace(' ', '_')}_Strategy.pdf"
    pdf.output(filename)
    return filename