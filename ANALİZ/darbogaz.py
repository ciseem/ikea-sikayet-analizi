import pandas as pd

# Dosya ismini kontrol et
DOSYA_ADI = "IKEA_FINAL_PIRIL_PIRIL.csv"

def ultra_darbogaz_analizi():
    try:
        print("Dosya okunuyor ve departmanlar derinlemesine taranıyor...")
        df = pd.read_csv(DOSYA_ADI)
        
        # --- GENİŞLETİLMİŞ DEPARTMAN SÖZLÜĞÜ (Ultra Detaylı) ---
        
        # 1. ÇAĞRI MERKEZİ & İLETİŞİM (Müşterinin ulaşamadığı anlar)
        cagri_merkezi = [
            'çağrı merkezi', 'telefon', 'ulaşamadım', 'bağlanmıyor', 'açmıyor', 
            'muhatap', 'müşteri hizmetleri', 'telefona', 'hat düşmüyor', 
            'bekletiyor', 'sırada', 'dakikadır', 'cevap vermiyor', 'iletişim', 
            'ulaşmak imkansız', 'telesekreter', 'operatör', 'yüzüme kapattı', 
            'bağlanmak', 'aradığımda', 'açan yok', 'numara', 'canlı destek',
            'bot', 'robot', 'tuşlama'
        ]
        
        # 2. TEKNİK SERVİS & MONTAJ (Eve gelen ekip)
        teknik_servis = [
            'montaj', 'kurulum', 'usta', 'servis', 'kurmamış', 'parça arttı', 
            'vidalamadı', 'ekip', 'kurmaya gelmedi', 'randevu', 'tarih verdi', 
            'gelmediler', 'saatinde', 'gün verdi', 'kurulum ekibi', 'yamuk kurdu', 
            'sallanıyor', 'işçilik', 'montaj hizmeti', 'teknik ekip', 'ekspertiz'
        ]
        
        # 3. LOJİSTİK & NAKLİYE (Taşıma süreci)
        lojistik = [
            'nakliye', 'kargo', 'teslimat', 'horoz', 'lojistik', 'getirmedi', 
            'yukarı çıkarmadı', 'taşıma', 'kargom', 'gelmedi', 'teslim edilmedi',
            'dağıtım', 'kata', 'asansör', 'apartman', 'bina önüne', 'kapıya',
            'teslimat tarihi', 'kurye', 'sevkiyat', 'adres', 'geç geldi', 
            'kargo şirketi', 'takip no', 'kargoda'
        ]
        
        # 4. MAĞAZA İÇİ PERSONEL (Fiziksel temas)
        magaza = [
            'personel', 'kasiyer', 'reyon', 'güvenlik', 'mağaza müdürü', 
            'çalışan', 'suratsız', 'ilgisiz', 'mağazada', 'şubesi', 'şube',
            'kasada', 'sıra', 'danışma', 'iade bankosu', 'değişim', 
            'reyon görevlisi', 'satış danışmanı', 'tavır', 'üslup', 'bağırdı',
            'kovdu', 'yardımcı olmadı'
        ]

        def departman_bul(yorum):
            yorum = str(yorum).lower()
            
            # Tarama Sırası Önemli: En spesifikten genele
            if any(k in yorum for k in cagri_merkezi):
                return "Çağrı Merkezi / İletişim"
            elif any(k in yorum for k in teknik_servis):
                return "Teknik Servis / Montaj"
            elif any(k in yorum for k in lojistik):
                return "Lojistik / Nakliye"
            elif any(k in yorum for k in magaza):
                return "Mağaza İçi Personel"
            else:
                return "Diğer"

        df['DEPARTMAN'] = df['temiz_sikayet'].apply(departman_bul)
        
        # 'Diğer' kategorisini çıkarıp asıl suçluları yarıştıralım
        suclu_df = df[df['DEPARTMAN'] != 'Diğer']
        
        darbogazlar = suclu_df['DEPARTMAN'].value_counts()
        yuzdeler = suclu_df['DEPARTMAN'].value_counts(normalize=True) * 100
        
        print("\n" + "="*60)
        print("📊 ULTRA DETAYLI DARBOĞAZ SONUÇLARI (2. SORU)")
        print("="*60)
        print(darbogazlar)
        print("\n--- Suç Payı (%) ---")
        print(yuzdeler)
        print("="*60)
        
        # Kaydet
        df.to_csv("IKEA_ANALIZ_2_DARBOGAZ.csv", index=False)
        print("\n✅ Dosya kaydedildi: IKEA_ANALIZ_2_DARBOGAZ.csv")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    ultra_darbogaz_analizi()