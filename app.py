import streamlit as st
from dashboard import show_dashboard
from timecode_page import show_timecode_page

# Sidebar navigation
page = st.sidebar.radio(
    "Select a Page",
    ("Chat Sentiment Analysis", "Timecode Event Selector")
)

if page == "Chat Sentiment Analysis":
    show_dashboard()
else:
    show_timecode_page()