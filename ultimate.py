import app as ap
import accurate as acc
import vision as vis
import streamlit as st
import documentchat as dc
from vector_search import ensure_index_exists
ensure_index_exists()
st.sidebar.title="Smart Chat Assisstant"

# Add a dropdown to select a page
page = st.sidebar.selectbox("Select Model", ("Chat With Your Data", "Accurate", "Vision","Chat With Your Documents locally"))

# Display different content based on the selected page
if page == "Chat With Your Data":
    ensure_index_exists()
    ap.fasto()

elif page == "Accurate":
    acc.accuto()

elif page == "Vision":
    vis.visoto()

elif page == "Chat With Your Documents locally":
    dc.docu()