from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import random
import os

# --- AYARLAR (V2) ---
# Filtreyi kaldırdım, sadece Türkçe IKEA şikayetleri. Fotoğraflılar da gelsin.
ARAMA_SORGUSU = "IKEA şikayet lang:tr"
DOSYA_ADI = "twitter_gercek_veri_v2.csv"
HEDEF_TWEET_SAYISI = 1000 # Hedefi büyüttük

def twitter_baglan_cek_v2():
    print(f"🚀 MEVCUT CHROME PENCERESİNE BAĞLANILIYOR (V2 - AGRESİF MOD)...")
    
    options = Options()
    # 9222 portundaki açık Chrome'a bağlan
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Bağlantı başarılı.")
    except Exception as e:
        print("\n❌ HATA: Açık Chrome penceresi bulunamadı!")
        print("Lütfen önce Windows+R ile Chrome'u debug modunda açtığından emin ol.")
        return

    cekilen_tweetler_kumesi = set()
    toplam_kaydedilen = 0

    try:
        # Arama sayfasına git (f=live: En Yeniler sekmesi)
        print(f"🔍 '{ARAMA_SORGUSU}' aranıyor (En Yeniler)...")
        url = f"https://twitter.com/search?q={ARAMA_SORGUSU.replace(' ', '%20')}&src=typed_query&f=live"
        driver.get(url)
        time.sleep(5)
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        bos_gecme = 0

        while toplam_kaydedilen < HEDEF_TWEET_SAYISI:
            # Tweetleri bul
            try:
                tweetler = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            except:
                time.sleep(2)
                continue

            yeni_veri = []
            
            for tweet in tweetler:
                try:
                    metin = tweet.text.strip().replace('\n', ' ').replace('\r', ' ')
                    # Çok kısa (tek kelime) şeyleri alma, gürültü yapmasın
                    if len(metin) > 5 and metin not in cekilen_tweetler_kumesi:
                        cekilen_tweetler_kumesi.add(metin)
                        yeni_veri.append({
                            "Sikayet": metin,
                            "Kaynak": "Twitter",
                            "Tarih": "-"
                        })
                except: continue

            # --- KAYIT ---
            if yeni_veri:
                df = pd.DataFrame(yeni_veri)
                header_yaz = not os.path.isfile(DOSYA_ADI)
                df.to_csv(DOSYA_ADI, mode='a', header=header_yaz, index=False, encoding="utf-8-sig")
                
                toplam_kaydedilen += len(yeni_veri)
                print(f"   💾 +{len(yeni_veri)} tweet eklendi. (Toplam: {toplam_kaydedilen})")
                bos_gecme = 0 # Veri bulduk, sayacı sıfırla
            else:
                bos_gecme += 1
                print(f"   (Bekliyor... {bos_gecme}/15)")

            # --- AKILLI KAYDIRMA (SCROLL) ---
            # Twitter bazen takılır, onu uyandırmak için önce biraz yukarı, sonra tam aşağı yapacağız.
            driver.execute_script("window.scrollBy(0, -300);") # Hafif yukarı
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Tam aşağı
            
            # Bekleme süresini rastgele yap ki bot sanmasın
            time.sleep(random.uniform(3.0, 6.0))

            # Sayfa Sonu Kontrolü
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Eğer boy değişmediyse hemen pes etme, 15 kere daha dene (Belki internet yavaştır)
                if bos_gecme > 15:
                    print("\n🏁 Gerçekten bitti. Twitter daha fazla yüklemiyor.")
                    break
            else:
                # Boy değiştiyse (yeni tweet geldiyse) sayacı sıfırla
                bos_gecme = 0
                
            last_height = new_height

    except Exception as e:
        print(f"\n❌ HATA: {e}")
        print("Tarayıcı kapanmış olabilir.")
    
    finally:
        print(f"\n🎉 İŞLEM BİTTİ. {toplam_kaydedilen} tweet '{DOSYA_ADI}' dosyasına eklendi.")

if __name__ == "__main__":
    twitter_baglan_cek_v2()