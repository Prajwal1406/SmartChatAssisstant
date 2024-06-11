import streamlit as st
import os
import pathlib
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv

def accuto():
    # Load environment variables from .env
    load_dotenv()
    os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    # App title
    st.title="Smart Assistant"

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')

    # Store generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = model.generate_content(
                    prompt
                )
                st.write(response.text) 
        message = {"role": "assistant", "content": response.text}
        st.session_state.messages.append(message)
