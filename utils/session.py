"""
Session state utilities
"""
import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'beranda'
    if 'detection_results' not in st.session_state:
        st.session_state.detection_results = None
    if 'detection_image' not in st.session_state:
        st.session_state.detection_image = None
    if 'detection_stats' not in st.session_state:
        st.session_state.detection_stats = None
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None
    if 'detection_history' not in st.session_state:
        st.session_state.detection_history = []
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'detection_method' not in st.session_state:
        st.session_state.detection_method = 'upload'
    if 'detected_classes' not in st.session_state:
        st.session_state.detected_classes = []
    if 'total_detections' not in st.session_state:
        st.session_state.total_detections = 0
    if 'detected_groups' not in st.session_state:
        st.session_state.detected_groups = []
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None


def set_page(page_name):
    """
    Set current page in session state and rerun
    
    Args:
        page_name: Nama halaman tujuan ('beranda', 'deteksi', 'hasil')
    """
    st.session_state.current_page = page_name
    st.rerun()


def go_to_beranda():
    """Redirect ke halaman beranda"""
    set_page('beranda')


def go_to_deteksi():
    """Redirect ke halaman deteksi"""
    set_page('deteksi')


def go_to_hasil():
    """Redirect ke halaman hasil"""
    set_page('hasil')


def reset_detection_state():
    """Reset detection-related session state"""
    st.session_state.detection_results = None
    st.session_state.detection_image = None
    st.session_state.detection_stats = None
    st.session_state.uploaded_image = None
    st.session_state.uploaded_filename = None
    st.session_state.detected_classes = []
    st.session_state.total_detections = 0
    st.session_state.detected_groups = []


def add_to_history(item):
    """Add item to detection history"""
    if 'detection_history' not in st.session_state:
        st.session_state.detection_history = []
    st.session_state.detection_history.append(item)


def get_history():
    """Get detection history"""
    return st.session_state.get('detection_history', [])


def reset_all_state():
    """Reset all session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()