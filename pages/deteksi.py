"""
Halaman Deteksi - Versi Batu Bata dengan Kamera Real-time
"""
import streamlit as st
import io
import base64
import cv2
import numpy as np
from PIL import Image
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
from av import VideoFrame

from utils.session import set_page, reset_detection_state
from utils.model_loader import load_model
from utils.statistics import format_detection_stats
from config import CONFIDENCE_THRESHOLD, CLASS_NAMES


# ====== FUNGSI HELPER UNTUK KONVERSI GAMBAR KE BASE64 ======
def image_to_base64(image):
    """Konversi gambar (PIL atau numpy) ke base64"""
    try:
        if isinstance(image, Image.Image):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
            return f"data:image/png;base64,{img_base64}"
        elif isinstance(image, np.ndarray):
            if len(image.shape) == 3 and image.shape[2] == 3:
                img_pil = Image.fromarray(image)
            else:
                img_pil = Image.fromarray(image.astype('uint8'))
            img_bytes = io.BytesIO()
            img_pil.save(img_bytes, format="PNG")
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
            return f"data:image/png;base64,{img_base64}"
        else:
            return None
    except Exception as e:
        return None


# ====== FUNGSI DETEKSI FRAME (DIGUNAKAN UNTUK UPLOAD & KAMERA) ======
def detect_frame(frame, model, frame_source="camera"):
    """
    Deteksi pada satu frame untuk kamera real-time dan upload gambar.
    
    Args:
        frame: numpy array (BGR dari camera) atau PIL Image (RGB dari upload)
        model: Model YOLO terload
        frame_source: "camera" (BGR format) atau "upload" (PIL/RGB format)
    
    Returns:
        frame_copy: Frame dengan bounding box (BGR format)
        stats: Dictionary berisi statistik deteksi
    """
    
    # ========== KONVERSI INPUT KE NUMPY ARRAY BGR ==========
    if isinstance(frame, Image.Image):
        # PIL Image selalu RGB
        frame_array = np.array(frame)
        frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
    elif isinstance(frame, np.ndarray):
        if frame_source == "camera":
            # Dari camera sudah BGR
            frame_bgr = frame.copy()
        else:
            # Dari file upload, asumsikan RGB jika dari PIL
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    else:
        raise ValueError(f"Tipe frame tidak didukung: {type(frame)}")
    
    # ========== PREDIKSI DENGAN MODEL ==========
    results = model.predict(frame_bgr, conf=CONFIDENCE_THRESHOLD, verbose=False)
    
    # Copy frame untuk digambar
    frame_copy = frame_bgr.copy()
    
    # ========== WARNA BOUNDING BOX (BGR Format!) ==========
    # PENTING: OpenCV menggunakan BGR, bukan RGB!
    # Hijau RGB(0,255,0) = BGR(0,255,0)
    # Merah RGB(255,0,0) = BGR(0,0,255)
    colors = {
        'matang': (0, 255, 0),           # HIJAU: BGR(0,255,0)
        'setengah_matang': (0, 0, 255),  # MERAH: BGR(0,0,255)
    }
    default_color = (48, 105, 232)      # ORANYE: BGR(48,105,232)
    
    detected_classes = []
    class_confidences = {}
    detection_count = 0
    
    # ========== GAMBAR BOUNDING BOX ==========
    for result in results:
        if hasattr(result, 'boxes') and result.boxes is not None:
            for box in result.boxes:
                conf = float(box.conf[0])
                
                # Filter berdasarkan threshold
                if conf >= CONFIDENCE_THRESHOLD:
                    cls_id = int(box.cls[0])
                    cls_name = model.names.get(cls_id, CLASS_NAMES.get(cls_id, "Unknown"))
                    detected_classes.append(cls_name)
                    detection_count += 1
                    
                    # Simpan confidence tertinggi per kelas
                    if cls_name not in class_confidences or conf > class_confidences[cls_name]:
                        class_confidences[cls_name] = conf
                    
                    # Koordinat bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    
                    # Pilih warna berdasarkan kelas
                    color = colors.get(cls_name, default_color)
                    
                    # ===== BOUNDING BOX =====
                    cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 4)
                    
                    # ===== LABEL =====
                    label = f"{cls_name} {conf*100:.1f}%"
                    (label_w, label_h), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                    )
                    
                    # Background label
                    cv2.rectangle(
                        frame_copy,
                        (x1, y1 - label_h - 12),
                        (x1 + label_w + 12, y1),
                        color,
                        -1  # Filled rectangle
                    )
                    
                    # Teks PUTIH
                    cv2.putText(
                        frame_copy,
                        label,
                        (x1 + 6, y1 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),  # PUTIH
                        2
                    )
    
    # ========== HITUNG STATISTIK ==========
    main_class = None
    if detected_classes:
        class_counts = {}
        for cls in detected_classes:
            class_counts[cls] = class_counts.get(cls, 0) + 1
        # Ambil kelas dengan jumlah deteksi terbanyak
        main_class = max(class_counts, key=class_counts.get)
    
    # Akurasi rata-rata
    avg_confidence = (
        np.mean(list(class_confidences.values()))
        if class_confidences
        else 0
    )
    
    # Format statistik
    stats = {
        'detected_classes': list(set(detected_classes)),
        'total_detections': detection_count,
        'main_class': main_class,
        'avg_confidence': avg_confidence,
        'class_confidences': class_confidences
    }
    
    return frame_copy, stats


def show_deteksi():
    """Render halaman deteksi batu bata dengan kamera real-time"""
    
    # CSS untuk tombol ORANYE dan hilangkan notifikasi
    st.markdown("""
    <style>
        div.stButton > button {
            background-color: #e86930 !important;
            color: white !important;
            border: 2px solid #e86930 !important;
            border-radius: 8px !important;
            padding: 0.8rem 1.5rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 12px rgba(232, 105, 48, 0.4) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
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
        /* Hilangkan notifikasi success */
        .stAlert {
            display: none !important;
        }
        .element-container div[data-testid="stAlert"] {
            display: none !important;
        }
        /* Style untuk camera input */
        .stCameraInput {
            border-radius: 12px !important;
            overflow: hidden !important;
        }
        .stCameraInput > div {
            border-radius: 12px !important;
        }
        /* Hilangkan border/kotak oranye pada tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent !important;
            border: none !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
            border: none !important;
            background: #f0ebe3 !important;
            color: #666 !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #e86930 !important;
            color: white !important;
            border: none !important;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important;
        }
        /* Style untuk hasil box */
        .result-box {
            background: #faf8f5;
            border-radius: 8px;
            padding: 16px 20px;
            border: 2px solid #e86930;
            text-align: center;
        }
        .result-box h3 {
            color: #e86930;
            margin: 0;
            font-size: 24px;
        }
        .result-box .label {
            color: #999;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }
        .result-box .value {
            font-size: 28px;
            font-weight: 800;
            color: #e86930;
        }
        .result-box .progress-bar {
            background: #f0ebe3;
            border-radius: 4px;
            height: 6px;
            margin-top: 8px;
            overflow: hidden;
        }
        .result-box .progress-fill {
            background: #e86930;
            height: 100%;
            border-radius: 4px;
            transition: width 0.8s ease;
        }
        .result-box-empty {
            background: #faf8f5;
            border-radius: 8px;
            padding: 16px 20px;
            border: 2px solid #dc3545;
            text-align: center;
        }
        .result-box-empty h3 {
            color: #dc3545;
            margin: 0;
            font-size: 20px;
        }
        .result-box-empty .label {
            color: #999;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }
        .result-box-empty .value {
            font-size: 28px;
            font-weight: 800;
            color: #dc3545;
        }
        .result-box-empty .progress-bar {
            background: #f0ebe3;
            border-radius: 4px;
            height: 6px;
            margin-top: 8px;
            overflow: hidden;
        }
        .result-box-empty .progress-fill {
            background: #dc3545;
            height: 100%;
            border-radius: 4px;
            transition: width 0.8s ease;
            width: 0%;
        }
        .live-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: white;
            border-radius: 50%;
            animation: pulse 1.5s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
       
    </style>
    """, unsafe_allow_html=True)
    
    # Tombol kembali ke beranda
    if st.button("← Kembali ke Beranda", key="back_detection_page"):
        set_page('beranda')
    
    st.markdown("""
    <h1 style='font-size: 32px; margin-top: 10px;'>
        <span style='color: #e86930;'>🧱</span> Deteksi Batu Bata
    </h1>
   
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # TIPS PENGAMBILAN GAMBAR
    st.markdown("""
    <div style="background-color: #f5f1e8; border-radius: 8px; padding: 24px; margin: 20px 0; border-left: 4px solid #e86930;">
        <h3 style="color: #e86930; font-size: 20px; margin-top: 0; margin-bottom: 16px;">🧱 Tips Pengambilan Gambar</h3>
        <p style="color: #1a1a1a; font-size: 15px; line-height: 1.9; margin: 0;">
            • Gunakan pencahayaan yang cukup<br>
            • Pastikan batu bata terlihat jelas<br>
            • Ambil gambar dari jarak yang sesuai<br>
            • Gunakan gambar asli tanpa filter atau efek tambahan<br>
            • Jangan gunakan foto yang bergerak atau buram<br>
            • Sistem hanya mendukung deteksi satu objek batu bata dalam satu gambar. Hindari mengunggah gambar yang berisi lebih dari satu batu bata    
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # ====== LOAD MODEL (CACHE) ======
    @st.cache_resource
    def get_cached_model():
        return load_model()
    
    model = get_cached_model()
    if model is None:
        st.error("❌ Gagal memuat model. Pastikan file model ada.")
        return
    
    # ====== TAB UPLOAD DAN KAMERA REAL-TIME ======
    tab1, tab2 = st.tabs(["📤 Upload Gambar", "📷 Kamera Real-time"])
    
    # ============================================================
    # TAB 1: UPLOAD GAMBAR
    # ============================================================
    with tab1:
        uploaded_file = st.file_uploader("Pilih gambar batu bata", type=["jpg", "jpeg", "png"], key="file_uploader")
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            st.session_state.uploaded_image = img
            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.detection_image = img.copy()
            
            # Tampilkan preview
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
            
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin: 16px 0;">
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{img_base64}" 
                         style="max-width: 100%; max-height: 400px; border-radius: 8px; object-fit: contain;">
                </div>
                <div style="text-align: center; margin-top: 10px; color: #888; font-size: 14px;">
                     {st.session_state.uploaded_filename}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div style="text-align: center; margin: 20px 0;">', unsafe_allow_html=True)
            
            col_detect = st.columns([0.35, 0.30, 0.35])
            with col_detect[1]:
                if st.button("🔍 Analisis Batu Bata", key="detect_button", use_container_width=True):
                    loading_placeholder = st.empty()
                    
                    with loading_placeholder.container():
                        st.markdown("""
                        <div style="text-align: center; padding: 40px 20px; background: #f5f1e8; border-radius: 12px;">
                            <div style="display: inline-block; width: 50px; height: 50px; 
                                        border: 4px solid #e86930; border-top-color: transparent;
                                        border-radius: 50%; animation: spin 0.8s linear infinite;">
                            </div>
                            <div style="margin-top: 16px; font-weight: 600; color: #e86930; font-size: 18px;">
                                 Sedang Mendeteksi...
                            </div>
                            <div style="color: #888; font-size: 14px; margin-top: 4px;">
                                Sistem AI sedang menganalisis gambar batu bata
                            </div>
                            <style>
                                @keyframes spin {
                                    0% { transform: rotate(0deg); }
                                    100% { transform: rotate(360deg); }
                                }
                            </style>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    try:
                        if st.session_state.get('uploaded_image') is None:
                            st.error("❌ Tidak ada gambar untuk dideteksi!")
                            loading_placeholder.empty()
                            return
                        
                        original_img = st.session_state.uploaded_image.copy()
                        st.session_state.original_image = original_img
                        
                        # ====== DETEKSI (dengan parameter frame_source="upload") ======
                        detection_image_bgr, stats = detect_frame(
                            original_img,
                            model,
                            frame_source="upload"  # Penting: untuk handle RGB dari PIL
                        )
                        
                        # Konversi BGR → RGB untuk PIL (untuk display)
                        detection_image_rgb = cv2.cvtColor(detection_image_bgr, cv2.COLOR_BGR2RGB)
                        detection_image = Image.fromarray(detection_image_rgb)
                        
                        # Konversi ke base64
                        img_base64_result = image_to_base64(detection_image)
                        if img_base64_result:
                            st.session_state.detection_image_base64 = img_base64_result
                            st.session_state.detection_image = detection_image
                        else:
                            st.session_state.detection_image = original_img
                        
                        # Simpan statistik
                        st.session_state.detection_stats = stats
                        st.session_state.detected_classes = stats['detected_classes']
                        st.session_state.total_detections = stats['total_detections']
                        
                        loading_placeholder.empty()
                        set_page("hasil")
                        
                    except Exception as e:
                        loading_placeholder.empty()
                        st.error(f"❌ Terjadi kesalahan: {str(e)}")
                        import traceback
                        st.info(f"💡 Debug: {traceback.format_exc()}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================
    # TAB 2: KAMERA REAL-TIME (WebRTC Streaming)
    # ============================================================
    with tab2:
        st.markdown("""
<div style="background-color:#f5f1e8; border-radius:8px; padding:12px 16px; margin-bottom:12px;">
<span style="color:#e86930;font-weight:600;">📷 Kamera Real-time</span>
<span style="color:#777;font-size:14px;margin-left:8px;">— Arahkan kamera ke batu bata</span>
</div>
""", unsafe_allow_html=True)
        
        # ====== VIDEO PROCESSOR UNTUK DETEKSI ======
        class VideoProcessor:
            def __init__(self):
                self.last_detection = None
            
            def recv(self, frame):
                img = frame.to_ndarray(format="bgr24")
                
                # Deteksi pada frame (frame_source="camera" karena sudah BGR)
                frame_result, detection_stats = detect_frame(
                    img,
                    model,
                    frame_source="camera"
                )
                
                # Simpan hasil deteksi terbaru
                self.last_detection = {
                    "main_class": detection_stats.get("main_class"),
                    "avg_confidence": detection_stats.get("avg_confidence"),
                    "detected_classes": detection_stats.get("detected_classes"),
                    "class_confidences": detection_stats.get("class_confidences")
                }
                
                return VideoFrame.from_ndarray(frame_result, format="bgr24")
        
        # ====== WEBRTC CONFIGURATION ======
        rtc_configuration = RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )

        # ====== PILIH KAMERA ======
        kamera = st.selectbox(
            "📷 Pilih Kamera",
            ["Kamera Belakang", "Kamera Depan"],
            key="kamera_pilihan"
        )

        facing_mode = (
            "environment"
            if kamera == "Kamera Belakang"
            else "user"
        )

        # ====== STREAMING SETUP ======
        # PENTING: key harus ikut berubah sesuai facing_mode.
        # Jika key statis ("brick-camera"), komponen WebRTC di browser
        # tidak akan di-restart ketika constraint video berubah, sehingga
        # kamera yang dipakai tetap kamera lama (biasanya kamera depan).
        # Dengan key dinamis, komponen akan remount dan memanggil ulang
        # getUserMedia() dengan facingMode yang baru.
        webrtc_ctx = webrtc_streamer(
            key=f"brick-camera-{facing_mode}",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=rtc_configuration,
            media_stream_constraints={
                "video": {
                    # "ideal" (bukan string biasa / "exact") agar browser
                    # tetap fallback ke kamera yang tersedia jika kamera
                    # dengan facingMode yang diminta tidak ada (mis. laptop
                    # yang hanya punya satu kamera depan), alih-alih error.
                    "facingMode": {"ideal": facing_mode}
                },
                "audio": False
            },
            async_processing=True,
            video_processor_factory=VideoProcessor,
        )

        # ====== INFO FALLBACK: PEMILIHAN KAMERA MANUAL ======
        # Catatan: dropdown "Pilih Kamera" di atas hanya memberi PREFERENSI
        # (facingMode) ke browser. Sebagian HP (tergantung merk/pabrikan)
        # tidak melaporkan facingMode kamera dengan benar ke browser,
        # sehingga preferensi ini kadang diabaikan oleh perangkat tsb.
        # Solusi paling akurat untuk kasus itu: gunakan tombol
        # "SELECT DEVICE" bawaan di pojok kanan bawah video, yang membaca
        # daftar kamera fisik langsung dari perangkat (selalu akurat,
        # tidak tergantung facingMode).
        st.markdown("""
<div style="background-color:#fff8ec; border-radius:8px; padding:10px 16px; margin-top:8px; border-left:3px solid #e86930; font-size:13px; color:#555;">
💡 Jika kamera yang tampil tidak sesuai pilihan di atas (misalnya memilih "Kamera Belakang" tapi yang muncul kamera depan), klik <b>SELECT DEVICE</b> di pojok kanan bawah video untuk memilih kamera fisik secara manual. Ini terjadi karena sebagian HP tidak melaporkan info kamera depan/belakang dengan benar ke browser.
</div>
""", unsafe_allow_html=True)

        # ====== STATISTIK REAL-TIME ======
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <span style="color: #777; font-size: 14px;">
                Status Kamera:
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        stats_placeholder1 = col1.empty()
        stats_placeholder2 = col2.empty()
        
        # Update statistik real-time
        if webrtc_ctx.state.playing:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <span class="live-indicator"></span>
                <span style="color: #e86930; font-weight: 600; margin-left: 8px;">STREAMING AKTIF</span>
            </div>
            """, unsafe_allow_html=True)
            
            import time
            while webrtc_ctx.state.playing:
                if webrtc_ctx.video_processor and hasattr(webrtc_ctx.video_processor, 'last_detection'):
                    detection = webrtc_ctx.video_processor.last_detection
                    
                    if detection:
                        main_class = detection.get("main_class")
                        avg_confidence = detection.get("avg_confidence", 0)
                        
                        # Tampilkan kategori
                        with stats_placeholder1.container():
                            if main_class:
                                st.markdown(f"""
                                <div class="result-box">
                                    <div class="label">KATEGORI TERDETEKSI</div>
                                    <h3>{main_class}</h3>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="result-box-empty">
                                    <div class="label">KATEGORI TERDETEKSI</div>
                                    <h3>—</h3>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Tampilkan akurasi
                        with stats_placeholder2.container():
                            if main_class:
                                accuracy_pct = avg_confidence * 100
                                st.markdown(f"""
                                <div class="result-box">
                                    <div class="label">AKURASI RATA-RATA</div>
                                    <div class="value">{accuracy_pct:.1f}%</div>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {min(accuracy_pct, 100)}%;"></div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="result-box-empty">
                                    <div class="label">AKURASI RATA-RATA</div>
                                    <div class="value">0%</div>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: 0%;"></div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                
                time.sleep(0.1)
        
        else:
            st.info("🎥 Kamera sedang berjalan secara real-time.")
            st.markdown("""
            <div style="text-align: center; padding: 40px 20px; color: #999;">
                <div style="font-size: 80px;">📸</div>
                <p style="font-size: 18px; margin-top: 20px; font-weight: 500;">Klik Tombol START untuk Mulai Streaming</p>
                <p style="font-size: 14px; color: #bbb; margin-top: 10px;">Arahkan kamera ke batu bata untuk deteksi real-time</p>
                <p style="font-size: 13px; color: #ccc; margin-top: 20px; line-height: 1.8;">
                    ✓ Bounding box langsung muncul pada objek terdeteksi<br>
                    ✓ Deteksi setiap frame secara real-time<br>
                    ✓ Statistik akurasi real-time
                </p>
            </div>
            """, unsafe_allow_html=True)


