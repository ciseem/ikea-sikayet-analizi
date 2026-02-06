import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer

# Dosya adını kontrol et
DOSYA_ADI = "IKEA_FINAL_PIRIL_PIRIL.csv"

def bigram_analizi_yap():
    try:
        print("Veri okunuyor ve ikili kelime grupları (Bigrams) analiz ediliyor...")
        df = pd.read_csv(DOSYA_ADI)
        
        # NaN verileri temizle
        df = df.dropna(subset=['temiz_sikayet'])
        
        # --- DURDURMA KELİMELERİ (Bunların ikili olmasını istemiyoruz) ---
        stop_words = [
            'bir', 've', 'bu', 'ile', 'için', 'ama', 'fakat', 'lakin', 'de', 'da', 
            'ki', 'mi', 'mu', 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'diye', 
            'gibi', 'kadar', 'olarak', 'sonra', 'daha', 'en', 'çok', 'bile', 
            'ise', 'yani', 'çünkü', 'veya', 'ya', 'hem', 'ne', 'her', 'hiç',
            'şekilde', 'zaten', 'hala', 'yine', 'sadece', 'böyle', 'öyle',
            'ikea', 'ürün', 'dedi', 'kendi', 'bile', 'artık', 'olan', 'bana',
            'bunu', 'beni', 'bize', 'sizin', 'falan', 'filan', 'tarafından'
        ]

        # Bigram (İkili Kelime) Oluşturucu
        # ngram_range=(2, 2) -> Sadece ikili gruplar
        vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words=stop_words, max_features=20)
        
        # Metni sayılara dök
        X = vectorizer.fit_transform(df['temiz_sikayet'].astype(str))
        
        # Toplamları al
        bigram_counts = X.toarray().sum(axis=0)
        vocab = vectorizer.get_feature_names_out()
        
        # Veri Çerçevesi yap
        bigram_df = pd.DataFrame({'Bigram': vocab, 'Frekans': bigram_counts})
        bigram_df = bigram_df.sort_values(by='Frekans', ascending=False).head(15) # İlk 15'i al

        # --- GÖRSELLEŞTİRME ---
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Frekans', y='Bigram', data=bigram_df, palette='viridis')
        
        plt.title('Şikayetlerde En Sık Yan Yana Gelen İfadeler (Bigram Analizi)', fontsize=14, fontweight='bold')
        plt.xlabel('Tekrar Sayısı', fontsize=11)
        plt.ylabel('İkili Kelime Grubu', fontsize=11)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        
        # Kaydet
        plt.savefig('ANALİZ/ekstra_bigram_grafigi.png', dpi=300, bbox_inches='tight')
        print("\n✅ Bigram Grafiği Hazır: ANALİZ/ekstra_bigram_grafigi.png")
        print(bigram_df) # Konsola da yazsın
        plt.show()

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    bigram_analizi_yap()