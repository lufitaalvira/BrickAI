"""
Halaman Hasil Deteksi - Brick AI
"""
import streamlit as st
import base64
import io
from PIL import Image
import os
from utils.session import set_page, reset_detection_state


def show_hasil():
    """Render halaman hasil deteksi"""
    
    # ====== HEADER ======
    st.markdown("""
    <div style="text-align: left; padding: 5px 0 5px 0;">
        <h1 style="font-size: 32px; font-weight: 800; color: #1a1a1a; margin: 0;">
            <span style="color: #e86930;">🧱 Brick</span><span style="color: #1a1a1a;">AI</span>
        </h1>
        <p style="color: #999; font-size: 14px; margin: 0; font-weight: 500;">
            Hasil Deteksi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ====== AMBIL DATA DARI SESSION STATE ======
    img_src = st.session_state.get('detection_image_base64', None)
    
    if img_src is None:
        detection_image = st.session_state.get('detection_image', None)
        if detection_image is not None:
            try:
                if isinstance(detection_image, Image.Image):
                    img_bytes = io.BytesIO()
                    detection_image.save(img_bytes, format="PNG")
                    img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
                    img_src = f"data:image/png;base64,{img_base64}"
                    st.session_state.detection_image_base64 = img_src
            except Exception as e:
                st.sidebar.error(f"Error konversi: {e}")
    
    detected_classes = st.session_state.get('detected_classes', [])
    stats = st.session_state.get('detection_stats', {})
    
    # ====== HITUNG HASIL ======
    has_detected_class = len(detected_classes) > 0
    
    if has_detected_class:
        class_counts = {}
        for cls in detected_classes:
            class_counts[cls] = class_counts.get(cls, 0) + 1
        main_class = max(class_counts, key=class_counts.get) if class_counts else "Tidak Ada"
        
        main_confidence = 0
        # FIX: key yang benar adalah 'class_confidences' (jamak),
        # bukan 'class_confidence'. Sebelumnya typo ini membuat
        # stats.get(...) selalu mengembalikan dict kosong sehingga
        # akurasi selalu 0%.
        for cls, conf in stats.get('class_confidences', {}).items():
            if cls == main_class:
                main_confidence = conf
                break
        
        # Fallback tambahan: kalau karena suatu sebab main_confidence
        # masih 0 (mis. nama kelas berbeda kapitalisasi), pakai
        # avg_confidence dari stats sebagai cadangan agar tidak
        # menampilkan 0% padahal sebenarnya ada deteksi.
        if main_confidence <= 0:
            main_confidence = stats.get('avg_confidence', 0)
        
        accuracy = main_confidence * 100 if main_confidence > 0 else 0
    else:
        main_class = "Tidak Terdeteksi"
        accuracy = 0
    
    # ====== DESKRIPSI ======
    st.markdown("""
    <p style="color: #666; font-size: 14px; text-align: left; margin: 5px 0 20px 0;">
        Berikut adalah hasil analisis citra untuk sampel <strong>Batu Bata Merah</strong>.
    </p>
    """, unsafe_allow_html=True)
    
    # ====== LAYOUT ======
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if img_src is not None and img_src != "":
            st.markdown(f"""
            <div style="background: #f5f1e8; border-radius: 12px; padding: 12px; 
                        border: 1px solid #e8e0d0;">
                <img src="{img_src}" style="width: 100%; border-radius: 8px; 
                        max-height: 400px; object-fit: contain;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f5f1e8; border-radius: 12px; padding: 50px 20px; 
                        border: 1px solid #e8e0d0; text-align: center;">
                <div style="font-size: 40px;">📸</div>
                <p style="color: #e74c3c; font-size: 13px; font-weight: 600;">
                    ⚠️ Gambar tidak ditemukan
                </p>
                <p style="color: #999; font-size: 11px; margin-top: 8px;">
                    Silakan upload gambar di halaman Deteksi
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # ====== KATEGORI ======
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <p style="font-size: 12px; color: #aaa; margin: 0 0 6px 0; font-weight: 600; letter-spacing: 1px;">
                Kategori
            </p>
        """, unsafe_allow_html=True)
        
        if has_detected_class:
            st.markdown(f"""
            <div style="background: #faf8f5; border-radius: 8px; padding: 10px 16px; 
                        border: 2px solid #e86930;">
                <span style="font-size: 18px; font-weight: 700; color: #e86930;">
                    {main_class}
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #faf8f5; border-radius: 8px; padding: 10px 16px; 
                        border: 2px solid #dc3545;">
                <span style="font-size: 16px; font-weight: 700; color: #dc3545;">
                    Tidak Terdeteksi
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ====== AKURASI ======
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <p style="font-size: 12px; color: #aaa; margin: 0 0 4px 0; font-weight: 600; letter-spacing: 1px;">
                Akurasi
            </p>
        """, unsafe_allow_html=True)
        
        if has_detected_class and accuracy > 0:
            st.markdown(f"""
            <p style="font-size: 30px; font-weight: 800; color: #e86930; margin: 0;">
                {accuracy:.1f}%
            </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <p style="font-size: 30px; font-weight: 800; color: #dc3545; margin: 0;">
                0%
            </p>
            """, unsafe_allow_html=True)
        
        # ====== PROGRESS BAR ======
        if has_detected_class and accuracy > 0:
            st.markdown(f"""
            <div style="background: #f0ebe3; border-radius: 4px; height: 6px; margin-top: 8px; overflow: hidden;">
                <div style="background: #e86930; width: {min(accuracy, 100)}%; height: 100%; 
                            border-radius: 4px; transition: width 0.8s ease;"></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f0ebe3; border-radius: 4px; height: 6px; margin-top: 8px; overflow: hidden;">
                <div style="background: #dc3545; width: 0%; height: 100%; border-radius: 4px;"></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ====== TOMBOL ANALISIS LAGI ======
        st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            div.stButton > button {
                background-color: #e86930 !important;
                color: white !important;
                border: 2px solid #e86930 !important;
                border-radius: 8px !important;
                padding: 0.8rem 1.2rem !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
                box-shadow: 0 4px 12px rgba(232, 105, 48, 0.4) !important;
                width: 100% !important;
                transition: all 0.3s ease !important;
            }
            div.stButton > button:hover {
                background-color: #d45d2a !important;
                border-color: #d45d2a !important;
                box-shadow: 0 6px 20px rgba(232, 105, 48, 0.6) !important;
                transform: translateY(-2px) !important;
            }
            div.stButton > button:active {
                transform: translateY(0px) !important;
                box-shadow: 0 2px 8px rgba(232, 105, 48, 0.3) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("Analisis Lagi", key="analyze_again", use_container_width=True):
            reset_detection_state()
            set_page('deteksi')
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)