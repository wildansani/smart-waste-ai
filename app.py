import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import base64

st.set_page_config(
    page_title="Smart Waste Classifier",
    page_icon="♻️",
    layout="wide"
)

# Fungsi untuk encode gambar ke base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Encode gambar background
try:
    img_base64 = get_base64_of_bin_file("bgsampah.jpg")
    bg_image = f"url(data:image/jpeg;base64,{img_base64})"
except:
    bg_image = "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)"

st.markdown(f"""
<style>
    .stApp {{
        background: {bg_image} !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-position: center center !important;
        background-attachment: fixed !important;
    }}
    
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.65);
        z-index: -1;
    }}
    
    .glass-card {{
        background: rgba(30, 30, 40, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }}
    
    .glass-title {{
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    
    .subtitle {{
        text-align: center;
        color: #e0e0e0;
        margin-bottom: 2rem;
        text-shadow: 0 1px 5px rgba(0,0,0,0.5);
    }}
    
    [data-testid="stSidebar"] {{
        background: rgba(20, 20, 30, 0.8);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    [data-testid="stSidebar"] * {{
        color: #e0e0e0 !important;
    }}
    
    .metric-card {{
        background: rgba(40, 40, 50, 0.7);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: #e0e0e0;
    }}
    
    .metric-label {{
        color: #c0c0d0;
        font-size: 0.85rem;
    }}
    
    .stButton > button {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        color: white;
    }}
    
    .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.25);
    }}
    
    [data-testid="stFileUploader"] {{
        background: rgba(30, 30, 40, 0.5);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        border: 1px dashed rgba(255, 255, 255, 0.3);
    }}
    
    .stProgress > div > div {{
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 20px;
    }}
    
    .stRadio > div {{
        gap: 1rem;
        justify-content: center;
    }}
    
    .stRadio label {{
        background: rgba(30, 30, 40, 0.6);
        backdrop-filter: blur(8px);
        padding: 0.5rem 1.5rem;
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        cursor: pointer;
    }}
    
    .image-container {{
        background: rgba(30, 30, 40, 0.5);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
    }}
    
    .footer {{
        text-align: center;
        color: #a0a0b0;
        font-size: 0.75rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-title">♻️ SMART WASTE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Klasifikasi Sampah Organik & Anorganik<br>Dengan ResNet50 & Transfer Learning</div>', unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3802/3802075.png", width=100)
    st.markdown("### Informasi Tim")
    st.write("👤 **Wildan Sani** - Model Development")
    st.write("👤 **Ilham Nurhakim** - Literature & Documentation")
    st.write("👤 **Adam Awalul Ihsan** - Data Preparation")
    st.markdown("---")
    st.write("**Model:** Ensemble (2 Model)")
    st.write("**Akurasi Gabungan:** 90%+")
    st.write("**Metode:** Weighted Average Ensemble")
    st.markdown("---")

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

option = st.radio("Pilih metode input gambar:", ["📤 Upload Gambar", "📸 Buka Kamera"], horizontal=True)

img = None

if option == "📤 Upload Gambar":
    uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
else:
    img = st.camera_input("", label_visibility="collapsed")

if img is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(img, caption="Gambar Sampah", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.spinner("🤖 AI Ensemble sedang menganalisis gambar..."):
        
        # Load kedua model
        @st.cache_resource
        def load_models():
            model_a = tf.keras.models.load_model('waste_classifier_final (2).h5')  # Akurasi tinggi
            model_b = tf.keras.models.load_model('waste_classifier_final (1).h5')  # Precision tinggi
            return model_a, model_b
        
        model_a, model_b = load_models()
        
        # Preprocessing gambar
        img_resized = img.resize((224, 224))
        img_array = np.array(img_resized)
        
        if img_array.shape[-1] == 4:
            img_array = img_array[:, :, :3]
        
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Prediksi dari kedua model
        pred_a = model_a.predict(img_array, verbose=0)[0][0]  # Model A (Akurasi)
        pred_b = model_b.predict(img_array, verbose=0)[0][0]  # Model B (Precision)
        
        # ============ ENSEMBLE METHOD ============
        # Method 1: Weighted Average (Rekomendasi)
        # Bobot: Model A 60% (akurasi), Model B 40% (precision)
        weight_a = 0.2  # Bobot untuk akurasi
        weight_b = 0.8  # Bobot untuk precision
        
        ensemble_prediction = (pred_a * weight_a) + (pred_b * weight_b)
        
        # Method 2: Max Confidence (Alternatif - uncomment jika ingin pakai ini)
        # ensemble_prediction = max(pred_a, pred_b)
        
        # Method 3: Voting with confidence boost (Alternatif)
        # if (pred_a > 0.5 and pred_b > 0.5) or (pred_a < 0.5 and pred_b < 0.5):
        #     # Jika kedua model setuju, confidence dinaikkan
        #     ensemble_prediction = (pred_a + pred_b) / 2
        #     ensemble_prediction = ensemble_prediction ** 0.8  # Boost confidence
        # else:
        #     # Jika tidak setuju, ambil yang paling yakin
        #     ensemble_prediction = max(pred_a, pred_b)
        
        st.markdown("---")
        
        # Tampilkan detail ensemble
        with st.expander("📊 Detail Prediksi Ensemble"):
            col_detail1, col_detail2 = st.columns(2)
            with col_detail1:
                st.metric("Model A (Akurasi 88.8%)", f"{pred_a*100:.1f}%")
                st.caption(f"Prediksi: {'ANORGANIK' if pred_a > 0.5 else 'ORGANIK'}")
            with col_detail2:
                st.metric("Model B (Precision 92.7%)", f"{pred_b*100:.1f}%")
                st.caption(f"Prediksi: {'ANORGANIK' if pred_b > 0.5 else 'ORGANIK'}")
            st.markdown("---")
            st.info(f"🎯 **Ensemble (Weighted Average)**\n\nBobot Model A: {weight_a*100:.0f}% | Bobot Model B: {weight_b*100:.0f}%\n\nHasil Final: **{ensemble_prediction*100:.1f}%**")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        if ensemble_prediction > 0.5:
            confidence = float(ensemble_prediction * 100)
            with col_m1:
                st.markdown('<div class="metric-card"><div class="metric-value">🗑️ ANORGANIK</div><div class="metric-label">Jenis Sampah</div></div>', unsafe_allow_html=True)
            with col_m2:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{confidence:.1f}%</div><div class="metric-label">Ensemble Confidence</div></div>', unsafe_allow_html=True)
            with col_m3:
                st.markdown('<div class="metric-card"><div class="metric-value">♻️</div><div class="metric-label">Dapat Didaur Ulang</div></div>', unsafe_allow_html=True)
            st.progress(confidence/100)
            st.success("**Masukkan ke tempat sampah ANORGANIK** (Kuning / Abu-abu)")
        else:
            confidence = float((1 - ensemble_prediction) * 100)
            with col_m1:
                st.markdown('<div class="metric-card"><div class="metric-value">🌿 ORGANIK</div><div class="metric-label">Jenis Sampah</div></div>', unsafe_allow_html=True)
            with col_m2:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{confidence:.1f}%</div><div class="metric-label">Ensemble Confidence</div></div>', unsafe_allow_html=True)
            with col_m3:
                st.markdown('<div class="metric-card"><div class="metric-value">🍂</div><div class="metric-label">Kompos / Basah</div></div>', unsafe_allow_html=True)
            st.progress(confidence/100)
            st.warning(" **Masukkan ke tempat sampah ORGANIK** (Hijau)")
        
        st.balloons()

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem;">📸</div>
        <div style="color: #e0e0e0;">Upload gambar sampah atau buka kamera</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    © 2026 Smart Waste AI | Ensemble Learning | 2 Model ResNet50 - Akurasi & Precision Optimal
</div>
""", unsafe_allow_html=True)
