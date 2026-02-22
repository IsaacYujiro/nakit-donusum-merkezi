import os
from datetime import datetime
import streamlit as st
import pandas as pd
import math

# --- SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="Nakit Dönüşüm Merkezi", page_icon="💸", layout="centered")

# CSS ile biraz makyaj yapalım (Öğrencilerin hoşuna gidecek modern bir görünüm)
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; color: #1E88E5;}
    .offer-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK VE AÇIKLAMA ---
st.title("💻 Anında Nakit, 30 Gün Geri Alım Garantisi")
st.markdown("Cihazını sat, nakit ihtiyacını anında çöz. Üstelik **Türk Borçlar Kanunu (Vefa Hakkı)** güvencesiyle 30 gün içinde geri al!")
st.divider() # Araya ince bir çizgi çeker

# --- VERİ TABANINI YÜKLEME ---
@st.cache_data # Veriyi her seferinde baştan okumasın diye önbelleğe alıyoruz
def veri_yukle():
    try:
        return pd.read_csv("piyasa_verisi.csv")
    except FileNotFoundError:
        st.error("Sistem hatası: Piyasa verisi bulunamadı!")
        return None

df = veri_yukle()

if df is not None:
    # --- KULLANICI ARAMA ÇUBUĞU ---
    st.subheader("Cihazının Değerini Öğren")
    aranacak_kelime = st.text_input("Marka veya Model Yazın (Örn: RTX 3050, RX 9060)")

    # Eğer kullanıcı bir şey yazdıysa ve Enter'a bastıysa
    if aranacak_kelime:
        aranacak_kelime = aranacak_kelime.upper()
        # Veri tabanında arama yapıyoruz
        eslesen_urunler = df[df['Urun_Adi'].str.upper().str.contains(aranacak_kelime)]
        
        if len(eslesen_urunler) == 0:
            st.warning(f"Sistemimizde henüz '{aranacak_kelime}' için yeterli fiyat verisi yok.")
        else:
            # Piyasayı hesapla
            ortalama_piyasa = eslesen_urunler['Piyasa_Fiyati_TL'].mean()
            
            # Senin kâr matematiğin devrede
            nakit_teklif = math.floor(ortalama_piyasa * 0.45)
            geri_alim = math.floor(nakit_teklif * 1.30)
            
            # --- SONUÇLARI EKRANDA GÖSTERME (VİTRİN) ---
            st.success(f"Piyasa taraması tamamlandı! Bu model için {len(eslesen_urunler)} adet ilan analiz edildi.")
            
            st.markdown('<div class="offer-box">', unsafe_allow_html=True)
            st.markdown(f'<p class="big-font">Size Özel Anında Nakit Teklifimiz: {nakit_teklif:,} TL</p>', unsafe_allow_html=True)
            st.markdown(f"**30 Gün İçinde Geri Alım Fiyatınız:** {geri_alim:,} TL")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("") # Boşluk bırak
            
            # --- SAHTE KAPI VE MÜŞTERİ KAYIT SİSTEMİ ---
            st.info("💡 Sistemimiz şu an Kapalı Beta aşamasındadır.")
            email = st.text_input("Sıraya girmek ve teklifi dondurmak için e-posta adresinizi bırakın:")
            
            if st.button("Teklifi Kabul Et ve Sıraya Gir"):
                if email:
                    # Müşterinin verilerini bir pakete koyuyoruz
                    yeni_musteri = pd.DataFrame([{
                        "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Email": email,
                        "Aranan_Cihaz": aranacak_kelime,
                        "Verilen_Teklif_TL": nakit_teklif
                    }])
                    
                    dosya_adi = "bekleme_listesi.csv"
                    
                    # Eğer dosya daha önce yoksa başlıklarla oluştur, varsa alt satıra ekle
                    if not os.path.isfile(dosya_adi):
                        yeni_musteri.to_csv(dosya_adi, mode='w', index=False, encoding='utf-8-sig')
                    else:
                        yeni_musteri.to_csv(dosya_adi, mode='a', header=False, index=False, encoding='utf-8-sig')
                    
                    st.balloons() 
                    st.success("Tebrikler! E-posta adresiniz sıraya alındı. Sistem açıldığında ilk sizinle iletişime geçeceğiz.")
                else:
                    st.error("Lütfen bir e-posta adresi girin.")
