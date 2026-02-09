"""
Module: reporter.py
Description: Generates professional PDF reports with AI Narratives.
"""
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'B2B Threat & Opportunity Intelligence', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def save_audit_report(name, url, score, ai_text, ssl_status, seo_data, ports):
    """Generates the Executive Audit PDF."""
    pdf = PDFReport()
    pdf.add_page()
    
    # 1. Title & Score
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Audit Report: {name}", 0, 1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Target: {url}", 0, 1)
    
    # Color code the score
    pdf.set_font("Arial", 'B', 14)
    status = "EXCELLENT" if score > 80 else "CRITICAL RISK" if score < 50 else "NEEDS IMPROVEMENT"
    pdf.cell(0, 10, f"Risk Score: {score}/100 ({status})", 0, 1)
    pdf.ln(5)

    # 2. Executive Summary (The AI Part)
    pdf.set_fill_color(240, 240, 240) # Light gray background
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Executive Summary", 0, 1)
    pdf.set_font("Arial", size=11)
    # Multi_cell handles text wrapping automatically
    pdf.multi_cell(0, 7, ai_text, border=0, fill=True)
    pdf.ln(10)

    # 3. Technical Appendix (Raw Data)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Technical Findings", 0, 1)
    
    pdf.set_font("Arial", size=10)
    
    # Security Row
    secure_str = "PASS (Encrypted)" if ssl_status else "FAIL (Unencrypted)"
    pdf.cell(0, 8, f"SSL Encryption: {secure_str}", 0, 1)
    
    open_p = [p for p in ports if ports[p] != "Closed"]
    pdf.multi_cell(0, 8, f"Open Ports: {open_p if open_p else 'None Detected'}")
    
    # Marketing Row
    seo_str = "PASS" if seo_data.get('description') else "FAIL (Missing Description)"
    pdf.cell(0, 8, f"SEO Meta Data: {seo_str}", 0, 1)
    
    filename = f"{name.replace(' ', '_')}_Executive_Audit.pdf"
    pdf.output(filename)
    return filename

def save_strategy_proposal(name, ai_content):
    """Generates the Strategy PDF (Branch B)."""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Digital Strategy: {name}", 0, 1)
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, ai_content)
    filename = f"{name.replace(' ', '_')}_Strategy.pdf"
    pdf.output(filename)
    return filename