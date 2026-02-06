import pandas as pd

# Dosya adının doğruluğundan emin ol
DOSYA_ADI = "IKEA_FINAL_PIRIL_PIRIL.csv"

def ultra_detayli_analiz():
    try:
        print("Dosya okunuyor ve dev kelime havuzu hazırlanıyor...")
        df = pd.read_csv(DOSYA_ADI)
        
        # --- GENİŞLETİLMİŞ KELİME HAVUZU (LEXICON) ---
        
        # 1. FABRİKA / ÜRETİM / KALİTE (Ürün odaklı sorunlar)
        fabrika_kelimeleri = [
            'kırık', 'çizik', 'eksik parça', 'vida', 'monte', 'kurulum şeması', 
            'hatalı üretim', 'kalitesiz', 'soyuldu', 'vida yeri', 'sunta', 
            'kaplama', 'kabarma', 'yamuk', 'dengesiz', 'delik', 'boya', 
            'deforme', 'çatlak', 'koku', 'vidalar', 'alyan', 'defolu', 
            'üretim hatası', 'paket içeriği', 'civata', 'somun', 'işçilik', 
            'profil', 'sallanıyor', 'kapanmıyor', 'çekmece rayı', 'kulp'
        ]
        
        # 2. HİZMET / BAYİ / PERSONEL (İnsan ve Süreç odaklı sorunlar)
        bayi_hizmet_kelimeleri = [
            'personel', 'suratsız', 'ilgisiz', 'kasiyer', 'mağaza', 'güvenlik', 
            'saygısız', 'yardımcı olmadı', 'muhatap', 'telefon', 'ulaşamadım', 
            'çalışanlar', 'tavır', 'üslup', 'azarladı', 'bağırdı', 'ilgisizlik', 
            'müşteri temsilcisi', 'danışma', 'iade süreci', 'reyon görevlisi', 
            'kasada', 'sıra', 'bekletildim', 'sistem yok', 'iade almıyor', 
            'değişim yapmıyor', 'mağaza müdürü', 'yetkili', 'kurumsal değil'
        ]
        
        # 3. LOJİSTİK / NAKLİYE (Taşıma odaklı sorunlar)
        lojistik_kelimeleri = [
            'kargo', 'teslimat', 'nakliye', 'getirmedi', 'gecikti', 'horoz', 
            'lojistik', 'tarihinde', 'kargom', 'dağıtım', 'kata çıkarma', 
            'asansör', 'koli', 'paket', 'ezik', 'yırtık', 'geç geldi', 
            'randevu', 'sevkiyat', 'teslim edilmedi', 'kurye', 'adres', 
            'taşıma', 'kargoda', 'hasarlı teslimat', 'apartman girişi'
        ]

        def etiketle(yorum):
            yorum = str(yorum).lower()
            
            # Öncelik sırasına göre tarama
            if any(kelime in yorum for kelime in fabrika_kelimeleri):
                return "Üretim / Fabrika"
            elif any(kelime in yorum for kelime in bayi_hizmet_kelimeleri):
                return "Hizmet / Bayi"
            elif any(kelime in yorum for kelime in lojistik_kelimeleri):
                return "Lojistik / Dağıtım"
            else:
                return "Diğer / Belirsiz"

        print("14.000 satır tek tek ultra detaylı taranıyor...")
        df['KOK_NEDEN'] = df['temiz_sikayet'].apply(etiketle)
        
        # Sonuçları Hesapla
        sonuclar = df['KOK_NEDEN'].value_counts()
        yuzdeler = df['KOK_NEDEN'].value_counts(normalize=True) * 100
        
        print("\n" + "="*50)
        print("SONUÇLAR (ULTRA DETAYLI ANALİZ)")
        print("="*50)
        print(sonuclar)
        print("\n--- Yüzdeler ---")
        print(yuzdeler)
        print("="*50)

        # Sonuç dosyasını kaydet
        df.to_csv("IKEA_ANALIZ_ULTRA.csv", index=False)
        print("\n✅ Dosya kaydedildi: IKEA_ANALIZ_ULTRA.csv")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    ultra_detayli_analiz()