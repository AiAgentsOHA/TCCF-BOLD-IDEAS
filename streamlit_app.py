import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="TCCF Bold Ideas Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] {display: none;}
    .stApp {
        background: #0a1628;
    }
</style>
""", unsafe_allow_html=True)

html_file_path = os.path.join(os.path.dirname(__file__), 'TCCF_Bold_Ideas_Dashboard.html')

if os.path.exists(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
else:
    with open('TCCF_Bold_Ideas_Dashboard.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

components.html(html_content, height=2000, scrolling=True)
