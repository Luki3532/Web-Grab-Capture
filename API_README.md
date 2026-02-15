# Web Grab & Capture API

A RESTful API for extracting company information, contact details, social media links, and images from any website.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API Server

```bash
uvicorn api:app --reload --port 8000
```

### 3. Open API Documentation

Navigate to **http://localhost:8000/docs** for interactive Swagger UI documentation.

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scrape` | GET | Extract all data from a website |
| `/api/contact` | GET | Extract emails and phone numbers only |
| `/api/social` | GET | Extract social media links only |
| `/api/images` | GET | Download all images as ZIP |
| `/api/icons` | GET | Download logos/favicons as ZIP |
| `/health` | GET | Health check |

---

## Usage Examples

### Python

```python
import requests

# Scrape all data
response = requests.get("http://localhost:8000/api/scrape", params={"url": "https://example.com"})
data = response.json()

print(f"Company: {data['company']['name']}")
print(f"Emails: {data['contact']['emails']}")
print(f"Phones: {[p['number'] for p in data['contact']['phones']]}")
print(f"Images found: {data['image_count']}")

# Download images
response = requests.get("http://localhost:8000/api/images", params={"url": "https://example.com"})
with open("images.zip", "wb") as f:
    f.write(response.content)
```

### JavaScript / Node.js

```javascript
// Using fetch
const response = await fetch('http://localhost:8000/api/scrape?url=https://example.com');
const data = await response.json();

console.log('Company:', data.company.name);
console.log('Emails:', data.contact.emails);
console.log('Social:', data.social);
```

### cURL

```bash
# Get all data
curl "http://localhost:8000/api/scrape?url=https://example.com"

# Get contact info only
curl "http://localhost:8000/api/contact?url=https://example.com"

# Download images
curl -o images.zip "http://localhost:8000/api/images?url=https://example.com"
```

### PowerShell

```powershell
# Scrape website
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/scrape?url=https://example.com"
$response.company.name
$response.contact.emails

# Download images
Invoke-WebRequest -Uri "http://localhost:8000/api/images?url=https://example.com" -OutFile "images.zip"
```

---

## Response Schema

### `/api/scrape` Response

```json
{
  "success": true,
  "url": "https://example.com",
  "company": {
    "name": "Example Company",
    "description": "We do amazing things",
    "keywords": "tech, innovation",
    "title": "Example Company | Home"
  },
  "contact": {
    "emails": ["hello@example.com", "support@example.com"],
    "phones": [
      {"number": "+1 (555) 123-4567", "label": "Sales"},
      {"number": "+1 (555) 987-6543", "label": "Support"}
    ],
    "address": "123 Main St, City, State 12345"
  },
  "social": {
    "linkedin": "https://linkedin.com/company/example",
    "twitter": "https://twitter.com/example",
    "facebook": "https://facebook.com/example",
    "instagram": null,
    "youtube": null
  },
  "images": [
    {"type": "favicon", "url": "https://example.com/favicon.ico", "alt": "favicon"},
    {"type": "logo", "url": "https://example.com/logo.png", "alt": "Company Logo"},
    {"type": "image", "url": "https://example.com/hero.jpg", "alt": "Hero image"}
  ],
  "image_count": 15,
  "logo_count": 3
}
```

---

## Running Both Services

You can run the Streamlit UI and API simultaneously:

```bash
# Terminal 1 - Streamlit UI (port 8501)
streamlit run app.py

# Terminal 2 - REST API (port 8000)
uvicorn api:app --reload --port 8000
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Failed to fetch URL: Connection timeout"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Invalid URL or request error
- `404` - No images/data found
- `500` - Server error

---

## License

MIT License - Lucas E. Carpenter © 2026
