import streamlit as st

st.set_page_config(page_title="Privacy Policy - Web Grab & Capture", page_icon="globe", layout="wide")

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
    .section-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: rgba(88, 166, 255, 0.1);
        border-radius: 6px;
        margin-right: 10px;
    }
    .section-icon i { color: var(--accent-blue); font-size: 0.85rem; }
    .section-title {
        display: flex;
        align-items: center;
        font-size: 1.05rem;
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
    .subsection { margin-top: 1rem; }
    .subsection-title { color: var(--text-primary); font-weight: 500; font-size: 0.9rem; margin-bottom: 0.5rem; }
    
    /* Highlight box */
    .highlight-box {
        background: rgba(88, 166, 255, 0.05);
        border-left: 3px solid var(--accent-blue);
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .highlight-box p { color: var(--text-secondary); margin: 0; font-size: 0.85rem; }
    
    /* Privacy feature */
    .privacy-feature {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.75rem 1rem;
        background: rgba(63, 185, 80, 0.05);
        border: 1px solid rgba(63, 185, 80, 0.2);
        border-radius: 8px;
        margin-bottom: 0.75rem;
    }
    .privacy-feature i { color: var(--accent-green); }
    .privacy-feature span { color: var(--text-secondary); font-size: 0.9rem; }
    
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
    <div class="page-title"><i class="fas fa-shield-halved"></i>Privacy Policy</div>
    <div class="page-meta"><i class="fas fa-calendar"></i>Last Updated: January 2024</div>
</div>
""", unsafe_allow_html=True)

# Privacy Highlights
st.markdown("""
<div class="privacy-feature"><i class="fas fa-check-circle"></i><span>Your scraped data stays on your device - we never store it</span></div>
<div class="privacy-feature"><i class="fas fa-check-circle"></i><span>No account or registration required</span></div>
<div class="privacy-feature"><i class="fas fa-check-circle"></i><span>Local processing - your data never leaves your computer</span></div>
""", unsafe_allow_html=True)

# Privacy Content
st.markdown("""
<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-info-circle"></i></span>Introduction</div>
    <div class="section-content">
        Web Grab & Capture is committed to protecting your privacy. This Privacy Policy explains how we collect, 
        use, disclose, and safeguard your information when you use our web scraping service. If you do not agree 
        with the terms of this privacy policy, please do not access the Service.
    </div>
</div>

<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-database"></i></span>Information We Collect</div>
    <div class="section-content">
        <div class="subsection">
            <div class="subsection-title">Information You Provide</div>
            <ul>
                <li><strong>URLs</strong>: The website addresses you submit for scraping</li>
                <li><strong>Usage Data</strong>: Information about how you interact with our Service</li>
            </ul>
        </div>
        <div class="subsection">
            <div class="subsection-title">Automatically Collected Information</div>
            <ul>
                <li><strong>Device Information</strong>: Browser type, operating system, device type</li>
                <li><strong>Log Data</strong>: IP address, access times, pages viewed</li>
            </ul>
        </div>
        <div class="highlight-box">
            <p><strong>We do NOT collect:</strong> Personal identification information, user accounts, or the data you scrape from third-party websites.</p>
        </div>
    </div>
</div>

<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-cogs"></i></span>How We Use Your Information</div>
    <div class="section-content">
        We use collected information to provide, operate, and maintain the Service; improve and personalize user 
        experience; understand usage patterns; develop new features; detect and prevent technical issues; 
        and comply with legal obligations.
    </div>
</div>

<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-lock"></i></span>Data Storage and Security</div>
    <div class="section-content">
        <div class="subsection">
            <div class="subsection-title">Local Processing</div>
            Web Grab & Capture processes data locally on your device. Scraped data, downloaded images, 
            and exported files remain on your computer and are never transmitted to our servers.
        </div>
        <div class="subsection">
            <div class="subsection-title">Security Measures</div>
            We implement appropriate technical and organizational security measures. However, no method 
            of transmission over the Internet is 100% secure.
        </div>
    </div>
</div>

<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-cookie"></i></span>Cookies</div>
    <div class="section-content">
        We may use cookies and similar tracking technologies to store preferences and understand how visitors 
        interact with the Service. You can instruct your browser to refuse all cookies or indicate when a 
        cookie is being sent.
    </div>
</div>

<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-user-shield"></i></span>Your Rights</div>
    <div class="section-content">
        Depending on your location, you may have rights including: access to your personal data, correction 
        of inaccurate data, deletion of your data, data portability, objection to processing, and restriction 
        of processing. Since scraped data is stored locally on your device, you control its retention and 
        may delete it at any time.
    </div>
</div>

<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-child"></i></span>Children's Privacy</div>
    <div class="section-content">
        The Service is not intended for individuals under 18. We do not knowingly collect personal information 
        from children under 18.
    </div>
</div>

<div class="content-card">
    <div class="section-title"><span class="section-icon"><i class="fas fa-sync"></i></span>Changes to This Policy</div>
    <div class="section-content">
        We may update this Privacy Policy from time to time. Changes will be posted on this page with an 
        updated "Last Updated" date. You are advised to review this policy periodically.
    </div>
</div>

<div class="highlight-box" style="margin-top: 1.5rem;">
    <p><i class="fas fa-check-circle" style="color: var(--accent-green); margin-right: 8px;"></i>
    By using Web Grab & Capture, you acknowledge that you have read, understood, and agree to this Privacy Policy.</p>
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
