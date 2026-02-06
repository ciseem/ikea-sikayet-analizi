from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
import os

# --- AYARLAR ---
BASE_URL = "https://www.trustpilot.com/review/www.ikea.com" 
SAYFA_SAYISI = 1000 
DOSYA_ADI = "trustpilot_ikea_usa_full.csv"

def trustpilot_usa_v3():
    print(f"🚀 IKEA USA OPERASYONU (LOGIN DESTEKLİ) BAŞLADI...")
    
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Giriş yapılmış tarayıcıya bağlanıldı.")
    except Exception as e:
        print("\n❌ HATA: Chrome debug modunda değil!")
        return

    cekilen_metinler = set()
    genel_toplam = 0

    # Eğer daha önce çektiysen, kaldığın yerden devam etmek için mevcut veriyi oku
    if os.path.exists(DOSYA_ADI):
        eski_df = pd.read_csv(DOSYA_ADI)
        genel_toplam = len(eski_df)
        cekilen_metinler = set(eski_df['Sikayet'].tolist())
        print(f"📊 Mevcut dosyada {genel_toplam} yorum var. Kaldığın yerden devam ediliyor...")

    try:
        for sayfa in range(1, SAYFA_SAYISI + 1):
            url = f"{BASE_URL}?page={sayfa}"
            print(f"\n📄 Sayfa {sayfa} taranıyor...", end="")
            
            driver.get(url)
            # Giriş yapılmış olsa bile Trustpilot bazen yavaş yüklenir
            time.sleep(random.uniform(4, 6))
            
            # Kartları bul
            kartlar = driver.find_elements(By.CSS_SELECTOR, "article")
            
            # Eğer kart bulamazsa ve giriş yap ekranı gelirse bizi uyar
            if not kartlar:
                if "login" in driver.current_url.lower():
                    print("\n⚠️ Olamaz! Trustpilot yine giriş istiyor. Lütfen tarayıcıdan giriş yap ve ENTER'a bas.")
                    input("Giriş yaptıysan ENTER'a bas >> ")
                    driver.get(url) # Sayfayı yenile
                    time.sleep(5)
                    kartlar = driver.find_elements(By.CSS_SELECTOR, "article")

            if not kartlar:
                print("\n🏁 Sayfa boş geldi. Operasyon tamamlandı.")
                break

            yeni_sayfa_verisi = []
            for kart in kartlar:
                try:
                    h2 = kart.find_element(By.TAG_NAME, "h2").text.strip()
                    try:
                        p = kart.find_element(By.CSS_SELECTOR, "[data-service-review-text-typography='true']").text.strip()
                    except: p = ""
                    
                    tam_metin = f"{h2} . {p}".strip()
                    
                    if len(tam_metin) > 10 and tam_metin not in cekilen_metinler:
                        cekilen_metinler.add(tam_metin)
                        yeni_sayfa_verisi.append({"Sikayet": tam_metin, "Kaynak": "Trustpilot_USA"})
                except: continue

            if yeni_sayfa_verisi:
                df = pd.DataFrame(yeni_sayfa_verisi)
                header_yaz = not os.path.isfile(DOSYA_ADI)
                df.to_csv(DOSYA_ADI, mode='a', header=header_yaz, index=False, encoding="utf-8-sig")
                genel_toplam += len(yeni_sayfa_verisi)
                print(f" -> +{len(yeni_sayfa_verisi)} (Toplam: {genel_toplam})")
            
            # Banlanmamak için her 5 sayfada bir uzun mola
            if sayfa % 5 == 0:
                print("☕ Kısa bir mola...")
                time.sleep(random.randint(5, 10))

    except Exception as e:
        print(f"\n❌ Hata: {e}")
    finally:
        print(f"\n🎉 İşlem durdu. Toplam veri: {genel_toplam}")

if __name__ == "__main__":
    trustpilot_usa_v3()