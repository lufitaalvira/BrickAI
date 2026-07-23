"""
Navbar component untuk Brick Detection System
"""
import streamlit as st


def show_navbar():
    """Render navbar component"""
    st.markdown("""
    <div class="navbar">
        <div class="navbar-logo">Brick<span>AI</span></div>
        <div class="navbar-tag">Computer Vision Platform</div>
    </div>
    """, unsafe_allow_html=True)


def show_navbar_with_nav(current_page):
    """Render navbar dengan navigation links"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("""
        <div class="navbar-logo">Brick<span>AI</span></div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="navbar-tag">Computer Vision Platform</div>
        """, unsafe_allow_html=True)
