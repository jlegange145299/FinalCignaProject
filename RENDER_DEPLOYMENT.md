# 🚀 ALICE - Render Deployment Guide

This guide will help you deploy the ALICE (AI-Led Insurance Customer Experience) application to Render.

## 📋 Prerequisites

1. **GitHub Account** - To host the repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **API Keys**:
   - OpenAI API Key
   - D-ID API Key (format: `Basic YXV0...`)

## 🔧 Step 1: Prepare the Repository

### Option A: Create New Repository

1. Go to GitHub and create a new repository (e.g., `alice-insurance-assistant`)
2. Make it **private** (contains sensitive code)
3. Don't initialize with README (we already have one)

### Option B: Use Existing Repository

If you already have a GitHub repo, you can use that.

## 📤 Step 2: Push to GitHub

Open terminal in the FinalCignaProject directory and run:

```bash
# If starting fresh (no remote set)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# If remote already exists, update it
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Add all files (respects .gitignore)
git add .

# Commit the changes
git commit -m "Prepare ALICE app for Render deployment"

# Push to GitHub
git push -u origin main
```

**Note:** Make sure `.env` and `.streamlit/secrets.toml` are NOT pushed (they're in .gitignore).

## 🌐 Step 3: Deploy on Render

### 3.1 Create New Web Service

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your repository from the list

### 3.2 Configure Service Settings

Fill in the following settings:

**Basic Settings:**
- **Name:** `alice-insurance-assistant` (or your preferred name)
- **Region:** Choose closest to your users (e.g., Oregon for US West)
- **Branch:** `main`
- **Root Directory:** Leave empty (or specify if in subdirectory)
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `sh setup.sh && streamlit run app8.py --server.port=$PORT --server.address=0.0.0.0`

**Instance:**
- **Instance Type:** Free tier is fine for testing, but for production use at least **Starter ($7/month)** for better performance

### 3.3 Add Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key |
| `DID_API_KEY` | `Basic YXV0...` | Your D-ID API key (include "Basic " prefix) |
| `PYTHON_VERSION` | `3.10.0` | Specify Python version |

**Important:** 
- Do NOT use quotes around the values
- Make sure D-ID key includes the "Basic " prefix

### 3.4 Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying
3. Wait 5-10 minutes for first deployment
4. You'll see build logs in real-time

## ✅ Step 4: Verify Deployment

Once deployed, you'll get a URL like: `https://alice-insurance-assistant.onrender.com`

**Test the following:**

1. **Login page** loads correctly
2. **ALICE banner** displays with dark blue theme
3. **Welcome video** plays in sidebar
4. **Chat functionality** works
5. **Voice input** button appears (works in Chrome/Edge)
6. **D-ID video generation** works (check API credits)

## 🔍 Troubleshooting

### Build Fails

**Error: `Could not find a version that satisfies the requirement...`**
- Check `requirements.txt` for typos
- Ensure Python version is set correctly

**Error: `setup.sh: Permission denied`**
- Render should handle this automatically
- If not, change start command to: `streamlit run app8.py --server.port=$PORT`

### App Crashes on Start

**Check Logs:**
1. Go to Render dashboard
2. Click your service
3. View **"Logs"** tab

**Common Issues:**
- Missing environment variables (OPENAI_API_KEY, DID_API_KEY)
- D-ID API key format incorrect (must include "Basic " prefix)
- Port binding issue (make sure `--server.port=$PORT` is in start command)

### Video Generation Fails

**Issue:** D-ID videos don't generate
- Check D-ID API credits at [studio.d-id.com](https://studio.d-id.com)
- Verify API key format: `Basic YXV0...` (include "Basic ")
- Check Render logs for D-ID API errors

### Voice Input Doesn't Work

**Issue:** Microphone button says "Not Supported"
- Voice input requires HTTPS (Render provides this automatically)
- Only works in Chrome, Edge, Safari (not Firefox)
- User must grant microphone permissions

## 🔒 Security Notes

1. **Never commit `.env` or `secrets.toml`** - They're in .gitignore
2. **Use environment variables** on Render for all secrets
3. **Make GitHub repo private** - Contains business logic
4. **Rotate API keys** if ever exposed
5. **Monitor API usage** - Set spending limits on OpenAI/D-ID

## 💰 Cost Estimates

### Render Hosting
- **Free Tier:** $0/month (sleeps after 15 min inactivity, 750 hours/month)
- **Starter:** $7/month (always on, better performance)
- **Standard:** $25/month (production-grade)

### API Costs
- **OpenAI GPT-4:** ~$0.03 per conversation
- **D-ID Video:** ~$0.10-0.30 per video (depending on plan)

**Recommendation:** Start with Free tier + monitor usage, upgrade as needed.

## 🔄 Updating the App

After making code changes:

```bash
# Commit changes
git add .
git commit -m "Update ALICE app"

# Push to GitHub
git push origin main
```

Render will automatically detect the push and redeploy (if auto-deploy is enabled).

## 📞 Support

**Render Issues:** [Render Support](https://render.com/docs)
**Streamlit Issues:** [Streamlit Docs](https://docs.streamlit.io)
**OpenAI Issues:** [OpenAI Help](https://help.openai.com)
**D-ID Issues:** [D-ID Support](https://docs.d-id.com)

---

## 🎉 Success!

Once deployed, share the Render URL with your team. Users can access ALICE from any device with a web browser!

**Your ALICE URL:** `https://your-service-name.onrender.com`
