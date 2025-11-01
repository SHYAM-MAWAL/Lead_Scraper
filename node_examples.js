/**
 * Google Maps Lead Generator - Node.js HTTP Examples
 * Use these examples in your Node.js projects or HTTP automation nodes
 */

// ============================================
// Method 1: Using Axios (Most Popular)
// ============================================

const axios = require('axios');

async function getLeadsWithAxios(query, numLeads, requireEmail = false) {
  try {
    const response = await axios.post('http://localhost:5000/api/leads', {
      query: query,
      num_leads: numLeads,
      email: 'your@email.com',
      require_email: requireEmail
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 300000 // 5 minutes timeout
    });

    console.log('✅ Success!');
    console.log('Total leads:', response.data.count);
    
    return response.data.leads;
    
  } catch (error) {
    console.error('❌ Error:', error.response?.data || error.message);
    throw error;
  }
}

// Usage:
// getLeadsWithAxios('Dental clinic, Pune', 5, true)
//   .then(leads => console.log(leads));


// ============================================
// Method 2: Using Fetch API (Node.js 18+)
// ============================================

async function getLeadsWithFetch(query, numLeads, requireEmail = false) {
  try {
    const response = await fetch('http://localhost:5000/api/leads', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        num_leads: numLeads,
        email: 'your@email.com',
        require_email: requireEmail
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Success!');
    console.log('Total leads:', data.count);
    
    return data.leads;
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    throw error;
  }
}

// Usage:
// getLeadsWithFetch('Coffee shops in London', 10, false)
//   .then(leads => console.log(leads));


// ============================================
// Method 3: Using Node HTTP (No dependencies)
// ============================================

const http = require('http');

function getLeadsWithHTTP(query, numLeads, requireEmail = false) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      query: query,
      num_leads: numLeads,
      email: 'your@email.com',
      require_email: requireEmail
    });

    const options = {
      hostname: 'localhost',
      port: 5000,
      path: '/api/leads',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };

    const req = http.request(options, (res) => {
      let body = '';

      res.on('data', (chunk) => {
        body += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          console.log('✅ Success!');
          console.log('Total leads:', result.count);
          resolve(result.leads);
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', (error) => {
      console.error('❌ Error:', error.message);
      reject(error);
    });

    req.write(data);
    req.end();
  });
}

// Usage:
// getLeadsWithHTTP('Hotels in Dubai', 5, false)
//   .then(leads => console.log(leads));


// ============================================
// Method 4: Complete Example with Error Handling
// ============================================

async function completeExample() {
  console.log('Starting lead generation...\n');

  const config = {
    query: 'Dental clinic, Pune',
    numLeads: 5,
    email: 'your@email.com',
    requireEmail: true
  };

  try {
    // Show what we're searching for
    console.log('Search Configuration:');
    console.log('  Query:', config.query);
    console.log('  Number of Leads:', config.numLeads);
    console.log('  Email Extraction:', config.requireEmail ? 'Enabled' : 'Disabled');
    console.log('\nThis will take', config.requireEmail ? '2-5 minutes' : '1-3 minutes', '...\n');

    // Make the request
    const response = await axios.post('http://localhost:5000/api/leads', {
      query: config.query,
      num_leads: config.numLeads,
      email: config.email,
      require_email: config.requireEmail
    });

    // Process results
    const { leads, count } = response.data;

    console.log('\n✅ SUCCESS!');
    console.log('=' .repeat(60));
    console.log(`Found ${count} leads:\n`);

    leads.forEach((lead, index) => {
      console.log(`${index + 1}. ${lead.name}`);
      console.log(`   📍 Address: ${lead.address}`);
      console.log(`   📞 Phone: ${lead.phone || 'N/A'}`);
      console.log(`   🌐 Website: ${lead.website || 'N/A'}`);
      console.log(`   📧 Email: ${lead.email || 'N/A'}`);
      console.log('');
    });

    console.log('=' .repeat(60));

    // Save to file (optional)
    const fs = require('fs');
    fs.writeFileSync('leads_export.json', JSON.stringify(leads, null, 2));
    console.log('✅ Results saved to: leads_export.json');

    return leads;

  } catch (error) {
    console.error('\n❌ ERROR:');
    
    if (error.response) {
      // Server responded with error
      console.error('Status:', error.response.status);
      console.error('Message:', error.response.data.error || error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('No response from server. Is the server running?');
      console.error('Check: http://localhost:5000/api/status');
    } else {
      // Other error
      console.error('Error:', error.message);
    }

    throw error;
  }
}

// Run the complete example
// completeExample();


// ============================================
// Method 5: For n8n HTTP Request Node
// ============================================

/*
n8n Configuration:

Node Type: HTTP Request
Method: POST
URL: http://localhost:5000/api/leads

Headers:
  Content-Type: application/json

Body:
{
  "query": "{{ $json.searchQuery }}",
  "num_leads": {{ $json.numberOfLeads }},
  "email": "{{ $json.userEmail }}",
  "require_email": {{ $json.extractEmails }}
}

Response:
  Output: All response data
  Response Format: JSON
*/


// ============================================
// Method 6: Promise-based wrapper
// ============================================

class LeadGenerator {
  constructor(baseUrl = 'http://localhost:5000') {
    this.baseUrl = baseUrl;
  }

  async checkStatus() {
    const response = await fetch(`${this.baseUrl}/api/status`);
    return await response.json();
  }

  async getLeads({ query, numLeads = 20, email, requireEmail = false }) {
    const response = await fetch(`${this.baseUrl}/api/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        num_leads: numLeads,
        email,
        require_email: requireEmail
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch leads');
    }

    return await response.json();
  }
}

// Usage:
// const generator = new LeadGenerator();
// 
// generator.checkStatus()
//   .then(status => console.log('API Status:', status));
//
// generator.getLeads({
//   query: 'Restaurants in Singapore',
//   numLeads: 10,
//   email: 'your@email.com',
//   requireEmail: true
// }).then(result => {
//   console.log('Leads:', result.leads);
// });


// ============================================
// Export functions for use in other modules
// ============================================

module.exports = {
  getLeadsWithAxios,
  getLeadsWithFetch,
  getLeadsWithHTTP,
  LeadGenerator,
  completeExample
};
