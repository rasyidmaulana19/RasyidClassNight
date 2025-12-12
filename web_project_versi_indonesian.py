import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, diff, latex, sympify, simplify
import plotly.graph_objects as go

# ---------------- Konfigurasi Halaman ----------------
st.set_page_config(
    page_title="Aplikasi Fungsi Matematika & Optimasi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== TEMA GELAP PREMIUM ===================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    color: #e4e4e7;
}

h1 {
    font-weight: 900;
    font-size: 2.5rem;
    text-align: center;
    color: #60a5fa;
    letter-spacing: 2px;
    text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
}

h2 {
    color: #e4e4e7;
    font-weight: 700;
    border-left: 4px solid #3b82f6;
    padding-left: 15px;
}

h3 {
    color: #cbd5e1;
    font-weight: 600;
}

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 700;
    padding: 0.7rem 2rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1729, #1a1a2e);
    border-right: 1px solid rgba(59, 130, 246, 0.3);
}

.stTextInput input, .stTextArea textarea {
    background: rgba(30,41,59,0.6);
    color: #e4e4e7;
    border: 1px solid rgba(100,116,139,0.3);
    border-radius: 8px;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

div.stMarkdown strong {
    color: #60a5fa;
}

/* Gaya Kartu Anggota Tim */
.team-card {
    background: rgba(30,41,59,0.8);
    border-radius: 20px;
    padding: 2rem;
    border: 2px solid transparent;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.team-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 20px;
    padding: 2px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.4s ease;
}

.team-card:hover::before {
    opacity: 1;
}

.team-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
}

.member-photo {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center;
    border: 4px solid;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    transition: all 0.4s ease;
    position: relative;
    z-index: 2;
    display: block;
    margin: 0 auto;
}

.team-card:hover .member-photo {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 15px 35px rgba(59, 130, 246, 0.5);
}

.member-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e4e4e7;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    transition: color 0.3s ease;
}

.team-card:hover .member-name {
    color: #60a5fa;
}

.member-role {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}

.member-desc {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.6;
}

.role-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.25rem;
    transition: all 0.3s ease;
}

.role-badge:hover {
    transform: scale(1.1);
}

.section-header {
    text-align: center;
    margin-bottom: 3rem;
    position: relative;
}

.section-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.section-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    font-weight: 400;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Fungsi pembantu ----------------
def display_member_card(github_url, name, role, description, border_color, role_bg):
    """Menampilkan kartu anggota dengan foto dan info."""
    st.markdown(f"""
    <div class='team-card'>
        <div style='text-align: center;'>
            <div style='width: 200px; height: 200px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 4px solid {border_color}; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4); position: relative;'>
                <img src='{github_url}' 
                     style='width: 100%; height: 100%; object-fit: cover; object-position: center center; transition: all 0.4s ease; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);'
                     onmouseover="this.style.transform='translate(-50%, -50%) scale(1.1) rotate(5deg)'"
                     onmouseout="this.style.transform='translate(-50%, -50%) scale(1) rotate(0deg)'"/>
            </div>
            <h3 class='member-name'>{name}</h3>
            <div class='role-badge' style='background: {role_bg}; color: white;'>
                {role}
            </div>
            <p class='member-desc'>{description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Navigasi Sidebar ----------------
st.sidebar.title("📋 Navigasi")
page = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "👥 Anggota Tim", "📈 Analisis Fungsi", "🎯 Pemecah Optimasi"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Tentang")
st.sidebar.info("""
Aplikasi ini mendemonstrasikan:
- Visualisasi fungsi
- Diferensiasi simbolik
- Pemecahan masalah optimasi
- Alat matematika interaktif
""")
st.sidebar.markdown("### 🛠️ Teknologi")
st.sidebar.markdown("""
- Python
- Streamlit
- SymPy
- Plotly
- NumPy
""")

# ================== HALAMAN 1: BERANDA ==================
if page == "🏠 Beranda":
    st.title("🎓 Aplikasi Web Fungsi Matematika & Optimasi")
    st.markdown("### Platform Alat Kalkulus Lanjutan & Pemecahan Masalah")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kartu Navigasi Cepat
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                     border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                     transition: all 0.3s ease; cursor: pointer;'
                     onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(59, 130, 246, 0.4)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)'">
            <h3 style='text-align: center; color: #60a5fa;'>👥 Anggota Tim</h3>
            <p style='text-align: center; color: #94a3b8;'>Temui tim pengembang</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                     border: 1px solid rgba(167, 139, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                     transition: all 0.3s ease; cursor: pointer;'
                     onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(167, 139, 246, 0.4)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)'">
            <h3 style='text-align: center; color: #a78bfa;'>📈 Analisis Fungsi</h3>
            <p style='text-align: center; color: #94a3b8;'>Visualisasikan dan diferensiasikan</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.7); padding: 2rem; border-radius: 15px; 
                     border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                     transition: all 0.3s ease; cursor: pointer;'
                     onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(59, 130, 246, 0.4)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)'">
            <h3 style='text-align: center; color: #60a5fa;'>🎯 Optimasi</h3>
            <p style='text-align: center; color: #94a3b8;'>Selesaikan masalah kata</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Konten Utama - Teori Turunan
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1)); 
                 padding: 2rem; border-radius: 20px; border: 2px solid rgba(59, 130, 246, 0.3);
                 margin-bottom: 2rem;'>
        <h2 style='color: #60a5fa; text-align: center; font-size: 2rem; margin-bottom: 1rem;'>
            📐 Apa itu Turunan (Derivatif)?
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_def1, col_def2 = st.columns([1, 1])
    
    with col_def1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                     border-left: 4px solid #3b82f6; height: 100%;'>
            <h3 style='color: #60a5fa; margin-bottom: 1rem;'>📖 Definisi</h3>
            <p style='color: #cbd5e1; line-height: 1.8; font-size: 1rem;'>
                Turunan merepresentasikan <strong style='color: #60a5fa;'>laju perubahan</strong> suatu fungsi 
                terhadap variabelnya. Secara geometris, ini merepresentasikan <strong style='color: #60a5fa;'>gradien 
                dari garis singgung</strong> pada suatu titik di kurva fungsi.
            </p>
            <p style='color: #94a3b8; font-style: italic; margin-top: 1rem;'>
                💡 Turunan menjawab: "Seberapa cepat fungsi berubah pada titik tertentu?"
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_def2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                     border-left: 4px solid #8b5cf6; height: 100%;'>
            <h3 style='color: #a78bfa; margin-bottom: 1rem;'>🧮 Definisi Matematis</h3>
            <p style='color: #cbd5e1; line-height: 1.8;'>
                Turunan dari fungsi f(x) didefinisikan sebagai limit:
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}")
        st.markdown("""
        <p style='color: #94a3b8; text-align: center; margin-top: 0.5rem;'>
            atau dapat ditulis sebagai:
        </p>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{dy}{dx} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bagian Aturan Turunan
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1)); 
                 padding: 2rem; border-radius: 20px; border: 2px solid rgba(139, 92, 246, 0.3);
                 margin-bottom: 2rem;'>
        <h2 style='color: #a78bfa; text-align: center; font-size: 2rem; margin-bottom: 1rem;'>
            📝 Rumus Turunan
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_rule1, col_rule2, col_rule3 = st.columns(3)
    
    with col_rule1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                     border: 2px solid rgba(59, 130, 246, 0.3); min-height: 320px;'>
            <h4 style='color: #60a5fa; text-align: center; margin-bottom: 1.5rem;'>⚡ Aturan Dasar</h4>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(c) = 0")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;'>Konstanta</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(x^n) = nx^{n-1}")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;'>Aturan Pangkat</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}\left(cf(x)\right) = c \cdot f'(x)")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Kelipatan Konstanta</p>", unsafe_allow_html=True)
    
    with col_rule2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                     border: 2px solid rgba(139, 92, 246, 0.3); min-height: 320px;'>
            <h4 style='color: #a78bfa; text-align: center; margin-bottom: 1.5rem;'>🔄 Trigonometri</h4>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\sin x) = \cos x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;'>Sinus</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\cos x) = -\sin x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;'>Kosinus</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\tan x) = \sec^2 x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Tangen</p>", unsafe_allow_html=True)
    
    with col_rule3:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 1.5rem; border-radius: 15px; 
                     border: 2px solid rgba(6, 182, 212, 0.3); min-height: 320px;'>
            <h4 style='color: #22d3ee; text-align: center; margin-bottom: 1.5rem;'>📈 Eksponen & Logaritma</h4>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(e^x) = e^x")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;'>Eksponensial</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(\ln x) = \frac{1}{x}")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;'>Logaritma Natural</p>", unsafe_allow_html=True)
        st.latex(r"\frac{d}{dx}(a^x) = a^x \ln a")
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Eksponensial Umum</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bagian Fitur
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(16, 185, 129, 0.1)); 
                 padding: 2rem; border-radius: 20px; border: 2px solid rgba(6, 182, 212, 0.3);
                 margin-bottom: 2rem;'>
        <h2 style='color: #22d3ee; text-align: center; font-size: 2rem; margin-bottom: 1rem;'>
            🚀 Fitur Aplikasi
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 2rem; border-radius: 15px; 
                     border-left: 5px solid #3b82f6; margin-bottom: 1rem;
                     transition: all 0.3s ease;'
                     onmouseover="this.style.transform='translateX(10px)'; this.style.boxShadow='0 8px 20px rgba(59, 130, 246, 0.3)'"
                     onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='none'">
            <h3 style='color: #60a5fa; margin-bottom: 1rem;'>📊 Visualisasi Fungsi</h3>
            <p style='color: #cbd5e1; line-height: 1.8;'>
                Plot dan visualisasikan fungsi matematika apa pun dengan grafik interaktif. 
                Jelajahi perilaku fungsi di berbagai rentang.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 2rem; border-radius: 15px; 
                     border-left: 5px solid #8b5cf6; margin-bottom: 1rem;
                     transition: all 0.3s ease;'
                     onmouseover="this.style.transform='translateX(10px)'; this.style.boxShadow='0 8px 20px rgba(139, 92, 246, 0.3)'"
                     onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='none'">
            <h3 style='color: #a78bfa; margin-bottom: 1rem;'>🧮 Komputasi Turunan</h3>
            <p style='color: #cbd5e1; line-height: 1.8;'>
                Hitung turunan secara otomatis dengan solusi langkah demi langkah. 
                Lihat hasil dalam format LaTeX yang indah.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 2rem; border-radius: 15px; 
                     border-left: 5px solid #06b6d4; margin-bottom: 1rem;
                     transition: all 0.3s ease;'
                     onmouseover="this.style.transform='translateX(10px)'; this.style.boxShadow='0 8px 20px rgba(6, 182, 212, 0.3)'"
                     onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='none'">
            <h3 style='color: #22d3ee; margin-bottom: 1rem;'>🎯 Pemecah Masalah Optimasi</h3>
            <p style='color: #cbd5e1; line-height: 1.8;'>
                Selesaikan masalah optimasi dunia nyata dengan solusi terperinci. 
                Sempurna untuk aplikasi teknik dan matematika.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: rgba(30,41,59,0.8); padding: 2rem; border-radius: 15px; 
                     border-left: 5px solid #10b981; margin-bottom: 1rem;
                     transition: all 0.3s ease;'
                     onmouseover="this.style.transform='translateX(10px)'; this.style.boxShadow='0 8px 20px rgba(16, 185, 129, 0.3)'"
                     onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='none'">
            <h3 style='color: #34d399; margin-bottom: 1rem;'>📈 Plot Interaktif</h3>
            <p style='color: #cbd5e1; line-height: 1.8;'>
                Visualisasi dinamis dan responsif menggunakan Plotly. 
                Perbesar, geser, dan jelajahi fungsi Anda secara interaktif.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ================== HALAMAN 2: ANGGOTA TIM ==================
elif page == "👥 Anggota Tim":
    # Bagian Header
    st.markdown("""
    <div class='section-header'>
        <h1 class='section-title'>👥 Tim Pengembang Kami</h1>
        <p class='section-subtitle'>Temui pemikir brilian di balik proyek ini</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # GitHub raw URL untuk foto
    github_base_url = "https://raw.githubusercontent.com/rasyidmaulana19/RasyidClass01Night/main/Image/"
    
    # Baris Anggota Tim 1
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        display_member_card(
            f"{github_base_url}rasyid.jpeg",
            "Rasyid Irvan Maulana",
            "🚀 Ketua Proyek • Arsitek Backend",
            "Merancang arsitektur sistem inti dan infrastruktur backend yang menggerakkan seluruh platform. Ahli dalam merancang solusi yang skalabel dan mengoptimalkan kinerja.",
            "#3b82f6",
            "linear-gradient(135deg, #3b82f6, #2563eb)"
        )
    
    with col2:
        display_member_card(
            f"{github_base_url}luthfi.jpeg",
            "Luthfi Ilham Pratama",
            "🎨 Insinyur Frontend • Desainer UI/UX",
            "Merancang antarmuka yang intuitif dan berpusat pada pengguna dengan tata letak modern dan responsif. Bersemangat menciptakan pengalaman pengguna yang mulus.",
            "#8b5cf6",
            "linear-gradient(135deg, #8b5cf6, #7c3aed)"
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Baris Anggota Tim 2
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        display_member_card(
            f"{github_base_url}andrian.jpeg",
            "Andrian Ramadhan",
            "🧮 Insinyur Algoritma & Matematika",
            "Menerjemahkan konsep matematika yang kompleks menjadi algoritma yang presisi dan optimal. Berspesialisasi dalam efisiensi komputasi dan pemodelan matematika.",
            "#06b6d4",
            "linear-gradient(135deg, #06b6d4, #0891b2)"
        )
    
    with col4:
        display_member_card(
            f"{github_base_url}restu.jpeg",
            "Restu Imam Fakhrezi",
            "📐 Insinyur Matematika Komputasi",
            "Menganalisis formulasi matematika untuk memastikan keandalan dan kebenaran. Berfokus pada metode numerik dan validasi matematis.",
            "#10b981",
            "linear-gradient(135deg, #10b981, #059669)"
        )

# ================== HALAMAN 3: ANALISIS FUNGSI ==================
elif page == "📈 Analisis Fungsi":
    st.title("📈 Visualisasi & Diferensiasi Fungsi")
    
    st.markdown("### 🎯 Pilih Kategori Fungsi")
    
    # Pemilihan Kategori
    category = st.radio(
        "Pilih kategori:",
        ["📐 Polinomial", "🔄 Trigonometri", "📈 Eksponensial", "🔀 Fungsi Campuran"],
        horizontal=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contoh fungsi berdasarkan kategori
    if category == "📐 Polinomial":
        example_functions = {
            "Kuadratik": "x**2 + 3*x + 2",
            "Kubik": "x**3 - 2*x**2 + x - 5",
            "Kuadrik": "x**4 - 4*x**3 + 6*x**2",
            "Linear": "2*x + 5",
            "Kustom": ""
        }
        default_func = "x**2 + 3*x + 2"
        help_text = "Contoh: x**2, x**3 - 2*x, 5*x**4 + 3*x**2 - 1"
    elif category == "🔄 Trigonometri":
        example_functions = {
            "Sinus": "sin(x)",
            "Kosinus": "cos(x)",
            "Tangen": "tan(x)",
            "Sinus + Kosinus": "sin(x) + cos(x)",
            "Kustom": ""
        }
        default_func = "sin(x)"
        help_text = "Contoh: sin(x), cos(x), tan(x), sin(2*x)"
    elif category == "📈 Eksponensial":
        example_functions = {
            "Eksponensial Natural": "exp(x)",
            "Eksponensial dengan koefisien": "2*exp(x)",
            "Eksponensial Negatif": "exp(-x)",
            "Logaritma Natural": "log(x)",
            "Kustom": ""
        }
        default_func = "exp(x)"
        help_text = "Contoh: exp(x), exp(-x), log(x), 2*exp(3*x)"
    else:  # Fungsi Campuran
        example_functions = {
            "Polinomial + Trig": "x**2 + sin(x)",
            "Eksponensial + Trig": "exp(x) * cos(x)",
            "Polinomial * Trig": "x * sin(x)",
            "Kompleks": "x**3 + 2*sin(x) - cos(x)",
            "Kustom": ""
        }
        default_func = "x**2 + sin(x)"
        help_text = "Contoh: x**2 + sin(x), exp(x)*cos(x), x*sin(x)"
    
    st.markdown("### 🔢 Masukkan Fungsi Matematika")
    
    col_select, col_range = st.columns([3, 1])
    
    with col_select:
        # Dropdown untuk pemilihan contoh
        selected_example = st.selectbox(
            "Pilih contoh atau pilih Kustom:",
            list(example_functions.keys()),
            index=0
        )
        
        # Input field
        if selected_example == "Kustom":
            input_function = st.text_input(
                "Fungsi (gunakan x sebagai variabel):",
                value="",
                help=help_text,
                placeholder="Masukkan fungsi kustom Anda di sini..."
            )
        else:
            input_function = st.text_input(
                "Fungsi (gunakan x sebagai variabel):",
                value=example_functions[selected_example],
                help=help_text
            )
    
    with col_range:
        x_range = st.slider("Rentang Plot", -20, 20, (-10, 10))
    
    try:
        x = symbols('x')
        function_expr = sympify(input_function)
        st.markdown("### 📝 Tampilan Fungsi")
        st.latex(f"f(x) = {latex(function_expr)}")
    except Exception as e:
        st.error(f"❌ Kesalahan mengurai fungsi: {e}")
        st.info("Gunakan sintaks Python/SymPy. " + help_text)
        function_expr = None

    if function_expr is not None:
        if st.button("🧮 Hitung Turunan", key="calc_derivative"):
            st.markdown("---")
            st.markdown("### 📊 Turunan Langkah demi Langkah")
            try:
                derivative = diff(function_expr, x)
                with st.expander("📖 Langkah-Langkah Diferensiasi", expanded=True):
                    st.markdown("**Langkah 1:** Identifikasi fungsi yang akan didiferensiasi")
                    st.latex(f"f(x) = {latex(function_expr)}")
                    st.markdown("**Langkah 2:** Terapkan aturan diferensiasi")
                    if function_expr.is_polynomial():
                        st.markdown("- Menggunakan **Aturan Pangkat**: $\\frac{d}{dx}[x^n] = nx^{n-1}$")
                    if function_expr.has(sp.sin) or function_expr.has(sp.cos):
                        st.markdown("- Menggunakan **Aturan Trigonometri**")
                    if function_expr.has(sp.exp):
                        st.markdown("- Menggunakan **Aturan Eksponensial**: $\\frac{d}{dx}[e^x] = e^x$")
                    if function_expr.has(sp.tan):
                        st.markdown("- Menggunakan **Aturan Tangen**: $\\frac{d}{dx}[\\tan x] = \\sec^2 x$")
                    st.markdown("**Langkah 3:** Sederhanakan hasilnya")
                    simplified_derivative = simplify(derivative)
                    st.markdown("**Langkah 4:** Turunan Akhir")
                    st.latex(f"f'(x) = {latex(simplified_derivative)}")
                st.success("✅ Turunan Berhasil Dihitung!")
                st.markdown("### 🎯 Hasil Akhir")
                st.latex(f"\\boxed{{f'(x) = {latex(simplified_derivative)}}}")
            except Exception as e:
                st.error(f"Gagal menghitung turunan: {e}")
                derivative = None

            st.markdown("---")
            st.markdown("### 📊 Visualisasi")
            colp1, colp2 = st.columns(2)
            x_values = np.linspace(x_range[0], x_range[1], 400)
            
            with colp1:
                st.markdown("#### Fungsi Asli f(x)")
                try:
                    f_lambda = sp.lambdify(x, function_expr, 'numpy')
                    y_values = f_lambda(x_values)
                    fig1 = go.Figure()
                    fig1.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='f(x)', line=dict(width=3, color='#60a5fa')))
                    fig1.update_layout(title="Fungsi Asli", xaxis_title="x", yaxis_title="f(x)", template='plotly_dark')
                    st.plotly_chart(fig1, use_container_width=True)
                except Exception:
                    st.error("Tidak dapat memplot fungsi ini pada rentang yang diberikan.")
            
            with colp2:
                st.markdown("#### Turunan f'(x)")
                try:
                    if 'derivative' in locals() and derivative is not None:
                        derivative_lambda = sp.lambdify(x, derivative, 'numpy')
                        dy_values = derivative_lambda(x_values)
                        fig2 = go.Figure()
                        fig2.add_trace(go.Scatter(x=x_values, y=dy_values, mode='lines', name="f'(x)", line=dict(width=3, color='#a78bfa')))
                        fig2.update_layout(title="Fungsi Turunan", xaxis_title="x", yaxis_title="f'(x)", template='plotly_dark')
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("Tekan tombol 'Hitung Turunan' terlebih dahulu untuk melihat plot turunan.")
                except Exception:
                    st.error("Tidak dapat memplot turunan pada rentang yang diberikan.")

# ================== HALAMAN 4: OPTIMASI ==================
elif page == "🎯 Pemecah Optimasi":
    st.title("🎯 Pemecah Masalah Kata Optimasi")
    st.markdown("### 📝 Pilih Kategori Masalah")
    
    # Pemilihan Kategori untuk Optimasi
    opt_category = st.radio(
        "Pilih kategori optimasi:",
        ["📐 Polinomial", "🔄 Trigonometri", "📈 Eksponensial", "🔀 Masalah Campuran"],
        horizontal=True,
        key="opt_category"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Masalah berdasarkan kategori
    if opt_category == "📐 Polinomial":
        example_problems = {
            "Luas Persegi Panjang (Kendala Keliling)": {
                "problem": "Seorang petani memiliki 40 meter pagar untuk memagari area persegi panjang. Dimensi apa yang akan memaksimalkan area yang dipagari?",
                "solution_type": "rectangle_perimeter"
            },
            "Volume Kotak (Luas Permukaan)": {
                "problem": "Sebuah kotak terbuka dibuat dari lembaran kardus persegi berukuran 12 inci di setiap sisi dengan memotong persegi yang sama dari sudut-sudutnya dan melipat sisi-sisinya. Temukan ukuran persegi sudut yang memaksimalkan volume.",
                "solution_type": "box_volume"
            },
            "Optimasi Produk": {
                "problem": "Temukan dua bilangan positif yang jumlahnya 50 dan hasil kalinya maksimum.",
                "solution_type": "sum_product"
            }
        }
    elif opt_category == "🔄 Trigonometri":
        example_problems = {
            "Gerak Proyektil": {
                "problem": "Sebuah proyektil ditembakkan dengan kecepatan awal 100 m/s. Pada sudut berapa ia harus ditembakkan untuk mencapai jangkauan horizontal maksimum? (Gunakan rumus jangkauan: R = (v²sin(2θ))/g, di mana g = 10 m/s²)",
                "solution_type": "projectile"
            },
            "Desain Jendela": {
                "problem": "Jendela Norman memiliki bentuk persegi panjang yang di atasnya terdapat setengah lingkaran. Jika kelilingnya adalah 30 kaki, temukan dimensi yang memaksimalkan luasnya.",
                "solution_type": "norman_window"
            }
        }
    elif opt_category == "📈 Eksponensial":
        example_problems = {
            "Pertumbuhan Populasi": {
                "problem": "Populasi bakteri tumbuh sesuai dengan P(t) = 1000e^(0.5t). Pada waktu berapa laju pertumbuhannya sama dengan 2000 bakteri per jam?",
                "solution_type": "population"
            },
            "Peluruhan Radioaktif": {
                "problem": "Zat radioaktif meluruh sesuai dengan A(t) = 100e^(-0.2t). Kapan laju peluruhannya sama dengan -10 gram per hari?",
                "solution_type": "decay"
            }
        }
    else:  # Masalah Campuran
        example_problems = {
            "Volume Silinder (Campuran)": {
                "problem": "Sebuah kaleng silinder harus memiliki volume 1000 cm³. Dimensi apa yang meminimalkan luas permukaannya? (V = πr²h, SA = 2πr² + 2πrh)",
                "solution_type": "cylinder"
            },
            "Pagar dan Sungai": {
                "problem": "Seorang petani ingin memagari ladang persegi panjang di sepanjang sungai. Tidak diperlukan pagar di sepanjang sungai. Jika ia memiliki 1200 meter pagar, dimensi apa yang memaksimalkan luasnya?",
                "solution_type": "fence_river"
            }
        }
    
    example_choice = st.selectbox(
        "Pilih masalah optimasi:",
        ["Masalah Kustom"] + list(example_problems.keys())
    )
    
    if example_choice == "Masalah Kustom":
        problem_text = st.text_area("Masukkan masalah kata:", height=150, placeholder="Jelaskan masalah optimasi Anda di sini...")
    else:
        problem_text = st.text_area("Masalah:", value=example_problems[example_choice]["problem"], height=150)

    if st.button("🔍 Pecahkan Masalah Optimasi"):
        if problem_text:
            st.markdown("---")
            st.markdown("### 🧮 Solusi")
            
            # Masalah Polinomial
            if example_choice == "Luas Persegi Panjang (Kendala Keliling)":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = panjang persegi panjang")
                    st.markdown("- Misalkan $y$ = lebar persegi panjang")
                    st.markdown("- Kendala Keliling: $2x + 2y = 40$")
                    st.markdown("**Langkah 2: Ekspresikan Fungsi Tujuan**")
                    st.markdown("- Tujuan: Memaksimalkan Luas $A = xy$")
                    st.markdown("- Dari kendala: $y = 20 - x$")
                    st.markdown("- Substitusi: $A(x) = x(20-x) = 20x - x^2$")
                    st.latex("A(x) = 20x - x^2")
                    st.markdown("**Langkah 3: Temukan Titik Kritis**")
                    st.markdown("- Ambil turunan: $A'(x) = 20 - 2x$")
                    st.latex("A'(x) = 20 - 2x")
                    st.markdown("- Atur sama dengan nol: $20 - 2x = 0$ → $x = 10$")
                    st.markdown("**Langkah 4: Verifikasi Maksimum**")
                    st.markdown("- $A''(x) = -2 < 0$ → maksimum")
                    st.markdown("**Langkah 5: Hitung Luas Maksimum**")
                    st.markdown("- Luas Maksimum = $10 \\times 10 = 100$ meter persegi")
                st.success("✅ **Solusi:** Persegi panjang harus berupa persegi dengan sisi 10 m, luas 100 m².")
                
                x_values = np.linspace(0, 20, 200)
                area_values = x_values * (20 - x_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=area_values, mode='lines', name='Luas', line=dict(width=3, color='#60a5fa')))
                fig.add_trace(go.Scatter(x=[10], y=[100], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Luas vs. Panjang", xaxis_title="Panjang (x) dalam meter", yaxis_title="Luas (m²)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
                
            elif example_choice == "Optimasi Produk":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = bilangan pertama, $y$ = bilangan kedua, $x+y=50$")
                    st.markdown("**Langkah 2: Tujuan**")
                    st.markdown("- Memaksimalkan $P=xy$, substitusi $y=50-x$ → $P(x)=50x-x^2$")
                    st.markdown("**Langkah 3: Titik Kritis**")
                    st.markdown("- $P'(x)=50-2x=0$ → $x=25$")
                    st.markdown("**Langkah 4: Hasil**")
                    st.markdown("- Kedua bilangan adalah 25 dan 25 → hasil kali adalah 625")
                st.success("✅ **Solusi:** 25 dan 25, hasil kali maksimum adalah 625.")
                
                x_values = np.linspace(0, 50, 200)
                product_values = x_values * (50 - x_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=product_values, mode='lines', name='Hasil Kali', line=dict(width=3, color='#a78bfa')))
                fig.add_trace(go.Scatter(x=[25], y=[625], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Hasil Kali vs. Bilangan Pertama", xaxis_title="Bilangan Pertama (x)", yaxis_title="Hasil Kali (xy)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
                
            elif example_choice == "Volume Kotak (Luas Permukaan)":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = panjang sisi potongan (inci), kardus adalah 12×12")
                    st.markdown("**Langkah 2: Fungsi Volume**")
                    st.latex("V(x) = x(12-2x)^2 = 4x^3 - 48x^2 + 144x")
                    st.markdown("**Langkah 3: Titik Kritis**")
                    st.latex("V'(x) = 12x^2 - 96x + 144 → x^2 - 8x +12 = 0 → (x-2)(x-6)=0")
                    st.markdown("**Langkah 4: Hasil**")
                    st.markdown("- x=2 valid (x=6 membuat alas nol). Volume maksimum = 128 in³")
                st.success("✅ **Solusi:** Potong persegi 2 inci dari setiap sudut → volume adalah 128 in³.")
                
                x_values = np.linspace(0.1, 6, 200)
                volume_values = 4*x_values**3 - 48*x_values**2 + 144*x_values
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=volume_values, mode='lines', name='Volume', line=dict(width=3, color='#60a5fa')))
                fig.add_trace(go.Scatter(x=[2], y=[128], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Volume vs. Ukuran Potongan", xaxis_title="Ukuran Potongan Sudut (x) in", yaxis_title="Volume (in³)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
            
            # Masalah Trigonometri
            elif example_choice == "Gerak Proyektil":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Rumus Jangkauan**")
                    st.latex(r"R(\theta) = \frac{v^2 \sin(2\theta)}{g} = \frac{100^2 \sin(2\theta)}{10} = 1000\sin(2\theta)")
                    st.markdown("**Langkah 2: Temukan Maksimum**")
                    st.markdown("- Ambil turunan: $R'(\\theta) = 2000\\cos(2\\theta)$")
                    st.markdown("- Atur sama dengan nol: $\\cos(2\\theta) = 0$")
                    st.markdown("- Solusi: $2\\theta = 90°$ → $\\theta = 45°$")
                    st.markdown("**Langkah 3: Verifikasi**")
                    st.markdown("- $R''(\\theta) = -4000\\sin(2\\theta) < 0$ pada $\\theta = 45°$ → maksimum")
                st.success("✅ **Solusi:** Tembakkan pada sudut 45° untuk jangkauan maksimum 1000 meter.")
                
                theta_values = np.linspace(0, 90, 200)
                range_values = 1000 * np.sin(2 * np.radians(theta_values))
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=theta_values, y=range_values, mode='lines', name='Jangkauan', line=dict(width=3, color='#a78bfa')))
                fig.add_trace(go.Scatter(x=[45], y=[1000], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Jangkauan vs. Sudut", xaxis_title="Sudut (derajat)", yaxis_title="Jangkauan (m)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
            
            elif example_choice == "Desain Jendela":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = lebar persegi panjang, $y$ = tinggi persegi panjang")
                    st.markdown("- Jari-jari setengah lingkaran = $x/2$")
                    st.markdown("**Langkah 2: Kendala Keliling**")
                    st.latex(r"P = x + 2y + \frac{\pi x}{2} = 30")
                    st.markdown("- Selesaikan untuk $y$: $y = \\frac{30 - x - \\frac{\\pi x}{2}}{2}$")
                    st.markdown("**Langkah 3: Fungsi Luas**")
                    st.latex(r"A(x) = xy + \frac{\pi x^2}{8}")
                    st.markdown("**Langkah 4: Optimasi**")
                    st.markdown("- Temukan titik kritis menggunakan kalkulus")
                    st.markdown("- Optimal: $x \\approx 8.4$ ft, $y \\approx 4.2$ ft")
                st.success("✅ **Solusi:** Lebar ≈ 8.4 ft, Tinggi ≈ 4.2 ft untuk luas maksimum ≈ 42 ft².")
            
            # Masalah Eksponensial
            elif example_choice == "Pertumbuhan Populasi":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Rumus Laju Pertumbuhan**")
                    st.latex(r"P(t) = 1000e^{0.5t}")
                    st.markdown("- Laju Pertumbuhan: $P'(t) = 500e^{0.5t}$")
                    st.markdown("**Langkah 2: Temukan Saat Laju = 2000**")
                    st.latex(r"500e^{0.5t} = 2000")
                    st.latex(r"e^{0.5t} = 4")
                    st.latex(r"0.5t = \ln(4)")
                    st.latex(r"t = 2\ln(4) \approx 2.77 \text{ jam}")
                st.success("✅ **Solusi:** Laju pertumbuhan sama dengan 2000 bakteri/jam pada t ≈ 2.77 jam.")
                
                t_values = np.linspace(0, 5, 200)
                rate_values = 500 * np.exp(0.5 * t_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=t_values, y=rate_values, mode='lines', name='Laju Pertumbuhan', line=dict(width=3, color='#10b981')))
                fig.add_trace(go.Scatter(x=[2.77], y=[2000], mode='markers', name='Target', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Laju Pertumbuhan vs. Waktu", xaxis_title="Waktu (jam)", yaxis_title="Laju Pertumbuhan (bakteri/jam)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
            
            elif example_choice == "Peluruhan Radioaktif":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Rumus Laju Peluruhan**")
                    st.latex(r"A(t) = 100e^{-0.2t}")
                    st.markdown("- Laju Peluruhan: $A'(t) = -20e^{-0.2t}$")
                    st.markdown("**Langkah 2: Temukan Saat Laju = -10**")
                    st.latex(r"-20e^{-0.2t} = -10")
                    st.latex(r"e^{-0.2t} = 0.5")
                    st.latex(r"-0.2t = \ln(0.5)")
                    st.latex(r"t = -\frac{\ln(0.5)}{0.2} \approx 3.47 \text{ hari}")
                st.success("✅ **Solusi:** Laju peluruhan sama dengan -10 g/hari pada t ≈ 3.47 hari.")
            
            # Masalah Campuran
            elif example_choice == "Volume Silinder (Campuran)":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Kendala Volume**")
                    st.latex(r"\pi r^2 h = 1000 \Rightarrow h = \frac{1000}{\pi r^2}")
                    st.markdown("**Langkah 2: Luas Permukaan**")
                    st.latex(r"SA = 2\pi r^2 + 2\pi r h = 2\pi r^2 + \frac{2000}{r}")
                    st.markdown("**Langkah 3: Minimalkan**")
                    st.latex(r"SA'(r) = 4\pi r - \frac{2000}{r^2} = 0")
                    st.markdown("- Optimal: $r \\approx 5.42$ cm, $h \\approx 10.84$ cm")
                st.success("✅ **Solusi:** Jari-jari ≈ 5.42 cm, Tinggi ≈ 10.84 cm meminimalkan luas permukaan.")
            
            elif example_choice == "Pagar dan Sungai":
                with st.expander("📋 Solusi Langkah demi Langkah", expanded=True):
                    st.markdown("**Langkah 1: Definisikan Variabel**")
                    st.markdown("- Misalkan $x$ = lebar (tegak lurus sungai)")
                    st.markdown("- Misalkan $y$ = panjang (sejajar sungai)")
                    st.markdown("**Langkah 2: Kendala Pagar**")
                    st.markdown("- Hanya 3 sisi yang butuh pagar: $2x + y = 1200$")
                    st.markdown("- Solusi: $y = 1200 - 2x$")
                    st.markdown("**Langkah 3: Fungsi Luas**")
                    st.latex(r"A(x) = xy = x(1200 - 2x) = 1200x - 2x^2")
                    st.markdown("**Langkah 4: Optimasi**")
                    st.markdown("- $A'(x) = 1200 - 4x = 0$ → $x = 300$ m")
                    st.markdown("- $y = 1200 - 600 = 600$ m")
                st.success("✅ **Solusi:** Lebar = 300 m, Panjang = 600 m, Luas Maksimum = 180,000 m².")
                
                x_values = np.linspace(0, 600, 200)
                area_values = x_values * (1200 - 2*x_values)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_values, y=area_values, mode='lines', name='Luas', line=dict(width=3, color='#06b6d4')))
                fig.add_trace(go.Scatter(x=[300], y=[180000], mode='markers', name='Maksimum', marker=dict(size=15, symbol='star', color='#fbbf24')))
                fig.update_layout(title="Luas vs. Lebar", xaxis_title="Lebar (m)", yaxis_title="Luas (m²)", template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.info("💡 Silakan pilih salah satu masalah yang telah ditentukan untuk melihat solusi terperinci.")
        else:
            st.warning("⚠️ Silakan masukkan masalah untuk dipecahkan.")
