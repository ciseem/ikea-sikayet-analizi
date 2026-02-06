import pandas as pd

# Listendeki en güncel temiz dosya
DOSYA = "IKEA_FINAL_PIRIL_PIRIL.csv"

def kok_neden_sayilarini_al():
    try:
        df = pd.read_csv(DOSYA)
        
        def kategorize_et(metin):
            metin = str(metin).lower()
            # Üretim/Fabrika Odaklı (Hatalı parça, eksik vida, kalite)
            if any(w in metin for w in ['kırık', 'eksik', 'vida', 'defolu', 'kalitesiz', 'çizik', 'bozuk', 'yırtık']):
                return "Üretim / Fabrika Kaynaklı"
            # Hizmet/Personel Odaklı (Personel tavrı, kaba davranış, mağaza içi)
            elif any(w in metin for w in ['personel', 'tavır', 'mağaza', 'ilgisiz', 'kaba', 'kasiyer', 'eleman', 'çalışan']):
                return "Hizmet / Bayi Kaynaklı"
            # Lojistik Odaklı (Kargo ve teslimat süreçleri)
            elif any(w in metin for w in ['kargo', 'nakliye', 'teslimat', 'geç geldi', 'bekleme', 'lojistik']):
                return "Lojistik / Dağıtım Kaynaklı"
            else:
                return "Genel / Tanımlanamayan"

        df['kök_neden'] = df['temiz_sikayet'].apply(kategorize_et)
        
        sonuclar = df['kök_neden'].value_counts()
        yuzdeler = df['kök_neden'].value_counts(normalize=True) * 100
        
        print("\n" + "="*45)
        print("📊 IKEA YÖNETİM RAPORU: KÖK NEDEN DAĞILIMI")
        print("="*45)
        for kategori, sayi in sonuclar.items():
            print(f"{kategori:<30}: {sayi} Adet (%{yuzdeler[kategori]:.1f})")
        print("="*45)

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    kok_neden_sayilarini_al()



    import matplotlib.pyplot as plt

# Kodundan çıkan veriler
labels = ['Hizmet / Bayi', 'Üretim / Fabrika', 'Lojistik', 'Genel']
sizes = [3298, 2372, 1860, 6735]
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
explode = (0.1, 0, 0, 0) # Hizmet kısmını öne çıkar

plt.figure(figsize=(10, 7))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('IKEA Şikayetlerinin Kök Neden Dağılımı', fontsize=14, fontweight='bold')
plt.axis('equal') 
plt.savefig('ANALİZ/kok_neden_pasta.png', dpi=300)
plt.show()