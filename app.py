import streamlit as st
import openai
from pinecone import ServerlessSpec
import qanda
from documentchat import get_text_chunks,get_pdf_text
from vector_search import encodeaddData,find_k_best_match1,delete,ensure_index_exists
from utils import *
from io  import StringIO
from dotenv import load_dotenv
import os
from pinecone.grpc import PineconeGRPC as pinecone
def fasto():
    ensure_index_exists()
    _ , col2,_ = st.columns([1,7,1])
    with col2:
        col2 = st.header="Simplchat: Chat with your data"
        url = False
        query = False
        pdf = False
        pdf2 = False
        data = False
        options = st.selectbox("Select the type of data source",
                                options=['Web URL','PDF','Existing data source'])
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
        elif options == 'Existing data source':
            data= True
            query = st.text_input("Enter your query")
            button = st.button("Submit")  
    if button and url:
        with st.spinner("Updating the database..."):
            corpusData = scrape_text(url)
            encodeaddData(corpusData, url=url, pdf=False, pdf2=None)
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
            encodeaddData(corpusData, pdf=pdf, url=False, pdf2=None)
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
            encodeaddData(corpusData, pdf2=pdf2, url=False, pdf=False) 
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
    