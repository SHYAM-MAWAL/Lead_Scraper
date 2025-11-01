# Google Maps Lead Generator

A powerful lead generation tool that extracts business information from Google Maps including name, address, phone number, website, and email.

## Features

- 🎯 Search Google Maps for any business type or location
- 📊 Extract up to 100 leads per search
- 📧 Get Name, Address, Phone, Website, and Email
- 💾 Export results to CSV or JSON
- 🎨 Beautiful, responsive UI
- ⚡ Fast and automated using Browser-Use Cloud

## Setup

1. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

2. **Get Browser-Use API Key**
   - Visit https://cloud.browser-use.com/
   - Sign up and get your API key

3. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add your API key:
   ```
   BROWSER_USE_API_KEY=bu_your_api_key_here
   ```

4. **Run the Application**
```powershell
python app.py
```

5. **Open in Browser**
   - Go to http://localhost:5000

## Usage

1. Enter your search query (e.g., "Restaurants in Singapore")
2. Specify how many leads you want (max 100)
3. Enter your email address
4. Click "Get Leads Now"
5. Wait for results (may take a few minutes)
6. Export results as CSV or JSON

## Project Structure

```
GoogleMap_Lead/
├── app.py              # Flask web server
├── lead_scraper.py     # Lead scraping logic
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create from .env.example)
├── .env.example       # Example environment file
├── static/
│   ├── index.html     # Frontend interface
│   ├── styles.css     # Styling
│   └── script.js      # Frontend logic
└── README.md          # This file
```

## API Endpoints

- `GET /` - Main web interface
- `POST /api/leads` - Fetch leads
  - Body: `{ "query": string, "num_leads": number, "email": string }`
- `GET /api/status` - Check API status

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, JavaScript
- **Automation**: Browser-Use Cloud
- **API**: RESTful API

## Notes

- Maximum 100 leads per request
- Processing time depends on number of leads requested
- Browser-Use Cloud handles browser automation
- Results include all available business information

## License

MIT License
