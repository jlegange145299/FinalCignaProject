# Quick Start Guide - Cigna AI Assistant

Get the app running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API account
- D-ID API account

## Step-by-Step Setup

### 1️⃣ Install Dependencies (1 minute)

```bash
cd FinalCignaProject
pip install -r requirements.txt
```

### 2️⃣ Get Your API Keys (3 minutes)

#### OpenAI Setup:
1. Go to https://platform.openai.com/api-keys
2. Create an API key and copy it

#### Create OpenAI Assistant:
1. Go to https://platform.openai.com/assistants
2. Click "Create Assistant"
3. Upload your Cigna Healthguard Brochure PDF
4. Copy the Assistant ID (starts with `asst_...`)

#### D-ID Setup:
1. Go to https://www.d-id.com/
2. Sign up for an account
3. Go to API settings and create an API key

### 3️⃣ Configure Environment (1 minute)

#### Create `.env` file:
```bash
# Copy the example file
copy .env.example .env

# Edit .env and paste your D-ID key:
DID_API=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

#### Create `.streamlit/secrets.toml` file:
```bash
# Copy the example file
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# Edit .streamlit/secrets.toml and add:
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
ASSISTANT_ID = "asst_xxxxxxxxxxxxxxxxxxxxxxxx"
```

### 4️⃣ Verify Setup (30 seconds)

```bash
python setup.py
```

Look for all ✅ checkmarks. If you see ❌, review the error messages.

### 5️⃣ Run the App (10 seconds)

```bash
streamlit run app7.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎉 You're Done!

Try asking: "What does Cigna Healthguard cover?"

---

## Troubleshooting

### "Missing secrets" error
- Make sure `.streamlit/secrets.toml` exists (note the `.streamlit` folder)
- Verify your API keys are correctly formatted (no extra spaces)

### "Invalid API key" error
- Check that your OpenAI/D-ID keys are active and have credits
- Try regenerating the keys if they're old

### "Assistant not found" error
- Verify your Assistant ID is correct
- Make sure the Assistant has files uploaded to it

### Video doesn't generate
- Check your D-ID account has credits remaining
- The app will still show text responses even if video fails

### Port already in use
- Kill the existing Streamlit process or use a different port:
  ```bash
  streamlit run app7.py --server.port 8502
  ```

---

## Next Steps

Once the app is running:

1. Test multiple questions to verify conversation context works
2. Check video generation with different response lengths
3. Test the sidebar widgets (contact preferences, satisfaction rating)
4. Review `FIXES_APPLIED.md` to understand what was fixed
5. See `README.md` for full documentation

---

## Need Help?

- Check `FIXES_APPLIED.md` for details on what was fixed
- Run `python setup.py` to diagnose configuration issues
- Review the console output for detailed error messages
- Ensure all requirements are installed correctly

Happy chatting! 🤖💬
