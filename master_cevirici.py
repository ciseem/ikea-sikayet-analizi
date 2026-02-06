import pandas as pd
from tqdm import tqdm
import os
import argostranslate.translate

# --- AYARLAR ---
GIRIS_DOSYASI = "IKEA_MASTER_HAM_VERI.csv"
CIKTI_DOSYASI = "IKEA_MASTER_TURKCE_FINAL.csv"

def is_english(text):
    """Basit ve hızlı bir İngilizce kontrolü."""
    # En yaygın İngilizce kelimelerden birkaçı varsa 'bu İngilizcedir' diyoruz
    en_words = {'the', 'and', 'with', 'for', 'this', 'that', 'was', 'were', 'from', 'but'}
    words = set(str(text).lower().split())
    return any(w in en_words for w in words)

def akilli_hizli_cevir():
    if not os.path.exists(GIRIS_DOSYASI):
        print(f"❌ {GIRIS_DOSYASI} bulunamadı!")
        return

    df = pd.read_csv(GIRIS_DOSYASI)
    print(f"🚀 Akıllı tarama başlıyor. Sadece İngilizce olanlar işlenecek...")

    def smart_translate(text):
        if not isinstance(text, str) or len(text) < 5:
            return text
        
        # Eğer metin zaten Türkçeye benziyorsa (içinde 'the' yoksa vb.) pas geç
        if not is_english(text):
            return text 
            
        try:
            return argostranslate.translate.translate(text, "en", "tr")
        except:
            return text

    tqdm.pandas(desc="⚡ Hızlı İşleniyor")
    df['sikayet'] = df['sikayet'].progress_apply(smart_translate)

    df.to_csv(CIKTI_DOSYASI, index=False, encoding="utf-8-sig")
    print(f"🎉 BİTTİ! Gereksiz beklemeler atlandı, dosya hazır: {CIKTI_DOSYASI}")

if __name__ == "__main__":
    akilli_hizli_cevir()