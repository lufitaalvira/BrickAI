"""
Styling loader
"""
import streamlit as st
from pathlib import Path


def load_css():
    """Load CSS dari file eksternal"""
    css_path = Path("assets/styles.css")
    if css_path.exists():
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Error loading CSS: {e}")


def apply_all_styles():
    """Apply semua styling"""
    load_css()

