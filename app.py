from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from lead_scraper import LeadScraper

# Load environment variables
load_dotenv()

# Debug: Print environment variable status
api_key = os.getenv('BROWSER_USE_API_KEY')
if api_key:
    print(f"✅ BROWSER_USE_API_KEY loaded: {api_key[:20]}...")
else:
    print("❌ WARNING: BROWSER_USE_API_KEY not found in environment!")
    print(f"Available env vars: {list(os.environ.keys())}")

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

lead_scraper = LeadScraper()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/leads', methods=['POST'])
def get_leads():
    try:
        data = request.json
        query = data.get('query', '')
        num_leads = data.get('num_leads', 20)
        email = data.get('email', '')
        require_email = data.get('require_email', False)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if num_leads > 100:
            num_leads = 100
        
        print(f"Fetching {num_leads} leads for query: {query}")
        print(f"Email extraction: {'ENABLED' if require_email else 'DISABLED'}")
        print(f"Results will be sent to: {email}")
        
        leads = lead_scraper.scrape_google_maps(query, num_leads, require_email)
        
        return jsonify({
            'success': True,
            'leads': leads,
            'count': len(leads),
            'email': email
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    api_key = os.getenv('BROWSER_USE_API_KEY')
    return jsonify({
        'status': 'ok', 
        'service': 'Google Maps Lead Scraper',
        'api_key_configured': bool(api_key),
        'api_key_preview': api_key[:20] + '...' if api_key else None
    })

@app.route('/api/debug', methods=['GET'])
def debug():
    """Debug endpoint to check environment variables"""
    api_key = os.getenv('BROWSER_USE_API_KEY')
    return jsonify({
        'api_key_found': bool(api_key),
        'api_key_length': len(api_key) if api_key else 0,
        'api_key_preview': api_key[:10] + '...' if api_key else None,
        'has_client': lead_scraper.client is not None,
        'env_vars_count': len(os.environ)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
