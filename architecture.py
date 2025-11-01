"""
Google Maps Lead Generator
Data Flow Diagram
"""

"""
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (Browser)                     │
│                     http://localhost:5000                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  🎯 Get Your Leads                                        │  │
│  │                                                            │  │
│  │  What are you looking for?                                │  │
│  │  [Restaurants in Singapore...........................]  │  │
│  │                                                            │  │
│  │  Number of Leads (Max 100)                                │  │
│  │  [20]                                                     │  │
│  │                                                            │  │
│  │  Email Address                                            │  │
│  │  [your@email.com...................................]  │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │ ⚡ Get Leads Now                                │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                      │
│                            │ HTTP POST Request                    │
│                            ▼                                      │
└─────────────────────────────────────────────────────────────────┘

                             ┌──────────────┐
                             │  Flask API   │
                             │  app.py      │
                             └──────────────┘
                                    │
                                    │ Calls
                                    ▼
                        ┌────────────────────────┐
                        │   Lead Scraper         │
                        │   lead_scraper.py      │
                        └────────────────────────┘
                                    │
                    ┌──────────────┴──────────────┐
                    │                              │
                    ▼                              ▼
           ┌────────────────┐          ┌──────────────────┐
           │  DEMO MODE     │          │  REAL MODE       │
           │  Sample Data   │          │  Browser-Use SDK │
           └────────────────┘          └──────────────────┘
                    │                              │
                    │                              │
                    │                              ▼
                    │                    ┌──────────────────┐
                    │                    │  Google Maps     │
                    │                    │  Automation      │
                    │                    └──────────────────┘
                    │                              │
                    │                              │ Extracts
                    │                              ▼
                    │                    ┌──────────────────┐
                    │                    │  - Name          │
                    │                    │  - Address       │
                    │                    │  - Phone         │
                    │                    │  - Website       │
                    │                    │  - Email         │
                    │                    └──────────────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   │
                                   │ Returns JSON
                                   ▼
                        ┌────────────────────────┐
                        │   Lead Data Array      │
                        │   [{...}, {...}, ...]  │
                        └────────────────────────┘
                                   │
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RESULTS DISPLAY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Lead Results                                             │  │
│  │                                                            │  │
│  │  Query: Restaurants in Singapore                          │  │
│  │  Leads Found: 5                                           │  │
│  │  Results sent to: your@email.com                          │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │ # │ Name │ Address │ Phone │ Website │ Email        │ │  │
│  │  ├─────────────────────────────────────────────────────┤ │  │
│  │  │ 1 │ Rest1│ 123 St  │ +65...│ Visit   │ info@...     │ │  │
│  │  │ 2 │ Rest2│ 456 Ave │ +65...│ Visit   │ contact@...  │ │  │
│  │  │ 3 │ Cafe3│ 789 Rd  │ +65...│ Visit   │ -            │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  [📥 Download CSV]  [📄 Download JSON]                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
"""

# File Structure and Responsibility

FILES = {
    "Frontend": {
        "static/index.html": "User interface structure",
        "static/styles.css": "Visual styling and layout",
        "static/script.js": "Form handling, API calls, export functions"
    },
    
    "Backend": {
        "app.py": "Flask server, API endpoints, request handling",
        "lead_scraper.py": "Lead extraction logic, data processing"
    },
    
    "Configuration": {
        ".env": "API keys and environment variables",
        "requirements.txt": "Python package dependencies",
        ".gitignore": "Files to exclude from version control"
    },
    
    "Documentation": {
        "README.md": "Project overview and introduction",
        "SETUP.md": "Detailed setup instructions",
        "QUICK_START.md": "Quick reference guide",
        "PROJECT_SUMMARY.md": "Complete project summary"
    },
    
    "Utilities": {
        "run.bat": "Windows batch script to start server",
        "test_api.py": "API testing script"
    }
}

# API Flow

API_FLOW = """
1. User fills form on frontend
2. JavaScript sends POST request to /api/leads
3. Flask receives and validates request
4. LeadScraper.scrape_google_maps() is called
5. If Browser-Use SDK available:
   - Automates browser to visit Google Maps
   - Searches for query
   - Clicks on each result
   - Extracts business information
   - Returns structured data
6. If no SDK (Demo Mode):
   - Returns sample data
7. Data is cleaned and formatted
8. JSON response sent back to frontend
9. Frontend displays results in table
10. User can export as CSV or JSON
"""

# Technology Stack

TECH_STACK = {
    "Frontend": {
        "HTML5": "Structure",
        "CSS3": "Styling with gradients and animations",
        "JavaScript": "Client-side logic and API calls",
        "Fetch API": "HTTP requests"
    },
    
    "Backend": {
        "Python 3.x": "Programming language",
        "Flask": "Web framework",
        "Flask-CORS": "Cross-origin resource sharing",
        "python-dotenv": "Environment variable management"
    },
    
    "Optional": {
        "browser-use-sdk": "Browser automation for real Google Maps scraping"
    },
    
    "Data Formats": {
        "JSON": "API responses and export",
        "CSV": "Export format"
    }
}

# Features Checklist

FEATURES = {
    "✅ Search Functionality": [
        "Custom query input",
        "Configurable lead count (1-100)",
        "Email notification support"
    ],
    
    "✅ Data Extraction": [
        "Business name",
        "Full address",
        "Phone number",
        "Website URL",
        "Email address"
    ],
    
    "✅ Export Options": [
        "Download as CSV",
        "Download as JSON"
    ],
    
    "✅ User Experience": [
        "Loading indicators",
        "Error handling",
        "Input validation",
        "Responsive design",
        "Professional UI"
    ],
    
    "✅ Modes": [
        "Demo mode (sample data)",
        "Real mode (Google Maps automation)"
    ]
}

print(__doc__)
print("\n" + "="*60)
print("DATA FLOW VISUALIZATION COMPLETE")
print("="*60)
