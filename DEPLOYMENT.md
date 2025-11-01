# Deploying to GitHub and Coolify

## Step 1: Push to GitHub

### Initialize Git Repository

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Google Maps Lead Scraper"

# Add remote repository
git remote add origin https://github.com/SHYAM-MAWAL/Lead_Scraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important:** The `.env` file with your API key is already excluded by `.gitignore` and will NOT be pushed to GitHub.

## Step 2: Deploy to Coolify

### Method 1: Import from GitHub (Recommended)

1. **Login to Coolify Dashboard**
   - Access your Coolify instance

2. **Create New Project**
   - Click "New Resource" or "Add New"
   - Select "GitHub Repository"

3. **Connect Repository**
   - Authorize GitHub access (if not already done)
   - Select repository: `SHYAM-MAWAL/Lead_Scraper`
   - Choose branch: `main`

4. **Configure Application**
   - **Build Pack:** Docker (Coolify will auto-detect Dockerfile)
   - **Port:** 5000
   - **Health Check:** Enabled (already configured in Dockerfile)

5. **Set Environment Variables**
   - Click "Environment Variables"
   - Add variable:
     ```
     BROWSER_USE_API_KEY=bu_F7dGOTrCoqud9chjyjJSx7H2gCV1pzO8kMbxk2Obyw8
     ```
   - Mark as "Secret" to hide the value

6. **Configure Domain (Optional)**
   - Add custom domain or use Coolify-provided domain
   - Enable HTTPS if desired

7. **Deploy**
   - Click "Deploy" button
   - Wait for build and deployment (usually 2-5 minutes)
   - Check logs for any errors

### Method 2: Manual Docker Deployment

If importing from GitHub doesn't work:

```bash
# On your Coolify server
git clone https://github.com/SHYAM-MAWAL/Lead_Scraper.git
cd Lead_Scraper

# Create .env file
echo "BROWSER_USE_API_KEY=bu_F7dGOTrCoqud9chjyjJSx7H2gCV1pzO8kMbxk2Obyw8" > .env

# Deploy with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

## Step 3: Verify Deployment

### Test the Application

1. **Web Interface:**
   ```
   https://your-domain.com
   ```
   or
   ```
   http://your-server-ip:5000
   ```

2. **API Status Check:**
   ```bash
   curl https://your-domain.com/api/status
   ```

   Expected response:
   ```json
   {
     "status": "ok",
     "service": "Google Maps Lead Scraper"
   }
   ```

3. **Test Lead Scraping:**
   ```bash
   curl -X POST https://your-domain.com/api/leads \
     -H "Content-Type: application/json" \
     -d '{
       "query": "dental clinic, Pune",
       "num_leads": 5,
       "email": "test@example.com",
       "require_email": false
     }'
   ```

## Troubleshooting

### Build Fails

- **Check logs:** Look for Python dependency errors
- **Solution:** Ensure `requirements.txt` is properly formatted
- **Rebuild:** Force rebuild in Coolify dashboard

### Application Starts But Not Accessible

- **Check port mapping:** Ensure port 5000 is exposed
- **Check firewall:** Allow incoming traffic on port 5000
- **Check health check:** May need time to pass initial health checks

### API Key Not Working

- **Verify environment variable:** Check it's set correctly in Coolify
- **Restart application:** After changing env vars, redeploy
- **Check logs:** Look for authentication errors

### Slow Scraping

- **Normal behavior:** Email extraction takes 2-5 minutes
- **Without email:** Should complete in 1-3 minutes
- **Check API limits:** Browser-Use may have rate limits

## Updating the Application

### Push Updates to GitHub

```powershell
# Make your changes
git add .
git commit -m "Description of changes"
git push
```

### Redeploy on Coolify

Coolify offers auto-deploy options:

1. **Manual:** Click "Redeploy" in Coolify dashboard
2. **Auto-deploy:** Enable webhook in Coolify, add to GitHub
3. **CI/CD:** Use GitHub Actions (optional)

## Security Recommendations

1. **Use HTTPS:** Enable SSL/TLS in Coolify
2. **API Key Rotation:** Regularly rotate Browser-Use API key
3. **Rate Limiting:** Consider adding rate limiting for production
4. **Authentication:** Add auth if exposing publicly
5. **Firewall:** Restrict access to known IPs if possible

## Coolify-Specific Tips

### Resource Limits

Set appropriate resource limits in Coolify:

- **Memory:** Minimum 512MB, recommended 1GB
- **CPU:** 1 vCPU should be sufficient
- **Storage:** 2GB for application + logs

### Monitoring

- Enable logging in Coolify dashboard
- Set up alerts for downtime
- Monitor resource usage

### Backup

- GitHub serves as code backup
- Coolify handles container state
- No database needed (stateless application)

## Support

If you encounter issues:

1. Check Coolify logs
2. Check application logs: `docker-compose logs -f`
3. Verify environment variables are set
4. Ensure API key is valid
5. Open issue on GitHub: https://github.com/SHYAM-MAWAL/Lead_Scraper/issues

---

**Next Steps:**
1. ✅ Push code to GitHub
2. ✅ Import to Coolify
3. ✅ Set environment variable
4. ✅ Deploy and test
5. 🎉 Start scraping leads!
