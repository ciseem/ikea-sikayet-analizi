import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Orijinal kaynak bilgisinin olduğu dosya
KAYNAK_DOSYASI = "IKEA_MASTER_TURKCE_FINAL.csv"

def profesyonel_grafik_ciz():
    try:
        df = pd.read_csv(KAYNAK_DOSYASI)
        
        # 1. DOSYA İSİMLERİNİ PLATFORM İSİMLERİNE ÇEVİRME SÖZLÜĞÜ
        isim_duzeltme = {
            'trustpilot_ikea_usa_full': 'Trustpilot (Global)',
            'eksi_ikea_FULL_VERI': 'Ekşi Sözlük',
            'ikea_buyuk_veri_seti': 'Şikayetvar / Genel',
            'uludag_ikea_yorumlari_GARANTI': 'Uludağ Sözlük',
            'pissed_consumer_ikea_gercek': 'Pissed Consumer',
            'twitter_gercek_veri_v2': 'Twitter (X)',
            'trustpilot_ikea_ıtaly_full': 'Trustpilot (İtalya)'
        }
        
        # İsimleri değiştir
        df['kaynak'] = df['kaynak'].replace(isim_duzeltme)
        
        # Sayıları al
        kaynak_sayilari = df['kaynak'].value_counts()
        
        # --- GÖRSELLEŞTİRME ---
        plt.figure(figsize=(12, 7))
        # 'magma' veya 'viridis' paleti profesyonel durur
        sns.barplot(x=kaynak_sayilari.values, y=kaynak_sayilari.index, palette='viridis')
        
        plt.title('IKEA Müşteri Geri Bildirimleri: Platform Bazlı Veri Dağılımı', fontsize=14, fontweight='bold')
        plt.xlabel('Toplam Yorum Sayısı', fontsize=12)
        plt.ylabel('Veri Kaynağı (Platform)', fontsize=12)
        
        # Izgara çizgileri ekle (Okunabilirliği artırır)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Grafiği kaydet
        plt.savefig('ANALİZ/kaynak_dagilimi_profesyonel.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("\n✅ Yeni grafik 'ANALİZ/kaynak_dagilimi_profesyonel.png' olarak kaydedildi.")
        print(kaynak_sayilari)

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    profesyonel_grafik_ciz()