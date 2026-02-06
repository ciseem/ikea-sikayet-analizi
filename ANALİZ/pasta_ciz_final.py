import matplotlib.pyplot as plt

# EN GÜNCEL VE DOĞRU VERİLER (Ultra Detaylı Analiz Sonucu)
labels = [
    'Hizmet / Bayi (%29.4)', 
    'Üretim / Fabrika (%16.3)', 
    'Lojistik / Dağıtım (%12.4)', 
    'Diğer / Genel (%41.9)'
]
sizes = [4194, 2323, 1769, 5979]

# Renkler (Anlamlı ve Profesyonel)
colors = [
    '#ff4d4d',  # Hizmet: KIRMIZI (En büyük kriz/alarm)
    '#ffda1a',  # Üretim: IKEA SARISI
    '#0051ba',  # Lojistik: IKEA MAVİSİ
    '#d3d3d3'   # Diğer: GRİ (Arka plan)
]

# Hizmet dilimini (Kırmızı) pastadan biraz ayırarak vurgula
explode = (0.1, 0, 0, 0)  

# Grafiği Çiz
plt.figure(figsize=(10, 7))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
        autopct='%1.1f%%', shadow=True, startangle=140, 
        textprops={'fontsize': 11, 'weight': 'bold'}) # Yazıları kalınlaştır

plt.title('IKEA Şikayetlerinin Kök Neden Dağılımı (2025-2026)', fontsize=14, fontweight='bold')
plt.axis('equal') 

# Kaydet
plt.savefig('ANALİZ/bolum2_pasta_final.png', dpi=300, bbox_inches='tight')
print("\n✅ Grafik Hazır: ANALİZ/bolum2_pasta_final.png")
plt.show()