"""
Image processing utilities
"""
import base64
from PIL import Image
import numpy as np
import cv2


def image_to_base64(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""


def load_image(uploaded_file):
    """Load image dari Streamlit uploaded file"""
    try:
        image = Image.open(uploaded_file)
        return np.array(image)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def load_image_cv2(uploaded_file):
    """Load image dengan OpenCV format (BGR)"""
    try:
        image = Image.open(uploaded_file)
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return image_cv
    except Exception as e:
        print(f"Error: {e}")
        return None


def resize_image(image, max_width=800):
    """Resize image untuk display"""
    try:
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        width, height = image.size
        if width > max_width:
            ratio = max_width / width
            new_height = int(height * ratio)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    except Exception as e:
        print(f"Error: {e}")
        return image


def validate_image_format(filename, allowed_formats):
    """Validate image format"""
    file_ext = filename.split('.')[-1].lower()
    return file_ext in allowed_formats


def convert_rgb_to_bgr(image):
    """Convert RGB ke BGR (OpenCV format)"""
    if isinstance(image, np.ndarray):
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def convert_bgr_to_rgb(image):
    """Convert BGR ke RGB"""
    if isinstance(image, np.ndarray):
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image
