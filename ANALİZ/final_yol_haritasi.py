import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def sik_yol_haritasi_ciz():
    # --- PROFESYONEL RENK PALETİ ---
    color_acil = "#C0392B"    # Derin Kırmızı
    color_orta = "#F39C12"    # Amber
    color_uzun = "#2980B9"    # Kurumsal Mavi
    text_color = "#2C3E50"    # Koyu Gri (Okunabilirlik için ana renk)
    grid_color = "#BDC3C7"    # Açık Gri

    # Grafik Alanı
    fig, ax = plt.subplots(figsize=(14, 8)) # Yükseklik biraz arttı
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # GÖREVLER
    tasks = [
        (0, 3, "ACİL: Call-Back & Chatbot Entegrasyonu", color_acil),
        (0, 3, "ACİL: Özel Müşteri Geri Kazanım Timi", color_acil),
        (3, 9, "ORTA VADE: Lojistik SLA Revizyonu & Partner Denetimi", color_orta),
        (3, 9, "ORTA VADE: Proaktif SMS/WhatsApp Bilgilendirme Sistemi", color_orta),
        (6, 6, "YAPISAL: Personel Kriz Eğitimi & Hizmet Kültürü Dönüşümü", color_uzun)
    ]

    # Çubukları Çiz
    for i, (start, duration, name, color) in enumerate(reversed(tasks)):
        # 1. Çubuğu çiz (Biraz daha ince ve zarif: height=0.5)
        ax.barh(i, duration, left=start, height=0.5, align='center', color=color, alpha=0.9, edgecolor='none')
        
        # 2. Yazıyı ÇUBUĞUN ÜSTÜNE koy (Artık beyaz değil, Koyu Gri)
        # Bu sayede çubuk kısa olsa bile yazı asla kaybolmaz.
        ax.text(start, i + 0.35, "▸ " + name, va='center', ha='left', 
                color=text_color, fontweight='bold', fontsize=11, fontfamily='sans-serif')

    # Eksen Ayarları
    ax.set_xlim(0, 12.5)
    ax.set_ylim(-0.5, len(tasks)) # Boşluk ayarı
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(grid_color)

    # X Ekseni
    xticks = [0, 3, 6, 9, 12]
    xticklabels = ['BAŞLANGIÇ\n(Bugün)', '3. AY\n(Kriz Kontrolü)', '6. AY\n(Süreç İyileşmesi)', '9. AY', '12. AY\n(Operasyonel Mükemmellik)']
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, fontsize=10, fontweight='bold', color=text_color)
    ax.set_yticks([])

    # Başlık
    plt.title('İKEA TÜRKİYE: STRATEJİK DÖNÜŞÜM VE AKSİYON PLANI (2026)', fontsize=16, fontweight='bold', pad=40, color=text_color, loc='left')
    
    # Izgara
    ax.grid(axis='x', color=grid_color, linestyle=':', linewidth=0.8, alpha=0.7)
    
    # Lejant
    legend_patches = [
        mpatches.Patch(color=color_acil, label='Faz 1: Acil Müdahale (0-3 Ay)'),
        mpatches.Patch(color=color_orta, label='Faz 2: Süreç İyileştirme (3-12 Ay)'),
        mpatches.Patch(color=color_uzun, label='Faz 3: Yapısal Dönüşüm (6+ Ay)')
    ]
    plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=False, fontsize=10, labelcolor=text_color)

    # Kaydet
    plt.tight_layout()
    plt.savefig('ANALİZ/final_roadmap_premium_v2.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("\n✅ Düzeltilmiş Görsel Hazır: ANALİZ/final_roadmap_premium_v2.png")
    plt.show()

if __name__ == "__main__":
    sik_yol_haritasi_ciz()