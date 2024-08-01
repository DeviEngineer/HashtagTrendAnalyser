import streamlit as st
# Apply custom UI
def apply_ui():
    primaryColor = "#4CAF50"    
    secondaryColor = "#E0E0E0"    
    backgroundColor = "#E1D6EF"
    sidebarBackgroundColor = "#F0F0F0"    
    buttonColor = "#6A1B9A"    
    title_color = "#6A1B9A"
    header_color = "#12BE5D"
    custom_css = f"""<style>
    body {{ background-color: {secondaryColor};font-family: Arial, sans-serif;
        background-size: cover;background-repeat: no-repeat;background-attachment: fixed;
         }}
    [data-testid="stSidebar"] 
         {{ background-color: {sidebarBackgroundColor};font-family: Arial, sans-serif;
           color: #333333;
         }}
    .stButton > button
         {{ background-color: {buttonColor}; color: white; padding: 15px 25px; text-align: center;
         text-decoration: none; display: inline-block; font-size: 16px;border-radius: 5px;
         }}
    .stButton > button:hover 
         {{ background-color: #4A148C;}}
    .sidebar-header {{font-size: 24px; color: {title_color};font-weight: bold;    }}
    </style"""
    st.markdown(custom_css, unsafe_allow_html=True)

 
