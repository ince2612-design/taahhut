import streamlit as st
from fpdf import FPDF
import base64
import os

st.set_page_config(page_title="İZSU Taahhütname Paneli", layout="wide")

# CSS: Yazılabilir alanları açık sarı yapma
st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; } 
    div[data-baseweb="input"] > div { background-color: #fff9c4 !important; }
    .big-font { font-size:20px !important; font-weight: bold; color: #003366; }
    </style>
""", unsafe_allow_html=True)

st.title("TAAHHÜTNAME (İZSU)")

# Sütunlu Form Yerleşimi
col1, col2 = st.columns(2)
with col1:
    ili = st.text_input("İLİ", "İZMİR")
    ilce = st.text_input("İLÇE")
    mahalle = st.text_input("MAHALLE")
    # Sol sütun (Su cephe)
    su_cephe_input = st.number_input("Su Cephe", min_value=0.0)

with col2:
    pafta = st.text_input("PAFTA")
    ada = st.text_input("ADA")
    parsel = st.text_input("PARSEL")
    # Sağ sütun (Kanal cephe)
    kanal_cephe_input = st.number_input("Kanal Cephe", min_value=0.0)

st.markdown('<p class="big-font">Hisseli mi?</p>', unsafe_allow_html=True)
is_hisseli = st.checkbox("Evet, hisseli")

if is_hisseli:
    toplam_bb = st.number_input("Toplam Bağımsız Bölüm Sayısı", min_value=1)
    bb_no = st.text_input("Bağımsız Bölüm No")
    su_cephe = su_cephe_input / toplam_bb if toplam_bb > 0 else 0
    kanal_cephe = kanal_cephe_input / toplam_bb if toplam_bb > 0 else 0
else:
    su_cephe = su_cephe_input
    kanal_cephe = kanal_cephe_input
    bb_no = ""

if st.button("BELGE OLUŞTUR"):
    su_bedel = (su_cephe * 4352.38) / 2
    kanal_bedel = (kanal_cephe * 7395.14) / 2
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    font_name = "DejaVu"
    if os.path.exists("DejaVuSans.ttf"):
        pdf.add_font(font_name, "", "DejaVuSans.ttf", uni=True)
    
    # BAŞLIKLAR
    pdf.set_font(font_name, size=14)
    pdf.cell(0, 8, "TAAHHÜTNAME", ln=True, align='C')
    pdf.cell(0, 8, "İÇME SUYU VE KANAL KATILIMI İÇİN", ln=True, align='C')
    pdf.cell(0, 8, "TAŞINMAZ TAPU KAYDI", ln=True, align='C')
    pdf.ln(10)
    
    # BİLGİLER
    pdf.set_font(font_name, size=11)
    pdf.text(20, 90, "İLİ"); pdf.text(45, 90, f": {ili}")
    pdf.text(20, 95, "İLÇE"); pdf.text(45, 95, f": {ilce}")
    pdf.text(20, 100, "MAHALLE"); pdf.text(45, 100, f": {mahalle}")
    
    pdf.text(120, 90, "PAFTA"); pdf.text(145, 90, f": {pafta}")
    pdf.text(120, 95, "ADA"); pdf.text(145, 95, f": {ada}")
    pdf.text(120, 100, "PARSEL"); pdf.text(145, 100, f": {parsel}")
    
    if is_hisseli and bb_no:
        pdf.text(120, 105, f"{bb_no} NOLU BAĞIMSIZ BÖLÜM İÇİNDİR")
    
    # ÖDEMELER
    pdf.text(20, 135, "Tahakkuk Eden")
    pdf.text(85, 135, ":")
    pdf.text(20, 140, "İçme suyu katılım bedeli %100")
    pdf.text(85, 140, f": {su_bedel:,.2f} TL")
    pdf.text(20, 145, "Kanal katılım bedeli %100")
    pdf.text(85, 145, f": {kanal_bedel:,.2f} TL")
    
    # METİN
    pdf.set_xy(20, 160)
    metin = ("Yukarıda tapu kaydı yazılı taşınmazın maliki sıfatıyla İZSU Genel Müdürlüğü tarafından yapılacak "
             "İçme suyu ve kanal katılım payları için belirlenen %100 katılım bedelini İdarece teknik alt yapı "
             "tamamlandığı zaman, o tarihte İdarece tespit edilip Yönetim Kurulunca Onaylanan birim fiyatlar "
             "üzerinden hesaplanacak alt yapı bedelinin tamamını (%100) olarak İZSU Genel Müdürlüğüne nakten "
             "ödeyeceğimi beyan kabul ve taahhüt ederim.")
    pdf.multi_cell(0, 5, metin, align='J')

    # İMZALAR
    pdf.text(20, 215, "Taahhüt Eden :")
    pdf.text(20, 220, "Telefon      :")
    pdf.text(20, 225, "Adres        :")

    pdf_bytes = pdf.output()
    if not isinstance(pdf_bytes, bytes): pdf_bytes = bytes(pdf_bytes)

    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)
    st.download_button("📥 PDF İNDİR", pdf_bytes, "Taahhutname.pdf", "application/pdf")
