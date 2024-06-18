import streamlit as st
import tempfile
from pinecone import ServerlessSpec
import qanda
from langchain_community.document_loaders import UnstructuredFileLoader
from documentchat import get_text_chunks,get_pdf_text
from vector_search import encodeaddData,find_k_best_match1,delete,ensure_index_exists
from utils import *
from dotenv import load_dotenv
from io import StringIO
import os
from pinecone.grpc import PineconeGRPC as pinecone
import cv2
def fasto():

    ensure_index_exists()
    def get_loader(file_path):
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in ['.pdf', '.txt', '.html', '.htm', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.gif','.xlsx']:
            return UnstructuredFileLoader(file_path, mode="elements")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    _ , col2,_ = st.columns([1,7,1])
    with col2:
        col2 = st.header="Simplchat: Chat with your data"
        url = False
        query = False
        pdf = False
        pdf2 = False
        data = False
        uns2 = None
        options = st.selectbox("Select the type of data source",
                        options=['Web URL','PDF','Unstructured Data','Existing data source'])
        if options == 'Web URL':
            url = st.text_input("Enter the URL of the data source")
            query = st.text_input("Enter your query")
            button = st.button("Submit")
        elif options == 'PDF':
            pdf = st.text_input("Enter your PDF link here") 
            st.write("Or choose .pdf from your local machine")
            pdf2 = st.file_uploader("Choose pdf file:", type="pdf",accept_multiple_files=True)
            query = st.text_input("Enter your query")
            button = st.button("Submit")
        elif options == 'Unstructured Data':
            # uns = st.text_input("Enter your File link here") 
            st.write("choose .* from your local machine")
            uns2 = st.file_uploader("Enter any file", accept_multiple_files=True)
            query = st.text_input("Enter your query")
            button = st.button("Submit")
        elif options == 'Existing data source':
            data= True
            query = st.text_input("Enter your query")
            button = st.button("Submit")  
    if button and url:
        with st.spinner("Updating the database..."):
            corpusData = scrape_text(url)
            encodeaddData(corpusData, url=url, pdf=False, pdf2=None,uns2 = None)
            st.success("Database Updated")
        with st.spinner("Finding an answer..."):
            res = find_k_best_match1(query)
            context = "\n\n".join([doc.page_content for doc in res])
            st.expander("Context").write(context)
            prompt = qanda.prompt(context,query)
            answer = qanda.get_answer(prompt)
            st.success("Answer: "+ answer)


    if button and pdf:
        with st.spinner("Updating the database..."):
            corpusData = pdf_text(pdf=pdf)
            encodeaddData(corpusData, pdf=pdf, url=False, pdf2=None,uns2 = None)
            st.success("Database Updated")
        with st.spinner("Finding an answer..."):
            res = find_k_best_match1(query)
            context = "\n\n".join([doc.page_content for doc in res])
            st.expander("Context").write(context)
            prompt = qanda.prompt(context,query)
            answer = qanda.get_answer(prompt)
            st.success("Answer: "+ answer)
            
    if button and pdf2:
        with st.spinner("Updating the database..."):
            text = get_pdf_text(pdf2)
            corpusData = get_text_chunks(text)
            # corpusData = extract_data(feed=pdf2)
            encodeaddData(corpusData, pdf2=pdf2, url=False, pdf=False,uns2 = None) 
            st.success("Database Updated")
        with st.spinner("Finding an answer..."):
            res = find_k_best_match1(query)
            context = "\n\n".join([doc.page_content for doc in res])
            st.expander("Context").write(context)
            prompt = qanda.prompt(context,query)
            answer = qanda.get_answer(prompt)
            st.success("Answer: "+ answer)


    if button and uns2:
        with st.spinner("Updating the database..."):
            page_content = ""  # Initialize as string
            metadata = {}  # Initialize an empty dictionary for metadata
            
            for uploaded_file in uns2:
                # Create a temporary file to save the uploaded file
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_file_path = temp_file.name

                try:
                    # Get the appropriate loader based on file type
                    loader = get_loader(temp_file_path)
                    docs = loader.load()

                    # Extract and concatenate the loaded documents' content
                    for doc in docs:
                        if hasattr(doc, 'page_content'):
                            page_content += doc.page_content + "\n"  # Concatenate page_content
                        else:
                            st.warning(f"Document object has no 'page_content' attribute: {doc}")

                        # Example of setting metadata (adjust as needed)
                        metadata['uploaded_files'] = uns2  # Store the uploaded files information
                        metadata['loader_used'] = str(loader)  # Store the loader information

                except ValueError as e:
                    st.warning(str(e))
                finally:
                    # Delete the temporary file
                    os.remove(temp_file_path)

            # Create document data with page_content and metadata
            document_data = {'page_content': page_content, 'metadata': metadata}
            metadata = document_data['metadata']
            corpusData = document_data['page_content']
            encodeaddData(corpusData, pdf=False, url=False, pdf2=None,uns2=metadata['uploaded_files'])
            st.success("Database Updated")

        with st.spinner("Finding an answer..."):
            res = find_k_best_match1(query)
            context = "\n\n".join([doc.page_content for doc in res])
            st.expander("Context").write(context)
            prompt = qanda.prompt(context,query)
            answer = qanda.get_answer(prompt)
            st.success("Answer: "+ answer)
            
    if button and data:
        with st.spinner("Finding an answer..."):
            res = find_k_best_match1(query)
            context = "\n\n".join([doc.page_content for doc in res])
            st.expander("Context").write(context)
            prompt = qanda.prompt(context,query)
            answer = qanda.get_answer(prompt)
            st.success("Answer: "+ answer)
            
            
    st.expander("Delete the indexes from the database")
    button1 = st.button("Delete the current vectors")
    if button1:
        delete()
    
