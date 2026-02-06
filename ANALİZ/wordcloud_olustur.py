import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Dosya adını kontrol et
DOSYA_ADI = "IKEA_FINAL_PIRIL_PIRIL.csv"

def kompakt_kelime_bulutu():
    try:
        print("Veri okunuyor...")
        df = pd.read_csv(DOSYA_ADI)
        
        # Metinleri birleştir
        tum_metin = " ".join(df['temiz_sikayet'].astype(str).tolist()).lower()
        
        # --- GEREKSİZ KELİMELERİ TEMİZLE ---
        stop_words = set([
            'bir', 've', 'bu', 'ile', 'için', 'ama', 'fakat', 'lakin', 'de', 'da', 
            'ki', 'mi', 'mu', 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'diye', 
            'gibi', 'kadar', 'olarak', 'sonra', 'daha', 'en', 'çok', 'bile', 
            'ise', 'yani', 'çünkü', 'veya', 'ya', 'hem', 'ne', 'her', 'hiç',
            'şekilde', 'zaten', 'hala', 'yine', 'sadece', 'böyle', 'öyle',
            'ikea', 'ürün', 'dedi', 'kendi', 'bile', 'artık'
        ])

        print("Daha küçük ve sade kelime bulutu oluşturuluyor...")
        
        # AYARLAR (Burayı Küçülttüm)
        wordcloud = WordCloud(
            width=800, height=400,       # Boyutu YARI YARIYA küçülttüm
            background_color='white',
            stopwords=stop_words,
            colormap='inferno',          
            max_words=75,                # Sadece en önemli 75 kelime!
            contour_width=1, contour_color='steelblue'
        ).generate(tum_metin)

        # Görselleştirme (Pencere boyutu da küçüldü)
        plt.figure(figsize=(9, 5))       # Ekrana sığacak makul boyut
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)

        # Kaydet
        plt.savefig('ANALİZ/wordcloud_sade.png', dpi=300, bbox_inches='tight')
        print("\n✅ Küçük ve Sade Bulut Hazır: ANALİZ/wordcloud_sade.png")
        plt.show()

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    kompakt_kelime_bulutu()