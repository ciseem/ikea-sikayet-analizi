from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import os

# --- AYARLAR ---
BASE_URL = "https://www.uludagsozluk.com/k/ikea/"
SAYFA_SAYISI = 2000 # Sen dur diyene kadar çok sayfa gezsin diye artırdım
DOSYA_ADI = "uludag_ikea_yorumlari_GARANTI.csv"

def uludag_garanti_cek():
    print(f"🚀 ULUDAĞ SÖZLÜK GARANTİ MODU BAŞLADI... (Dosya: {DOSYA_ADI})")
    print("💾 Her sayfa bittiğinde otomatik kayıt yapılacak.")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    # Bot algılanmasını azaltmak için User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Eğer dosya varsa üzerine yazmasın, öncekileri korusun diye kontrol edebiliriz
    # Ama basitlik olsun diye her çalıştırışta sıfırdan başlatıp biriktirerek gidiyoruz.
    tum_veriler = []
    
    try:
        for sayfa in range(1, SAYFA_SAYISI + 1):
            url = f"{BASE_URL}{sayfa}/"
            print(f"\n📄 Sayfa {sayfa} taranıyor...")
            
            try:
                driver.get(url)
                time.sleep(random.uniform(3.0, 5.0)) # Yüklenmesi için bekle
                
                # --- VERİ ÇEKME ---
                # Geniş kapsamlı seçici (li.entry veya alternatifleri)
                entryler = driver.find_elements(By.CSS_SELECTOR, "li.entry")
                
                # Eğer li.entry bulamazsa alternatif yapı (div.entry-item vb)
                if not entryler:
                    entryler = driver.find_elements(By.XPATH, "//div[contains(@class, 'entry')]")

                sayfa_veri_sayisi = 0
                
                for entry in entryler:
                    try:
                        # Metni al
                        metin = entry.text.strip()
                        
                        # Tarih ve Yazar bilgisini almaya çalışalım (Varsa)
                        try:
                            # Metni satırlara bölüp temizleyelim (Genelde en altta yazar/tarih olur)
                            satirlar = metin.split('\n')
                            ana_metin = satirlar[0] # İlk satır genelde yorumdur
                            # Yazarı bulmaya çalış
                            yazar_elem = entry.find_element(By.CSS_SELECTOR, "a.auth")
                            yazar = yazar_elem.text.strip()
                        except:
                            ana_metin = metin
                            yazar = "Uludag_Yazari"

                        # Boş veya çok kısa değilse ekle
                        if len(ana_metin) > 10:
                            tum_veriler.append({
                                "Yazar": yazar,
                                "Tarih": "-", # Tarih formatı karışık, şimdilik boş geçelim
                                "Sikayet": ana_metin,
                                "Kaynak": "Uludag_Sozluk",
                                "Link": url
                            })
                            sayfa_veri_sayisi += 1
                    except: continue

                print(f"   ✅ {sayfa_veri_sayisi} yeni veri bulundu. (Toplam: {len(tum_veriler)})")
                
                # --- KRİTİK KISIM: HER SAYFADA KAYDET ---
                if tum_veriler:
                    df = pd.DataFrame(tum_veriler)
                    df.to_csv(DOSYA_ADI, index=False, encoding="utf-8-sig")
                    print(f"   💾 Veriler '{DOSYA_ADI}' dosyasına kaydedildi.")

                # Eğer hiç veri çıkmadıysa belki sayfa sonudur veya engel vardır
                if sayfa_veri_sayisi == 0:
                    print("   ⚠️ Bu sayfada veri bulunamadı. Yapı değişmiş olabilir veya konu bitmiş olabilir.")
                    # Yine de devam et, belki sonraki sayfada vardır.

            except Exception as e:
                print(f"   ❌ Sayfa hatası: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\n🛑 Sen durdurdun! (Ctrl+C)")
    
    except Exception as e:
        print(f"❌ Genel Hata: {e}")
        
    finally:
        driver.quit()
        print(f"\n🏁 İŞLEM BİTTİ. Son Durum: Toplam {len(tum_veriler)} veri '{DOSYA_ADI}' dosyasında.")

if __name__ == "__main__":
    uludag_garanti_cek()