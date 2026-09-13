# 🤖 ALICE - AI-Led Insurance Customer Experience

**ALICE** is an intelligent AI assistant designed to provide personalized insurance support through natural conversation and AI-generated video responses.

![ALICE](https://img.shields.io/badge/AI-Powered-0066FF?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge)

## ✨ Features

- 🎬 **AI Video Responses** - D-ID powered avatar delivers personalized video answers
- 🎤 **Voice Input** - Speak your questions using Web Speech API
- 💬 **Intelligent Chat** - OpenAI GPT-4 powered conversations
- 🎨 **Modern Dark UI** - Sleek dark blue theme (#000033, #0066FF)
- 🔐 **User Authentication** - Simple login system
- 📚 **Knowledge Base** - Trained on Cigna insurance documentation
- 📱 **Mobile Responsive** - Works on all devices
- ⚡ **Real-time Interaction** - Instant chat and video generation

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.10+
- OpenAI API Key
- D-ID API Key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd FinalCignaProject
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create `.env` file:
```bash
DID_API_KEY=Basic_your_d_id_key_here
OPENAI_API_KEY=sk-your_openai_key_here
```

Create `.streamlit/secrets.toml` file:
```toml
OPENAI_API_KEY = "sk-your_openai_key_here"
```

4. **Run the app**
```bash
streamlit run app8.py
```

5. **Open browser**
Navigate to `http://localhost:8501`

## 🌐 Deploy to Render

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for complete deployment instructions.

**Quick Deploy:**

1. Push code to GitHub
2. Connect to Render
3. Set environment variables:
   - `OPENAI_API_KEY`
   - `DID_API_KEY`
4. Deploy!

## 🎯 Usage

### Login
- Email: Any valid email format (e.g., `user@example.com`)
- Password: Minimum 6 characters

### Asking Questions

**Text Input:**
- Type your insurance question in the chat box
- Click send or press Enter

**Voice Input:**
- Click "🎤 Click to Speak" button
- Speak your question
- It will automatically transcribe and submit

**Quick Questions:**
- Click pre-populated question tiles
- Instant responses

### Video Responses

- ALICE generates personalized video responses
- Videos appear at the top of the screen
- Takes 10-20 seconds to generate
- Text response shown immediately

## 🛠️ Technology Stack

- **Frontend:** Streamlit 1.32.2
- **AI Model:** OpenAI GPT-4 (Chat Completions API)
- **Video Generation:** D-ID AI Avatar API
- **Voice Input:** Web Speech API (browser-based)
- **Language:** Python 3.10
- **Hosting:** Render (recommended)

## 📁 Project Structure

```
FinalCignaProject/
├── app8.py                    # Main application (latest version)
├── app7.py                    # Stable milestone version
├── requirements.txt           # Python dependencies
├── Procfile                   # Render start command
├── setup.sh                   # Render setup script
├── runtime.txt                # Python version specification
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── .streamlit/
│   ├── config.toml           # Streamlit configuration
│   ├── secrets.toml          # API keys (local only, not in git)
│   └── secrets.toml.example  # Secrets template
├── README.md                  # This file
├── RENDER_DEPLOYMENT.md       # Deployment guide
└── docs/
    ├── MIGRATION_2026.md      # API migration notes
    ├── FIXES_APPLIED.md       # Bug fixes log
    └── MILESTONE_APP7.md      # Version history
```

## 🔧 Configuration

### Theme Colors

ALICE uses a professional dark blue theme:

- **Background:** `#000033` → `#000066` gradient
- **Accent:** `#0066FF` (bright blue)
- **Text:** `#E8F4FD` (light blue-white)
- **Labels:** `#6699FF` (medium blue)

### D-ID API

Video generation settings (in `app8.py`):
- **Presenter ID:** `amy-jcwCkr1grs`
- **Voice ID:** `en-US-JennyNeural`
- **Truncation:** 50 characters (for testing, increase to 225+ for production)

### OpenAI API

Chat settings:
- **Model:** `gpt-4`
- **Temperature:** 0.7
- **System Prompt:** ALICE personality (articulate, friendly, professional)

## 🔒 Security

- ✅ API keys stored in environment variables
- ✅ `.env` and `secrets.toml` in `.gitignore`
- ✅ No hardcoded credentials
- ✅ Simple authentication system
- ⚠️ For production: Implement proper user database and OAuth

## 💰 Cost Estimates

### API Usage
- **OpenAI GPT-4:** ~$0.03 per conversation
- **D-ID Video:** ~$0.10-0.30 per video

### Hosting (Render)
- **Free Tier:** $0/month (750 hours, sleeps after inactivity)
- **Starter:** $7/month (always on, recommended)
- **Standard:** $25/month (production-grade)

## 🐛 Troubleshooting

### Video Generation Fails
- Check D-ID API credits
- Verify API key format includes "Basic " prefix
- Check D-ID service status

### Voice Input Not Working
- Requires HTTPS (works on Render automatically)
- Only supported in Chrome, Edge, Safari
- User must grant microphone permissions

### OpenAI API Errors
- Verify API key is valid
- Check OpenAI account has credits
- Ensure model name is correct (`gpt-4`)

## 📝 Development Notes

### Version History
- **app8.py** - Current version with voice input
- **app7.py** - Stable milestone (frozen)
- Previous versions archived

### Key Improvements
- ✅ Migrated from Assistants API to Chat Completions API
- ✅ Fixed D-ID video generation and polling
- ✅ Added ALICE branding and dark blue theme
- ✅ Implemented voice-to-text input
- ✅ Optimized video-centric layout
- ✅ Added authentication system

## 🤝 Contributing

This is a private project. For feature requests or bug reports, contact the development team.

## 📄 License

Proprietary - All rights reserved

## 👥 Credits

- **AI Models:** OpenAI GPT-4
- **Video Generation:** D-ID
- **Framework:** Streamlit
- **Branding:** ALICE (AI-Led Insurance Customer Experience)

## 📞 Support

For issues or questions:
- Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for deployment help
- Review troubleshooting docs for common issues
- Contact the development team

---

**Built with ❤️ for modern insurance customer experience**
