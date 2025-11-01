let currentLeads = [];

document.getElementById('leadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = document.getElementById('query').value;
    const numLeads = parseInt(document.getElementById('numLeads').value);
    const email = document.getElementById('email').value;
    const requireEmail = document.getElementById('requireEmail').checked;
    
    // Hide previous results/errors
    document.getElementById('resultsDiv').style.display = 'none';
    document.getElementById('errorDiv').style.display = 'none';
    
    // Show loading
    document.getElementById('loadingDiv').style.display = 'block';
    document.getElementById('submitBtn').disabled = true;
    
    try {
        const response = await fetch('/api/leads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                num_leads: numLeads,
                email: email,
                require_email: requireEmail
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch leads');
        }
        
        // Store leads for export
        currentLeads = data.leads;
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        // Hide loading
        document.getElementById('loadingDiv').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('resultsDiv');
    const summaryDiv = document.getElementById('resultsSummary');
    const tableDiv = document.getElementById('resultsTable');
    
    // Summary
    summaryDiv.innerHTML = `
        <p><strong>Query:</strong> ${document.getElementById('query').value}</p>
        <p><strong>Leads Found:</strong> ${data.count}</p>
        <p><strong>Results sent to:</strong> ${data.email}</p>
    `;
    
    // Table
    if (data.leads && data.leads.length > 0) {
        let tableHTML = `
            <table class="lead-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Address</th>
                        <th>Phone</th>
                        <th>Website</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.leads.forEach((lead, index) => {
            tableHTML += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${escapeHtml(lead.name)}</td>
                    <td>${escapeHtml(lead.address)}</td>
                    <td>${escapeHtml(lead.phone)}</td>
                    <td>${lead.website ? `<a href="${escapeHtml(lead.website)}" target="_blank">Visit</a>` : '-'}</td>
                    <td>${lead.email ? `<a href="mailto:${escapeHtml(lead.email)}">${escapeHtml(lead.email)}</a>` : '-'}</td>
                </tr>
            `;
        });
        
        tableHTML += `
                </tbody>
            </table>
        `;
        
        tableDiv.innerHTML = tableHTML;
    } else {
        tableDiv.innerHTML = '<p>No leads found.</p>';
    }
    
    resultsDiv.style.display = 'block';
}

function showError(message) {
    const errorDiv = document.getElementById('errorDiv');
    errorDiv.textContent = `Error: ${message}`;
    errorDiv.style.display = 'block';
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function exportToCSV() {
    if (currentLeads.length === 0) {
        alert('No leads to export');
        return;
    }
    
    let csv = 'Name,Address,Phone,Website,Email\n';
    
    currentLeads.forEach(lead => {
        csv += `"${lead.name}","${lead.address}","${lead.phone}","${lead.website}","${lead.email}"\n`;
    });
    
    downloadFile(csv, 'leads.csv', 'text/csv');
}

function exportToJSON() {
    if (currentLeads.length === 0) {
        alert('No leads to export');
        return;
    }
    
    const json = JSON.stringify(currentLeads, null, 2);
    downloadFile(json, 'leads.json', 'application/json');
}

function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}
