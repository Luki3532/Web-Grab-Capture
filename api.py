"""
Web Grab & Capture API
=======================
A RESTful API for extracting company information, contact details, 
social media links, and images from any website.

Run with: uvicorn api:app --reload --port 8000
Docs at: http://localhost:8000/docs
"""

# Use system CA certificates for SSL verification
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import io
import zipfile
from pathlib import Path

# ============== API Setup ==============

app = FastAPI(
    title="Web Grab & Capture API",
    description="""
## Extract website data programmatically

This API allows you to scrape and extract:
- **Company information** (name, description, keywords)
- **Contact details** (emails, phone numbers with labels, addresses)
- **Social media links** (LinkedIn, Twitter/X, Facebook, Instagram, YouTube)
- **Images** (logos, favicons, all images)

### Quick Start
```python
import requests

response = requests.get("https://lucascode.org/webgrab-api/api/scrape", params={"url": "https://example.com"})
data = response.json()
print(data["company"]["name"])
```
    """,
    version="1.0.0",
    root_path="/webgrab-api",
    contact={
        "name": "Lucas E. Carpenter",
        "url": "https://lucascode.org",
        "email": "contact@lucascode.org"
    },
    license_info={
        "name": "MIT",
    }
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== Models ==============

class PhoneNumber(BaseModel):
    number: str = Field(..., description="Phone number")
    label: str = Field(..., description="Context label (e.g., Sales, Support, Main)")

class ContactInfo(BaseModel):
    emails: List[str] = Field(default_factory=list, description="Email addresses found")
    phones: List[PhoneNumber] = Field(default_factory=list, description="Phone numbers with labels")
    address: Optional[str] = Field(None, description="Physical address if found")

class SocialMedia(BaseModel):
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None

class ImageInfo(BaseModel):
    type: str = Field(..., description="Image type: favicon, logo, or image")
    url: str = Field(..., description="Full URL to the image")
    alt: Optional[str] = Field(None, description="Alt text if available")

class CompanyInfo(BaseModel):
    name: Optional[str] = Field(None, description="Company or website name")
    description: Optional[str] = Field(None, description="Meta description")
    keywords: Optional[str] = Field(None, description="Meta keywords")
    title: Optional[str] = Field(None, description="Page title")

class ScrapeResponse(BaseModel):
    success: bool
    url: str = Field(..., description="Final URL after redirects")
    company: CompanyInfo
    contact: ContactInfo
    social: SocialMedia
    images: List[ImageInfo]
    image_count: int
    logo_count: int

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None

# ============== Core Functions ==============

def get_soup(url: str):
    """Fetch and parse a webpage"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.content, "lxml"), response.url

def extract_meta(soup) -> dict:
    """Extract company/meta information"""
    meta = {}
    meta["title"] = soup.title.string.strip() if soup.title and soup.title.string else ""
    for tag in soup.find_all("meta"):
        name = tag.get("name", tag.get("property", "")).lower()
        if name in ["description", "og:description"]:
            meta["description"] = tag.get("content", "")
        if name in ["keywords"]:
            meta["keywords"] = tag.get("content", "")
        if name in ["og:site_name"]:
            meta["company_name"] = tag.get("content", "")
    if "company_name" not in meta:
        meta["company_name"] = meta.get("title", "").split("|")[0].split("-")[0].strip()
    return meta

def extract_contact(soup, text: str) -> dict:
    """Extract contact information"""
    contact = {"emails": [], "phones": [], "address": ""}
    
    # Emails
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    contact["emails"] = list(set(emails)) if emails else []
    
    # Phones with context
    phones_with_context = []
    seen_numbers = set()
    
    # Method 1: tel: links
    for a in soup.find_all("a", href=re.compile(r"tel:", re.I)):
        phone = a.get("href", "").replace("tel:", "").strip()
        if phone and phone not in seen_numbers:
            parent = a.find_parent(["div", "li", "p", "span"])
            context = ""
            if parent:
                parent_text = parent.get_text(" ", strip=True)
                match = re.search(r"([A-Za-z\s]+?)\s*:?\s*" + re.escape(a.get_text(strip=True)), parent_text)
                if match:
                    context = match.group(1).strip()
            if not context:
                context = a.get("title", a.get("aria-label", "General"))
            phones_with_context.append({"number": phone, "label": context or "Phone"})
            seen_numbers.add(phone)
    
    # Method 2: Labeled phone patterns
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
    
    contact["phones"] = phones_with_context[:15]
    
    # Address
    addr_div = soup.find(class_=re.compile(r"address|contact|location", re.I))
    contact["address"] = addr_div.get_text(strip=True)[:200] if addr_div else ""
    
    return contact

def extract_social(soup, base_url: str) -> dict:
    """Extract social media links"""
    social = {"linkedin": "", "twitter": "", "facebook": "", "instagram": "", "youtube": ""}
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        for platform in social:
            if platform in href or (platform == "twitter" and "x.com" in href):
                social[platform] = a["href"]
                break
    return social

def extract_images(soup, base_url: str) -> list:
    """Extract all images including favicons and logos"""
    images = []
    
    # Favicons
    for link in soup.find_all("link", rel=re.compile(r"icon", re.I)):
        href = link.get("href")
        if href:
            images.append({"type": "favicon", "url": urljoin(base_url, href), "alt": "favicon"})
    
    # Images
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if not src:
            continue
        full_url = urljoin(base_url, src)
        img_type = "logo" if re.search(r"logo", src + str(img.get("class", [])) + str(img.get("alt", "")), re.I) else "image"
        images.append({"type": img_type, "url": full_url, "alt": img.get("alt", "")})
    
    return images

def download_images_to_zip(images: list, filter_type: list = None) -> io.BytesIO:
    """Download images and create a ZIP archive"""
    buffer = io.BytesIO()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, img in enumerate(images):
            if filter_type and img["type"] not in filter_type:
                continue
            try:
                r = requests.get(img["url"], timeout=10, headers=headers)
                if r.status_code == 200 and len(r.content) > 100:
                    ext = Path(urlparse(img["url"]).path).suffix or ".png"
                    ext = ext.split("?")[0][:5]
                    filename = f"{img['type']}_{i}{ext}"
                    zf.writestr(filename, r.content)
            except:
                pass
    
    buffer.seek(0)
    return buffer

# ============== API Endpoints ==============

@app.get("/", tags=["Info"])
async def root():
    """API welcome message and quick links"""
    return {
        "message": "Web Grab & Capture API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "scrape": "/api/scrape?url=https://example.com",
            "images": "/api/images?url=https://example.com",
            "icons": "/api/icons?url=https://example.com"
        }
    }

@app.get("/health", tags=["Info"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get(
    "/api/scrape",
    response_model=ScrapeResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    tags=["Scraping"],
    summary="Scrape website data",
    description="Extract company info, contact details, social links, and image URLs from a website."
)
async def scrape_website(
    url: str = Query(..., description="The website URL to scrape (e.g., https://example.com)")
):
    """
    Scrape a website and extract all available information.
    
    Returns:
    - **company**: Name, description, keywords, title
    - **contact**: Emails, phone numbers with labels, address
    - **social**: Links to LinkedIn, Twitter, Facebook, Instagram, YouTube
    - **images**: List of all images with type (favicon/logo/image) and URLs
    """
    try:
        # Ensure URL has protocol
        if not url.startswith("http"):
            url = f"https://{url}"
        
        soup, final_url = get_soup(url)
        text = soup.get_text()
        
        meta = extract_meta(soup)
        contact = extract_contact(soup, text)
        social = extract_social(soup, final_url)
        images = extract_images(soup, final_url)
        
        logos = [img for img in images if img["type"] in ["logo", "favicon"]]
        
        return ScrapeResponse(
            success=True,
            url=final_url,
            company=CompanyInfo(
                name=meta.get("company_name"),
                description=meta.get("description"),
                keywords=meta.get("keywords"),
                title=meta.get("title")
            ),
            contact=ContactInfo(
                emails=contact["emails"],
                phones=[PhoneNumber(**p) for p in contact["phones"]],
                address=contact["address"] or None
            ),
            social=SocialMedia(**social),
            images=[ImageInfo(**img) for img in images],
            image_count=len(images),
            logo_count=len(logos)
        )
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")

@app.get(
    "/api/images",
    tags=["Downloads"],
    summary="Download all images as ZIP",
    description="Download all images from a website as a ZIP archive."
)
async def download_all_images(
    url: str = Query(..., description="The website URL to scrape")
):
    """Download all images from a website as a ZIP file"""
    try:
        if not url.startswith("http"):
            url = f"https://{url}"
        
        soup, final_url = get_soup(url)
        images = extract_images(soup, final_url)
        
        if not images:
            raise HTTPException(status_code=404, detail="No images found on this page")
        
        domain = urlparse(final_url).netloc.replace("www.", "")
        zip_buffer = download_images_to_zip(images)
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={domain}_images.zip"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    "/api/icons",
    tags=["Downloads"],
    summary="Download logos and favicons as ZIP",
    description="Download only logos and favicons from a website as a ZIP archive."
)
async def download_icons(
    url: str = Query(..., description="The website URL to scrape")
):
    """Download logos and favicons as a ZIP file"""
    try:
        if not url.startswith("http"):
            url = f"https://{url}"
        
        soup, final_url = get_soup(url)
        images = extract_images(soup, final_url)
        
        icons = [img for img in images if img["type"] in ["logo", "favicon"]]
        if not icons:
            raise HTTPException(status_code=404, detail="No logos or favicons found")
        
        domain = urlparse(final_url).netloc.replace("www.", "")
        zip_buffer = download_images_to_zip(images, filter_type=["logo", "favicon"])
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={domain}_icons.zip"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    "/api/contact",
    tags=["Scraping"],
    summary="Extract contact info only",
    description="Quick endpoint to extract just emails and phone numbers."
)
async def get_contact_only(
    url: str = Query(..., description="The website URL to scrape")
):
    """Extract only contact information (emails and phones)"""
    try:
        if not url.startswith("http"):
            url = f"https://{url}"
        
        soup, final_url = get_soup(url)
        text = soup.get_text()
        contact = extract_contact(soup, text)
        
        return {
            "success": True,
            "url": final_url,
            "emails": contact["emails"],
            "phones": contact["phones"],
            "address": contact["address"] or None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    "/api/social",
    tags=["Scraping"],
    summary="Extract social media links only",
    description="Quick endpoint to extract just social media profile links."
)
async def get_social_only(
    url: str = Query(..., description="The website URL to scrape")
):
    """Extract only social media links"""
    try:
        if not url.startswith("http"):
            url = f"https://{url}"
        
        soup, final_url = get_soup(url)
        social = extract_social(soup, final_url)
        
        # Filter out empty values
        found_social = {k: v for k, v in social.items() if v}
        
        return {
            "success": True,
            "url": final_url,
            "social": found_social,
            "count": len(found_social)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
