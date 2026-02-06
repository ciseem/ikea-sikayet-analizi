from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

# --- AYARLAR ---
DOSYA_ADI = "eksi_ikea_FULL_VERI.csv"
BASLANGIC_URL = "https://eksisozluk.com/ikea--126934"

def veri_cek():
    print("🚀 SINIRSIZ MOD BAŞLATILIYOR... (Son sayfaya kadar gider)")
    print("⚠️ Kapatmak istersen terminalde CTRL+C yapabilirsin.")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(BASLANGIC_URL)
    time.sleep(3)
    
    tum_veriler = []
    sayfa_sayaci = 1

    # Sonsuz döngü (Break komutu gelene kadar dön)
    while True:
        try:
            print(f"\n📄 [Sayfa {sayfa_sayaci}] Taranıyor: {driver.current_url}")
            
            entryler = driver.find_elements(By.CSS_SELECTOR, "ul#entry-item-list li")
            
            if not entryler:
                print("🛑 Entry bulunamadı. Muhtemelen son sayfadayız veya engel yedik.")
                break

            sayfa_verisi = []
            
            for entry in entryler:
                try:
                    icerik = entry.find_element(By.CSS_SELECTOR, "div.content").text.strip()
                    try:
                        yazar = entry.find_element(By.CSS_SELECTOR, "a.entry-author").text.strip()
                    except: yazar = "Anonim"
                    try:
                        tarih = entry.find_element(By.CSS_SELECTOR, "a.entry-date").text.strip()
                    except: tarih = "-"

                    veri = {
                        "Yazar": yazar,
                        "Tarih": tarih,
                        "Baslik": "IKEA Genel",
                        "Sikayet": icerik,
                        "Kaynak": "Ekşi Sözlük"
                    }
                    
                    if veri not in tum_veriler:
                        tum_veriler.append(veri)
                        sayfa_verisi.append(veri)
                except:
                    continue
            
            print(f"   ✅ {len(sayfa_verisi)} yeni veri alındı. (Toplam: {len(tum_veriler)})")

            # HER SAYFADA KAYDET (Veri kaybı olmasın)
            df = pd.DataFrame(tum_veriler)
            df.to_csv(DOSYA_ADI, index=False, encoding="utf-8-sig")
            print(f"   💾 Kayıt güncellendi.")

            # --- SONRAKİ SAYFAYA GEÇİŞ ---
            try:
                # Sayfanın altındaki "Sonraki" (ok işareti) butonunu bul
                sonraki_buton = driver.find_element(By.CSS_SELECTOR, "a.next")
                link = sonraki_buton.get_attribute("href")
                
                if link:
                    driver.get(link)
                    sayfa_sayaci += 1
                    # Ban yememek için 2-4 saniye bekle
                    time.sleep(random.uniform(2.0, 4.0))
                else:
                    print("🏁 Sonraki sayfa linki yok. İŞLEM BİTTİ.")
                    break
            except:
                print("🏁 'Sonraki Sayfa' butonu bulunamadı. SON SAYFAYA ULAŞILDI.")
                break

        except Exception as e:
            print(f"❌ Beklenmedik Hata: {e}")
            print("5 saniye bekleyip tekrar deniyorum...")
            time.sleep(5)
            continue

    driver.quit()
    print(f"\n🎉 TOPLAM {len(tum_veriler)} VERİ ÇEKİLDİ.")
    print(f"Dosya: {DOSYA_ADI}")

if __name__ == "__main__":
    veri_cek()