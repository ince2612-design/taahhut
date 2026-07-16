import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="İZSU Taahhütname Paneli", layout="wide")

st.title("NOTER TAAHHÜTNAMESİ")

# Form alanlarını buraya eklediğiniz şekilde bırakın...
# (Kısalık adına burayı geçiyorum, kendi kodunuzdaki form kısmını koruyun)
# ...

if st.button("BELGE OLUŞTUR"):
    # HESAPLAMALAR...
    su_bedel = (4352.38) / 2 # Örnek
    kanal_bedel = (7395.14) / 2 # Örnek
    
    # FPDF'i bu şekilde tanımlayın (Font yüklemeden)
    pdf = FPDF()
    pdf.add_page()
    
    # Türkçe karakter hatasını önlemek için set_font'ta 'latin-1' zorlaması
    # 'helvetica' standarttır ve ek dosya gerektirmez.
    pdf.set_font("helvetica", size=14)
    
    # Metinleri doğrudan yazarken encode/decode kullanarak hatayı engelliyoruz
    def t(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    pdf.cell(0, 8, t("TAAHHÜTNAME"), ln=True, align='C')
    pdf.cell(0, 8, t("İÇME SUYU VE KANAL KATILIMI İÇİN"), ln=True, align='C')
    pdf.cell(0, 8, t("TAŞINMAZ TAPU KAYDI"), ln=True, align='C')
    pdf.ln(10)
    
    # Bilgiler...
    pdf.set_font("helvetica", size=11)
    pdf.text(20, 90, t("İLİ: İZMİR"))
    
    # ... (Diğer tüm text satırlarını t() fonksiyonu içine alın)
    
    pdf_bytes = pdf.output()
    # ... (Geri kalan aynı)
