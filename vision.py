import os
import time
from PIL import Image
import streamlit as st
import google.generativeai as genai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure the Google AI Python SDK
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    # print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    # print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    # print("...all files ready")
    # print()

def get_gemini_response(input, image):
    context = """Generates a response based on the image and input prompt."""
    model = genai.GenerativeModel('gemini-pro-vision')
    if input != "":
        input += context
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

def visoto():
    """Main function to run the Streamlit app."""
    st.title = "Gemini Image Demo"
    st.header ="Image Chat Assistant" 
    input = st.text_input("Input Prompt: ", key="input")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""   
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    submit = st.button("Tell me about the image")
    if submit:
        response = get_gemini_response(input, image)
        st.subheader("The Response is")
        st.write(response)

# if __name__ == "__main__":
#     main()
