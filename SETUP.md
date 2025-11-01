# SETUP INSTRUCTIONS

## Quick Start Guide

### Step 1: Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

### Step 2: Get Your Browser-Use API Key

1. Visit: https://cloud.browser-use.com/
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key (starts with `bu_`)
5. Copy the API key

### Step 3: Configure Your API Key

Open the `.env` file and replace `bu_your_api_key_here` with your actual API key:

```
BROWSER_USE_API_KEY=bu_1234567890abcdef...
```

### Step 4: Run the Application

Option A - Using the batch file:
```powershell
.\run.bat
```

Option B - Direct command:
```powershell
python app.py
```

### Step 5: Access the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

## How to Use

1. **Enter Search Query**: Type what you're looking for (e.g., "Restaurants in Singapore", "Hotels in New York")
2. **Set Number of Leads**: Choose how many leads you want (1-100)
3. **Enter Email**: Provide your email address
4. **Click "Get Leads Now"**: Wait for the results
5. **Export Data**: Download results as CSV or JSON

## Features Included

✅ Search Google Maps for any business type
✅ Extract business information:
   - Business Name
   - Full Address
   - Phone Number
   - Website URL
   - Email Address (when available)
✅ Export to CSV format
✅ Export to JSON format
✅ Beautiful responsive UI
✅ Real-time progress indication

## Demo Mode

If you run the application without the API key, it will work in DEMO MODE with sample data. This is useful for:
- Testing the interface
- Understanding how the application works
- Development and debugging

To use real Google Maps data, you MUST configure a valid Browser-Use API key.

## Troubleshooting

### Issue: Import errors
**Solution**: Make sure all dependencies are installed
```powershell
pip install -r requirements.txt
```

### Issue: API key not working
**Solution**: 
1. Check that your .env file exists
2. Verify the API key is correct
3. Make sure there are no extra spaces
4. Ensure the key starts with "bu_"

### Issue: Port 5000 already in use
**Solution**: Modify app.py and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Issue: Browser automation fails
**Solution**:
1. Check your Browser-Use account credits
2. Verify your API key is active
3. Check the console for error messages

## Project Structure

```
GoogleMap_Lead/
├── app.py                 # Main Flask application
├── lead_scraper.py        # Lead scraping logic
├── requirements.txt       # Python dependencies
├── .env                   # Your API key (create from .env.example)
├── .env.example          # Template for .env
├── run.bat               # Quick start script
├── SETUP.md              # This file
├── README.md             # Project documentation
└── static/
    ├── index.html        # Web interface
    ├── styles.css        # Styling
    └── script.js         # Frontend functionality
```

## API Pricing

Browser-Use Cloud operates on a credit-based system. Check:
- https://cloud.browser-use.com/pricing

Free tier usually includes:
- Limited number of tasks per month
- Basic browser automation features

## Support

For issues related to:
- **Browser-Use API**: https://docs.cloud.browser-use.com/
- **This Project**: Check the code comments and README.md

## Next Steps

1. Get your API key from Browser-Use
2. Configure the .env file
3. Run the application
4. Start generating leads!

Enjoy generating leads! 🎯
