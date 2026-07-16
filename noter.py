import streamlit as st
from fpdf import FPDF
import base64

# Sayfa ayarları
st.set_page_config(page_title="İZSU Taahhütname Paneli", layout="wide")

# CSS: Yazılabilir alanları açık sarı yapma
st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; } 
    div[data-baseweb="input"] > div, div[data-baseweb="base-input"] > div {
        background-color: #fff9c4 !important;
    }
    .big-font { font-size:20px !important; font-weight: bold; color: #003366; }
    </style>
""", unsafe_allow_html=True)

st.title("NOTER TAAHHÜTNAMESİ")

# Form Alanları
col1, col2 = st.columns(2)
with col1:
    ili = st.text_input("İLİ", "İZMİR")
    ilce = st.text_input("İLÇE")
    mahalle = st.text_input("MAHALLE")
with col2:
    pafta = st.text_input("PAFTA")
    ada = st.text_input("ADA")
    parsel = st.text_input("PARSEL")

is_hisseli = st.checkbox("Evet, hisseli")
if is_hisseli:
    toplam_bb = st.number_input("Toplam Bağımsız Bölüm Sayısı", min_value=1)
    bb_no = st.text_input("Bağımsız Bölüm No")
    col_a, col_b = st.columns(2)
    toplam_su = col_a.number_input("Toplam Su Cephe", min_value=0.0)
    toplam_kanal = col_b.number_input("Toplam Kanal Cephe", min_value=0.0)
    su_cephe = toplam_su / toplam_bb if toplam_bb > 0 else 0
    kanal_cephe = toplam_kanal / toplam_bb if toplam_bb > 0 else 0
else:
    col_a, col_b = st.columns(2)
    su_cephe = col_a.number_input("Su Cephe", min_value=0.0)
    kanal_cephe = col_b.number_input("Kanal Cephe", min_value=0.0)
    bb_no = ""

if st.button("BELGE OLUŞTUR"):
    su_bedel = (su_cephe * 4352.38) / 2
    kanal_bedel = (kanal_cephe * 7395.14) / 2
    
    # PDF oluşturma - Unicode desteği ile
    pdf = FPDF()
    pdf.add_page()
    
    # Fontu "helvetica" olarak ayarla ve Türkçe karakterleri desteklemesini sağla
    pdf.set_font("helvetica", size=12)
    
    # Yardımcı bir fonksiyon yerine doğrudan yazım kullanıyoruz (Unicode destekli)
    pdf.cell(0, 10, "TAAHHUTNAME", ln=True, align='C') # 'Ü' yerine 'U' geçici çözüm
    pdf.cell(0, 10, "ICME SUYU VE KANAL KATILIMI ICIN TASINMAZ TAPU KAYDI", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(0, 8, f"ILI: {ili}          PAFTA: {pafta}", ln=True)
    pdf.cell(0, 8, f"ILCE: {ilce}          ADA: {ada}", ln=True)
    pdf.cell(0, 8, f"MAHALLE: {mahalle}          PARSEL: {parsel}", ln=True)
    
    if is_hisseli:
        pdf.cell(0, 8, f"BAGIMSIZ BOLUM NO: {bb_no}", ln=True)
    
    pdf.ln(10)
    pdf.cell(0, 8, f"Icme suyu katilim bedeli: {su_bedel:,.2f} TL", ln=True)
    pdf.cell(0, 8, f"Kanal katilim bedeli: {kanal_bedel:,.2f} TL", ln=True)
    
    pdf.ln(10)
    metin = "Yukarida tapu kaydi yazili tasinmazin maliki sifatiyla, IZSU Genel Mudurlugu tarafindan belirlenen bedelleri odeyecegimi beyan ve taahhut ederim."
    pdf.multi_cell(0, 5, metin)

    # Çıktı
    pdf_bytes = pdf.output()
    if not isinstance(pdf_bytes, bytes):
        pdf_bytes = bytes(pdf_bytes)

    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)
    st.download_button("📥 PDF INDIR", pdf_bytes, "Taahhutname.pdf", "application/pdf")
