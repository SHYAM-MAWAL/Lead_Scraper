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

Return ONLY a valid JSON object. Do not include any explanatory text before or after the JSON.
The response must start with {{ and end with }}.

Format:
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

IMPORTANT: Return ONLY the JSON object above, nothing else. No introduction, no conclusion, just the JSON.
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

Return ONLY a valid JSON object. Do not include any explanatory text before or after the JSON.
The response must start with {{ and end with }}.

Format:
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

IMPORTANT: Return ONLY the JSON object above, nothing else. No introduction, no conclusion, just the JSON.
"""
        
        print(f"🔍 Creating task for query: {query}")
        print(f"📊 Requested leads: {num_leads}")
        print(f"📧 Email extraction: {'ENABLED ✅' if require_email else 'DISABLED'}")
        
        # If no client available, raise error
        if self.client is None:
            error_msg = "Browser-Use SDK not initialized. BROWSER_USE_API_KEY environment variable is missing or invalid."
            print(f"❌ ERROR: {error_msg}")
            raise ValueError(error_msg)
        
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
                print(f"📝 Raw output: {str(result.output)}")
                
                # Try to parse the output
                if isinstance(result.output, str):
                    # Try to find JSON in the output (might be wrapped in text)
                    import re
                    
                    # Look for JSON object in the output
                    json_match = re.search(r'\{[\s\S]*"leads"[\s\S]*\}', result.output)
                    if json_match:
                        try:
                            output_data = json.loads(json_match.group(0))
                            if isinstance(output_data, dict) and 'leads' in output_data:
                                leads = output_data['leads']
                                print(f"✅ Extracted {len(leads)} leads from JSON")
                            else:
                                print(f"⚠️  JSON found but no 'leads' key")
                                leads = []
                        except json.JSONDecodeError as e:
                            print(f"⚠️  JSON parsing error: {e}")
                            print(f"⚠️  Matched text: {json_match.group(0)[:200]}...")
                            leads = []
                    else:
                        # Try direct JSON parse
                        try:
                            output_data = json.loads(result.output)
                            if isinstance(output_data, dict) and 'leads' in output_data:
                                leads = output_data['leads']
                            elif isinstance(output_data, list):
                                leads = output_data
                            else:
                                leads = []
                        except json.JSONDecodeError:
                            print(f"⚠️  Could not parse output as JSON")
                            print(f"⚠️  Output was: {result.output[:500]}")
                            leads = []
                elif isinstance(result.output, dict) and 'leads' in result.output:
                    leads = result.output['leads']
                elif isinstance(result.output, list):
                    leads = result.output
                else:
                    print(f"⚠️  Unexpected output type: {type(result.output)}")
                    leads = []
            else:
                print("⚠️  No output received from task")
                leads = []
            
            # Clean and validate leads
            cleaned_leads = self._clean_leads(leads)
            
            print(f"✅ Successfully extracted {len(cleaned_leads)} leads")
            
            if len(cleaned_leads) == 0:
                error_msg = "No leads extracted from Google Maps. The Browser-Use task may have failed or returned empty results."
                print(f"❌ ERROR: {error_msg}")
                raise ValueError(error_msg)
            
            return cleaned_leads
        
        except ValueError as ve:
            # Re-raise ValueError (our custom errors)
            raise ve
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            print(f"❌ Error type: {type(e).__name__}")
            import traceback
            print(f"❌ Full traceback:")
            traceback.print_exc()
            # Re-raise the exception instead of returning sample data
            raise Exception(f"Browser-Use scraping failed: {str(e)}") from e
    
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
