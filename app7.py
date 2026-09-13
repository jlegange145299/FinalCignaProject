from openai import OpenAI
import time
import streamlit as st
import requests
from dotenv import load_dotenv
import os


load_dotenv()

DID_API_ENV = os.getenv("DID_API")

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

def get_ai_response(client, messages):
    """Get response from OpenAI using Chat Completions API"""
    try:
        system_message = {
            "role": "system",
            "content": """You are a helpful assistant for Cigna Health Insurance, specifically for the Healthguard product. 
            You answer questions about Cigna health insurance plans, coverage, benefits, and policies. 
            Be professional, informative, and concise. If you don't know something, say so clearly."""
        }
        
        # Combine system message with conversation history
        full_messages = [system_message] + messages
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return f"I apologize, but I encountered an error: {str(e)}"

def show_welcome_screen():
    """Display welcome/login screen"""
    st.markdown("""
        <style>
        .welcome-container {
            text-align: center;
            padding: 50px 20px;
        }
        .welcome-title {
            font-size: 48px;
            font-weight: bold;
            color: #FF4D00;
            margin-bottom: 20px;
        }
        .welcome-subtitle {
            font-size: 24px;
            color: #0033FF;
            margin-bottom: 40px;
        }
        .welcome-description {
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center column for login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Cigna logo
        st.image("https://logos-world.net/wp-content/uploads/2022/05/Cigna-Logo.png", width=400)
        
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
        st.markdown('<div class="welcome-title">Welcome to Cigna AI Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtitle">Your Personal Health Insurance Guide</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="welcome-description">
            Get instant answers about your Cigna Healthguard coverage, benefits, and policies.<br>
            Powered by AI with personalized video responses.
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Login form
        st.markdown("### 🔐 Sign In to Continue")
        
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b, col_c = st.columns([1, 1, 1])
            with col_b:
                submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if email and password:
                    # Simple validation (you can enhance this)
                    if "@" in email and len(password) >= 6:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.success("✅ Login successful! Redirecting...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please check your email format and ensure password is at least 6 characters.")
                else:
                    st.warning("⚠️ Please enter both email and password.")
        
        st.markdown("---")
        st.caption("Don't have an account? Contact your Cigna administrator.")
        st.caption("Forgot password? [Reset here](#)")


def show_main_app():
    """Display main chat application"""
    api_key = st.secrets["OPENAI_API_KEY"]
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
    
    # Initialize OpenAI client
    st.session_state.client = OpenAI(api_key=api_key)
    
    if st.session_state.client:
        st.session_state.start_chat = True
    
    # User info and logout in sidebar
    st.sidebar.markdown(f"### 👤 Welcome!")
    st.sidebar.markdown(f"**{st.session_state.user_email}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.messages = []
        st.rerun()
    
    st.sidebar.markdown("---") 
       
    
    col1,col2 = st.columns(2)       
        
    with col1:
        # Add custom CSS for question tiles
        st.markdown("""
            <style>
            .question-tile {
                background-color: #f0f2f6;
                border: 2px solid #FF4D00;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: center;
                font-weight: 500;
            }
            .question-tile:hover {
                background-color: #FF4D00;
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Cigna logo
        image_path = "https://logos-world.net/wp-content/uploads/2022/05/Cigna-Logo.png"
        st.image(image_path, caption='',width=300)
        
        # Quick question tiles (only show if no conversation started)
        if len(st.session_state.messages) == 0:
            st.markdown("### 💡 Quick Questions")
            
            col_q1, col_q2 = st.columns(2)
            with col_q1:
                if st.button("📋 What is my policy limit?", use_container_width=True, key="q1"):
                    st.session_state.quick_question = "What is my policy limit?"
                    st.rerun()
            with col_q2:
                if st.button("📅 When is my policy due for renewal?", use_container_width=True, key="q2"):
                    st.session_state.quick_question = "When is my policy due for renewal?"
                    st.rerun()

    with col2:
        with st.expander("About",expanded=True):             
                st.header("I am trained on the below collaterals")
                st.image(image3_path, caption='https://photosfordidd.s3.eu-central-1.amazonaws.com/Cigna+Healthguard+Brochure.pdf')
                #st.image(image4_path, caption='',width=640)
               
    st.sidebar.write(f'<video width="300" height="220" controls autoplay><source src="{video_path}" type="video/mp4"></video>', unsafe_allow_html=True)  

    add_selectbox = st.sidebar.selectbox(
        'How often would you like to be contacted?',
        ('Daily', 'Weekly', 'Monthly','Never')
    )
    
    add_selectbox = st.sidebar.selectbox(
        'How would you like to be contacted?',
        ('Email', 'WhatsApp', 'Phone')
    )
    
    slider_value = st.sidebar.slider("How satisfied out of 10 were you with your last Cigna interaction?", 0, 10, 5)

    
    # Display existing messages in the chat (in col1)
    with col1:
        if st.session_state.start_chat:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    
    # Handle quick question button click
    prompt_to_process = None
    if st.session_state.quick_question:
        prompt_to_process = st.session_state.quick_question
        st.session_state.quick_question = None  # Clear it
        # Add to messages and process
        st.session_state.messages.append({"role": "user", "content": prompt_to_process})
        st.rerun()
                
    # Process prompt from chat input
    with col1:
        if prompt_to_process or (prompt_input := st.chat_input("Ask me anything about your Cigna coverage...")):
            if not prompt_to_process:
                prompt_to_process = prompt_input
            
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
                ai_response = get_ai_response(st.session_state.client, st.session_state.messages)
            
            print(f"AI_RESPONSE: {ai_response}")

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            print(f"MESSAGES: {st.session_state.messages}")       
                                                              
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            
            # Generate video with enhanced loading indicator
            video_placeholder = st.empty()
            
            with video_placeholder.container():
                st.markdown("""
                    <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; border-left: 5px solid #FF4D00;'>
                        <h3 style='color: #FF4D00; margin-bottom: 10px;'>🎬 Creating Your Video Response</h3>
                        <p style='color: #666; font-size: 16px;'>Our AI avatar is preparing to answer your question...</p>
                        <p style='color: #999; font-size: 14px;'>This usually takes 10-20 seconds</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.spinner(""):
                    video_url = generate_video(ai_response[:50])
            
            video_placeholder.empty()  # Clear the loading message
            
            if video_url and video_url != "error":
                st.success("✅ Video ready! Press play to watch.")
                st.write(f'<video width="640" height="480" controls autoplay><source src="{video_url}" type="video/mp4"></video>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Video generation unavailable. Your text response is shown above.")


def main():
    """Main application entry point"""
    # Must be first Streamlit command
    st.set_page_config(
        page_title="Cigna AI Assistant",
        page_icon="📚",
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
