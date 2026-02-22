import streamlit as st
import pandas as pd
import math
import requests
from datetime import datetime

st.set_page_config(page_title="Nakit Dönüşüm Merkezi", page_icon="💸", layout="centered")

st.markdown("""
<style>
.big-font { font-size:24px !important; font-weight: bold; color: #1E88E5;}
.offer-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

st.title("💻 Anında Nakit, 30 Gün Geri Alım Garantisi")
st.markdown("Cihazını sat, nakit ihtiyacını anında çöz. Üstelik Türk Borçlar Kanunu (Vefa Hakkı) güvencesiyle 30 gün içinde geri al!")
st.divider()

@st.cache_data
def veri_yukle():
try:
return pd.read_csv("piyasa_verisi.csv")
except FileNotFoundError:
st.error("Sistem hatası: Piyasa verisi bulunamadı!")
return None

df = veri_yukle()

if df is not None:
st.subheader("Cihazının Değerini Öğren")
aranacak_kelime = st.text_input("Marka veya Model Yazın (Örn: RTX 3050, RX 9060)")

if aranacak_kelime:
    aranacak_kelime = aranacak_kelime.upper()
    eslesen_urunler = df[df['Urun_Adi'].str.upper().str.contains(aranacak_kelime)]
    
    if len(eslesen_urunler) == 0:
        st.warning(f"Sistemimizde henüz '{aranacak_kelime}' için yeterli fiyat verisi yok.")
    else:
        ortalama_piyasa = eslesen_urunler['Piyasa_Fiyati_TL'].mean()
        nakit_teklif = math.floor(ortalama_piyasa * 0.45)
        geri_alim = math.floor(nakit_teklif * 1.30)
        
        st.success(f"Piyasa taraması tamamlandı! Bu model için {len(eslesen_urunler)} adet ilan analiz edildi.")
        st.markdown('<div class="offer-box">', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font">Size Özel Anında Nakit Teklifimiz: {nakit_teklif:,} TL</p>', unsafe_allow_html=True)
        st.markdown(f"**30 Gün İçinde Geri Alım Fiyatınız:** {geri_alim:,} TL")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")
        
        st.info("💡 Sistemimiz şu an Kapalı Beta aşamasındadır.")
        email = st.text_input("Sıraya girmek ve teklifi dondurmak için e-posta adresinizi bırakın:")
        
        if st.button("Teklifi Kabul Et ve Sıraya Gir"):
            if email:
                veri_paketi = {
                    "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Email": email,
                    "Cihaz": aranacak_kelime,
                    "Teklif": nakit_teklif
                }
                
                google_url = "[https://script.google.com/macros/s/AKfycbwnBoJA3WCy0LKWA0K1sCXvmie3fYPpx9Mg3hmTtildoe7_sUyNEHUz7FUI8koPyQrDuQ/exec](https://script.google.com/macros/s/AKfycbwnBoJA3WCy0LKWA0K1sCXvmie3fYPpx9Mg3hmTtildoe7_sUyNEHUz7FUI8koPyQrDuQ/exec)"
                
                try:
                    yanit = requests.post(google_url, json=veri_paketi)
                    if yanit.status_code == 200:
                        st.balloons()
                        st.success("Tebrikler! E-posta adresiniz başarıyla listeye eklendi.")
                    else:
                        st.error("Kayıt sırasında bir hata oluştu, lütfen tekrar deneyin.")
                except Exception as e:
                    st.error("Sistemsel bir bağlantı hatası oluştu.")
            else:
                st.error("Lütfen bir e-posta adresi girin.")
