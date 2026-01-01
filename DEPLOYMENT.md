# AZ-104 Study Hub - GitHub Pages Deployment Guide

This guide explains how to deploy the AZ-104 Study Hub entirely on GitHub's free platform with AI features powered by Cloudflare Workers.

## Architecture Overview

```
GitHub Pages (Static Files)     Cloudflare Workers (API)
┌─────────────────────────┐     ┌─────────────────────────┐
│  docs/                  │     │  /api/extract-concepts  │
│  - index.html           │────▶│  /api/generate-cprs     │
│  - 88 study guides      │     │                         │
│  - shared-navbar.js     │     │  OpenAI API ◀──────────┤
│  - api-config.js        │     │  (your API key)         │
└─────────────────────────┘     └─────────────────────────┘
        FREE                           FREE (100K req/day)
```

## Step 1: Deploy Cloudflare Worker (AI Backend)

### 1.1 Create a Cloudflare Account
1. Go to https://dash.cloudflare.com/sign-up
2. Create a free account (no credit card required)

### 1.2 Install Wrangler CLI
```bash
npm install -g wrangler
```

### 1.3 Login to Cloudflare
```bash
wrangler login
```

### 1.4 Deploy the Worker
```bash
cd cloudflare-worker
wrangler deploy
```

This will output a URL like: `https://az104-study-api.YOUR_SUBDOMAIN.workers.dev`

### 1.5 Add Your OpenAI API Key
```bash
wrangler secret put OPENAI_API_KEY
```
When prompted, paste your OpenAI API key.

### 1.6 Verify the Worker
Visit your worker URL in a browser. You should see:
```json
{
  "status": "AZ-104 Study Hub API",
  "endpoints": ["/api/extract-concepts", "/api/generate-cprs"]
}
```

## Step 2: Configure Frontend for GitHub Pages

### 2.1 Update API Configuration
Edit `docs/api-config.js` with your Cloudflare Worker URL:

```javascript
window.AZ104_API_CONFIG = {
  baseUrl: 'https://az104-study-api.YOUR_SUBDOMAIN.workers.dev'
};
```

Replace `YOUR_SUBDOMAIN` with your actual Cloudflare subdomain.

### 2.2 Commit the Change
```bash
git add docs/api-config.js
git commit -m "Configure API URL for production"
git push
```

## Step 3: Deploy to GitHub Pages

### 3.1 Enable GitHub Pages
1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Under "Source", select **Deploy from a branch**
4. Choose `main` branch and `/docs` folder
5. Click **Save**

### 3.2 Wait for Deployment
GitHub will build and deploy your site. After a few minutes, your site will be live at:
`https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

## Step 4: Test Your Deployment

1. Visit your GitHub Pages URL
2. Navigate to "Personalized Review"
3. Try the CPRS Question Generator - enter a concept like "VNet Peering"
4. Verify you get 6 MCQ questions generated

## Troubleshooting

### "Connection Failed" Error
- Check that `api-config.js` has the correct Cloudflare Worker URL
- Verify the Worker is deployed: visit the URL directly
- Check browser console for CORS errors

### "AI Unavailable" Message
- Verify your OpenAI API key is set: `wrangler secret list`
- Check your OpenAI account has credits
- View Worker logs: `wrangler tail`

### CORS Errors
The Worker already includes CORS headers for all origins. If you still see CORS errors:
1. Check the Worker is running: `wrangler tail`
2. Verify the API URL doesn't have a trailing slash

## Cost Breakdown

| Service | Free Tier | Your Usage |
|---------|-----------|------------|
| GitHub Pages | Unlimited static hosting | $0 |
| Cloudflare Workers | 100,000 requests/day | $0 |
| OpenAI API | Pay per use (~$0.01-0.05 per generation) | ~$1-5/month |

## Local Development

For local development, keep `api-config.js` with an empty `baseUrl`:
```javascript
window.AZ104_API_CONFIG = {
  baseUrl: ''
};
```

Then run the Flask server locally:
```bash
python server.py
```

## Files Modified for Deployment

- `docs/api-config.js` - API URL configuration (edit for production)
- `docs/azure_personalized_review_guide.html` - Uses configurable API URL
- `cloudflare-worker/worker.js` - Cloudflare Worker with API endpoints
- `cloudflare-worker/wrangler.toml` - Worker configuration

## Quick Commands Reference

```bash
# Deploy Worker
cd cloudflare-worker && wrangler deploy

# Set OpenAI Key
wrangler secret put OPENAI_API_KEY

# View Worker Logs
wrangler tail

# Test Worker Locally
wrangler dev
```
