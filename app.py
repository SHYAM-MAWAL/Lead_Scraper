from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from lead_scraper import LeadScraper

load_dotenv()

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
    return jsonify({'status': 'running', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
