import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Dosya adını kontrol et
DOSYA_ADI = "IKEA_FINAL_PIRIL_PIRIL.csv"

def yapay_zeka_dogrulama():
    try:
        print("Yapay Zeka (LDA) modeli çalışıyor... Sonuçlar önceki analizi doğrulayacak.")
        df = pd.read_csv(DOSYA_ADI)
        df = df.dropna(subset=['temiz_sikayet'])

        # --- GÜÇLÜ TEMİZLİK (Gereksiz kelimeler eleniyor) ---
        stop_words = [
            'bir', 've', 'bu', 'ile', 'için', 'ama', 'fakat', 'lakin', 'de', 'da', 
            'ki', 'mi', 'mu', 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'diye', 
            'gibi', 'kadar', 'olarak', 'sonra', 'daha', 'en', 'çok', 'bile', 
            'ise', 'yani', 'çünkü', 'veya', 'ya', 'hem', 'ne', 'her', 'hiç',
            'şekilde', 'zaten', 'hala', 'yine', 'sadece', 'böyle', 'öyle',
            'ikea', 'ürün', 'dedi', 'kendi', 'bile', 'artık', 'olan', 'bana',
            'bunu', 'beni', 'bize', 'sizin', 'falan', 'filan', 'tarafından',
            'var', 'yok', 'bir', 'iki', 'üç', 'gün', 'saat', 'tl', 'kuruş',
            'merhaba', 'iyi', 'günler', 'rica', 'ederim', 'lütfen', 'tşk', 'teşekkürler'
        ]

        # Metni sayılara dök
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words=stop_words, max_features=1000)
        tf = tf_vectorizer.fit_transform(df['temiz_sikayet'].astype(str))

        # LDA Modelini Kur (4 Ana Konu Başlığı Yeterli)
        lda = LatentDirichletAllocation(n_components=4, max_iter=10, learning_method='online', random_state=42)
        lda.fit(tf)

        print("\n" + "="*70)
        print("🤖 YAPAY ZEKA DOĞRULAMA SONUÇLARI (RAPORUN EN SONUNA EKLENECEK)")
        print("="*70)

        feature_names = tf_vectorizer.get_feature_names_out()
        
        # Her konunun en baskın 6 kelimesini yazdır
        for topic_idx, topic in enumerate(lda.components_):
            message = " ".join([feature_names[i] for i in topic.argsort()[:-7:-1]])
            print(f"🔹 KÜME #{topic_idx + 1}: {message}")

        print("="*70)

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    yapay_zeka_dogrulama()