
"""
Model loader utilities
"""
import streamlit as st
from ultralytics import YOLO
from pathlib import Path
from config import MODEL_PATH


@st.cache_resource
def load_model():
    """
    Load YOLO model dengan caching
    
    Returns:
        YOLO model or None if error
    """
    try:
        model_path = Path(MODEL_PATH)
        if not model_path.exists():
            st.error(f"❌ Model tidak ditemukan di: {model_path}")
            return None
        
        model = YOLO(str(model_path))
        return model
    
    except Exception as e:
        st.error(f"❌ Gagal memuat model: {str(e)}")
        return None


def get_model():
    """Get loaded model (alias untuk load_model)"""
    return load_model()
