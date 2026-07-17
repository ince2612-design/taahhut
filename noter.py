import streamlit as st
from fpdf import FPDF
import base64
import os

# Page Configuration
st.set_page_config(page_title="İZSU Taahhütname Paneli", layout="wide")

# Style Configuration - Yazılabilir alanları açık sarı yapma
st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; } 
    h1 { color: #003366; text-align: center; }
    div[data-baseweb="input"] > div {
        background-color: #fff9c4 !important;
    }
    .big-font { font-size:20px !important; font-weight: bold; color: #003366; }
    </style>
""", unsafe_allow_html=True)

st.title("TAAHHÜTNAME (İZSU)")

col1, col2 = st.columns(2)
with col1:
    ili = st.text_input("İLİ", "İZMİR", key="ili_input")
    ilce = st.text_input("İLÇE", key="ilce_input")
    mahalle = st.text_input("MAHALLE", key="mahalle_input")
with col2:
    pafta = st.text_input("PAFTA", key="pafta_input")
    ada = st.text_input("ADA", key="ada_input")
    parsel = st.text_input("PARSEL", key="parsel_input")

st.markdown('<p class="big-font">Hisseli mi?</p>', unsafe_allow_html=True)
is_hisseli = st.checkbox("Evet, hisseli", key="hisseli_check")

if is_hisseli:
    toplam_bb = st.number_input("Toplam Bağımsız Bölüm Sayısı", min_value=1, key="toplam_bb")
    bb_no = st.text_input("Bağımsız Bölüm No", key="bb_no")
    col_a, col_b = st.columns(2)
    toplam_su_cephe = col_a.number_input("Toplam Su Cephe", min_value=0.0, key="top_su")
    toplam_kanal_cephe = col_b.number_input("Toplam Kanal Cephe", min_value=0.0, key="top_kanal")
    su_cephe = toplam_su_cephe / toplam_bb if toplam_bb > 0 else 0
    kanal_cephe = toplam_kanal_cephe / toplam_bb if toplam_bb > 0 else 0
else:
    col_a, col_b = st.columns(2)
    su_cephe = col_a.number_input("Su Cephe", min_value=0.0, key="tek_su")
    kanal_cephe = col_b.number_input("Kanal Cephe", min_value=0.0, key="tek_kanal")
    bb_no = ""

if st.button("BELGE OLUŞTUR"):
    su_bedel = (su_cephe * 4352.38) / 2
    kanal_bedel = (kanal_cephe * 7395.14) / 2
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Font kontrolü
    if os.path.exists("DejaVuSans.ttf"):
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
    else:
        pdf.set_font("helvetica", size=12)
    
    # PDF İçeriği
    pdf.cell(0, 10, "TAAHHÜTNAME", ln=True, align='C')
    pdf.cell(0, 10, "İÇME SUYU VE KANAL KATILIMI İÇİN", ln=True, align='C')
    pdf.cell(0, 10, "TAŞINMAZ TAPU KAYDI", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(0, 8, f"İLİ: {ili}          PAFTA: {pafta}", ln=True)
    pdf.cell(0, 8, f"İLÇE: {ilce}          ADA: {ada}", ln=True)
    pdf.cell(0, 8, f"MAHALLE: {mahalle}          PARSEL: {parsel}", ln=True)
    
    if is_hisseli and bb_no:
        pdf.cell(0, 8, f"{bb_no} NOLU BAĞIMSIZ BÖLÜM İÇİNDİR", ln=True)
    
    pdf.ln(10)
    pdf.cell(0, 8, f"İçme suyu katılım bedeli: {su_bedel:,.2f} TL", ln=True)
    pdf.cell(0, 8, f"Kanal katılım bedeli: {kanal_bedel:,.2f} TL", ln=True)
    
    pdf.ln(10)
    metin = ("Yukarıda tapu kaydı yazılı taşınmazın maliki sıfatıyla İZSU Genel Müdürlüğü tarafından yapılacak "
             "İçme suyu ve kanal katılım payları için belirlenen %100 katılım bedelini İdarece teknik alt yapı "
             "tamamlandığı zaman, o tarihte İdarece tespit edilip Yönetim Kurulunca Onaylanan birim fiyatlar "
             "üzerinden hesaplanacak alt yapı bedelinin tamamını (%100) olarak İZSU Genel Müdürlüğüne nakten "
             "ödeyeceğimi beyan kabul ve taahhüt ederim.")
    pdf.multi_cell(0, 5, metin, align='J')

    pdf.ln(10)
    pdf.cell(0, 8, "Taahhüt Eden :", ln=True)
    pdf.cell(0, 8, "Telefon      :", ln=True)
    pdf.cell(0, 8, "Adres        :", ln=True)

    # PDF Çıktı
    pdf_bytes = pdf.output()
    if not isinstance(pdf_bytes, bytes):
        pdf_bytes = bytes(pdf_bytes)

    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)
    st.download_button("📥 PDF İNDİR", pdf_bytes, "Taahhutname.pdf", "application/pdf")
