from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
import os

# --- AYARLAR ---
BASE_URL = "https://ikea.pissedconsumer.com/review.html"
DOSYA_ADI = "pissed_consumer_ikea_gercek.csv"
SAYFA_SINIRI = 1000 # Gidebildiği yere kadar gitsin
BASLANGIC_SAYFASI = 101 # Madem 100'e kadar çektin, 101'den başlatalım

def pissed_consumer_unlimited_cek():
    print(f"🚀 PISSED CONSUMER DEV OPERASYON (Sayfa {BASLANGIC_SAYFASI} -> {SAYFA_SINIRI})")
    
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Tarayıcıya bağlanıldı. Kaldığın yerden devam ediliyor...")
    except Exception as e:
        print(f"\n❌ HATA: Chrome bağlantısı kurulamadı! Port 9222'nin açık olduğundan emin ol.")
        return

    cekilen_sayac = 0
    # Mevcut dosyayı kontrol et (Varsa kaç tane olduğunu bilmek için)
    if os.path.exists(DOSYA_ADI):
        mevcut_df = pd.read_csv(DOSYA_ADI)
        print(f"📊 Mevcut dosyada {len(mevcut_df)} yorum zaten var.")

    try:
        for sayfa in range(BASLANGIC_SAYFASI, SAYFA_SINIRI + 1):
            url = f"{BASE_URL}?page={sayfa}"
            print(f"\n📄 Sayfa {sayfa} taranıyor...", end="")
            
            driver.get(url)
            # Sayfanın tam yüklenmesi ve robot koruması için bekleme süresini biraz artırdık
            time.sleep(random.uniform(6, 9))

            # --- YORUM BULMA ---
            # En güncel ve farklı seçicileri kullanıyoruz
            yorumlar = driver.find_elements(By.CSS_SELECTOR, "div.copy-text")
            if not yorumlar:
                yorumlar = driver.find_elements(By.CSS_SELECTOR, "[itemprop='reviewBody']")
            
            # Eğer sayfa boş gelirse bir kez daha yenileyip şansımızı deneyelim
            if not yorumlar:
                print(" ⚠️ Sayfa boş görünüyor, bir kez yenileniyor...")
                driver.refresh()
                time.sleep(10)
                yorumlar = driver.find_elements(By.CSS_SELECTOR, "div.copy-text")

            if not yorumlar:
                print(" 🏁 Veri bitti veya kalıcı engele takıldık. İşlem durduruluyor.")
                break

            sayfa_verisi = []
            for yorum in yorumlar:
                try:
                    metin = yorum.text.strip().replace('\n', ' ').replace('\r', ' ')
                    
                    if len(metin) > 30:
                        sayfa_verisi.append({"Sikayet": metin, "Kaynak": "PissedConsumer_Global"})
                        cekilen_sayac += 1
                        print(".", end="", flush=True)
                except:
                    continue

            # --- ANLIK KAYIT (SAYFA BİTTİĞİNDE) ---
            if sayfa_verisi:
                df = pd.DataFrame(sayfa_verisi)
                header_durumu = not os.path.exists(DOSYA_ADI)
                df.to_csv(DOSYA_ADI, mode='a', index=False, header=header_durumu, encoding="utf-8-sig")
                print(f" -> Bu sayfadan {len(sayfa_verisi)} veri eklendi.")
            
            # Her 10 sayfada bir daha uzun mola vererek siteyi şüphelendirme
            if sayfa % 10 == 0:
                print("☕ Bot kısa bir kahve molası veriyor (15 saniye)...")
                time.sleep(15)

    except Exception as e:
        print(f"\n❌ BEKLENMEDİK HATA: {e}")
    finally:
        print(f"\n🎉 OPERASYON TAMAMLANDI.")
        print(f"📈 Bu oturumda eklenen toplam veri: {cekilen_sayac}")

if __name__ == "__main__":
    pissed_consumer_unlimited_cek()