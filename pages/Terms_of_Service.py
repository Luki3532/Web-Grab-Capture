import streamlit as st

st.set_page_config(page_title="Terms of Service - Web Grab & Capture", page_icon="globe", layout="wide")

# Modern professional dark theme CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Hide Streamlit deploy button only */
    .stDeployButton { display: none !important; }
    [data-testid="stToolbarActionButton"][aria-label="Deploy"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    
    /* Root variables */
    :root {
        --bg-primary: #0D1117;
        --bg-secondary: #161B22;
        --bg-card: #1C2128;
        --border-color: #30363D;
        --accent-blue: #58A6FF;
        --accent-green: #3FB950;
        --text-primary: #E6EDF3;
        --text-secondary: #8B949E;
        --text-muted: #6E7681;
    }
    
    .stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #1C2128 0%, #0D1117 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
    }
    .page-title {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .page-title i { color: var(--accent-blue); }
    .page-meta {
        font-size: 0.9rem;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .page-meta i { font-size: 0.8rem; }
    
    /* Content card */
    .content-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Section styling */
    .section-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        background: var(--accent-blue);
        color: white;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 10px;
    }
    .section-title {
        display: flex;
        align-items: center;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }
    .section-content {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .section-content ul { margin: 0.5rem 0; padding-left: 1.25rem; }
    .section-content li { margin-bottom: 0.35rem; }
    
    /* Highlight box */
    .highlight-box {
        background: rgba(88, 166, 255, 0.05);
        border-left: 3px solid var(--accent-blue);
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .highlight-box p { color: var(--text-secondary); margin: 0; font-size: 0.85rem; }
    
    /* Footer */
    .modern-footer {
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid var(--border-color);
        text-align: center;
    }
    .footer-brand { font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem; }
    .footer-brand i { color: var(--accent-blue); margin-right: 8px; }
    .footer-text { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem; }
    .footer-nav { font-size: 0.8rem; color: var(--text-muted); }
    .footer-copyright { font-size: 0.75rem; color: var(--text-muted); margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown("""
<div class="page-header">
    <div class="page-title"><i class="fas fa-file-contract"></i>Terms of Service</div>
    <div class="page-meta"><i class="fas fa-calendar"></i>Last Updated: January 2024</div>
</div>
""", unsafe_allow_html=True)

# Terms Content
terms_sections = [
    ("1", "Acceptance of Terms", "By accessing and using Web Grab & Capture, you accept and agree to be bound by the terms and conditions of this agreement. If you do not agree to these terms, please do not use the Service."),
    ("2", "Description of Service", """Web Grab & Capture is a web scraping tool that allows users to extract publicly available information from websites, including company information and metadata, contact details, social media links, images, logos, and favicons."""),
    ("3", "Acceptable Use", """You agree to use the Service only for lawful purposes. You shall not use the Service to scrape websites that prohibit scraping, collect personal information for spamming or harassment, circumvent security measures, use automated scripts excessively, or violate any applicable laws."""),
    ("4", "User Responsibilities", """You are solely responsible for ensuring compliance with applicable laws, obtaining necessary permissions before scraping, respecting intellectual property rights, reviewing target website terms of service, and any consequences arising from your use of scraped data."""),
    ("5", "Intellectual Property", """The Service is owned by Web Grab & Capture and protected by intellectual property laws. Data scraped using the Service remains the property of respective website owners. The Service does not grant you rights to such content beyond what is permitted by law."""),
    ("6", "Disclaimer of Warranties", """THE SERVICE IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND. We do not warrant that the Service will be uninterrupted, error-free, or that results will be accurate or reliable."""),
    ("7", "Limitation of Liability", """Web Grab & Capture shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of the Service, third-party conduct, or unauthorized access to your data."""),
    ("8", "Indemnification", """You agree to defend, indemnify, and hold harmless Web Grab & Capture from any claims, damages, or expenses arising from your use of the Service or violation of these Terms."""),
    ("9", "Changes to Terms", """We reserve the right to modify these Terms at any time. Material changes will be communicated with at least 30 days' notice."""),
    ("10", "Governing Law", """These Terms shall be governed by the laws of the jurisdiction in which Web Grab & Capture operates."""),
]

for num, title, content in terms_sections:
    st.markdown(f"""
    <div class="content-card">
        <div class="section-title"><span class="section-num">{num}</span>{title}</div>
        <div class="section-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box" style="margin-top: 1.5rem;">
    <p><i class="fas fa-check-circle" style="color: var(--accent-green); margin-right: 8px;"></i>
    By using Web Grab & Capture, you acknowledge that you have read, understood, and agree to these Terms of Service.</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="modern-footer">
    <div class="footer-brand"><i class="fas fa-globe"></i>Web Grab & Capture</div>
    <p class="footer-text">Professional website analysis and brand asset extraction</p>
    <p class="footer-nav"><i class="fas fa-compass"></i>Navigate using the sidebar menu</p>
    <p class="footer-copyright">2026 Web Grab & Capture. Built with precision.</p>
</div>
""", unsafe_allow_html=True)
