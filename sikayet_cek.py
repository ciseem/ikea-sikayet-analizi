import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# --- AYARLAR ---
HEDEF_SAYFA_SAYISI = 1000
DOSYA_ADI = "ikea_buyuk_veri_seti.csv"
LISTE_URL = "https://www.sikayetvar.com/ikea?page={}"
ANA_DOMAIN = "https://www.sikayetvar.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def veri_cek():
    tum_sikayetler = []
    print(f"🚀 GÜVENLİ SCRAPER BAŞLADI! Hedef: {HEDEF_SAYFA_SAYISI} sayfa.")
    print(f"💾 Veriler HER SAYFADA BİR '{DOSYA_ADI}' dosyasına kaydedilecek.\n")

    for sayfa in range(1, HEDEF_SAYFA_SAYISI + 1):
        url = LISTE_URL.format(sayfa)
        print(f"📂 [Sayfa {sayfa}/{HEDEF_SAYFA_SAYISI}] Listesi çekiliyor...")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"⚠️ Sayfa {sayfa} açılamadı (Kod: {response.status_code}). 10 sn bekleniyor...")
                time.sleep(10)
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            
            kartlar = soup.find_all("article", class_="card-v2")
            if not kartlar:
                kartlar = soup.find_all("article") 

            if not kartlar:
                print("🛑 Şikayetler bitti. İşlem sonlandırılıyor.")
                break

            print(f"   ↳ {len(kartlar)} şikayet bulundu. Detaylara giriliyor...")

            for index, kart in enumerate(kartlar):
                try:
                    link_tag = kart.find("a") 
                    if not link_tag: continue
                    
                    sikayet_url = ANA_DOMAIN + link_tag.get("href")
                    
                    detay_response = requests.get(sikayet_url, headers=headers)
                    if detay_response.status_code != 200: continue
                    
                    detay_soup = BeautifulSoup(detay_response.content, "html.parser")
                    
                    # TAM METİN
                    description_div = detay_soup.find("div", class_="complaint-detail-description")
                    if description_div:
                        tam_metin = description_div.text.strip()
                    else:
                        p_tags = detay_soup.find_all("p")
                        tam_metin = " ".join([p.text.strip() for p in p_tags if len(p.text) > 20])

                    # Başlık, Yazar, Tarih
                    try: baslik = detay_soup.find("h1", class_="complaint-detail-title").text.strip()
                    except: baslik = "Başlık Yok"
                    
                    try: yazar = detay_soup.find("span", class_="username").text.strip()
                    except: yazar = "Gizli"
                    
                    try: tarih = detay_soup.find("div", class_="time").text.strip()
                    except: tarih = "-"

                    tum_sikayetler.append({
                        "Yazar": yazar,
                        "Tarih": tarih,
                        "Başlık": baslik,
                        "Şikayet": tam_metin,
                        "Link": sikayet_url
                    })
                    
                    print(f"      ✅ [{index+1}/{len(kartlar)}] Alındı: {baslik[:30]}...")
                    time.sleep(random.uniform(0.5, 1.0))
                    
                except Exception:
                    continue 

            # --- ARTIK HER SAYFA SONUNDA KAYDEDİYOR ---
            df = pd.DataFrame(tum_sikayetler)
            df.to_csv(DOSYA_ADI, index=False, encoding="utf-8-sig")
            print(f"💾 --- SAYFA {sayfa} BİTTİ VE KAYDEDİLDİ. (Toplam: {len(tum_sikayetler)}) ---")
            
            time.sleep(2)

        except Exception as e:
            print(f"❌ Sayfa Hatası: {e}")
            time.sleep(5)
            continue

    print(f"\n🏁 İŞLEM TAMAMLANDI! Dosya: {DOSYA_ADI}")
    df = pd.DataFrame(tum_sikayetler)
    df.to_csv(DOSYA_ADI, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    veri_cek()