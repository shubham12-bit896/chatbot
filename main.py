import os 

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load envireonment variables 
load_dotenv()

# Configure Streamlite page settings 
st.set_page_config(
    page_title="Chat with Gemini_Pro!",
    page_icon=":brain:", # Icon for the page
    layout="centered", # Layout of the page
)

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Sidebar: model selection
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose Gemini Model:",
    ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-flash-latest", "gemini-pro-latest"],
    index=0
)

# Set up Google-Pro AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_choice)

# Function to translate roles between Gemini and Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else "user"

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are a helpful AI chatbot named Gemchat. "
                    "You were created by Shubham, not Google. "
                    "Always introduce yourself as Gemchat when talking to users."
                ]
            }
        ]
    )

# Display chatbot title
st.title("Gemni_Pro Chatbot :brain:")
st.write("Ask anything you want!")

# Display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(translate_role_for_streamlit(message["author"])):
        st.markdown(message["content"])

# Accept user input
user_prompt=st.chat_input("Ask me anything!")
if user_prompt:
    # Add users message to char history
    st.chat_message("user").markdown(user_prompt)

    # send users message to gemini-pro and get the response 
    gemini_response=st.session_state.chat_session.send_message(user_prompt)

    #Display gemini-pro's response in the chat message container
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

    # Save both user and model messages to chat history
    st.session_state.chat_history.append({"author": "user", "content": user_prompt})
    st.session_state.chat_history.append({"author": "model", "content": gemini_response.text})

