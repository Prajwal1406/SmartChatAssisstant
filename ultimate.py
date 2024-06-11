import app as ap
import accurate as acc
import vision as vis
import streamlit as st
import documentchat as dc

st.sidebar.title("My Sidebar")

# Add a dropdown to select a page
page = st.sidebar.selectbox("Select Model", ("Fastest", "Accurate", "Vision","Chat With Your Documents"))

# Display different content based on the selected page
if page == "Fastest":
    ap.fasto()

elif page == "Accurate":
    acc.accuto()

elif page == "Vision":
    vis.visoto()

elif page == "Chat With Your Documents":
    dc.main()