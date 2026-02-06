import pandas as pd

# Dosya adını kontrol et
DOSYA_ADI = "IKEA_FINAL_PIRIL_PIRIL.csv"

def churn_risk_analizi_pro():
    try:
        print("Dosya okunuyor ve DEVAS kelime havuzu ile taranıyor...")
        df = pd.read_csv(DOSYA_ADI)
        
        # Küçük harfe çevir ki kaçırmayalım
        df['temiz_sikayet'] = df['temiz_sikayet'].astype(str).str.lower()
        
        # --- ULTRA GENİŞLETİLMİŞ RİSK SÖZLÜĞÜ ---
        
        # 1. CHURN (KAYIP) SİNYALLERİ (Müşteri gidiyor / Vazgeçiyor)
        churn_kelimeler = [
            'asla', 'bir daha', 'tövbe', 'iptal', 'iade et', 'haram', 'bitti', 
            'kapattım', 'sildim', 'lanet', 'bulaşmayın', 'pişmanlık', 'rezil',
            'birdaha', 'asla almam', 'alışveriş yapmam', 'bitmiştir', 'son olsun',
            'üyelik', 'hesabımı', 'sileceğim', 'koçtaş', 'vivense', 'tekzen', # Rakiplere gitme tehdidi
            'başka marka', 'tercih etmeyeceğim', 'yolumu ayırıyorum', 'kaybettiniz', 
            'müşteri kaybettiniz', 'önünden geçmem', 'tavsiye etmem', 'uzak durun',
            'paramı verin', 'paramı iade', 'vazgeçtim', 'çöpe attım'
        ]
        
        # 2. YASAL RİSK (Devlet / Mahkeme / CİMER tehdidi)
        yasal_kelimeler = [
            'mahkeme', 'dava', 'hakem heyeti', 'tüketici hakları', 'cimer', 
            'avukat', 'savcılık', 'yasal', 'şikayet edeceğim', 'thh', 'heyet',
            'maliye', 'fatura kesmedi', 'haklarımı', 'mahkemeye', 'icra', 
            'tazminat', 'hukuki', 'resmi', 'bakanlık', 'ticaret bakanlığı', 
            'suç duyurusu', 'kanuni', 'usulsüzlük', 'vergi dairesi'
        ]
        
        # 3. TOKSİK / AĞIR TEPKİ (Marka İtibarını Zedeleyenler)
        toksik_kelimeler = [
            'rezillik', 'rezalet', 'dolandırıcı', 'sahtekar', 'yazıklar olsun', 
            'terbiyesiz', 'ahlaksız', 'kandırıldık', 'utanmaz', 'soygun', 
            'hırsız', 'dalga geçiyor', 'oyalıyor', 'yalan', 'yalancı', 
            'zehir', 'zıkkım', 'burnumdan', 'lanet olsun', 'allah belanı', 
            'çöp', 'berbat', 'iğrenç', 'saygısızlık', 'kepazelik', 'fiyasko',
            'mağdur', 'mağduriyet', 'dalga geçer gibi', 'insanları kandırıyorlar'
        ]

        # Sayımları Yap (Her bir satırı kontrol et)
        churn_sayisi = df[df['temiz_sikayet'].str.contains('|'.join(churn_kelimeler), na=False)].shape[0]
        yasal_sayisi = df[df['temiz_sikayet'].str.contains('|'.join(yasal_kelimeler), na=False)].shape[0]
        toksik_sayisi = df[df['temiz_sikayet'].str.contains('|'.join(toksik_kelimeler), na=False)].shape[0]
        
        toplam_sikayet = len(df)
        
        print("\n" + "="*60)
        print("🔥 BÖLÜM 4: KRİZ VE CHURN ANALİZİ SONUÇLARI (ULTRA)")
        print("="*60)
        print(f"Toplam Veri: {toplam_sikayet}")
        print("-" * 30)
        print(f"🔴 Kritik Churn (Kaybedilen Müşteri) : {churn_sayisi} (%{churn_sayisi/toplam_sikayet*100:.1f})")
        print(f"⚖️ Yasal Risk (Dava Tehdidi)         : {yasal_sayisi} (%{yasal_sayisi/toplam_sikayet*100:.1f})")
        print(f"⚠️ Toksik/Ağır Tepki (İtibar Riski)  : {toksik_sayisi} (%{toksik_sayisi/toplam_sikayet*100:.1f})")
        print("="*60)
        
        # İstersen bu riskli müşterileri ayrı bir dosyaya kaydet (İncelemek için)
        df['RİSK_DURUMU'] = 'Normal'
        df.loc[df['temiz_sikayet'].str.contains('|'.join(churn_kelimeler), na=False), 'RİSK_DURUMU'] = 'Churn Riski'
        df.loc[df['temiz_sikayet'].str.contains('|'.join(yasal_kelimeler), na=False), 'RİSK_DURUMU'] = 'Yasal Risk'
        
        df.to_csv("IKEA_ANALIZ_3_RISKLI_MUSTERILER.csv", index=False)
        print("✅ Riskli müşteriler 'IKEA_ANALIZ_3_RISKLI_MUSTERILER.csv' olarak kaydedildi.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    churn_risk_analizi_pro()