import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
import re
import os
import io
import zipfile
from pathlib import Path

st.set_page_config(page_title="Web Grab & Capture", page_icon="globe", layout="wide")

# Modern professional dark theme CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Hide Streamlit deploy button only */
    .stDeployButton { display: none !important; }
    [data-testid="stToolbarActionButton"][aria-label="Deploy"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    
    /* Root variables for consistent theming */
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
    
    /* Global styles */
    .stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #1C2128 0%, #0D1117 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .hero-title i { color: var(--accent-blue); margin-right: 12px; }
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    /* Card styles */
    .info-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    .card-header i {
        font-size: 1.1rem;
        color: var(--accent-blue);
        width: 20px;
    }
    .card-header h3 {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    .card-content { color: var(--text-secondary); }
    .card-content p { margin: 0.5rem 0; font-size: 0.9rem; }
    .card-content strong { color: var(--text-primary); font-weight: 500; }
    
    /* Data labels */
    .data-label {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .data-value {
        color: var(--text-primary);
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }
    
    /* Phone list styling */
    .phone-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 0;
        border-bottom: 1px solid rgba(48, 54, 61, 0.5);
    }
    .phone-item:last-child { border-bottom: none; }
    .phone-label {
        background: rgba(88, 166, 255, 0.1);
        color: var(--accent-blue);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .phone-number { color: var(--text-primary); font-size: 0.9rem; }
    
    /* Social links */
    .social-link {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        background: rgba(88, 166, 255, 0.05);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-bottom: 8px;
        color: var(--text-secondary);
        text-decoration: none;
        transition: all 0.2s ease;
    }
    .social-link:hover {
        background: rgba(88, 166, 255, 0.1);
        border-color: var(--accent-blue);
    }
    .social-link i { width: 20px; text-align: center; }
    
    /* Stats badge */
    .stats-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(63, 185, 80, 0.1);
        color: var(--accent-green);
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Transparency grid for PNG images */
    [data-testid="stImage"] img {
        background-image: linear-gradient(45deg, #2a2a2a 25%, transparent 25%),
                          linear-gradient(-45deg, #2a2a2a 25%, transparent 25%),
                          linear-gradient(45deg, transparent 75%, #2a2a2a 75%),
                          linear-gradient(-45deg, transparent 75%, #2a2a2a 75%);
        background-size: 12px 12px;
        background-position: 0 0, 0 6px, 6px -6px, -6px 0px;
        background-color: #1a1a1a;
        border-radius: 6px;
        padding: 4px;
    }
    
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
    .footer-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    .footer-nav {
        font-size: 0.8rem;
        color: var(--text-muted);
    }
    .footer-nav i { margin-right: 6px; }
    .footer-copyright {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 1rem;
    }
    
    /* Success message styling */
    .success-banner {
        background: rgba(63, 185, 80, 0.1);
        border: 1px solid rgba(63, 185, 80, 0.3);
        border-radius: 8px;
        padding: 12px 16px;
        color: var(--accent-green);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Image grid */
    .image-grid-item {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero-section">
    <div class="hero-title"><i class="fas fa-globe"></i>Web Grab & Capture</div>
    <div class="hero-subtitle">Extract company information, images, and brand assets from any website</div>
</div>
""", unsafe_allow_html=True)

# URL Input section
st.markdown('<p class="data-label">Enter Website URL</p>', unsafe_allow_html=True)
url = st.text_input("Website URL", placeholder="https://example.com", label_visibility="collapsed")

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers, timeout=15)
    return BeautifulSoup(response.content, "lxml"), response.url

def extract_meta(soup):
    meta = {}
    meta["title"] = soup.title.string.strip() if soup.title else ""
    for tag in soup.find_all("meta"):
        name = tag.get("name", tag.get("property", "")).lower()
        if name in ["description", "og:description"]: meta["description"] = tag.get("content", "")
        if name in ["keywords"]: meta["keywords"] = tag.get("content", "")
        if name in ["og:site_name"]: meta["company_name"] = tag.get("content", "")
    if "company_name" not in meta: meta["company_name"] = meta.get("title", "").split("|")[0].split("-")[0].strip()
    return meta

def extract_contact(soup, text):
    contact = {}
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    contact["emails"] = list(set(emails)) if emails else []
    
    # Extract phones with context from tel: links and labeled elements
    phones_with_context = []
    seen_numbers = set()
    
    # Method 1: tel: links (most reliable)
    for a in soup.find_all("a", href=re.compile(r"tel:", re.I)):
        phone = a.get("href", "").replace("tel:", "").strip()
        if phone and phone not in seen_numbers:
            # Get context from parent or sibling text
            parent = a.find_parent(["div", "li", "p", "span"])
            context = ""
            if parent:
                parent_text = parent.get_text(" ", strip=True)
                # Extract label before the number
                match = re.search(r"([A-Za-z\s]+?)\s*:?\s*" + re.escape(a.get_text(strip=True)), parent_text)
                if match: context = match.group(1).strip()
            if not context: context = a.get("title", a.get("aria-label", "General"))
            phones_with_context.append({"number": phone, "label": context or "Phone"})
            seen_numbers.add(phone)
    
    # Method 2: Look for labeled phone patterns (limit to 10)
    phone_patterns = soup.find_all(string=re.compile(r"(phone|tel|call|fax|mobile|cell)[:\s]*", re.I))
    for pattern in phone_patterns[:10]:
        parent = pattern.find_parent()
        if parent:
            full_text = parent.get_text(" ", strip=True)
            match = re.search(r"(phone|tel|call|fax|mobile|cell)[:\s]*([\+\d\s\-\(\)\.]{7,20})", full_text, re.I)
            if match:
                label, number = match.groups()
                clean_num = re.sub(r"[^\d+]", "", number)
                if len(clean_num) >= 7 and clean_num not in seen_numbers:
                    phones_with_context.append({"number": number.strip(), "label": label.strip().title()})
                    seen_numbers.add(clean_num)
    
    contact["phones"] = phones_with_context[:15]  # Limit to 15 numbers max
    
    # Address (look for common patterns)
    addr_div = soup.find(class_=re.compile(r"address|contact|location", re.I))
    contact["address"] = addr_div.get_text(strip=True)[:200] if addr_div else ""
    return contact

def extract_social(soup, base_url):
    social = {"linkedin": "", "twitter": "", "facebook": "", "instagram": "", "youtube": ""}
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        for platform in social:
            if platform in href or (platform == "twitter" and "x.com" in href):
                social[platform] = a["href"]
                break
    return social

def extract_images(soup, base_url):
    images = []
    # Favicon
    for link in soup.find_all("link", rel=re.compile(r"icon", re.I)):
        href = link.get("href")
        if href: images.append({"type": "favicon", "url": urljoin(base_url, href)})
    
    # Logo (common patterns)
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if not src: continue
        full_url = urljoin(base_url, src)
        img_type = "logo" if re.search(r"logo", src + str(img.get("class", [])) + str(img.get("alt", "")), re.I) else "image"
        images.append({"type": img_type, "url": full_url, "alt": img.get("alt", "")})
    return images

def download_images(images, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    downloaded = []
    for i, img in enumerate(images):
        try:
            ext = Path(urlparse(img["url"]).path).suffix or ".png"
            ext = ext.split("?")[0][:5]  # Clean extension
            filename = f"{img['type']}_{i}{ext}"
            filepath = os.path.join(folder, filename)
            r = requests.get(img["url"], timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200 and len(r.content) > 100:
                with open(filepath, "wb") as f: f.write(r.content)
                downloaded.append({**img, "local_path": filepath, "content": r.content})
        except: pass
    return downloaded

def create_zip(images, filter_type=None):
    """Create a zip file from downloaded images"""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for img in images:
            if filter_type and img["type"] not in filter_type:
                continue
            if "content" in img:
                filename = Path(img["local_path"]).name
                zf.writestr(filename, img["content"])
    buffer.seek(0)
    return buffer

# Terms acceptance with localStorage persistence
import streamlit.components.v1 as components

# Initialize session state for terms
if 'terms_accepted' not in st.session_state:
    st.session_state.terms_accepted = False

# Check localStorage for previous acceptance using a component
components.html("""
<script>
    const termsAccepted = localStorage.getItem('wgc_terms_accepted') === 'true';
    if (termsAccepted) {
        // Send message to parent to indicate terms were previously accepted
        window.parent.postMessage({type: 'termsAccepted', value: true}, '*');
    }
</script>
""", height=0)

# Terms checkbox
terms_agreed = st.checkbox(
    "I agree to the Terms of Service and Privacy Policy",
    value=st.session_state.terms_accepted,
    key="terms_checkbox"
)

# Links to terms pages
st.markdown('<p style="color: var(--text-muted); font-size: 0.8rem; margin-top: -10px;">View our <a href="/Terms_of_Service" target="_blank" style="color: var(--accent-blue);">Terms of Service</a> and <a href="/Privacy_Policy" target="_blank" style="color: var(--accent-blue);">Privacy Policy</a></p>', unsafe_allow_html=True)

# Save to localStorage when checked
if terms_agreed:
    st.session_state.terms_accepted = True
    components.html("""
    <script>
        localStorage.setItem('wgc_terms_accepted', 'true');
    </script>
    """, height=0)

# Auto-check if previously accepted (runs on page load)
components.html("""
<script>
    (function() {
        const termsAccepted = localStorage.getItem('wgc_terms_accepted') === 'true';
        if (termsAccepted) {
            const checkInterval = setInterval(() => {
                const checkboxes = window.parent.document.querySelectorAll('[data-testid="stCheckbox"] input');
                for (let checkbox of checkboxes) {
                    if (!checkbox.checked) {
                        checkbox.click();
                        clearInterval(checkInterval);
                        break;
                    }
                }
            }, 200);
            setTimeout(() => clearInterval(checkInterval), 2000);
        }
    })();
</script>
""", height=0)

# Show warning if terms not accepted
if not terms_agreed:
    st.info("Please accept the Terms of Service to analyze websites", icon=":material/gavel:")

# Analyze button - only enabled when terms are accepted
if st.button("Analyze Website", type="primary", use_container_width=True, disabled=not terms_agreed) and url and terms_agreed:
    with st.spinner("Analyzing website..."):
        try:
            soup, final_url = get_soup(url if url.startswith("http") else f"https://{url}")
            text = soup.get_text()
            
            meta = extract_meta(soup)
            contact = extract_contact(soup, text)
            social = extract_social(soup, final_url)
            images = extract_images(soup, final_url)
            
            # Create export folder
            domain = urlparse(final_url).netloc.replace("www.", "")
            export_folder = Path("exports") / domain
            img_folder = export_folder / "images"
            
            # Download images
            downloaded = download_images(images, img_folder)
            
            # Success banner
            st.markdown(f"""
            <div class="success-banner">
                <i class="fas fa-check-circle"></i>
                <span>Successfully analyzed <strong>{domain}</strong></span>
                <span class="stats-badge" style="margin-left: auto;"><i class="fas fa-image"></i> {len(downloaded)} images</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display results in modern cards
            col1, col2 = st.columns(2)
            
            with col1:
                # Company Info Card
                st.markdown("""
                <div class="info-card">
                    <div class="card-header">
                        <i class="fas fa-building"></i>
                        <h3>Company Information</h3>
                    </div>
                    <div class="card-content">
                """, unsafe_allow_html=True)
                
                st.markdown(f'<p class="data-label">Company Name</p><p class="data-value">{meta.get("company_name", "Not found")}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="data-label">Description</p><p class="data-value">{meta.get("description", "Not found")[:250]}</p>', unsafe_allow_html=True)
                if meta.get("keywords"):
                    st.markdown(f'<p class="data-label">Keywords</p><p class="data-value">{meta.get("keywords", "")[:150]}</p>', unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Contact Info Card
                st.markdown("""
                <div class="info-card">
                    <div class="card-header">
                        <i class="fas fa-address-book"></i>
                        <h3>Contact Information</h3>
                    </div>
                    <div class="card-content">
                """, unsafe_allow_html=True)
                
                emails = contact.get('emails', [])
                if emails:
                    st.markdown(f'<p class="data-label">Email Addresses</p><p class="data-value">{", ".join(emails[:5])}</p>', unsafe_allow_html=True)
                
                phones = contact.get('phones', [])
                if phones:
                    st.markdown('<p class="data-label">Phone Numbers</p>', unsafe_allow_html=True)
                    phones_html = ""
                    for p in phones[:8]:
                        phones_html += f'<div class="phone-item"><span class="phone-label">{p["label"]}</span><span class="phone-number">{p["number"]}</span></div>'
                    st.markdown(phones_html, unsafe_allow_html=True)
                
                if contact.get('address'):
                    st.markdown(f'<p class="data-label" style="margin-top: 1rem;">Address</p><p class="data-value">{contact.get("address", "")[:150]}</p>', unsafe_allow_html=True)
                
                if not emails and not phones and not contact.get('address'):
                    st.markdown('<p class="data-value" style="color: var(--text-muted);">No contact information found</p>', unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
            
            with col2:
                # Social Media Card
                st.markdown("""
                <div class="info-card">
                    <div class="card-header">
                        <i class="fas fa-share-nodes"></i>
                        <h3>Social Media</h3>
                    </div>
                    <div class="card-content">
                """, unsafe_allow_html=True)
                
                social_icons = {
                    "linkedin": "fab fa-linkedin",
                    "twitter": "fab fa-x-twitter",
                    "facebook": "fab fa-facebook",
                    "instagram": "fab fa-instagram",
                    "youtube": "fab fa-youtube"
                }
                has_social = False
                for platform, link in social.items():
                    if link:
                        has_social = True
                        icon = social_icons.get(platform, "fas fa-link")
                        st.markdown(f'<a href="{link}" target="_blank" class="social-link"><i class="{icon}"></i><span>{platform.title()}</span></a>', unsafe_allow_html=True)
                
                if not has_social:
                    st.markdown('<p class="data-value" style="color: var(--text-muted);">No social media links found</p>', unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Brand Assets Preview Card
                st.markdown(f"""
                <div class="info-card">
                    <div class="card-header">
                        <i class="fas fa-palette"></i>
                        <h3>Brand Assets</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                logos = [img for img in downloaded if img["type"] in ["logo", "favicon"]]
                if logos:
                    cols = st.columns(min(len(logos), 4))
                    for i, img in enumerate(logos[:4]):
                        with cols[i]: 
                            st.image(img["local_path"], caption=img["type"].title(), width=70)
                else:
                    st.markdown('<p class="data-value" style="color: var(--text-muted);">No logos or favicons found</p>', unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Store in session state for download buttons
            st.session_state['downloaded'] = downloaded
            st.session_state['show_all_images'] = True
            st.session_state['domain'] = domain
            
            # Create CSV data
            phones_str = "; ".join([f"{p['label']}: {p['number']}" for p in contact.get("phones", [])])
            emails_str = ", ".join(contact.get("emails", []))
            
            data = {
                "URL": final_url,
                "Company Name": meta.get("company_name", ""),
                "Description": meta.get("description", ""),
                "Keywords": meta.get("keywords", ""),
                "Emails": emails_str,
                "Phones": phones_str,
                "Address": contact.get("address", ""),
                **{f"Social_{k}": v for k, v in social.items()},
                "Images_Folder": str(img_folder.absolute()),
                "Total_Images": len(downloaded),
            }
            
            df = pd.DataFrame([data])
            csv_path = export_folder / "company_data.csv"
            df.to_csv(csv_path, index=False)
            
            # Also create Excel
            xlsx_path = export_folder / "company_data.xlsx"
            df.to_excel(xlsx_path, index=False)
            
            # Download section header
            st.markdown("""
            <div class="info-card" style="margin-top: 1.5rem;">
                <div class="card-header">
                    <i class="fas fa-download"></i>
                    <h3>Export Data</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Download buttons row
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                st.download_button("CSV Data", df.to_csv(index=False), f"{domain}_data.csv", "text/csv", use_container_width=True)
            
            with btn_col2:
                icons_zip = create_zip(downloaded, filter_type=["logo", "favicon"])
                st.download_button("Icons Archive", icons_zip, f"{domain}_icons.zip", "application/zip", use_container_width=True)
            
            with btn_col3:
                all_images_zip = create_zip(downloaded)
                st.download_button("All Images", all_images_zip, f"{domain}_images.zip", "application/zip", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # See All Images expander
            if downloaded:
                with st.expander("View All Downloaded Images"):
                    # Filter tabs
                    tab_all, tab_logos, tab_images = st.tabs(["All Assets", "Logos & Icons", "Other Images"])
                    
                    with tab_all:
                        img_cols = st.columns(5)
                        for i, img in enumerate(downloaded):
                            with img_cols[i % 5]:
                                st.image(img["local_path"], caption=f"{img['type']}: {img.get('alt', '')[:20]}", use_container_width=True)
                    
                    with tab_logos:
                        logos_favicons = [img for img in downloaded if img["type"] in ["logo", "favicon"]]
                        if logos_favicons:
                            logo_cols = st.columns(4)
                            for i, img in enumerate(logos_favicons):
                                with logo_cols[i % 4]:
                                    st.image(img["local_path"], caption=img["type"].title(), use_container_width=True)
                        else:
                            st.info("No logos or favicons found")
                    
                    with tab_images:
                        other_imgs = [img for img in downloaded if img["type"] not in ["logo", "favicon"]]
                        if other_imgs:
                            other_cols = st.columns(5)
                            for i, img in enumerate(other_imgs):
                                with other_cols[i % 5]:
                                    st.image(img["local_path"], caption=img.get("alt", "")[:25] or "Image", use_container_width=True)
                        else:
                            st.info("No other images found")
            
        except Exception as e:
            st.error(f"Analysis failed: {e}")

# Footer
st.markdown("""
<div class="modern-footer">
    <div class="footer-brand"><i class="fas fa-globe"></i>Web Grab & Capture</div>
    <p class="footer-text">Professional website analysis and brand asset extraction</p>
    <p class="footer-nav"><i class="fas fa-compass"></i>Navigate using the sidebar menu</p>
    <p class="footer-copyright">2026 Web Grab & Capture. Built with precision.</p>
</div>
""", unsafe_allow_html=True)
