"""
Camera utilities
"""
import streamlit as st
import cv2


def capture_from_camera():
    """Tangkap gambar dari webcam"""
    try:
        picture = st.camera_input("Ambil foto dari kamera")
        if picture is not None:
            return picture
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def test_camera_access():
    """Test akses kamera"""
    try:
        cap = cv2.VideoCapture(0)
        ret = cap.isOpened()
        cap.release()
        return ret
    except:
        return False
