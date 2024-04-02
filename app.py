import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Initialize search history list
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# Display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

    # Append user's message to search history
    st.session_state.search_history.append(user_prompt)

# Sidebar tab to display past search history
with st.sidebar:
    st.title("Search History")
    for idx, search in enumerate(reversed(st.session_state.search_history)):
        if st.sidebar.button(f"{idx+1}. {search}"):
            st.session_state.search_history.append(search)
            user_prompt = search
            st.session_state.chat_session.send_message(user_prompt)
