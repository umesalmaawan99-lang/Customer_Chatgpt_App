import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title='Your Custom Assistant',
    page_icon='🤖'
)

st.subheader('Your Custom ChatGPT🤖')

# --- SIDEBAR: API KEY & CHAT SESSIONS ---
with st.sidebar:
    st.title("🔐 Configuration")
    
    # User inputs OpenAI API key here for deployment security
    user_api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    if user_api_key:
        os.environ["OPENAI_API_KEY"] = user_api_key
        st.success("API Key loaded successfully!")
    else:
        st.warning("Please enter your OpenAI API key to use the app.")

    st.divider()
    st.subheader("💬 Chat Sessions")
    
    # Managing chat history list in sidebar
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = ["Session 1"]
        
    selected_session = st.selectbox("Select Past Chat", st.session_state.chat_sessions)
    
    if st.button("➕ New Chat"):
        new_session_name = f"Session {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions.append(new_session_name)
        st.rerun()

    st.divider()
    system_message = st.text_input(label='System role', placeholder="e.g., You are a helpful python tutor")

# --- APP LOCK UNLESS API KEY IS PROVIDED ---
if not os.environ.get("OPENAI_API_KEY"):
    st.info("👈 Please enter your OpenAI API Key in the sidebar login screen to unlock your custom ChatGPT app.")
    st.stop()

# Initialize Chat Model
#chat = ChatOpenAI(model_name='gpt-3.5', temperature=0.5)

# Change this line:
# chat = ChatOpenAI(model_name='gpt-3.5', temperature=0.5)

# To this:  
chat = ChatOpenAI(model_name='gpt-4o-mini', temperature=0.5)
# chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

# Initializing messages in session state (fixed typo from 'message' to 'messages')
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Handle System Message
if system_message:
    if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
        st.session_state.messages.append(
            SystemMessage(content=system_message)
        )

# User chat input at the bottom of the screen
user_prompt = st.chat_input("Send a message...")

if user_prompt:
    st.session_state.messages.append(
        HumanMessage(content=user_prompt)
    )
    with st.spinner('Working on your request...'):
        response = chat.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

# Adding a default SystemMessage if none entered
if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant.'))

# Display chat messages (skipping index 0 which is the SystemMessage)
for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("human"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.write(msg.content)