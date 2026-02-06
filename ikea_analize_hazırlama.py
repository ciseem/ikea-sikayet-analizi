import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords

# Gerekli paketleri indir
nltk.download('stopwords')

# --- AYARLAR ---
GIRIS_DOSYASI = "IKEA_MASTER_TURKCE_FINAL.csv" 
CIKTI_DOSYASI = "IKEA_FINAL_PIRIL_PIRIL.csv"

# Türkçe etkisiz kelimeler
stop_words = set(stopwords.words('turkish'))

def komple_temizlik_ve_birleştirme(metin):
    if not isinstance(metin, str):
        return ""
    
    # 1. SATIR BİRLEŞTİRME (EN ÖNEMLİ ADIM)
    # Metin içindeki tüm \n (enter), \r ve \t karakterlerini boşluğa çevirir
    metin = metin.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # 2. TÜRKÇE KARAKTER KORUYARAK KÜÇÜK HARF YAPMA
    # Standart lower() yerine Türkçe karakterleri manuel koruyoruz
    metin = metin.replace('İ', 'i').replace('I', 'ı').replace('Ş', 'ş').replace('Ğ', 'ğ').replace('Ç', 'ç').replace('Ö', 'ö').replace('Ü', 'ü')
    metin = metin.lower()
    
    # 3. LİNK VE URL TEMİZLİĞİ
    metin = re.sub(r'http\S+|www\S+|https\S+', '', metin)
    
    # 4. NOKTALAMA VE ÖZEL SEMBOL TEMİZLİĞİ (Türkçe harfleri korur)
    # Sadece küçük harfleri, Türkçe karakterleri ve boşlukları tutar
    metin = re.sub(r'[^a-zçğıöşü\s]', '', metin)
    
    # 5. ETKİSİZ KELİME (STOPWORDS) TEMİZLİĞİ
    kelimeler = metin.split()
    temiz_kelimeler = [w for w in kelimeler if w not in stop_words]
    
    # 6. FAZLA BOŞLUKLARI SİL VE TEK SATIRA İNDİR
    # split() ve join() metni tamamen sıkıştırır ve aradaki boş satırları yok eder
    return " ".join(temiz_kelimeler).strip()

def ana_islem():
    print(f"🚀 Dev Temizlik ve Satır Birleştirme Operasyonu Başladı...")
    
    try:
        # Dosyayı oku
        df = pd.read_csv(GIRIS_DOSYASI, encoding='utf-8-sig')
        
        # Tüm işlemleri uygula
        df['temiz_sikayet'] = df['sikayet'].apply(komple_temizlik_ve_birleştirme)
        
        # TEKRARLI VERİLERİ SİL
        df.drop_duplicates(subset=['temiz_sikayet'], inplace=True)
        
        # BOŞ KALANLARI SİL
        df = df[df['temiz_sikayet'].str.len() > 3]
        
        # KAYIT: lineterminator='\n' ile her yorumu tek bir fiziksel satıra zorluyoruz
        df.to_csv(CIKTI_DOSYASI, index=False, columns=['temiz_sikayet'], encoding='utf-8-sig', lineterminator='\n')
        
        print("\n" + "="*50)
        print(f"✅ İŞLEM TAMAMLANDI!")
        print(f"📊 Net Benzersiz Yorum: {len(df)}")
        print(f"📂 Dosya Adı: {CIKTI_DOSYASI}")
        print("="*50)
        
        print("\n📝 Örnek Değişim (Kontrol Et):")
        print(f"❌ ESKİ: {df['sikayet'].iloc[0][:100] if 'sikayet' in df else 'Bulunamadı'}...")
        print(f"✅ YENİ: {df['temiz_sikayet'].iloc[0][:100]}...")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    ana_islem()