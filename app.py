import streamlit as st
import pandas as pd
import math
import requests
from datetime import datetime

st.set_page_config(page_title="Nakit Dönüşüm Merkezi", page_icon="💸", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold;}
    .offer-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 10px; text-align: center;}
    .condition-box { background-color: #ffffff; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 15px;}
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
    st.subheader("1. Cihazınızı Seçin")
    aranacak_kelime = st.text_input("Marka veya Model Yazın (Örn: RTX 3050, RX 9060)")

    if aranacak_kelime:
        aranacak_kelime = aranacak_kelime.upper()
        eslesen_urunler = df[df['Urun_Adi'].str.upper().str.contains(aranacak_kelime)]
        
        if len(eslesen_urunler) == 0:
            st.warning(f"Sistemimizde henüz '{aranacak_kelime}' için yeterli fiyat verisi yok.")
        else:
            ortalama_piyasa = eslesen_urunler['Piyasa_Fiyati_TL'].mean()
            
            st.subheader("2. Cihazın Durumu")
            st.markdown('<div class="condition-box">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                kutu_durumu = st.radio("Kutu ve Fatura", ["Kutu ve Fatura Tam", "Sadece Kutu Var", "Kutu/Fatura Yok"])
                garanti_durumu = st.radio("Garanti Durumu", ["Garantisi Bitti", "Garantisi Devam Ediyor"])
            with col2:
                kozmetik_durum = st.selectbox("Kozmetik Durum", ["Kusursuz (Sıfır Ayarında)", "Ufak Çizikler / Kullanım İzi", "Hasarlı / Tamir Görmüş"])
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            carpan = 1.0
            if kutu_durumu == "Sadece Kutu Var":
                carpan -= 0.05
            elif kutu_durumu == "Kutu/Fatura Yok":
                carpan -= 0.10
                
            if garanti_durumu == "Garantisi Devam Ediyor":
                carpan += 0.05
                
            if kozmetik_durum == "Ufak Çizikler / Kullanım İzi":
                carpan -= 0.10
            elif kozmetik_durum == "Hasarlı / Tamir Görmüş":
                carpan -= 0.25
                
            guncel_deger = ortalama_piyasa * carpan
            
            # İki farklı teklifi hesapla
            direkt_satis = math.floor(guncel_deger * 0.55)
            vefa_nakit = math.floor(guncel_deger * 0.40)
            vefa_geri_alim = math.floor(vefa_nakit * 1.30)
            
            st.subheader("3. Teklifinizi Seçin")
            teklif_col1, teklif_col2 = st.columns(2)
            
            with teklif_col1:
                st.markdown('<div class="offer-box">', unsafe_allow_html=True)
                st.markdown("### 🚀 Direkt Satış")
                st.markdown("Cihazı tamamen sat, en yüksek nakdi al.")
                st.markdown(f'<p class="big-font" style="color:#e53935;">{direkt_satis:,} TL</p>', unsafe_allow_html=True)
                st.markdown("(Geri alım hakkı yoktur)")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with teklif_col2:
                st.markdown('<div class="offer-box">', unsafe_allow_html=True)
                st.markdown("### 🔄 30 Gün Emanet")
                st.markdown("Paranı al, 30 gün içinde geri ödeyip cihazını al.")
                st.markdown(f'<p class="big-font" style="color:#43a047;">{vefa_nakit:,} TL</p>', unsafe_allow_html=True)
                st.markdown(f"(Geri Alım Bedeli: {vefa_geri_alim:,} TL)")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("")
            secilen_teklif = st.radio("Hangi teklifi değerlendirmek istersiniz?", ["Direkt Satış (Yüksek Nakit)", "30 Gün Emanet (Geri Alım Garantili)"])
            
            st.info("💡 Sistemimiz şu an Kapalı Beta aşamasındadır.")
            email = st.text_input("Sıraya girmek ve teklifi dondurmak için e-posta adresinizi bırakın:")
            
            if st.button("Teklifi Kabul Et ve Sıraya Gir"):
                if email:
                    gonderilecek_teklif = f"{direkt_satis} TL (Direkt Satış)" if "Direkt" in secilen_teklif else f"{vefa_nakit} TL (Vefa)"
                    
                    veri_paketi = {
                        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Email": email,
                        "Cihaz": aranacak_kelime,
                        "Teklif": gonderilecek_teklif
                    }
                    
                    google_url = "https://script.google.com/macros/s/AKfycbwnBoJA3WCy0LKWA0K1sCXvmie3fYPpx9Mg3hmTtildoe7_sUyNEHUz7FUI8koPyQrDuQ/exec"
                    
                    try:
                        yanit = requests.post(google_url, json=veri_paketi)
                        if yanit.status_code == 200:
                            st.balloons()
                            st.success(f"Tebrikler! {secilen_teklif} tercihinizle sıraya alındınız.")
                        else:
                            st.error("Kayıt sırasında bir hata oluştu, lütfen tekrar deneyin.")
                    except Exception as e:
                        st.error("Sistemsel bir bağlantı hatası oluştu.")
                else:
                    st.error("Lütfen bir e-posta adresi girin.")
