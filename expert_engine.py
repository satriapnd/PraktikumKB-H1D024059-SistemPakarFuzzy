def evaluate_sponsorship(loyalty_status, category, subscriber_tier, violation_history, age_demo, upload_freq):
    # Basis Harga Tengah per Tier
    base_prices = {
        'nano': 875000,
        'micro': 4500000,
        'macro': 28750000,
        'mega': 150000000
    }
    
    # Pengali Kategori
    category_multipliers = {
        'edukasi/teknologi': 1.5,
        'beauty/fashion': 1.3,
        'gaming/hiburan': 0.9,
        'lainnya': 1.0
    }
    
    # Pengali Status Loyalitas
    loyalty_multipliers = {
        'pasif': 0.8,
        'aktif': 1.0,
        'militan': 1.2
    }
    
    # Forward Chaining Logic
    status = "Sangat Layak"
    recommendation = "Kontrak Eksklusif"
    
    # 1. Rule: Riwayat Pelanggaran
    if violation_history.lower() == 'pernah strike':
        return {
            'status': 'Tolak',
            'recommendation': 'Batalkan Kerjasama - Risiko Brand Safety Tinggi',
            'estimated_value': 0
        }
        
    # 2. Rule: Status Loyalitas Pasif
    if loyalty_status.lower() == 'pasif':
        status = "Pertimbangkan"
        recommendation = "Lakukan Uji Coba (One-off Video) dengan KPI ketat"
        
    # 3. Rule: Frekuensi Upload Rendah (Inkonsisten)
    if upload_freq.lower() == 'jarang (<1 per bulan)' and status == 'Sangat Layak':
        status = "Pertimbangkan"
        recommendation = "Kontrak berbasis performa karena kreator kurang konsisten"
        
    # Perhitungan Estimasi Nilai Kontrak
    base_price = base_prices.get(subscriber_tier.lower(), 4500000)
    cat_multi = category_multipliers.get(category.lower(), 1.0)
    loyalty_multi = loyalty_multipliers.get(loyalty_status.lower(), 1.0)
    
    final_price = base_price * cat_multi * loyalty_multi
    
    if loyalty_status.lower() == 'militan' and status == 'Sangat Layak':
        recommendation = "Sangat disarankan untuk Kontrak Jangka Panjang (Eksklusif)"
        
    return {
        'status': status,
        'recommendation': recommendation,
        'estimated_value': int(final_price)
    }

if __name__ == '__main__':
    res = evaluate_sponsorship('Militan', 'Edukasi/Teknologi', 'Micro', 'Bersih', '18-24', 'Rutin (1-2 per minggu)')
    print(res)
