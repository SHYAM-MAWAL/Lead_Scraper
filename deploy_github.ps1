# GitHub Deployment Script for Lead Scraper
# Run this script to push your project to GitHub

Write-Host "=== Google Maps Lead Scraper - GitHub Deployment ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Yellow
    git init
} else {
    Write-Host "[1/5] Git already initialized" -ForegroundColor Green
}

# Add all files
Write-Host "[2/5] Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "[3/5] Committing changes..." -ForegroundColor Yellow
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Deploy: Google Maps Lead Scraper with Coolify support"
}
git commit -m "$commitMessage"

# Check if remote exists
$remoteExists = git remote | Select-String "origin"
if (-not $remoteExists) {
    Write-Host "[4/5] Adding remote repository..." -ForegroundColor Yellow
    git remote add origin https://github.com/SHYAM-MAWAL/Lead_Scraper.git
} else {
    Write-Host "[4/5] Remote already exists" -ForegroundColor Green
}

# Push to GitHub
Write-Host "[5/5] Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host ""
Write-Host "=== Deployment Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://github.com/SHYAM-MAWAL/Lead_Scraper" -ForegroundColor White
Write-Host "2. Import to Coolify from GitHub" -ForegroundColor White
Write-Host "3. Set environment variable: BROWSER_USE_API_KEY" -ForegroundColor White
Write-Host "4. Deploy!" -ForegroundColor White
Write-Host ""
Write-Host "See DEPLOYMENT.md for detailed instructions" -ForegroundColor Yellow
