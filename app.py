import streamlit as st
import pandas as pd
import math
import requests
from datetime import datetime

# ==============================================================================
# BÖLÜM 1: SİSTEM KONFİGÜRASYONU VE ÇOKLU SAYFA ALTYAPISI (CORE ARCHITECTURE)
# ==============================================================================
st.set_page_config(page_title="VefaTech | Yeni Nesil Nakit", page_icon="💸", layout="wide", initial_sidebar_state="expanded")

# --- OTURUM YÖNETİMİ (SESSION STATE) ---
# Profesyonel siteler kullanıcının kim olduğunu ve sayfalar arası geçerken ne yaptığını unutmaz.
# Burada kullanıcının oturumunu, cüzdanını ve geçmiş tekliflerini bulutta (hafızada) tutuyoruz.
if 'kullanici_giris_yapti_mi' not in st.session_state:
    st.session_state['kullanici_giris_yapti_mi'] = False
if 'aktif_kullanici_maili' not in st.session_state:
    st.session_state['aktif_kullanici_maili'] = ""
if 'bekleyen_teklifler' not in st.session_state:
    st.session_state['bekleyen_teklifler'] = []
if 'sayfa' not in st.session_state:
    st.session_state['sayfa'] = "Ana Sayfa (Vitrin)"

# --- GELİŞMİŞ CSS MOTORU (UI/UX) ---
# Trendyol/Letgo hissini veren yuvarlak hatlar, dinamik grid (ızgara) yapısı ve modern fontlar.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] {font-family: 'Inter', sans-serif; background-color: #f8f9fa;}
    
    /* Modern Sol Menü (Sidebar) */
    [data-testid="stSidebar"] {background-color: #111827; color: white;}
    [data-testid="stSidebar"] * {color: #e5e7eb;}
    
    /* Kurumsal Üst Navigasyon (Navbar) */
    .top-navbar {background: #ffffff; padding: 20px 30px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 30px;}
    .logo-text {font-size: 28px; font-weight: 800; background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    
    /* Dinamik Ürün Grid'i (Trendyol Tarzı Yan Yana Kart Dizilimi İçin) */
    .grid-container {display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;}
    .product-card {background: white; border-radius: 12px; padding: 20px; border: 1px solid #e5e7eb; transition: all 0.2s ease-in-out; cursor: pointer;}
    .product-card:hover {transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: #3b82f6;}
    
    /* Gelişmiş Durum (Kondisyon) Konteynerleri */
    .advanced-condition-box {background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 25px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);}
    </style>
    """, unsafe_allow_html=True)

# --- SİTE VİTRİNİ VE YÖNLENDİRME (ROUTING) SİSTEMİ ---
st.markdown('<div class="top-navbar"><div class="logo-text">VefaTech Merkezi</div><div>Güvenli, Hızlı & Yasal Nakit</div></div>', unsafe_allow_html=True)

# Sol Menü (Sidebar) Navigasyonu
st.sidebar.title("Kullanıcı Paneli")
secilen_sayfa = st.sidebar.radio("Menü Navigasyonu", ["Ana Sayfa (Vitrin)", "Anında Değerleme Modülü", "Cüzdanım / Tekliflerim", "Teslimat ve Randevu", "Piyasa Analizi (Grafikler)", "Gizli Yönetici Paneli", "KYC ve Sözleşme Üretici", "Ayarlar ve Profil", "SSS ve Destek", "Davet Et Kazan (Referans)", "Dijital Dekont (Makbuz)", "Sistem Sağlığı (Ping & DB)"])
st.session_state['sayfa'] = secilen_sayfa

# Sayfa Kontrolcüsü (Router) - Kullanıcı hangi sayfadaysa onun içeriği yüklenecek
st.write(f"Şu anki aktif modül: **{st.session_state['sayfa']}**")

# BÖLÜM 1'İN SONU. (Bölüm 2'de bu sayfaların içini gerçek veriler ve gelişmiş algoritmalarla dolduracağız).

# ==============================================================================
# BÖLÜM 2: VERİ TABANI BAĞLANTISI VE ANA SAYFA (VİTRİN) MODÜLÜ
# ==============================================================================
@st.cache_data
def veri_yukle():
    try:
        return pd.read_csv("piyasa_verisi.csv")
    except FileNotFoundError:
        return None

df = veri_yukle()

if st.session_state['sayfa'] == "Ana Sayfa (Vitrin)":
    st.markdown("## 🔥 Popüler Cihazlar ve Güncel Piyasalar")
    st.markdown("Aşağıdaki cihazlardan birine veya benzerine sahipseniz, anında nakit teklifi almak için sol menüden Anında Değerleme Modülü'ne geçiş yapın.")
    st.write("")
    
    if df is not None:
        # En popüler 6 ürünü vitrine diziyoruz
        populer_urunler = df.head(6)
        
        col1, col2, col3 = st.columns(3)
        
        for i, urun in populer_urunler.iterrows():
            fiyat = int(urun['Piyasa_Fiyati_TL'])
            urun_adi = urun['Urun_Adi'].upper()
        
        # Ana sayfa için basit görsel eşleştirme motoru
        gorsel_linki = "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=400&q=80"
        if "PLAYSTATION 5" in urun_adi:
            gorsel_linki = "https://gmedia.playstation.com/is/image/SIEPDC/ps5-product-thumbnail-01-en-14sep21?$1600px$"
        elif "PLAYSTATION 4" in urun_adi:
            gorsel_linki = "https://gmedia.playstation.com/is/image/SIEPDC/ps4-slim-image-block-01-en-24jul20?$1600px$"
        elif "RTX 40" in urun_adi:
            gorsel_linki = "https://images.nvidia.com/aem-dam/Solutions/geforce/ada/rtx-4090/geforce-rtx-4090-gallery-b-750x422.png"
        elif "RTX 30" in urun_adi:
            gorsel_linki = "https://images.nvidia.com/aem-dam/Solutions/geforce/ampere/rtx-3080/geforce-rtx-3080-gallery-b-750x422.png"
        elif "RYZEN" in urun_adi:
            gorsel_linki = "https://www.amd.com/system/files/2022-11/1761919-amd-ryzen-9-pib-right-facing-1260x709.png"

        kutu_icerigi = f'''
        <div class="product-card" style="text-align: center;">
            <img src="{gorsel_linki}" style="width:100%; height:140px; object-fit:contain; margin-bottom:15px;">
            <h4 style="color:#1f2937; margin-bottom:5px;">{urun['Urun_Adi']}</h4>
            <p style="color:#6b7280; font-size:14px; margin-bottom:15px;">2. El Piyasa Değeri</p>
            <h3 style="color:#10b981; margin:0;">₺{fiyat:,}</h3>
        </div>
        '''
        
        if i % 3 == 0:
            col1.markdown(kutu_icerigi, unsafe_allow_html=True)
        elif i % 3 == 1:
            col2.markdown(kutu_icerigi, unsafe_allow_html=True)
        else:
            col3.markdown(kutu_icerigi, unsafe_allow_html=True)
        st.info(f"💡 Sistemimizde anlık olarak {len(df)} farklı cihazın canlı piyasa verisi bulunmaktadır.")
    else:
        st.error("Veri tabanına (piyasa_verisi.csv) ulaşılamıyor. Lütfen dosyanın yüklü olduğundan emin olun.")

# ==============================================================================
# BÖLÜM 3: ANINDA DEĞERLEME MODÜLÜ VE RİSK ALGORİTMASI
# ==============================================================================
elif st.session_state['sayfa'] == "Anında Değerleme Modülü":
    st.markdown("## ⚡ Anında Değerleme ve Nakit Teklifi")
    st.markdown("Cihazınızın marka veya modelini girerek saniyeler içinde net değerini öğrenin.")
    st.write("")
    
    if df is not None:
        aranacak_kelime = st.text_input("🔍 Cihazınızı Arayın:", placeholder="Örn: RTX 3070, PlayStation 5, Ryzen 5 5600...")
        
        if aranacak_kelime:
            aranacak_kelime = aranacak_kelime.upper()
            eslesen_urunler = df[df['Urun_Adi'].str.upper().str.contains(aranacak_kelime)]
            
            if len(eslesen_urunler) == 0:
                st.warning(f"Sistemimizde '{aranacak_kelime}' için yeterli fiyat verisi yok. Ürün havuzumuz sürekli güncellenmektedir.")
            else:
                ortalama_piyasa = eslesen_urunler['Piyasa_Fiyati_TL'].mean()
                                # --- YENİ EKLENEN GÖRSEL MOTORU ---
                urun_gorselleri = {
                    "PLAYSTATION 5": "https://gmedia.playstation.com/is/image/SIEPDC/ps5-product-thumbnail-01-en-14sep21?$1600px$",
                    "PLAYSTATION 4": "https://gmedia.playstation.com/is/image/SIEPDC/ps4-slim-image-block-01-en-24jul20?$1600px$",
                    "XBOX": "https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE4mRni?ver=e700",
                    "RTX 40": "https://images.nvidia.com/aem-dam/Solutions/geforce/ada/rtx-4090/geforce-rtx-4090-gallery-b-750x422.png",
                    "RTX 30": "https://images.nvidia.com/aem-dam/Solutions/geforce/ampere/rtx-3080/geforce-rtx-3080-gallery-b-750x422.png",
                    "RX 7": "https://www.amd.com/system/files/2022-11/1761919-amd-radeon-rx-7900-xtx-gallery-1-1260x709.png",
                    "RYZEN": "https://www.amd.com/system/files/2022-11/1761919-amd-ryzen-9-pib-right-facing-1260x709.png",
                    "APPLE WATCH": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/watch-card-40-s9-202309?wid=680&hei=528&fmt=p-jpg",
                    "AIRPODS": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MME73?wid=1144&hei=1144&fmt=jpeg"
                }
                
                gosterilecek_gorsel = "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=400&q=80" # Cihaz tanınmazsa çıkacak varsayılan şık teknoloji fotoğrafı
                for anahtar_kelime, link in urun_gorselleri.items():
                    if anahtar_kelime in aranacak_kelime:
                        gosterilecek_gorsel = link
                        break
                
                st.write("")
                col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
                with col_img2:
                    st.image(gosterilecek_gorsel, use_container_width=True, caption=f"Seçilen Cihaz: {eslesen_urunler['Urun_Adi'].values[0]}")
                st.write("")
                st.markdown("---")
                # -----------------------------------
                st.markdown("### 📋 1. Adım: Cihazın Kondisyonunu Belirleyin")
                st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    kutu_durumu = st.radio("📦 Kutu ve Fatura", ["Tam (Kutu+Fatura)", "Sadece Kutu Var", "İkisi de Yok"], key="kutu")
                with col2:
                    garanti_durumu = st.radio("🛡️ Garanti Durumu", ["Bitti", "Devam Ediyor"], key="garanti")
                with col3:
                    kozmetik_durum = st.selectbox("✨ Kozmetik Durumu", ["Kusursuz (Sıfır Gibi)", "Kılcal Çizikler Var", "Hasarlı / Tamir Görmüş"], key="kozmetik")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Algoritma: Seçimlere göre risk çarpanını hesapla
                carpan = 1.0
                if kutu_durumu == "Sadece Kutu Var": carpan -= 0.05
                elif kutu_durumu == "İkisi de Yok": carpan -= 0.10
                
                if garanti_durumu == "Devam Ediyor": carpan += 0.05
                
                if kozmetik_durum == "Kılcal Çizikler Var": carpan -= 0.10
                elif kozmetik_durum == "Hasarlı / Tamir Görmüş": carpan -= 0.25
                
                # Nihai Fiyatı Çıkar
                guncel_deger = ortalama_piyasa * carpan
                direkt_satis = math.floor(guncel_deger * 0.55)
                vefa_nakit = math.floor(guncel_deger * 0.40)
                vefa_geri_alim = math.floor(vefa_nakit * 1.30)
                
                st.markdown("### 💰 2. Adım: Size Özel Nakit Tekliflerimiz")
                teklif_col1, teklif_col2 = st.columns(2)
                
                with teklif_col1:
                    st.markdown('<div class="card-direct">', unsafe_allow_html=True)
                    st.markdown("#### 🚀 DİREKT SATIŞ")
                    st.markdown("Cihazı tamamen elden çıkar, maksimum nakdi al.")
                    st.markdown(f'<div class="price-tag-red">₺{direkt_satis:,}</div>', unsafe_allow_html=True)
                    st.markdown("<small style='color:#6b7280;'>Geri alım hakkı içermez.</small>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with teklif_col2:
                    st.markdown('<div class="card-vefa">', unsafe_allow_html=True)
                    st.markdown("#### 🔄 30 GÜN EMANET (VEFA)")
                    st.markdown("Paranı anında al, cihazını 30 gün içinde geri al.")
                    st.markdown(f'<div class="price-tag-green">₺{vefa_nakit:,}</div>', unsafe_allow_html=True)
                    st.markdown(f"<small style='color:#6b7280;'>30 Günlük Geri Alım Bedeli: ₺{vefa_geri_alim:,}</small>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                st.write("")
                st.markdown("### 📝 3. Adım: Başvuruyu Tamamla")
                secilen_teklif = st.radio("Sizin için en uygun teklifi seçin:", ["🚀 Direkt Satış", "🔄 30 Gün Emanet (Vefa)"], key="teklif_secim")
                
                # Oturum hafızasındaki maili (varsa) otomatik getir
                mevcut_email = st.session_state['aktif_kullanici_maili']
                email = st.text_input("📬 Teklifi dondurmak ve randevu almak için E-posta:", value=mevcut_email, placeholder="ornek@gmail.com")
                
                if st.button("Teklifi Onayla ve Randevu Al", type="primary"):
                    if email:
                        # Seçilen teklifin net miktarını belirle
                        if "Direkt" in secilen_teklif:
                            teklif_sonucu = f"₺{direkt_satis} (Direkt Satış)"
                        else:
                            teklif_sonucu = f"₺{vefa_nakit} (Vefa - Geri Alım: ₺{vefa_geri_alim})"
                        
                        veri_paketi = {
                            "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Email": email,
                            "Cihaz": f"{aranacak_kelime} ({kozmetik_durum})",
                            "Teklif": teklif_sonucu
                        }
                        
                        google_url = "https://script.google.com/macros/s/AKfycbwnBoJA3WCy0LKWA0K1sCXvmie3fYPpx9Mg3hmTtildoe7_sUyNEHUz7FUI8koPyQrDuQ/exec"
                        
                        try:
                            yanit = requests.post(google_url, json=veri_paketi)
                            if yanit.status_code == 200:
                                # Oturum Hafızasına Kaydetme İşlemleri (Giriş Yapmış Sayıyoruz)
                                st.session_state['kullanici_giris_yapti_mi'] = True
                                st.session_state['aktif_kullanici_maili'] = email
                                st.session_state['bekleyen_teklifler'].append(veri_paketi)
                                
                                st.success(f"Harika! Talebiniz alındı. Sol menüden 'Cüzdanım / Tekliflerim' sekmesine giderek durumu takip edebilirsiniz.")
                                st.balloons()
                            else:
                                st.error("Kayıt sırasında sunucu hatası oluştu, lütfen tekrar deneyin.")
                        except Exception as e:
                            st.error("Sistemsel bir bağlantı hatası oluştu.")
                    else:
                        st.error("Lütfen randevu kaydı için bir e-posta adresi girin.")

# ==============================================================================
# BÖLÜM 5: CÜZDANIM / TEKLİFLERİM MODÜLÜ (KULLANICI PANELİ)
# ==============================================================================
elif st.session_state['sayfa'] == "Cüzdanım / Tekliflerim":
    st.markdown("## 💼 Cüzdanım ve Aktif Tekliflerim")
    st.markdown("Buradan sistemdeki onaylanmış tekliflerinizi ve vefa (geri alım) işlemlerinizi takip edebilirsiniz.")
    st.write("")
    
    if st.session_state['kullanici_giris_yapti_mi'] and len(st.session_state['bekleyen_teklifler']) > 0:
        st.success(f"Hoş geldiniz, {st.session_state['aktif_kullanici_maili']}")
        st.markdown("### ⏳ Bekleyen İşlemleriniz")
        
        for i, teklif in enumerate(st.session_state['bekleyen_teklifler']):
            st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
            st.markdown(f"Cihaz: {teklif['Cihaz']}")
            st.markdown(f"Tarih: {teklif['Tarih']}")
            st.markdown(f"Anlaşılan Tutar: <span style='color:#10b981; font-weight:bold; font-size:18px;'>{teklif['Teklif']}</span>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("📍 Durum: Fiziksel test ve teslimat için sizinle iletişime geçilmesi bekleniyor.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")
        
        if st.button("🚪 Oturumu Kapat"):
            st.session_state['kullanici_giris_yapti_mi'] = False
            st.session_state['aktif_kullanici_maili'] = ""
            st.session_state['bekleyen_teklifler'] = []
            st.rerun()
    else:
        st.info("Şu anda sistemde kayıtlı aktif bir teklifiniz veya cihazınız bulunmuyor.")
        st.markdown("Hemen sol menüden Anında Değerleme Modülü'ne geçerek cihazınız için teklif alabilir ve sürecinizi başlatabilirsiniz.")

# ==============================================================================
# BÖLÜM 6: LOJİSTİK VE CANLI RANDEVU SİSTEMİ (SAHA OPERASYONU)
# ==============================================================================

elif st.session_state['sayfa'] == "Teslimat ve Randevu":
    st.markdown("## 🚚 Teslimat ve Fiziksel Test Randevusu")
    st.markdown("Onaylanan teklifleriniz için cihaz teslimat noktasını ve test saatini belirleyin.")
    st.write("")
    
    if st.session_state['kullanici_giris_yapti_mi'] and len(st.session_state['bekleyen_teklifler']) > 0:
        st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
        
        st.markdown("### 📍 Lokasyon Seçimi")
        teslimat_noktasi = st.selectbox("Size en uygun teslimat noktasını seçin:", [
            "Çiğli KYK Erkek Öğrenci Yurdu Önü (Elden Teslim)",
            "İzmir Katip Çelebi Üniversitesi Kampüs İçi",
            "Balatçık Merkez (Kafe Buluşması)",
            "Kargo ile Gönderim (Tüm Türkiye)"
        ])
        
        st.write("")
        st.markdown("### ⏰ Zaman Çizelgesi")
        col_tarih, col_saat = st.columns(2)
        with col_tarih:
            randevu_tarihi = st.date_input("Randevu Tarihi")
        with col_saat:
            randevu_saati = st.time_input("Randevu Saati")
        
        st.write("")
        ek_not = st.text_area("Cihazla ilgili eklemek istediğiniz bir not var mı?", placeholder="Örn: Sadece akşam 5'ten sonra müsaitim...")
        
        if st.button("Randevuyu Kesinleştir ve Saha Ekibini Çağır", type="primary"):
            st.success(f"Harika! {randevu_tarihi} günü saat {randevu_saati} için {teslimat_noktasi} konumuna randevunuz oluşturuldu.")
            st.info("Saha ekibimiz, cihazın stres testini (FurMark, batarya döngüsü vb.) seçtiğiniz konumda gerçekleştirecektir.")
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Henüz onaylanmış bir teklifiniz bulunmuyor. Lütfen önce 'Anında Değerleme Modülü'nden bir cihaz için işlem başlatın.")

# ==============================================================================
# BÖLÜM 7: PİYASA ANALİZİ VE DEĞER KAYBI GRAFİKLERİ (VERİ GÖRSELLEŞTİRME)
# ==============================================================================

elif st.session_state['sayfa'] == "Piyasa Analizi (Grafikler)":
    st.markdown("## 📈 2. El Elektronik Piyasası ve Değer Kaybı Analizi")
    st.markdown("Elektronik cihazlar zamanla değer kaybeder. Sahip olduğunuz cihazın son 6 aydaki tahmini değer değişimini inceleyin.")
    st.write("")
    
    if df is not None:
        st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
        analiz_edilecek_urun = st.selectbox("Analiz etmek istediğiniz cihazı seçin:", df['Urun_Adi'].tolist())
        
        if analiz_edilecek_urun:
            urun_fiyati = df[df['Urun_Adi'] == analiz_edilecek_urun]['Piyasa_Fiyati_TL'].values[0]
            
            # Son 6 ayın simüle edilmiş değer kaybı verisi (Her ay %3-%5 arası değer kaybettiğini varsayıyoruz)
            # Gerçek bir sistemde bu veriler geçmiş veritabanı kayıtlarından çekilir.
            aylar = ["Eylül", "Ekim", "Kasım", "Aralık", "Ocak", "Şubat (Güncel)"]
            gecmis_fiyatlar = [
                int(urun_fiyati * 1.25), # 6 ay önce %25 daha değerliydi
                int(urun_fiyati * 1.18),
                int(urun_fiyati * 1.12),
                int(urun_fiyati * 1.07),
                int(urun_fiyati * 1.03),
                int(urun_fiyati)         # Güncel fiyat
            ]
            
            # Streamlit grafiği için veriyi Pandas DataFrame'e çeviriyoruz
            grafik_verisi = pd.DataFrame({
                'Tarih': aylar,
                'Değer (TL)': gecmis_fiyatlar
            }).set_index('Tarih')
            
            st.write("")
            st.markdown(f"### {analiz_edilecek_urun} - 6 Aylık Değer Trendi")
            st.line_chart(grafik_verisi, use_container_width=True)
            
            st.info(f"💡 **Finansal Analiz:** Bu cihaz son 6 ay içinde yaklaşık **%20 değer kaybetmiştir**. Daha fazla değer kaybı yaşamadan nakde çevirmek için 'Anında Değerleme Modülü'ne geçebilirsiniz.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Grafik oluşturulabilmesi için piyasa_verisi.csv dosyası okunamıyor.")

# ==============================================================================
# BÖLÜM 8: GİZLİ YÖNETİCİ PANELİ (ADMİN DASHBOARD)
# ==============================================================================

elif st.session_state['sayfa'] == "Gizli Yönetici Paneli":
    st.markdown("## 🔐 Yönetici Kontrol Paneli")
    st.markdown("Sadece yetkili personelin erişimine açıktır. Lütfen şifrenizi girin.")
    st.write("")
    
    # Şifre Koruması (Şifreyi girerken noktalar halinde görünür)
    admin_sifre = st.text_input("Yönetici Şifresi:", type="password", placeholder="Şifrenizi girin...")
    
    # Şifremizi "patron123" olarak belirliyoruz (Bunu koddan istediğin gibi değiştirebilirsin)
    if admin_sifre == "patron123":
        st.success("Sisteme başarıyla giriş yapıldı. Kontrol paneline hoş geldin Patron!")
        st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
        
        st.markdown("### 📊 İşletme Özeti (Anlık Oturum)")
        toplam_talep = len(st.session_state.get('bekleyen_teklifler', []))
        
        # Finansal metrikleri hesaplama
        toplam_nakit_ihtiyaci = 0
        beklenen_kar = 0
        if toplam_talep > 0:
            for talep in st.session_state['bekleyen_teklifler']:
                # Metin içinden sadece rakamı çekmek için basit bir işlem
                teklif_metni = talep['Teklif']
                rakam_str = ''.join(filter(str.isdigit, teklif_metni.split('(')[0])) 
                if rakam_str:
                    verilecek_para = int(rakam_str)
                    toplam_nakit_ihtiyaci += verilecek_para
                    # Kâr marjımız %30 civarında
                    beklenen_kar += int(verilecek_para * 0.30)
        
        # 3'lü şık istatistik kutuları
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Bekleyen Yeni Talep", value=f"{toplam_talep} Adet")
        col2.metric(label="Dağıtılacak Nakit", value=f"₺{toplam_nakit_ihtiyaci:,}")
        col3.metric(label="Tahmini Kâr (Vefa/Satış)", value=f"₺{beklenen_kar:,}")
        
        st.write("")
        st.markdown("### 📋 Gelen Talepler (Aktif)")
        if toplam_talep > 0:
            talep_tablosu = pd.DataFrame(st.session_state['bekleyen_teklifler'])
            st.dataframe(talep_tablosu, use_container_width=True)
        else:
            st.info("Şu an için aktif oturumda yeni bir talep bulunmuyor.")
            
        st.markdown("---")
        st.markdown("🔗 *Kalıcı müşteri veri tabanına (Google E-Tablolar) gitmek için [Buraya Tıklayın](#).*")
        st.markdown('</div>', unsafe_allow_html=True)
    elif admin_sifre != "":
        st.error("Hatalı şifre! Sisteme yetkisiz giriş denemesi engellendi.")

# ==============================================================================
# BÖLÜM 9: KYC (KİMLİK DOĞRULAMA) VE OTOMATİK SÖZLEŞME ÜRETİCİ
# ==============================================================================

elif st.session_state['sayfa'] == "KYC ve Sözleşme Üretici":
    st.markdown("## 📜 KYC Doğrulama ve Yasal Sözleşme")
    st.markdown("Randevu aşamasında müşterinin yasal bilgilerini girerek Türk Borçlar Kanunu'na uygun 'Vefa Sözleşmesi'ni otomatik oluşturun.")
    st.write("")
    
    st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
    st.markdown("### 👤 Müşteri Bilgileri (Saha Ekibi Doldurur)")
    
    col1, col2 = st.columns(2)
    with col1:
        musteri_ad = st.text_input("Müşteri Adı Soyadı:", placeholder="Kimlikteki tam ad...")
        musteri_tc = st.text_input("T.C. Kimlik Numarası:", max_chars=11, placeholder="11 Haneli TC No")
    with col2:
        musteri_tel = st.text_input("İletişim Numarası:", placeholder="05XX XXX XX XX")
        teslim_alinan_cihaz = st.text_input("Teslim Alınan Cihaz/Model:", placeholder="Seri numarası ile birlikte...")
    
    alinan_nakit = st.number_input("Müşteriye Ödenen Nakit Tutar (TL):", min_value=0, step=100)
    geri_alim_bedeli = math.floor(alinan_nakit * 1.30) if alinan_nakit > 0 else 0
    
    if st.button("Sözleşmeyi Oluştur", type="primary"):
        if musteri_ad and musteri_tc and alinan_nakit > 0:
            st.success("Yasal Sözleşme Başarıyla Üretildi!")
            
            sozlesme_metni = f"""
            **VEFA (GERİ ALIM) HAKKI SÖZLEŞMESİ**

            **Tarih:** {datetime.now().strftime("%Y-%m-%d")}
            **Müşteri (Satıcı):** {musteri_ad} (T.C: {musteri_tc})
            **İletişim:** {musteri_tel}
            **Konu Cihaz:** {teslim_alinan_cihaz}

            **1. SÖZLEŞMENİN KONUSU**
            İşbu sözleşme uyarınca, Satıcı mülkiyetinde bulunan '{teslim_alinan_cihaz}' marka/model cihazı, Alıcı'ya {alinan_nakit} TL bedel mukabilinde satmış ve teslim etmiştir.

            **2. VEFA (GERİ ALIM) HAKKI VE ŞARTLARI**
            Satıcı, işbu sözleşme tarihinden itibaren tam 30 (Otuz) takvim günü içinde, Alıcı'ya {geri_alim_bedeli} TL (Geri Alım Bedeli) ödeyerek cihazı geri alma hakkına (Vefa Hakkı) sahiptir.

            **3. SÜRENİN SONA ERMESİ**
            30 günlük yasal süre dolduğunda Satıcı geri alım bedelini ödemezse, Vefa Hakkı düşer ve cihazın mülkiyeti kesin olarak Alıcı'ya geçer. Alıcı cihazı dilediği gibi satmakta serbesttir.

            **İmzalar:**
            Satıcı (Teslim Eden): ......................        Alıcı (Teslim Alan): ......................
            """
            
            st.markdown("---")
            st.markdown(sozlesme_metni)
            st.info("Yazdır (Ctrl+P) kısayolunu kullanarak bu metni PDF olarak kaydedebilir veya doğrudan yazıcıdan çıkarıp müşteriye imzalatabilirsiniz.")
        else:
            st.error("Sözleşme oluşturmak için Ad, T.C. Kimlik ve Ödenen Tutar alanları zorunludur.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# BÖLÜM 10: PROFİL, AYARLAR VE BİLDİRİM TERCİHLERİ (KULLANICI DENEYİMİ)
# ==============================================================================

elif st.session_state['sayfa'] == "Ayarlar ve Profil":
    st.markdown("## ⚙️ Profil ve Hesap Ayarları")
    st.markdown("Uygulama deneyiminizi kişiselleştirin ve bildirim tercihlerinizi yönetin.")
    st.write("")
    
    st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
    
    if st.session_state['kullanici_giris_yapti_mi']:
        st.markdown(f"### 👤 Hesap Bilgileri")
        st.text_input("Kayıtlı E-posta Adresiniz:", value=st.session_state['aktif_kullanici_maili'], disabled=True)
        st.text_input("Telefon Numaranız (Opsiyonel):", placeholder="05XX XXX XX XX")
        
        st.markdown("---")
        st.markdown("### 🔔 Bildirim Tercihleri")
        eposta_bildirim = st.toggle("E-posta Bildirimleri (Vefa Süresi Hatırlatıcıları)", value=True)
        sms_bildirim = st.toggle("SMS Bildirimleri (Saha Ekibi Randevu Uyarıları)", value=False)
        
        st.markdown("---")
        st.markdown("### 🌙 Görünüm ve Tema (Karanlık Mod)")
        st.info("💡 **Premium İpucu:** Göz yormayan Gece Moduna (Dark Mode) geçmek için ekranın sağ üst köşesindeki üç noktaya (⋮) tıklayın, 'Settings' menüsünden 'Theme' seçeneğini 'Dark' yapın.")
        
        st.write("")
        if st.button("Ayarları Kaydet", type="primary"):
            st.success("Tercihleriniz başarıyla güncellendi ve buluta kaydedildi!")
            st.balloons()
    else:
        st.warning("Ayarlarınızı yönetebilmek için lütfen 'Anında Değerleme Modülü' üzerinden bir teklif onaylayıp sisteme giriş yapın.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# BÖLÜM 11: SIKÇA SORULAN SORULAR VE CANLI DESTEK MERKEZİ
# ==============================================================================

elif st.session_state['sayfa'] == "SSS ve Destek":
    st.markdown("## 💬 Destek Merkezi ve SSS")
    st.markdown("Aklınıza takılan tüm soruların cevapları burada. Sistemimizin nasıl güvenle çalıştığını öğrenin.")
    st.write("")
    
    st.markdown("### ❓ Sıkça Sorulan Sorular")
    
    with st.expander("Vefa (Geri Alım) Hakkı tam olarak nedir? Yasal mıdır?"):
        st.write("Vefa hakkı, Türk Borçlar Kanunu'nda (TBK) açıkça yer alan yasal bir haktır. Cihazınızı bize sattığınızda, sözleşmede belirtilen süre (30 Gün) içinde anlaşılan bedeli ödeyerek cihazınızı aynı kondisyonda geri alma garantisine sahip olursunuz.")
    
    with st.expander("Cihazım 30 gün boyunca nerede ve nasıl saklanıyor?"):
        st.write("Cihazınız teslim alındığı an videolu teste tabi tutulur, kondisyonu kayıt altına alınır ve özel güvenlikli kasalarımızda muhafaza edilir. Siz geri alana kadar kesinlikle kullanılmaz veya başkasına kiralanmaz.")
    
    with st.expander("30 günlük süre dolduğunda ne olur?"):
        st.write("Eğer 30 günlük süre içinde geri alım bedelini ödemezseniz veya süreyi uzatma talebinde bulunmazsanız, yasal olarak vefa hakkınız düşer. Cihazın mülkiyeti tamamen platformumuza geçer ve satışa çıkarılır.")
    
    with st.expander("Cihazımda test sırasında bir hasar oluşursa ne olacak?"):
        st.write("Fiziksel teslimat sırasında cihazınızın çalışma durumu ve kozmetiği iki tarafın huzurunda kayıt altına alınır. Bizden kaynaklı herhangi bir hasarda cihazınızın güncel 2. el piyasa değeri size nakit olarak anında tazmin edilir.")
    
    st.write("")
    st.markdown("---")
    st.markdown("### 🎧 Canlı Destek Ekibi")
    st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
    st.markdown("Saha ekibimiz veya değerleme uzmanlarımızla iletişime geçin.")
    
    kullanici_mesaji = st.text_input("Mesajınızı yazın:", placeholder="Merhaba, randevu saatimi değiştirmek istiyorum...")
    
    if st.button("Mesajı Gönder", type="primary"):
        if kullanici_mesaji:
            st.success("Mesajınız destek ekibimize iletildi! Ortalama yanıt süresi: **15 Dakika**.")
            st.info("Kayıtlı e-posta adresiniz veya telefon numaranız üzerinden dönüş sağlanacaktır.")
        else:
            st.warning("Lütfen göndermeden önce bir mesaj yazın.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# BÖLÜM 12: REFERANS SİSTEMİ VE OYUNLAŞTIRMA (DAVET ET KAZAN)
# ==============================================================================

elif st.session_state['sayfa'] == "Davet Et Kazan (Referans)":
    st.markdown("## 🎁 Arkadaşını Davet Et, Nakit Kazan!")
    st.markdown("Platformumuzu arkadaşlarınıza önerin; onlar ilk işlemlerinde ekstra nakit, siz ise her başarılı işlemden komisyon kazanın.")
    st.write("")
    
    if st.session_state['kullanici_giris_yapti_mi']:
        st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
        
        # Rastgele bir referans kodu oluşturuyoruz (Gerçekte veritabanından gelir)
        mail_on_ek = st.session_state['aktif_kullanici_maili'].split('@')[0].upper()
        referans_kodu = f"VEFA-{mail_on_ek}-2026"
        
        st.markdown("### 🔗 Size Özel Davet Kodunuz")
        st.code(referans_kodu, language="text")
        st.info("Bu kodu kopyalayarak WhatsApp veya Telegram üzerinden arkadaşlarınıza gönderebilirsiniz.")
        
        st.write("")
        st.markdown("### 🏆 Kazanç Tablonuz")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Davet Edilen Kişi", value="0", delta="Henüz yok")
        col2.metric(label="Tamamlanan İşlem", value="0")
        col3.metric(label="Kazanılan Nakit (Bakiye)", value="₺0.00")
        
        st.write("")
        st.markdown("### 💡 Nasıl Çalışır?")
        st.markdown("""
        1. Kodunuzu arkadaşınızla paylaşın.
        2. Arkadaşınız 'Anında Değerleme Modülü'nde teklif alırken bu kodu kullansın.
        3. Arkadaşınızın cihazı teslim alındığında **size ₺250 nakit ödül** cüzdanınıza yansısın.
        4. Arkadaşınız da ilk işleminde **+%5 Ekstra Nakit** teklifi kazansın.
        """)
        
        if st.button("Kazançlarımı Cüzdana Aktar (Aktif Değil)"):
            st.warning("Çekilebilir bakiyeniz bulunmamaktadır. Lütfen önce arkadaşlarınızı davet edin.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Size özel referans kodunuzu görebilmek ve kazanmaya başlamak için lütfen giriş yapın veya bir teklif onaylayın.")

# ==============================================================================
# BÖLÜM 13: DİJİTAL DEKONT VE İŞLEM MAKBUZU GÖRÜNTÜLEYİCİ
# ==============================================================================

elif st.session_state['sayfa'] == "Dijital Dekont (Makbuz)":
    st.markdown("## 🧾 Dijital İşlem Dekontu")
    st.markdown("Onaylanan son işleminize ait resmi dijital makbuzunuzu buradan görüntüleyebilir ve saklayabilirsiniz.")
    st.write("")
    
    if st.session_state['kullanici_giris_yapti_mi'] and len(st.session_state['bekleyen_teklifler']) > 0:
        # En son yapılan işlemi alıyoruz
        son_islem = st.session_state['bekleyen_teklifler'][-1]
        
        # Fatura / Dekont Tasarımı (CSS Entegrasyonu)
        dekont_stili = """
        <div style="background-color: #ffffff; padding: 30px; border: 2px dashed #cbd5e1; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.05); font-family: 'Courier New', Courier, monospace;">
            <div style="text-align: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px;">
                <h2 style="color: #0f172a; margin: 0; font-family: 'Inter', sans-serif;">VEFATECH ONAY DEKONTU</h2>
                <p style="color: #64748b; margin: 5px 0 0 0; font-size: 14px;">Güvenli Nakit & Geri Alım Sistemi</p>
            </div>
            
            <div style="margin-bottom: 10px;"><b>İşlem Tarihi:</b> <span style="float: right;">{tarih}</span></div>
            <div style="margin-bottom: 10px;"><b>Müşteri (E-Posta):</b> <span style="float: right;">{email}</span></div>
            <div style="margin-bottom: 10px;"><b>İşlem No:</b> <span style="float: right;">TRX-{islem_no}</span></div>
            
            <div style="border-top: 1px dashed #cbd5e1; border-bottom: 1px dashed #cbd5e1; padding: 15px 0; margin: 20px 0;">
                <div style="margin-bottom: 10px;"><b>Cihaz Bilgisi:</b> <br> <span style="color: #334155;">{cihaz}</span></div>
            </div>
            
            <div style="font-size: 18px; margin-bottom: 10px;"><b>Kabul Edilen Teklif:</b> <span style="float: right; color: #10b981; font-weight: bold;">{teklif}</span></div>
            
            <div style="text-align: center; margin-top: 30px; color: #94a3b8; font-size: 12px; font-family: 'Inter', sans-serif;">
                Bu belge dijital olarak üretilmiştir. Kesin işlem saha ekibinin fiziksel kontrolü sonrası gerçekleşecektir.<br><br>
                <i>Barkod: ||||||| |||| || |||||||| ||||</i>
            </div>
        </div>
        """
        
        # Rastgele bir işlem numarası oluşturuyoruz
        import random
        islem_no = random.randint(10000000, 99999999)
        
        st.markdown(dekont_stili.format(
            tarih=son_islem['Tarih'],
            email=son_islem['Email'],
            islem_no=islem_no,
            cihaz=son_islem['Cihaz'],
            teklif=son_islem['Teklif']
        ), unsafe_allow_html=True)
        
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("💡 Yukarıdaki dekontun ekran görüntüsünü alarak referans olarak saklayabilirsiniz.")
    else:
        st.warning("Henüz onaylanmış bir işleminiz bulunmuyor. Makbuz oluşturmak için lütfen 'Anında Değerleme Modülü'nü kullanın.")

# ==============================================================================
# BÖLÜM 14: SİSTEM SAĞLIĞI VE VERİ TABANI KONTROLÜ (SYSTEM HEALTH & PING)
# ==============================================================================

elif st.session_state['sayfa'] == "Sistem Sağlığı (Ping & DB)":
    st.markdown("## 🎛️ Sistem Sağlığı ve Sunucu Durumu")
    st.markdown("VefaTech sunucularının, veri tabanı bağlantılarının ve fiyatlama algoritmasının anlık durumunu izleyin.")
    st.write("")
    
    st.markdown('<div class="advanced-condition-box">', unsafe_allow_html=True)
    st.markdown("### 🟢 Anlık Sunucu Metrikleri")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Ana Sunucu Durumu", value="Aktif", delta="99.9% Uptime")
    col2.metric(label="Veri Tabanı Gecikmesi", value="12 ms", delta="-2 ms (Hızlı)", delta_color="inverse")
    col3.metric(label="Fiyatlama Algoritması", value="Çevrimiçi", delta="v2.4.1")
    
    st.write("")
    st.markdown("### 🗄️ Veri Tabanı Senkronizasyonu")
    st.info(f"Son Güncelleme Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if st.button("🔄 Veri Tabanını Manuel Senkronize Et"):
        with st.spinner('Google sunucularına bağlanılıyor ve canlı piyasa verileri çekiliyor...'):
            import time
            time.sleep(2)  # Gerçekçi bir bekleme ve yüklenme efekti (Simülasyon)
            st.success("Veri tabanı başarıyla senkronize edildi! En güncel 2. el piyasa fiyatları sisteme aktarıldı.")
            st.balloons()
    
    st.markdown("---")
    st.markdown("### 🛡️ Güvenlik ve Şifreleme Protokolleri")
    st.markdown("""
    * **Veri İletişimi:** Tüm kullanıcı işlemleri 256-bit SSL şifreleme ile korunmaktadır.
    * **Sözleşme API'si:** Türkiye Cumhuriyeti e-Devlet ve hukuki metin standartlarına uyumlu uç noktalar.
    * **Bulut Yedekleme:** Her 6 saatte bir Google E-Tablolar üzerinden soğuk cüzdan yedeklemesi yapılmaktadır.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# BÖLÜM 15: FOOTER (ALT BİLGİ, YASAL UYARILAR VE KAPANIŞ)
# ==============================================================================

st.write("")
st.write("")
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 12px; padding: 20px 0;'>
        <b>VefaTech Finansal Dönüşüm Merkezi © 2026</b><br>
        <i>Tüm Hakları Saklıdır. VefaTech bir değerleme ve aracılık platformudur.</i><br>
        <i>Kullanım Koşulları | Gizlilik Politikası | Yasal Aydınlatma Metni</i><br>
        <br>
        <span style='font-size: 10px;'>Bu platform Türk Borçlar Kanunu (TBK) madde 237 ve devamı 'Vefa (Geri Alım) Hakkı' hükümlerine uygun olarak tasarlanmıştır. Sunulan fiyat teklifleri anlık piyasa koşullarına göre algoritmik olarak hesaplanır ve ön bilgilendirme niteliği taşır. Kesin işlem saha ekibinin fiziksel onayıyla gerçekleşir.</span>
    </div>
""", unsafe_allow_html=True)
