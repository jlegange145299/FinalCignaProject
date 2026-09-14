import openai
import time
import streamlit as st
import requests
from dotenv import load_dotenv
import os


load_dotenv()

# Try to get D-ID API key from environment variable (Render) or .env file (local)
DID_API_ENV = os.getenv("DID_API_KEY") or os.getenv("DID_API")

def generate_video(script):
    """Generate D-ID talking avatar video"""
    
    # Check if D-ID API key is configured
    if not DID_API_ENV:
        print("WARNING: DID_API not configured in .env file")
        return "error"
    
    url = "https://api.d-id.com/talks"
    
    # Use the API key as-is (it already contains "Basic " prefix)
    api_key = DID_API_ENV.strip().strip('"')
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization" : api_key
        }

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "ssml": "false",
            "input":script
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0",
            "stitch": "true"
        },
        "source_url": "https://photosfordidd.s3.eu-central-1.amazonaws.com/alice.png"
    }

    try:
        print(f"ATTEMPTING TO GENERATE VIDEO WITH SCRIPT: {script}")
        print(f"URL: {url}")
        print(f"PAYLOAD: {payload}")
        print(f"HEADERS: {headers}")

        response = requests.post(url, json=payload, headers=headers)
        print(f"RESPONSE STATUS: {response.status_code}")
        print(f"RESPONSE BODY: {response.text}")

        if response.status_code == 201:
            print("RESPONSE WAS 201")
            res = response.json()
            id = res["id"]
            status = "created"
            while status != "done":
                print("TRYING AGAIN")
                try:
                    getresponse = requests.get(f"{url}/{id}", headers=headers)
                except Exception as e:
                    print(f"EXCEPTION: {e}")
                    time.sleep(10)
                    getresponse = requests.get(f"{url}/{id}", headers=headers)
                print(f"GET RESPONSE: {getresponse}")
                if getresponse.status_code == 200:
                    res = getresponse.json()
                    status = res["status"]
                    print(f"RESPONSE: {res}")
                    if res["status"] == "done":
                        print("ITS DONE")
                        video_url =  res["result_url"]
                        break
                    else:
                        print("WILL TRY AGAIN IN 3 SECONDS")
                        time.sleep(3)
                else:
                    status = "error"
                    video_url = "error"
        else:
            print("RESPONSE WAS NOT 201")
            video_url = "error"   
    except Exception as e:
        print(f"EXCEPTION: {e}")      
        video_url = "error"          

    return video_url

def get_ai_response(messages):
    """Get response from OpenAI using Chat Completions API (v0.28.x style)"""
    try:
        system_message = {
            "role": "system",
            "content": """You are ALICE (AI-Led Insurance Customer Experience), Cigna's intelligent insurance concierge. 
            You are articulate, friendly, and professional. You provide clear, accurate answers about Cigna health insurance plans, 
            specifically the Healthguard product, including coverage, benefits, policies, and claims.
            
            Your communication style:
            - Warm and approachable, yet professional
            - Clear and concise—avoid jargon unless necessary
            - Proactive—anticipate customer needs
            - Empathetic—acknowledge concerns and provide reassurance
            - Confident—you're an expert in insurance matters
            
            Always aim to provide actionable guidance. If you don't know something, be honest and direct the customer 
            to the appropriate resource or representative."""
        }
        
        # Combine system message with conversation history
        full_messages = [system_message] + messages
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Latest GPT-4 Omni model (faster and smarter)
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except openai.error.AuthenticationError:
        return "I apologize, but there's an authentication issue with the AI service. Please contact support."
    except openai.error.RateLimitError:
        return "I apologize, but we've reached our rate limit. Please try again in a moment."
    except openai.error.APIError as e:
        print(f"OpenAI API Error: {e}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again."
    except Exception as e:
        print(f"Unexpected error calling OpenAI: {e}")
        return "I apologize, but I encountered an unexpected error. Please try again or contact support."

def show_welcome_screen():
    """Display welcome/login screen with ALICE branding"""
    st.markdown("""
        <style>
        /* Dark modern theme */
        .stApp {
            background: linear-gradient(135deg, #000033 0%, #000066 100%);
        }
        
        .welcome-container {
            text-align: center;
            padding: 20px;
        }
        
        .welcome-title {
            font-size: 48px;
            font-weight: 700;
            background: linear-gradient(135deg, #0066FF 0%, #0099FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }
        
        .welcome-subtitle {
            font-size: 18px;
            color: #6699FF;
            margin-bottom: 8px;
            font-weight: 400;
            letter-spacing: 0.5px;
        }
        
        .alice-acronym {
            font-size: 14px;
            color: #99BBFF;
            margin-bottom: 20px;
            font-style: italic;
        }
        
        .welcome-description {
            font-size: 15px;
            color: #B8C5D6;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        /* Form styling */
        .stTextInput > div > div > input {
            background-color: #000066 !important;
            border: 1px solid #0066FF !important;
            color: #E8F4FD !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #0066FF !important;
            box-shadow: 0 0 0 2px rgba(0, 102, 255, 0.3) !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(0, 102, 255, 0.5) !important;
            background: linear-gradient(135deg, #0077FF 0%, #0066DD 100%) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center column for login
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        st.markdown('<div style="text-align: center; margin: 30px 0 20px 0;">', unsafe_allow_html=True)
        st.image("https://logos-world.net/wp-content/uploads/2022/05/Cigna-Logo.png", width=350)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
        st.markdown('<div class="welcome-title">ALICE</div>', unsafe_allow_html=True)
        st.markdown('<div class="alice-acronym">AI-Led Insurance Customer Experience</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtitle">Your Intelligent Insurance Concierge</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="welcome-description">
            Experience seamless, intelligent assistance for all your Cigna insurance needs.<br>
            ALICE provides instant answers, personalized guidance, and expert support—anytime, anywhere.
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Login form with clean styling
        st.markdown('<div style="background: #000066; padding: 30px; border-radius: 12px; border: 1px solid #0066FF; margin-top: 25px;">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="your.email@example.com", label_visibility="collapsed")
            st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if email and password:
                    if "@" in email and len(password) >= 6:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.success("✅ Welcome to ALICE!")
                        time.sleep(0.8)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.warning("⚠️ Please enter your credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #6699FF; font-size: 13px; margin-top: 15px;">Need access? Contact your administrator</p>', unsafe_allow_html=True)


def show_main_app():
    """Display main chat application with modern dark theme"""
    # Try to get API key from Streamlit secrets first, then from environment variable
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("OpenAI API key not found. Please configure OPENAI_API_KEY in environment variables.")
        return
    video_path = "https://photosfordidd.s3.eu-central-1.amazonaws.com/baselinevideo2.mp4"   
    image2_path = "https://photosfordidd.s3.eu-central-1.amazonaws.com/2.png"
    image3_path = "https://photosfordidd.s3.eu-central-1.amazonaws.com/PDFcover.png"
    image4_path = "https://photosfordidd.s3.eu-central-1.amazonaws.com/SC.png"
    
    # Initialize session state FIRST
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "quick_question" not in st.session_state:
        st.session_state.quick_question = None

    if "start_chat" not in st.session_state:
        st.session_state.start_chat = False
    
    if "show_quote_form" not in st.session_state:
        st.session_state.show_quote_form = False
    
    if "selected_plan" not in st.session_state:
        st.session_state.selected_plan = None
    
    # Set OpenAI API key (v0.28.x style)
    openai.api_key = api_key
    st.session_state.start_chat = True
    
    # Modern dark theme CSS with blue palette
    st.markdown("""
        <style>
        /* Global dark theme with deep navy and bright blue */
        .stApp {
            background: linear-gradient(135deg, #000033 0%, #000066 100%);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #000033 0%, #000055 100%);
            border-right: 1px solid #0066FF;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: #E8F4FD;
        }
        
        /* Compact spacing */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Chat message styling */
        .stChatMessage {
            background: #000066 !important;
            border: 1px solid #0066FF !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
        }
        
        /* Chat input */
        .stChatInputContainer {
            background: #000066 !important;
            border: 1px solid #0066FF !important;
            border-radius: 10px !important;
        }
        
        .stChatInputContainer textarea {
            background: transparent !important;
            color: #E8F4FD !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #000066 0%, #000099 100%) !important;
            color: #6699FF !important;
            border: 1px solid #0066FF !important;
            border-radius: 8px !important;
            padding: 10px 18px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            font-size: 14px !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #0066FF 0%, #0099FF 100%) !important;
            color: #FFFFFF !important;
            border-color: #0099FF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 16px rgba(0, 102, 255, 0.5) !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: #000066 !important;
            border: 1px solid #0066FF !important;
            border-radius: 8px !important;
            color: #E8F4FD !important;
            font-weight: 600 !important;
        }
        
        /* Video container */
        video {
            border-radius: 10px;
            border: 1px solid #0066FF;
            box-shadow: 0 4px 20px rgba(0, 102, 255, 0.3);
        }
        
        /* Selectbox and slider */
        .stSelectbox > div > div {
            background: #000066 !important;
            border: 1px solid #0066FF !important;
            border-radius: 8px !important;
            color: #E8F4FD !important;
        }
        
        .stSlider > div > div > div {
            background: #0066FF !important;
        }
        
        /* Reduce padding everywhere */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        h1, h2, h3 {
            color: #E8F4FD !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Loading indicator */
        .stSpinner > div {
            border-top-color: #0066FF !important;
        }
        
        /* Success/Error messages */
        .stSuccess {
            background: rgba(0, 102, 255, 0.1) !important;
            border: 1px solid #0066FF !important;
            color: #6699FF !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar with logo at top
    st.sidebar.image("https://logos-world.net/wp-content/uploads/2022/05/Cigna-Logo.png", width=150)
    st.sidebar.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
        <div style='background: linear-gradient(135deg, #000066 0%, #000099 100%); 
                    padding: 12px; border-radius: 8px; border: 1px solid #0066FF; margin-bottom: 12px;'>
            <div style='color: #6699FF; font-size: 12px; margin-bottom: 4px;'>SIGNED IN AS</div>
            <div style='color: #E8F4FD; font-size: 14px; font-weight: 600;'>{st.session_state.user_email}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.messages = []
        st.session_state.show_quote_form = False
        st.session_state.selected_plan = None
        st.rerun()
    
    st.sidebar.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
    
    # Get a Quote Button
    if st.sidebar.button("💰 Get a Quote", use_container_width=True, type="primary"):
        st.session_state.show_quote_form = not st.session_state.show_quote_form
        st.session_state.selected_plan = None
    
    # Quote Form
    if st.session_state.show_quote_form:
        st.sidebar.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
        
        st.sidebar.markdown("""
            <div style='background: linear-gradient(135deg, #000066 0%, #000099 100%); 
                        padding: 12px; border-radius: 8px; border: 1px solid #0066FF; margin-bottom: 12px;'>
                <div style='color: #0066FF; font-size: 14px; font-weight: 700; margin-bottom: 8px;'>
                    📋 INSURANCE QUOTE
                </div>
                <div style='color: #99BBFF; font-size: 12px;'>
                    Select your coverage level:
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Plan selection
        plan = st.sidebar.radio(
            "Coverage Level:",
            ["Bronze", "Silver", "Gold"],
            key="plan_selection"
        )
        
        if st.sidebar.button("Calculate Premium", use_container_width=True):
            st.session_state.selected_plan = plan
            st.rerun()
        
        # Display quote result
        if st.session_state.selected_plan:
            plan_prices = {
                "Bronze": "$600",
                "Silver": "$800", 
                "Gold": "$1,000"
            }
            
            premium = plan_prices[st.session_state.selected_plan]
            
            st.sidebar.markdown(f"""
                <div style='background: linear-gradient(135deg, #003300 0%, #004400 100%); 
                            padding: 16px; border-radius: 8px; border: 2px solid #00CC66; margin-bottom: 12px;'>
                    <div style='text-align: center; margin-bottom: 12px;'>
                        <div style='color: #00FF88; font-size: 12px; font-weight: 600; margin-bottom: 4px;'>
                            {st.session_state.selected_plan.upper()} PLAN
                        </div>
                        <div style='color: #FFFFFF; font-size: 28px; font-weight: 700;'>
                            {premium}
                        </div>
                        <div style='color: #99FFCC; font-size: 11px;'>
                            per month
                        </div>
                    </div>
                    <div style='border-top: 1px solid #00CC66; padding-top: 12px; margin-top: 12px;'>
                        <div style='color: #99FFCC; font-size: 11px; line-height: 1.5;'>
                            <strong>📌 Estimate Notice:</strong><br/>
                            This premium is an estimate based on existing information on record for your account.
                            <br/><br/>
                            Before the policy is issued, you may need to provide additional details for a final binding quote.
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True) 
       
    
    col1,col2 = st.columns([1.2, 0.8])       
        
    with col1:
        # Compact header with ALICE branding
        st.markdown("""
            <div style='background: linear-gradient(135deg, #000066 0%, #000099 100%); 
                        padding: 18px; border-radius: 10px; border: 1px solid #0066FF; margin-bottom: 12px;'>
                <div>
                    <h2 style='margin: 0; font-size: 24px; color: #E8F4FD; font-weight: 700;'>ALICE</h2>
                    <p style='margin: 4px 0 0 0; font-size: 12px; color: #99BBFF; font-style: italic;'>AI-Led Insurance Customer Experience</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Video placeholder at top (will show video after generation)
        video_container = st.empty()

    with col2:
        # Compact About section - expanded by default
        with st.expander("📚 Knowledge Base", expanded=True):
            st.markdown('<p style="font-size: 13px; color: #6699FF; margin-bottom: 8px;">Trained on Cigna documentation:</p>', unsafe_allow_html=True)
            st.image(image3_path, caption='Healthguard Brochure', use_column_width=True)
               
    st.sidebar.markdown('<p style="color: #6699FF; font-size: 12px; font-weight: 600; margin-bottom: 8px;">WELCOME VIDEO</p>', unsafe_allow_html=True)
    st.sidebar.write(f'<video width="100%" height="180" controls autoplay><source src="{video_path}" type="video/mp4"></video>', unsafe_allow_html=True)  
    
    st.sidebar.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="color: #6699FF; font-size: 12px; font-weight: 600; margin-bottom: 8px;">📞 CONTACT PREFERENCES</p>', unsafe_allow_html=True)

    add_selectbox = st.sidebar.selectbox(
        'Frequency',
        ('Daily', 'Weekly', 'Monthly','Never'),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
    
    add_selectbox = st.sidebar.selectbox(
        'Method',
        ('Email', 'WhatsApp', 'Phone'),
        label_visibility="collapsed"
    )

    # Display existing messages in the chat (in col1)
    with col1:
        if st.session_state.start_chat and len(st.session_state.messages) > 0:
            st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input and quick questions at bottom
        st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
        
        # Quick question tiles (only show if no conversation started)
        if len(st.session_state.messages) == 0:
            st.markdown('<p style="color: #6699FF; font-size: 14px; font-weight: 600; margin: 12px 0 8px 0;">💡 QUICK QUESTIONS</p>', unsafe_allow_html=True)
            
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                if st.button("📋 What is my policy limit?", use_container_width=True, key="q1"):
                    st.session_state.quick_question = "What is my policy limit?"
                    st.rerun()
            with col_q2:
                if st.button("📅 When is my policy due for renewal?", use_container_width=True, key="q2"):
                    st.session_state.quick_question = "When is my policy due for renewal?"
                    st.rerun()
            
            st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
        
        # Voice-to-text interface with microphone button
        st.markdown("""
            <div id="voice-input-container" style="margin-bottom: 8px;">
                <button id="voiceButton" style="
                    background: linear-gradient(135deg, #000066 0%, #000099 100%);
                    color: #6699FF;
                    border: 1px solid #0066FF;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: 600;
                " onmouseover="this.style.background='linear-gradient(135deg, #0066FF 0%, #0099FF 100%)'; this.style.color='#FFFFFF';" 
                   onmouseout="this.style.background='linear-gradient(135deg, #000066 0%, #000099 100%)'; this.style.color='#6699FF';">
                    🎤 Click to Speak
                </button>
                <span id="voiceStatus" style="color: #6699FF; margin-left: 12px; font-size: 13px;"></span>
            </div>
            
            <script>
                const voiceButton = document.getElementById('voiceButton');
                const voiceStatus = document.getElementById('voiceStatus');
                let recognition;
                let isListening = false;

                // Check if browser supports speech recognition
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = 'en-US';

                    voiceButton.onclick = function() {
                        if (!isListening) {
                            recognition.start();
                            isListening = true;
                            voiceButton.textContent = '🔴 Listening...';
                            voiceButton.style.background = 'linear-gradient(135deg, #CC0000 0%, #FF0000 100%)';
                            voiceButton.style.color = '#FFFFFF';
                            voiceStatus.textContent = 'Speak now...';
                        } else {
                            recognition.stop();
                            isListening = false;
                            voiceButton.textContent = '🎤 Click to Speak';
                            voiceButton.style.background = 'linear-gradient(135deg, #000066 0%, #000099 100%)';
                            voiceButton.style.color = '#6699FF';
                            voiceStatus.textContent = '';
                        }
                    };

                    recognition.onresult = function(event) {
                        const transcript = event.results[0][0].transcript;
                        voiceStatus.textContent = 'Recognized: ' + transcript;
                        
                        // Find the chat input and set the value
                        const chatInput = document.querySelector('textarea[data-testid="stChatInputTextArea"]');
                        if (chatInput) {
                            chatInput.value = transcript;
                            chatInput.dispatchEvent(new Event('input', { bubbles: true }));
                            
                            // Trigger submit after short delay
                            setTimeout(() => {
                                const submitButton = chatInput.parentElement.querySelector('button');
                                if (submitButton) {
                                    submitButton.click();
                                }
                            }, 500);
                        }
                        
                        isListening = false;
                        voiceButton.textContent = '🎤 Click to Speak';
                        voiceButton.style.background = 'linear-gradient(135deg, #000066 0%, #000099 100%)';
                        voiceButton.style.color = '#6699FF';
                    };

                    recognition.onerror = function(event) {
                        voiceStatus.textContent = 'Error: ' + event.error;
                        isListening = false;
                        voiceButton.textContent = '🎤 Click to Speak';
                        voiceButton.style.background = 'linear-gradient(135deg, #000066 0%, #000099 100%)';
                        voiceButton.style.color = '#6699FF';
                    };

                    recognition.onend = function() {
                        if (isListening) {
                            isListening = false;
                            voiceButton.textContent = '🎤 Click to Speak';
                            voiceButton.style.background = 'linear-gradient(135deg, #000066 0%, #000099 100%)';
                            voiceButton.style.color = '#6699FF';
                        }
                    };
                } else {
                    voiceButton.textContent = '🎤 Not Supported';
                    voiceButton.disabled = true;
                    voiceButton.style.opacity = '0.5';
                    voiceStatus.textContent = 'Voice input not supported in this browser';
                }
            </script>
        """, unsafe_allow_html=True)
    
    # Handle quick question button click - set flag but don't add to messages yet
    prompt_to_process = None
    if st.session_state.quick_question:
        prompt_to_process = st.session_state.quick_question
        st.session_state.quick_question = None  # Clear it immediately
                
    # Process prompt from chat input or quick question
    with col1:
        if prompt_to_process:
            # Quick question was clicked - process it directly
            pass  # Will be handled below
        elif prompt_input := st.chat_input("Ask ALICE anything about your insurance..."):
            prompt_to_process = prompt_input
        
        if prompt_to_process:
            
            print("---------------------PROMPT RECEIVED-------------------")
            print(f"PROMPT: {prompt_to_process}")
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt_to_process})
            print(f"MESSAGES: {st.session_state.messages}")
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt_to_process)

            # Get AI response using Chat Completions API
            with st.spinner("Thinking..."):
                ai_response = get_ai_response(st.session_state.messages)
            
            print(f"AI_RESPONSE: {ai_response}")

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            print(f"MESSAGES: {st.session_state.messages}")       
                                                              
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            
            # Generate video with ALICE branding and show loading at top
            with video_container.container():
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #000066 0%, #000099 100%); 
                                padding: 20px; border-radius: 10px; border: 2px solid #0066FF; 
                                text-align: center;'>
                        <h3 style='color: #0066FF; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;'>
                            ALICE is preparing your response
                        </h3>
                        <p style='color: #6699FF; font-size: 14px; margin: 0 0 4px 0;'>
                            Creating personalized video answer...
                        </p>
                        <p style='color: #99BBFF; font-size: 12px; margin: 0;'>
                            This takes 10-20 seconds
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.spinner(""):
                    video_url = generate_video(ai_response[:50])
            
            # Display video at top or show error
            if video_url and video_url != "error":
                with video_container.container():
                    st.write(f'<video width="100%" height="400" controls autoplay style="border-radius: 10px; border: 2px solid #0066FF; margin-bottom: 12px;"><source src="{video_url}" type="video/mp4"></video>', unsafe_allow_html=True)
            else:
                with video_container.container():
                    st.markdown("""
                        <div style='background: linear-gradient(135deg, #3D2200 0%, #4D3300 100%); 
                                    padding: 12px; border-radius: 8px; border: 1px solid #FF9900; 
                                    margin-bottom: 12px; text-align: center;'>
                            <span style='color: #FFBB00; font-size: 14px; font-weight: 600;'>⚠️ Video unavailable</span>
                        </div>
                    """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    # Must be first Streamlit command
    st.set_page_config(
        page_title="ALICE - Cigna Insurance Concierge",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    
    # Route to appropriate screen
    if st.session_state.authenticated:
        show_main_app()
    else:
        show_welcome_screen()

                 
if __name__ == "__main__":
    main()
