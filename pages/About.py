import streamlit as st

st.set_page_config(page_title="About - Web Grab & Capture", page_icon="globe", layout="wide")

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
    .page-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 700px;
    }
    
    /* Section styling */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    .section-title i { color: var(--accent-blue); }
    
    /* Info cards */
    .info-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease;
    }
    .feature-card:hover { border-color: var(--accent-blue); }
    .feature-icon {
        width: 40px;
        height: 40px;
        background: rgba(88, 166, 255, 0.1);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    .feature-icon i { color: var(--accent-blue); font-size: 1.1rem; }
    .feature-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .feature-desc { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; }
    
    /* Creator card */
    .creator-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        display: flex;
        gap: 2rem;
        align-items: flex-start;
    }
    .creator-avatar {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, var(--accent-blue), #2EA043);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .creator-avatar i { color: white; font-size: 2rem; }
    .creator-info h3 {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    .creator-role {
        color: var(--accent-blue);
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .creator-location {
        color: var(--text-muted);
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 1rem;
    }
    .creator-bio {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .creator-links {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .creator-link {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: var(--accent-blue);
        text-decoration: none;
        font-size: 0.9rem;
        padding: 6px 12px;
        background: rgba(88, 166, 255, 0.1);
        border-radius: 6px;
        transition: background 0.2s;
    }
    .creator-link:hover { background: rgba(88, 166, 255, 0.2); }
    
    /* Project cards */
    .project-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 1rem;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-bottom: 0.75rem;
        transition: border-color 0.2s;
    }
    .project-item:hover { border-color: var(--accent-blue); }
    .project-icon {
        width: 36px;
        height: 36px;
        background: rgba(88, 166, 255, 0.1);
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .project-icon i { color: var(--accent-blue); font-size: 0.9rem; }
    .project-name {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 4px;
    }
    .project-name a { color: var(--accent-blue); text-decoration: none; }
    .project-name a:hover { text-decoration: underline; }
    .project-desc { color: var(--text-secondary); font-size: 0.85rem; }
    
    /* Steps */
    .step-item {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .step-number {
        width: 32px;
        height: 32px;
        background: var(--accent-blue);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .step-content h4 {
        color: var(--text-primary);
        font-size: 1rem;
        margin-bottom: 4px;
    }
    .step-content p { color: var(--text-secondary); font-size: 0.9rem; }
    
    /* Footer */
    .modern-footer {
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid var(--border-color);
        text-align: center;
    }
    .footer-brand {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .footer-brand i { color: var(--accent-blue); margin-right: 8px; }
    .footer-text { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem; }
    .footer-nav { font-size: 0.8rem; color: var(--text-muted); }
    .footer-copyright { font-size: 0.75rem; color: var(--text-muted); margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown("""
<div class="page-header">
    <div class="page-title"><i class="fas fa-info-circle"></i>About Web Grab & Capture</div>
    <p class="page-subtitle">A professional web scraping tool designed to help you extract valuable company information, contact details, and brand assets from any website.</p>
</div>
""", unsafe_allow_html=True)

# Creator Section
st.markdown('<div class="section-title"><i class="fas fa-user"></i>Meet the Creator</div>', unsafe_allow_html=True)

st.markdown("""
<div class="creator-card">
    <div class="creator-avatar"><i class="fas fa-code"></i></div>
    <div class="creator-info">
        <h3>Lucas E. Carpenter</h3>
        <div class="creator-role">Software Developer | Designer | Founder</div>
        <div class="creator-location"><i class="fas fa-map-marker-alt"></i>South Bend, Indiana</div>
        <p class="creator-bio">
            Lucas is a developer and designer with a B.A. in Computer Science from Indiana University. 
            He brings a unique combination of technical expertise and hands-on experience. Web Grab & Capture 
            is part of his mission to create tools that make organizations more efficient, built with a focus 
            on listening to users' needs and delivering practical solutions.
        </p>
        <div class="creator-links">
            <a href="https://lucascode.org" target="_blank" class="creator-link"><i class="fas fa-globe"></i>lucascode.org</a>
            <a href="mailto:contact@lucascode.org" class="creator-link"><i class="fas fa-envelope"></i>contact@lucascode.org</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Other Projects
st.markdown('<div class="section-title"><i class="fas fa-folder-open"></i>Other Projects</div>', unsafe_allow_html=True)

st.markdown("""
<div class="project-item">
    <div class="project-icon"><i class="fas fa-film"></i></div>
    <div>
        <div class="project-name"><a href="https://frameforge.ddns.net/" target="_blank">Frame Forge</a></div>
        <div class="project-desc">An alternative rotoscoping tool for animators, focused on streamlining the animation workflow</div>
    </div>
</div>
<div class="project-item">
    <div class="project-icon"><i class="fas fa-list-ol"></i></div>
    <div>
        <div class="project-name"><a href="https://lucascode.org/tierrank" target="_blank">Collab Tier Ranker</a></div>
        <div class="project-desc">A collaborative real-time tier list maker with live synchronization</div>
    </div>
</div>
<div class="project-item">
    <div class="project-icon"><i class="fas fa-snowflake"></i></div>
    <div>
        <div class="project-name"><a href="https://lucascode.org/snowbounty" target="_blank">SnowBounty</a></div>
        <div class="project-desc">A community platform connecting people who need snow removal with volunteers</div>
    </div>
</div>
<div class="project-item">
    <div class="project-icon"><i class="fas fa-heart"></i></div>
    <div>
        <div class="project-name"><a href="https://lucascode.org/Projects/project.html?id=lcw" target="_blank">Lucas Carpenter Works</a></div>
        <div class="project-desc">Charity work helping South Bend residents in need</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown('<div class="section-title"><i class="fas fa-star"></i>Features</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-building"></i></div>
        <div class="feature-title">Company Information</div>
        <div class="feature-desc">Extract company names, descriptions, keywords, and other meta information automatically from any website.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-phone"></i></div>
        <div class="feature-title">Contact Details</div>
        <div class="feature-desc">Find email addresses, phone numbers with labels (Sales, Support, etc.), and physical addresses.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-share-nodes"></i></div>
        <div class="feature-title">Social Media Links</div>
        <div class="feature-desc">Automatically detect and collect links to LinkedIn, Twitter/X, Facebook, Instagram, and YouTube profiles.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-images"></i></div>
        <div class="feature-title">Images & Icons</div>
        <div class="feature-desc">Download all images, logos, and favicons from a website with a single click. Export as ZIP for convenience.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-file-export"></i></div>
        <div class="feature-title">Export Options</div>
        <div class="feature-desc">Export all collected data to CSV or Excel format for easy integration with your existing workflows.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon"><i class="fas fa-bolt"></i></div>
        <div class="feature-title">Fast & Easy</div>
        <div class="feature-desc">Simply paste a URL, click analyze, and get all the information you need in seconds. No technical knowledge required.</div>
    </div>
    """, unsafe_allow_html=True)

# How It Works Section
st.markdown('<div class="section-title"><i class="fas fa-cogs"></i>How It Works</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <div class="step-item">
        <div class="step-number">1</div>
        <div class="step-content">
            <h4>Enter a URL</h4>
            <p>Paste any website URL into the input field on the main page</p>
        </div>
    </div>
    <div class="step-item">
        <div class="step-number">2</div>
        <div class="step-content">
            <h4>Analyze</h4>
            <p>Click the analyze button and our tool extracts all relevant information from the webpage</p>
        </div>
    </div>
    <div class="step-item">
        <div class="step-number">3</div>
        <div class="step-content">
            <h4>Review Results</h4>
            <p>See company info, contacts, social links, and images displayed in an organized layout</p>
        </div>
    </div>
    <div class="step-item">
        <div class="step-number">4</div>
        <div class="step-content">
            <h4>Download</h4>
            <p>Export data as CSV or download images and icons as ZIP archives</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Use Cases Section
st.markdown('<div class="section-title"><i class="fas fa-lightbulb"></i>Use Cases</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-card">
        <div class="feature-title">Competitive Analysis</div>
        <div class="feature-desc">Research competitor websites and gather intelligence on their branding and contact strategies</div>
    </div>
    <div class="info-card">
        <div class="feature-title">Lead Generation</div>
        <div class="feature-desc">Extract contact information from potential client websites for your sales pipeline</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="feature-title">Brand Research</div>
        <div class="feature-desc">Collect logos and brand assets for reference materials and design inspiration</div>
    </div>
    <div class="info-card">
        <div class="feature-title">Market Research</div>
        <div class="feature-desc">Gather company information for industry analysis and market positioning studies</div>
    </div>
    """, unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="info-card" style="border-left: 3px solid var(--accent-blue); margin-top: 2rem;">
    <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
        <i class="fas fa-info-circle" style="color: var(--accent-blue); margin-right: 8px;"></i>
        Web Grab & Capture is designed for legitimate research and business purposes. Please ensure you comply with 
        website terms of service and applicable laws when using this tool.
    </p>
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
