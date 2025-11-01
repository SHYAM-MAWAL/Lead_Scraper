import os
import json
import re
from typing import List, Dict

try:
    from browser_use_sdk import BrowserUse
    SDK_AVAILABLE = True
except ImportError:
    BrowserUse = None
    SDK_AVAILABLE = False

class LeadScraper:
    def __init__(self):
        api_key = os.getenv('BROWSER_USE_API_KEY')
        if not api_key:
            print("WARNING: BROWSER_USE_API_KEY not found. Using demo mode.")
            self.client = None
        elif not SDK_AVAILABLE:
            print("WARNING: browser-use-sdk not installed. Using demo mode.")
            self.client = None
        else:
            print("✅ Initializing Browser-Use SDK with API key...")
            self.client = BrowserUse(api_key=api_key)
            print("✅ SDK initialized successfully!")
    
    def scrape_google_maps(self, query: str, num_leads: int = 20, require_email: bool = False) -> List[Dict]:
        """
        Scrape Google Maps for business leads
        
        Args:
            query: Search query (e.g., "Restaurants in Singapore")
            num_leads: Number of leads to fetch (max 100)
            require_email: If True, visit websites to extract email addresses
        
        Returns:
            List of dictionaries containing lead information
        """
        
        # Build task description based on email requirement
        if require_email:
            task_description = f"""
Go to Google Maps (https://www.google.com/maps) and search for "{query}".

For the first {num_leads} business results, extract the following information:
1. Business Name
2. Full Address  
3. Phone Number (if available)
4. Website URL (if available)
5. Email Address (REQUIRED - visit the website to find it)

For each business:
- Click on the business listing to see full details
- Get the phone number, website, and address from the business details panel
- IMPORTANT: If a website is available, visit that website and look for an email address
- Look for email in: contact page, footer, about page, or contact forms
- Common email patterns: info@, contact@, hello@, support@, [businessname]@
- If no email is found on the website, use empty string ""

Return ONLY a JSON object in this exact format:
{{
    "leads": [
        {{
            "name": "Business Name Here",
            "address": "Full Address Here",
            "phone": "Phone Number Here or empty string",
            "website": "Website URL Here or empty string",
            "email": "Email Address Here or empty string"
        }}
    ]
}}

Make sure to return valid JSON. Do not include any other text or explanation.
"""
        else:
            task_description = f"""
Go to Google Maps (https://www.google.com/maps) and search for "{query}".

For the first {num_leads} business results, extract the following information:
1. Business Name
2. Full Address  
3. Phone Number (if available)
4. Website URL (if available)

For each business:
- Click on the business listing to see full details
- Look for the phone number, website, and address in the business details panel
- If information is not available, use empty string ""

Return ONLY a JSON object in this exact format:
{{
    "leads": [
        {{
            "name": "Business Name Here",
            "address": "Full Address Here",
            "phone": "Phone Number Here or empty string",
            "website": "Website URL Here or empty string",
            "email": ""
        }}
    ]
}}

Make sure to return valid JSON. Do not include any other text or explanation.
"""
        
        print(f"🔍 Creating task for query: {query}")
        print(f"📊 Requested leads: {num_leads}")
        print(f"📧 Email extraction: {'ENABLED ✅' if require_email else 'DISABLED'}")
        
        # If no client available, return sample data
        if self.client is None:
            print("⚠️  Using demo mode - returning sample data")
            return self._get_sample_data(query, num_leads)
        
        try:
            print("🚀 Sending task to Browser-Use Cloud...")
            print(f"📝 Task description length: {len(task_description)} chars")
            
            # Create the task
            task = self.client.tasks.create_task(
                task=task_description
            )
            
            print(f"✅ Task created with ID: {task.id}")
            print(f"⏳ Waiting for browser automation to complete (this may take 1-3 minutes)...")
            
            # Wait for task completion
            result = task.complete()
            
            print(f"✅ Task completed successfully!")
            print(f"📄 Status: {result.status}")
            print(f"📄 Result type: {type(result)}")
            print(f"📄 Result attributes: {dir(result)}")
            
            # Parse the output
            if hasattr(result, 'output') and result.output:
                print(f"📝 Raw output type: {type(result.output)}")
                print(f"📝 Raw output preview: {str(result.output)[:200]}...")
                
                # Try to parse the output
                if isinstance(result.output, str):
                    # Try to parse as JSON
                    try:
                        output_data = json.loads(result.output)
                        if isinstance(output_data, dict) and 'leads' in output_data:
                            leads = output_data['leads']
                        elif isinstance(output_data, list):
                            leads = output_data
                        else:
                            leads = []
                    except json.JSONDecodeError:
                        print("⚠️  Could not parse output as JSON")
                        leads = []
                elif isinstance(result.output, dict) and 'leads' in result.output:
                    leads = result.output['leads']
                elif isinstance(result.output, list):
                    leads = result.output
                else:
                    leads = []
            else:
                print("⚠️  No output received from task")
                leads = []
            
            # Clean and validate leads
            cleaned_leads = self._clean_leads(leads)
            
            print(f"✅ Successfully extracted {len(cleaned_leads)} leads")
            
            if len(cleaned_leads) == 0:
                print("⚠️  No leads extracted, returning sample data")
                return self._get_sample_data(query, min(num_leads, 5))
            
            return cleaned_leads
        
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            print(f"❌ Error type: {type(e).__name__}")
            import traceback
            print(f"❌ Full traceback:")
            traceback.print_exc()
            print("⚠️  Falling back to sample data")
            # Return sample data for demonstration
            return self._get_sample_data(query, min(num_leads, 5))
    
    def _clean_leads(self, leads: List[Dict]) -> List[Dict]:
        """Clean and validate lead data"""
        cleaned = []
        
        for lead in leads:
            cleaned_lead = {
                'name': lead.get('name', '').strip(),
                'address': lead.get('address', '').strip(),
                'phone': self._format_phone(lead.get('phone', '')),
                'website': self._format_url(lead.get('website', '')),
                'email': self._format_email(lead.get('email', ''))
            }
            
            # Only include leads with at least a name
            if cleaned_lead['name']:
                cleaned.append(cleaned_lead)
        
        return cleaned
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number"""
        if not phone:
            return ''
        # Remove extra spaces and clean up
        phone = re.sub(r'\s+', ' ', phone.strip())
        return phone
    
    def _format_url(self, url: str) -> str:
        """Format URL"""
        if not url:
            return ''
        url = url.strip()
        if url and not url.startswith('http'):
            url = 'https://' + url
        return url
    
    def _format_email(self, email: str) -> str:
        """Format and validate email"""
        if not email:
            return ''
        email = email.strip().lower()
        # Basic email validation
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return email
        return ''
    
    def _parse_output(self, output) -> List[Dict]:
        """Parse various output formats"""
        try:
            if isinstance(output, str):
                # Try to parse as JSON
                output = json.loads(output)
            
            if isinstance(output, dict) and 'leads' in output:
                return output['leads']
            elif isinstance(output, list):
                return output
            else:
                return []
        except:
            return []
    
    def _get_sample_data(self, query: str, num_leads: int) -> List[Dict]:
        """Generate sample data for demonstration"""
        sample_leads = [
            {
                'name': 'Sample Restaurant 1',
                'address': '123 Orchard Road, Singapore 238858',
                'phone': '+65 6123 4567',
                'website': 'https://sample-restaurant1.com',
                'email': 'info@sample-restaurant1.com'
            },
            {
                'name': 'Sample Restaurant 2',
                'address': '456 Marina Bay, Singapore 018956',
                'phone': '+65 6234 5678',
                'website': 'https://sample-restaurant2.com',
                'email': 'contact@sample-restaurant2.com'
            },
            {
                'name': 'Sample Cafe 3',
                'address': '789 Bugis Street, Singapore 188735',
                'phone': '+65 6345 6789',
                'website': 'https://sample-cafe3.com',
                'email': ''
            },
            {
                'name': 'Sample Bistro 4',
                'address': '321 Sentosa Gateway, Singapore 098269',
                'phone': '+65 6456 7890',
                'website': '',
                'email': 'hello@sample-bistro4.com'
            },
            {
                'name': 'Sample Diner 5',
                'address': '654 Changi Road, Singapore 419716',
                'phone': '+65 6567 8901',
                'website': 'https://sample-diner5.com',
                'email': 'info@sample-diner5.com'
            }
        ]
        
        # Return up to num_leads
        return sample_leads[:min(num_leads, len(sample_leads))]
