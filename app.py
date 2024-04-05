import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import courses_scrap as scrap
# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="wide",  # Page layout option
)

# Load Google API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API key is available
if not GOOGLE_API_KEY:
    st.error(
        "Google API key not found. Please set GOOGLE_API_KEY environment variable.")
    st.stop()  # Stop execution if API key is not found

# Initialize Google Gemini-Pro AI model
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Failed to initialize Gemini-Pro AI model: {e}")
    st.stop()  # Stop execution if model initialization fails

current_theme = st.session_state.get("current_theme", "light")
t1 = st.session_state.get("t1", " Dark 🌜")

# Button to toggle dark and light themes
if st.button(f"{t1}", key="theme_toggle_button"):
    if current_theme == "light":
        st.session_state["t1"] = " Dark 🌜"
        st.session_state["current_theme"] = "dark"
        st._config.set_option(f'theme.base', "dark")
    else:
        st.session_state["t1"] = " Light 🌞"
        st.session_state["current_theme"] = "light"
        st._config.set_option(f'theme.base', "light")

# Function to translate roles between Gemini-Pro and Streamlit terminology


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Function to check if input contains keywords related to domains or careers
def contains_keywords(input_text):
    # Add more keywords as needed
    keywords = ["web", "app", "cyber", "aiml", "artificial intelligence" ,"iot" ,"cybersecurity","video editing","graphic designing","machine learning","data science"]
    return [keyword for keyword in keywords if keyword in input_text]

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Failed to start chat session: {e}")
        st.stop()  # Stop execution if chat session initialization fails

# Initialize set to store unique search terms
if "search_history" not in st.session_state:
    st.session_state.search_history = set()

# Display the chatbot's title on the page
st.title("🎓🤖 CareerGPT")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask CareerGPT...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    # Send user's message to Gemini-Pro and get the response
    try:
        gemini_response = st.session_state.chat_session.send_message(
            "Roadmap on "+user_prompt+" domain and also give examples of softwares. Have Software section as '##Software Examples'")
    except Exception as e:
        st.error(f"Failed to send message to CareerGPT: {e}")
        st.stop()  # Stop execution if sending message fails
    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
        found_keywords = contains_keywords(user_prompt.lower())
        if found_keywords:
            # Display related links for each found keyword
            courses_links =[]
            for keyword in found_keywords:
                st.markdown(f"### Courses related to {keyword.capitalize()} domain:")
                url = f"https://www.coursebuffet.com/search?q={keyword}"
                courses_links=scrap.scrapit(url)
                courses_list = "\n".join([f"<li><a href='{link}' target='_blank'>{link}</a></li>" for link in courses_links])
                st.markdown(f"<ol>{courses_list}</ol>", unsafe_allow_html=True)
                
    # Add user's message to search history set
    st.session_state.search_history.add(user_prompt)

# Sidebar tab to display past search history
with st.sidebar:
    st.title("Search History")
    for idx, search in enumerate(st.session_state.search_history):
        if st.sidebar.button(f"{idx+1}. {search}"):
            try:
                st.session_state.chat_session.send_message(search)
            except Exception as e:
                st.error(f"Failed to send message to CareerGPT: {e}")
