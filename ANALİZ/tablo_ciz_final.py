import matplotlib.pyplot as plt
import pandas as pd

# AZ ÖNCE BULDUĞUMUZ EN GÜNCEL VERİLER
data = {
    'Kategori': [
        'Hizmet / Bayi Kaynaklı', 
        'Üretim / Fabrika Kaynaklı', 
        'Lojistik / Dağıtım Kaynaklı', 
        'Genel / Tanımlanamayan'
    ],
    'Şikâyet Adedi': ['4.194', '2.323', '1.769', '5.979'],
    'Yüzdesel Dağılım (%)': ['%29,4', '%16,3', '%12,4', '%41,9']
}

df = pd.DataFrame(data)

def tabloyu_resme_dok():
    # Görsel ayarları
    fig, ax = plt.subplots(figsize=(10, 3)) # Boyut
    ax.axis('tight')
    ax.axis('off')
    
    # Renkler (Senin resmindeki o koyu mavi ton)
    header_color = '#0B4F6C'  # Petrol Mavisi / Koyu Mavi
    row_colors = ['#E1F5FE', 'white'] # Satırlar bir açık mavi, bir beyaz olsun (Okuması kolay)
    
    # Tabloyu çiz
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='center',
                     colColours=[header_color] * 3) # Başlık arka planı
    
    # Font ve boyut ayarları
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2.3) # Satır yüksekliği ve genişliği
    
    # Başlık yazı rengini BEYAZ ve KALIN yap (Resimdeki gibi)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(color='white', weight='bold', fontsize=12)
            cell.set_edgecolor('white') # Çizgileri de beyaz yap
            cell.set_facecolor(header_color)
        else:
            # Satır renklerini ayarla
            cell.set_facecolor(row_colors[row % 2])
            cell.set_edgecolor('#dddddd') # Satır çizgileri gri

    # Tablo Başlığı (İstersen kaldırabilirsin)
    plt.title('Tablo: Şikayetlerin Departman Bazlı Dağılımı ', 
              fontsize=13, weight='bold', color='#333333', pad=10, loc='left')
    
    # Kaydet
    plt.savefig('ANALİZ/tablo2_guncel.png', dpi=300, bbox_inches='tight')
    print("\n✅ Mavi Tablo Hazır: ANALİZ/tablo2_guncel.png")
    plt.show()

if __name__ == "__main__":
    tabloyu_resme_dok()