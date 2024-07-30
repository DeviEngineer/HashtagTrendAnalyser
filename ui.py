# ui.py
import streamlit as st

# Color Palette
primaryColor = "#4CAF50"
secondaryColor = "#E0E0E0"
backgroundColor = "#E1D6EF"
sidebarBackgroundColor = "#F0F0F0"
buttonColor = "#6A1B9A"
title_color = "#A020F0" 
header_color = "#00FFFF"

# Custom CSS for styling
custom_css = f"""
<style>
body {{
    background-color: {secondaryColor};
    font-family: Arial, sans-serif;
}}
[data-testid="stSidebar"] {{
    background-color: {sidebarBackgroundColor};
    font-family: Arial, sans-serif;
    color: #333333;
}}
.css-1v3fvcr {{
    font-size: 30px; /* Adjust size for headers */
    color: {header_color}; /* Use the header color */
    font-weight: bold; /* Make header bold */
}}
.stButton > button {{
    background-color: {buttonColor};
    color: white;
    padding: 15px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    border-radius: 5px;
}}
.stButton > button:hover {{
    background-color: #4A148C;
}}

.sidebar-title {{
    font-size: 48px; /* Adjust the size as needed */
    color: {title_color};
    font-weight: bold;
}}
</style>
"""

def apply_ui():
    st.set_page_config(page_title="Hashtag Analyzer", page_icon="")
    st.markdown(custom_css, unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-title">Hashtag Analyzer</div>', unsafe_allow_html=True)
    st.sidebar.image("C://Users//ADMIN//Desktop//GUVI//HTimg.png", use_column_width=True)
