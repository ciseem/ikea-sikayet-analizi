import matplotlib.pyplot as plt
import pandas as pd

# SON YAPTIĞIMIZ ULTRA DETAYLI ANALİZ SONUÇLARI (En güncel veriler)
data = {
    'Sorumlu Departman': [
        'Çağrı Merkezi / İletişim', 
        'Lojistik / Nakliye', 
        'Mağaza İçi Personel', 
        'Teknik Servis / Montaj'
    ],
    'Şikayet Hacmi': [4604, 1530, 918, 850],
    'Etki Payı': ['%58,3', '%19,4', '%11,6', '%10,8'],
    'Kriz Seviyesi': [
        '🔴 KRİTİK (Acil Müdahale)', 
        '🟠 Yüksek Risk', 
        '🟡 Orta Risk', 
        '🔵 Standart Süreç'
    ]
}

df = pd.DataFrame(data)

def tabloyu_resme_dok():
    # Görsel ayarları
    fig, ax = plt.subplots(figsize=(11, 4)) 
    ax.axis('tight')
    ax.axis('off')
    
    # Renkler (IKEA Mavisi başlık)
    header_color = '#0051ba'  # Başlık rengi
    row_colors = ['#f1f1f2', 'white'] # Satır renkleri (Gri - Beyaz şeritli)
    
    # Tabloyu oluştur
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='center',
                     colColours=[header_color] * 4)
    
    # Yazı Tipi ve Boyut Ayarları
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2.5) # Satır yüksekliği
    
    # Başlığı Beyaz ve Kalın Yap
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(color='white', weight='bold', fontsize=12)
            cell.set_edgecolor('white')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[row % 2])
            cell.set_edgecolor('#dddddd')

    # Tablo Üstüne Başlık Ekle
    plt.title('IKEA Operasyonel Darboğaz Analizi (Güncel - 2026)', fontsize=14, weight='bold', pad=15, color='#333333')
    
    # Kaydet
    plt.savefig('ANALİZ/bolum3_tablo_final.png', dpi=300, bbox_inches='tight')
    print("\n✅ Tablo güncellendi: ANALİZ/bolum3_tablo_final.png")
    plt.show()

if __name__ == "__main__":
    tabloyu_resme_dok()