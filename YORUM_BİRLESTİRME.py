import pandas as pd
import os

# --- AYARLAR ---
CIKTI_DOSYASI = "IKEA_MASTER_HAM_VERI.csv"

def en_uzun_metin_sutununu_bul(df):
    """Tablodaki en uzun ortalama karakter sayısına sahip sütunu bulur."""
    max_uzunluk = 0
    hedef_sutun = None
    
    # Sadece metin tabanlı (object) sütunları kontrol et
    for col in df.select_dtypes(include=['object']):
        # Boş olmayan satırların ortalama uzunluğuna bak
        ortalama_uzunluk = df[col].astype(str).str.len().mean()
        if ortalama_uzunluk > max_uzunluk:
            max_uzunluk = ortalama_uzunluk
            hedef_sutun = col
            
    return hedef_sutun

def akilli_birlestir_ve_raporla():
    dosyalar = [f for f in os.listdir() if f.endswith('.csv') and f != CIKTI_DOSYASI]
    print(f"📂 {len(dosyalar)} dosya inceleniyor...\n")

    birlesmis_liste = []
    dosya_istatistikleri = [] # Rapor için veri saklayacağız

    for dosya in dosyalar:
        try:
            df = pd.read_csv(dosya)
            asıl_sutun = en_uzun_metin_sutununu_bul(df)
            
            if asıl_sutun:
                temp_df = df[[asıl_sutun]].copy()
                temp_df.columns = ['sikayet']
                temp_df['kaynak'] = dosya.replace('.csv', '')
                
                # Bu dosyadan kaç satır geldiğini kaydet
                satir_sayisi = len(temp_df)
                birlesmis_liste.append(temp_df)
                dosya_istatistikleri.append({"Dosya Adı": dosya, "Sütun": asıl_sutun, "Satır Sayısı": satir_sayisi})
                
                print(f"✅ {dosya.ljust(40)} -> '{asıl_sutun}' sütunundan {satir_sayisi} satır alındı.")
            else:
                print(f"⚠️ {dosya.ljust(40)} -> Uygun metin sütunu bulunamadı!")
                
        except Exception as e:
            print(f"❌ {dosya.ljust(40)} -> Okunurken hata: {e}")

    # --- BİRLEŞTİRME VE FİNAL RAPORU ---
    if birlesmis_liste:
        final_df = pd.concat(birlesmis_liste, ignore_index=True)
        
        ham_toplam = len(final_df)
        
        # Temizlik: Boşları ve tam eşleşen tekrarları sil
        final_df.dropna(subset=['sikayet'], inplace=True)
        final_df.drop_duplicates(subset=['sikayet'], inplace=True)
        
        temiz_toplam = len(final_df)
        silinen_tekrar = ham_toplam - temiz_toplam

        final_df.to_csv(CIKTI_DOSYASI, index=False, encoding="utf-8-sig")
        
        # --- GÖRSEL RAPORLAMA ---
        print("\n" + "="*50)
        print("📊 FİNAL VERİ SETİ RAPORU")
        print("="*50)
        rapor_df = pd.DataFrame(dosya_istatistikleri)
        print(rapor_df.to_string(index=False))
        print("-" * 50)
        print(f"📦 Ham birleştirilmiş veri:  {ham_toplam} satır")
        print(f"🧹 Silinen mükerrer (tekrar): {silinen_tekrar} satır")
        print(f"⭐ Net benzersiz şikayet:    {temiz_toplam} satır")
        print("="*50)
        print(f"📂 Sonuç dosyası: {CIKTI_DOSYASI}")
    else:
        print("\n❌ Hiçbir veri birleştirilemedi.")

if __name__ == "__main__":
    akilli_birlestir_ve_raporla()