import streamlit as st
import os
import pathlib
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv

def fasto():
    # Load environment variables from .env
    load_dotenv()
    os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    # App title
    st.title= "Fast Response"

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Store generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you?"}]

    # Create two columns
    col1, col2 = st.columns([3, 1])

    # User-provided prompt and chat messages in the left column
    with col1:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # User-provided prompt
        prompt = st.text_input("Enter your prompt:")

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Generate a new response if last message is not from assistant
            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = model.generate_content(prompt)
                        st.write(response.text) 
                message = {"role": "assistant", "content": response.text}
                st.session_state.messages.append(message)

    # Select box for user role in the right column
    with col2:
        role = st.selectbox(
            "Select your role:",
            ("Doctor", "Electronic Expert", "Lawyer", "Chef"),
            index=None,
            placeholder="Select a role...",
        )

        # Predefined chat prompt templates
        templates = {
            "Doctor": "As a doctor, I can help you with medical advice.",
            "Electronic Expert": "As an electronic expert, I can help you with electronic devices.",
            "Lawyer": "As a lawyer, I can help you with legal advice.",
            "Chef": "As a chef, I can help you with cooking advice.",
        }

        # Add the selected role's template to the prompt
        if role in templates:
            prompt += " " + templates[role]

if __name__ == "__main__":
    fasto()
