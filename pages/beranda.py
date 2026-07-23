
"""
Halaman Beranda - Landing page utama
"""
import streamlit as st
from pathlib import Path
import base64
from utils.session import initialize_session_state

# Initialize
initialize_session_state()

def image_to_base64(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""
    except Exception:
        return ""

def show_beranda():
    """Render halaman beranda"""
    
    # CSS Styling
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
        background-color: #f5f1e8 !important;
    }

    header, footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        padding: 0 !important;
    }
    [data-testid="column"] {
        padding: 0 !important;
        min-width: 0 !important;
    }

    .navbar {
        background: #f5f1e8;
        padding: 1.1rem 5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(0,0,0,0.08);
    }
    .navbar-logo {
        font-size: 1.35rem;
        font-weight: 800;
        color: #e86930;
        letter-spacing: -0.5px;
    }
    .navbar-logo span { color: #1a1a1a; }
    .navbar-tag { font-size: 0.78rem; color: #aaa; font-weight: 500; }

    .hero-left-inner {
        padding: 4rem 3rem 0.2rem 5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 450px;
        background: #f5f1e8;
    }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(232, 105, 48, 0.1);
        border: 1px solid rgba(232, 105, 48, 0.28);
        color: #e86930;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        padding: 0.4rem 1rem;
        border-radius: 100px;
        margin-bottom: 1rem;
        width: fit-content;
    }
    .eyebrow-dot {
        width: 7px; height: 7px;
        background: #e86930;
        border-radius: 50%;
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink {
        0%,100% { opacity:1; } 50% { opacity:0.25; }
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #1a1a1a;
        line-height: 1.15;
        letter-spacing: -1px;
        margin-bottom: 0.8rem;
    }
    .hero-title .orange { color: #e86930; }

    .hero-desc {
        font-size: 1rem;
        color: #777;
        line-height: 1.75;
        max-width: 420px;
        margin-bottom: 0.8rem;
    }

    .hero-right-inner {
        padding: 4rem 5rem 4rem 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 450px;
        background: #f5f1e8;
        position: relative;
    }

    .hero-img-wrap {
        position: relative;
        width: 100%;
    }
    # .hero-ring {
    #     position: absolute;
    #     top: -14px; right: -14px;
    #     width: 100%; height: 100%;
    #     border: 2px dashed rgba(232,105,48,0.22);
    #     border-radius: 22px;
    #     pointer-events: none;
    #     z-index: 0;
    # }
    .hero-img-frame {
        position: relative;
        z-index: 1;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 24px 60px rgba(0,0,0,0.18);
    }
    .hero-img-frame::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom, transparent 50%, rgba(0,0,0,0.42) 100%);
        border-radius: 20px;
        z-index: 1;
    }
    .hero-img-frame img {
        width: 100%;
        height: 380px;
        object-fit: cover;
        display: block;
        border-radius: 20px;
    }
    .hero-img-ph {
        width: 100%;
        height: 380px;
        background: #ddd6c8;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        color: #bbb;
        font-size: 0.9rem;
    }

    .cara-section {
        padding: 4.5rem 5rem;
        background: white;
    }
    .sec-head { text-align: center; margin-bottom: 3rem; }
    .sec-overline {
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 2.5px; text-transform: uppercase;
        color: #e86930; margin-bottom: 0.6rem;
    }
    .sec-title {
        font-size: 2rem; font-weight: 800;
        color: #1a1a1a; letter-spacing: -0.5px;
    }
    .sec-bar {
        width: 48px; height: 4px;
        background: #e86930; border-radius: 2px;
        margin: 0.75rem auto 0;
    }
    .ck-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .ck-card {
        background: #fafaf8;
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 2rem 1.5rem 1.75rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.28s ease;
    }
    .ck-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px; background: #e86930;
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    .ck-card:hover::after { transform: scaleX(1); }
    .ck-card:hover {
        background: white;
        box-shadow: 0 16px 40px rgba(0,0,0,0.09);
        transform: translateY(-5px);
    }
    .ck-num {
        font-size: 3rem; font-weight: 800;
        color: rgba(232,105,48,0.1);
        line-height: 1; margin-bottom: 0.25rem;
    }
    .ck-icon {
        width: 54px; height: 54px;
        background: rgba(232,105,48,0.1);
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 1rem; color: #e86930;
    }
    .ck-ttl { font-size: 1rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.5rem; }
    .ck-dsc { font-size: 0.84rem; color: #888; line-height: 1.65; }

    .tingkat-section { padding: 4.5rem 5rem; background: #f5f1e8; }
    .tingkat-inner {
        display: grid;
        grid-template-columns: 220px 1fr;
        gap: 4rem;
        align-items: start;
        max-width: 1200px;
        margin: 0 auto;
    }
    .tk-label {
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: #e86930; margin-bottom: 0.75rem;
    }
    .tk-title {
        font-size: 1.9rem; font-weight: 800;
        color: #1a1a1a; letter-spacing: -0.5px;
        line-height: 1.2; margin-bottom: 0.9rem;
    }
    .tk-title span { color: #e86930; }
    .tk-bar { width: 44px; height: 4px; background: #e86930; border-radius: 2px; margin-bottom: 1rem; }
    .tk-sub { font-size: 0.85rem; color: #999; line-height: 1.65; }
    .tk-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
    .tk-card {
        background: white;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 4px 18px rgba(0,0,0,0.07);
        transition: all 0.28s ease;
        padding: 2rem 0 0 0;
    }
    .tk-card:hover {
        box-shadow: 0 16px 44px rgba(0,0,0,0.12);
        transform: translateY(-5px);
    }
    .tk-img { width: 100%; height: 200px; object-fit: cover; display: block; }
    .tk-img-ph {
        width: 100%; height: 200px;
        background: #e8e0d0;
        display: flex; align-items: center; justify-content: center;
        color: #ccc; font-size: 0.85rem; gap: 0.5rem; flex-direction: column;
    }
    .tk-body { padding: 1.3rem 1.5rem; }
    .tk-badge {
        display: inline-block;
        font-size: 0.68rem; font-weight: 700;
        letter-spacing: 1.2px; text-transform: uppercase;
        padding: 0.28rem 0.75rem; border-radius: 100px;
        margin-bottom: 0.6rem;
    }
    .badge-semi { background: rgba(245,158,11,0.12); color: #b45309; }
    .badge-matang { background: rgba(34,197,94,0.1); color: #15803d; }
    .tk-name { font-size: 1rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.35rem; }
    .tk-desc { font-size: 0.84rem; color: #888; line-height: 1.6; }

    .site-footer {
        background: #1a1a1a;
        padding: 2.2rem 5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .ft-brand { font-size: 1.1rem; font-weight: 800; color: #e86930; }
    .ft-brand span { color: #555; }
    .ft-copy { font-size: 0.78rem; color: #555; }

    .stButton {
        width: fit-content !important;
        margin-top: -0.8rem !important;
        margin-bottom: 6rem !important;
    }

    .stButton > button {
        background: #e86930 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.88rem 2.2rem !important;
        font-weight: 700 !important;
        font-size: 0.97rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: 0.2px !important;
        box-shadow: 0 6px 20px rgba(232,105,48,0.38) !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        width: fit-content !important;
        min-width: 200px !important;
    }
    .stButton > button:hover {
        background: #cf5c23 !important;
        box-shadow: 0 10px 28px rgba(232,105,48,0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    .element-container:has(.stButton) {
        display: flex !important;
        justify-content: flex-start !important;
        padding-left: 5rem !important;
        padding-bottom: 0 !important;
        margin-bottom: 0 !important;
    }
    @media (max-width: 768px) {
    .hero-left-inner {
    padding: 1rem 3rem !important;
    }
    .navbar {
    padding: 1.1rem 3rem; !important;
    }
    .element-container:has(.stButton) {
    padding-left: 3rem !important;
    }
    .hero-right-inner {
    padding: 0 2rem 3rem !important ;
    min-height: unset !important;
    }
    .cara-section {
    padding: 4rem 3rem !important;
    }
    .ck-grid, .tk-grid {
    grid-template-columns: repeat(1, 1fr);
    }
    .ck-num {
    margin-bottom: 1rem !important;
    }
    .tingkat-section {
    padding: 4rem 3rem !important;
    }
    .tingkat-inner {
    grid-template-columns: repeat(1, 1fr);
    gap: 2rem;
    }
    .tk-card {
    padding: 14px !important;
    }
    .tk-body {
    padding: 8px !important;
    }
    .site-footer {
    flex-direction: column;
    gap: 6px;
    text-align: center;
    }
    .stButton {
        margin-bottom: 3rem !important;
    }
     .hero-title {
        font-size: 32px;
    }
    
    }
    </style>""", unsafe_allow_html=True)

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'detection_method' not in st.session_state:
        st.session_state.detection_method = 'upload'

    # Load hero image
    hero_image_path = Path("assets/olahan.png")
    hero_image_base64 = image_to_base64(str(hero_image_path)) if hero_image_path.exists() else ""

    # Navbar
    st.markdown("""
    <div class="navbar">
        <div class="navbar-logo">Brick<span>AI</span></div>
        <div class="navbar-tag">Computer Vision Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("""
        <div class="hero-left-inner">
            <div class="hero-eyebrow">
                <div class="eyebrow-dot"></div>
                BrickAI &mdash; Computer Vision
            </div>
            <div class="hero-title">
                Deteksi Otomatis<br>
                <span class="orange">Tingkat Kematangan</span><br>
                Batu Bata Merah
            </div>
            <div class="hero-desc">
                Sistem berbasis Computer Vision untuk membantu mengidentifikasikan
                tingkat kematangan batu bata merah secara otomatis dan akurat.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Mulai Deteksi", key="btn_mulai_deteksi"):
            st.session_state.current_page = 'deteksi'
            st.rerun()

    with col_right:
        if hero_image_base64:
            img_content = f'<img src="data:image/png;base64,{hero_image_base64}" alt="Brick Kiln">'
        else:
            img_content = """
            <div class="hero-img-ph">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <polyline points="21 15 16 10 5 21"/>
                </svg>
                <span>Gambar belum tersedia</span>
            </div>
            """

        st.markdown(f"""
        <div class="hero-right-inner">
            <div class="hero-img-wrap">
                # <div class="hero-ring"></div>
                <div class="hero-img-frame">
                    {img_content}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Cara Kerja Section
    st.markdown("""
    <div class="cara-section">
        <div class="sec-head">
            <div class="sec-overline">Alur Penggunaan</div>
            <div class="sec-title">Cara Kerja Sistem</div>
            <div class="sec-bar"></div>
        </div>
        <div class="ck-grid">
            <div class="ck-card">
                <div class="ck-num">01</div>
                <div class="ck-icon">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="17 8 12 3 7 8"/>
                        <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                </div>
                <div class="ck-ttl">Upload Gambar</div>
                <div class="ck-dsc">Unggah foto batu bata merah yang ingin Anda analisis</div>
            </div>
            <div class="ck-card">
                <div class="ck-num">02</div>
                <div class="ck-icon">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="3"/>
                        <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83
                                 M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
                    </svg>
                </div>
                <div class="ck-ttl">AI Memproses</div>
                <div class="ck-dsc">Algoritma AI menganalisis gambar dan mengidentifikasi pola kematangan</div>
            </div>
            <div class="ck-card">
                <div class="ck-num">03</div>
                <div class="ck-icon">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="12 3 20 7.5 20 16.5 12 21 4 16.5 4 7.5 12 3"/>
                        <polyline points="12 12 20 7.5"/>
                        <polyline points="12 12 12 21"/>
                        <polyline points="12 12 4 7.5"/>
                    </svg>
                </div>
                <div class="ck-ttl">Klasifikasi Model</div>
                <div class="ck-dsc">Model mengklasifikasikan batu bata ke kategori matang atau setengah matang</div>
            </div>
            <div class="ck-card">
                <div class="ck-num">04</div>
                <div class="ck-icon">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                </div>
                <div class="ck-ttl">Hasil Deteksi</div>
                <div class="ck-dsc">Dapatkan hasil teridentifikasi dengan tingkat kepercayaan akurat</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tingkat Kematangan Section
    setengah_path = Path("assets/setengah_matang.jpg")
    matang_path = Path("assets/matang.jpg")
    setengah_b64 = image_to_base64(str(setengah_path)) if setengah_path.exists() else ""
    matang_b64 = image_to_base64(str(matang_path)) if matang_path.exists() else ""

    def tk_img(b64, alt="Brick"):
        if b64:
            return f'<img class="tk-img" src="data:image/jpeg;base64,{b64}" alt="{alt}">'
        return """<div class="tk-img-ph">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
            </svg>
            <span>Gambar belum tersedia</span>
        </div>"""

    st.markdown(f"""
    <div class="tingkat-section">
        <div class="tingkat-inner">
            <div>
                <div class="tk-label">Kategori</div>
                <div class="tk-title">Tingkat<br><span>Kematangan</span></div>
                <div class="tk-bar"></div>
                <div class="tk-sub">Sistem mengenali dua kategori kematangan berdasarkan warna dan tekstur permukaan bata hasil pembakaran.</div>
            </div>
            <div class="tk-grid">
                <div class="tk-card">
                    {tk_img(setengah_b64, "Setengah Matang")}
                    <div class="tk-body">
                        <div class="tk-badge badge-semi">Setengah Matang</div>
                        <div class="tk-name">Setengah Matang</div>
                        <div class="tk-desc">Warna kemerahaan muda, pembakaran belum merata dan struktur masih rapuh.</div>
                    </div>
                </div>
                <div class="tk-card">
                    {tk_img(matang_b64, "Matang")}
                    <div class="tk-body">
                        <div class="tk-badge badge-matang">Matang</div>
                        <div class="tk-name">Matang</div>
                        <div class="tk-desc">Warna merah merata, struktur kuat, dan pembakaran sempurna di seluruh permukaan.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="site-footer">
        <div class="ft-brand">Brick<span>AI</span></div>
        <div class="ft-copy">2024 &mdash; Teknologi Deteksi Otomatis Batu Bata Merah &mdash; Powered by Computer Vision</div>
    </div>
    """, unsafe_allow_html=True)