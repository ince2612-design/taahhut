import streamlit as st
from fpdf import FPDF
import base64
import os

# Page Configuration
st.set_page_config(page_title="İZSU Taahhütname Paneli", layout="wide")

# Style Configuration
st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; } 
    h1 { color: #003366; text-align: center; }
    input { background-color: #fff9c4 !important; }
    .big-font { font-size:20px !important; font-weight: bold; color: #003366; }
    </style>
""", unsafe_allow_html=True)

st.title("NOTER TAAHHÜTNAMESİ ")

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
    
    # Sunucu üzerindeki yüklü fontu kullanma
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if os.path.exists(font_path):
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=14)
    else:
        pdf.set_font("helvetica", size=14)
    
    pdf.cell(0, 8, "TAAHHÜTNAME", ln=True, align='C')
    pdf.cell(0, 8, "İÇME SUYU VE KANAL KATILIMI İÇİN", ln=True, align='C')
    pdf.cell(0, 8, "TAŞINMAZ TAPU KAYDI", ln=True, align='C')
    pdf.ln(10)
    
    # Information Layout
    pdf.set_font("DejaVu" if os.path.exists(font_path) else "helvetica", size=11)
    pdf.text(20, 90, "İLİ"); pdf.text(45, 90, f": {ili}")
    pdf.text(20, 95, "İLÇE"); pdf.text(45, 95, f": {ilce}")
    pdf.text(20, 100, "MAHALLE"); pdf.text(45, 100, f": {mahalle}")
    
    pdf.text(120, 90, "PAFTA"); pdf.text(145, 90, f": {pafta}")
    pdf.text(120, 95, "ADA"); pdf.text(145, 95, f": {ada}")
    pdf.text(120, 100, "PARSEL"); pdf.text(145, 100, f": {parsel}")
    
    if is_hisseli and bb_no:
        pdf.text(120, 105, f"{bb_no} NOLU BAĞIMSIZ BÖLÜM İÇİNDİR")
    
    # Payment Sections
    pdf.text(20, 135, "Tahakkuk Eden")
    pdf.text(85, 135, ":")
    pdf.text(20, 140, "İçme suyu katılım bedeli %100")
    pdf.text(85, 140, f": {su_bedel:,.2f} TL")
    pdf.text(20, 145, "Kanal katılım bedeli %100")
    pdf.text(85, 145, f": {kanal_bedel:,.2f} TL")
    
    # Main Text Block
    pdf.set_xy(20, 160)
    metin = ("Yukarıda tapu kaydı yazılı taşınmazın maliki sıfatıyla İZSU Genel Müdürlüğü tarafından yapılacak "
             "İçme suyu ve kanal katılım payları için belirlenen %100 katılım bedelini İdarece teknik alt yapı "
             "tamamlandığı zaman, o tarihte İdarece tespit edilip Yönetim Kurulunca Onaylanan birim fiyatlar "
             "üzerinden hesaplanacak alt yapı bedelinin tamamını (%100) olarak İZSU Genel Müdürlüğüne nakten "
             "ödeyeceğimi beyan kabul ve taahhüt ederim.")
    pdf.multi_cell(0, 5, metin, align='J')

    # Signature Area
    pdf.set_y(215) 
    pdf.text(20, 215, "Taahhüt Eden :")
    pdf.text(20, 220, "Telefon        :")
    pdf.text(20, 225, "Adres          :")

    # Output Generation
    pdf_bytes = pdf.output()
    b64 = base64.b64encode(pdf_bytes).decode()
    pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600px"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    st.download_button("📥 PDF İNDİR", pdf_bytes, "Taahhutname.pdf", "application/pdf")
