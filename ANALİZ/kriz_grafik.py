import matplotlib.pyplot as plt

# SENİN BULDUĞUN GERÇEK SAYILAR (Ultra Analiz Sonucu)
kategoriler = ['Kritik Churn (Terk)', 'İtibar Riski (Toksik)', 'Yasal Risk (Dava)']
sayilar = [2603, 1910, 996]
yuzdeler = [18.2, 13.4, 7.0]

# Renkler (Kırmızı tonları tehlikeyi simgeler)
colors = ['#d9534f', '#f0ad4e', '#5bc0de'] 

plt.figure(figsize=(10, 6))

# Çubuk Grafiği Çiz
bars = plt.bar(kategoriler, sayilar, color=colors, edgecolor='black', alpha=0.9, width=0.6)

# Sütunların üzerine sayıları ve yüzdeleri yaz
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 50,
             f'{height} Kişi\n(%{yuzdeler[i]})',
             ha='center', va='bottom', fontsize=11, fontweight='bold', color='#333333')

plt.title('IKEA Müşteri Kriz ve Risk Analizi (2026)', fontsize=14, fontweight='bold', pad=20)
plt.ylabel('Risk Altındaki Müşteri Sayısı', fontsize=11)
plt.ylim(0, 3000) # Grafiğin tepesi biraz boş kalsın
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Kaydet
plt.savefig('ANALİZ/bolum4_kriz_final.png', dpi=300, bbox_inches='tight')
print("\n✅ Grafik Hazır: ANALİZ/bolum4_kriz_final.png")
plt.show()