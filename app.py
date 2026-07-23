"""
Brick Detection System - Aplikasi Deteksi Tingkat Kematangan Batu Bata Merah dengan YOLOv8
"""

import streamlit as st
from config import APP_TITLE, APP_ICON, PAGE_LAYOUT
from utils.session import initialize_session_state
from pages.beranda import show_beranda
from pages.deteksi import show_deteksi
from pages.hasil import show_hasil

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="collapsed"
)

# ============ HIDE SIDEBAR & NAVBAR ============
st.markdown("""
<style>
    /* Sembunyikan sidebar sepenuhnya */
    [data-testid="stSidebar"] {
        display: none !important;
        width: 0 !important;
        min-width: 0 !important;
    }
    
    /* Sembunyikan tombol hamburger menu (3 garis) */
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    /* Sembunyikan tombol toggle sidebar di header */
    button[kind="header"] {
        display: none !important;
    }
    
    /* Sembunyikan Streamlit branding di pojok */
    #MainMenu {
        visibility: hidden !important;
    }
    
    footer {
        visibility: hidden !important;
    }
    
    header {
        visibility: hidden !important;
    }
    
    /* Lebarkan konten utama - full width */
    .main > div {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Hilangkan ruang kosong dari sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Hilangkan dekorasi header */
    .stAppHeader {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


# ============ INITIALIZE SESSION STATE ============
initialize_session_state()

# ============ PAGE ROUTING ============
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'beranda'

if st.session_state.current_page == 'beranda':
    show_beranda()
elif st.session_state.current_page == 'deteksi':
    show_deteksi()
elif st.session_state.current_page == 'hasil':
    show_hasil()