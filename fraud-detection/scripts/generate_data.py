"""
Fraud Detection Sistemi - Synthetic Veri Üretici
Para aklama ve anomali senaryoları içeren örnek veri üretir.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Reproducible randomness
np.random.seed(42)

# Dataset boyut parametreleri
NUM_USERS = 1000
NUM_NORMAL_TRANSACTIONS = 40000
NUM_FRAUDSTERS = 50
FRAUD_TRANSACTION_MULTIPLIER = 10

print("=" * 60)
print("SYNTHETIC VERI ÜRETIMI BAŞLIYOR...")
print("=" * 60)

# =============================================
# 1. KULLANICI PROFİLLERİ OLUŞTUR
#    Her kullanıcı için demografik ve risk profili.
# =============================================
print("\n[1/3] Kullanıcı profilleri oluşturuluyor...")

users = []
professions = ['Mühendis', 'Öğretmen', 'Öğrenci', 'Hizmetçi', 'İşletmeci', 'Doktor', 'Hemşire', 'Satışçı']
cities = ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya', 'Gaziantep', 'Konya', 'Kayseri']

for i in range(NUM_USERS):
    is_fraudster = i < NUM_FRAUDSTERS
    
    users.append({
        'user_id': f'USER_{i:05d}',
        'profession': np.random.choice(professions),
        'city': np.random.choice(cities),
        'monthly_income': np.random.gamma(2, 2000) + 2000,  # 2k-10k ₺
        'account_age_days': np.random.randint(30, 1000),
        'is_fraudster': is_fraudster,
        'risk_score': 80 if is_fraudster else np.random.randint(5, 30)
    })

user_df = pd.DataFrame(users)
user_df.to_csv('data/users.csv', index=False)
print(f"✅ {len(user_df)} kullanıcı profili oluşturuldu")

# =============================================
# 2. NORMAL İŞLEMLER OLUŞTUR
#    Gelirle orantılı miktarlarda, yıl içine dağılmış işlemler.
# =============================================
print("\n[2/3] Normal işlemler oluşturuluyor...")

normal_transactions = []
start_date = datetime(2026, 1, 1)
transaction_id_counter = 100000

# Normal kullanıcılar
for user in users:
    if not user['is_fraudster']:
        user_id = user['user_id']
        monthly_income = user['monthly_income']
        
        # Her kullanıcı ay içinde 10-50 işlem yapıyor
        num_transactions = np.random.randint(10, 50)
        
        for _ in range(num_transactions):
            # Rastgele tarih (365 gün içinde)
            days_offset = np.random.randint(0, 365)
            transaction_date = start_date + timedelta(days=days_offset)
            
            # Normal işlem miktarı: gelirin %1-5'i
            amount = np.random.gamma(2, monthly_income / 20)
            
            normal_transactions.append({
                'transaction_id': f'TXN_{transaction_id_counter:08d}',
                'user_id': user_id,
                'amount': round(amount, 2),
                'timestamp': transaction_date.isoformat(),
                'recipient_id': f'USER_{np.random.randint(0, NUM_USERS):05d}',
                'channel': np.random.choice(['ATM', 'Online', 'Branch', 'Mobile']),
                'location': user['city'],
                'fraud_label': 0,
                'fraud_type': None,
                'confidence_score': 0.0
            })
            transaction_id_counter += 1

print(f"✅ {len(normal_transactions)} normal işlem oluşturuldu")

# =============================================
# 3. DOLANDIRICI İŞLEMLERİ OLUŞTUR
#    Dört farklı fraud pattern senaryosu.
# =============================================
print("\n[3/3] Dolandırıcı işlemleri oluşturuluyor...")

fraud_transactions = []

fraudsters = users[:NUM_FRAUDSTERS]

for idx, fraudster in enumerate(fraudsters):
    user_id = fraudster['user_id']
    monthly_income = fraudster['monthly_income']
    city = fraudster['city']
    
    # Her dolandırıcı birkaç farklı saldırı yapıyor
    fraud_date = start_date + timedelta(days=np.random.randint(100, 300))
    
    # ============================================
    # PATTERN 1: Fan-Out Money Laundering
    # Çok alıcıya dağıtılmış para transferleri.
    # ============================================
    num_recipients = np.random.randint(5, 15)
    total_fraud_amount = monthly_income * np.random.randint(10, 30)
    per_recipient_amount = total_fraud_amount / num_recipients
    
    for recipient_idx in range(num_recipients):
        fraud_transactions.append({
            'transaction_id': f'FRAUD_{transaction_id_counter:08d}',
            'user_id': user_id,
            'amount': round(per_recipient_amount, 2),
            'timestamp': (fraud_date + timedelta(minutes=np.random.randint(1, 120))).isoformat(),
            'recipient_id': f'USER_{np.random.randint(0, NUM_USERS):05d}',
            'channel': np.random.choice(['Online', 'Mobile']),
            'location': city,
            'fraud_label': 1,
            'fraud_type': 'fan_out_money_laundering',
            'confidence_score': 0.95
        })
        transaction_id_counter += 1
    
    # ============================================
    # PATTERN 2: Impossible Movement (İmkansız Hareket)
    # Kısa sürede uzak lokasyonlardan yapılan işlemler.
    # ============================================
    locations = ['Istanbul', 'Tokyo', 'New York', 'London', 'Singapore']
    
    for i, loc in enumerate(locations[:np.random.randint(2, 4)]):
        fraud_transactions.append({
            'transaction_id': f'FRAUD_{transaction_id_counter:08d}',
            'user_id': user_id,
            'amount': round(monthly_income * np.random.randint(5, 15), 2),
            'timestamp': (fraud_date + timedelta(hours=i)).isoformat(),
            'recipient_id': f'USER_{np.random.randint(0, NUM_USERS):05d}',
            'channel': 'Online',
            'location': loc,
            'fraud_label': 1,
            'fraud_type': 'impossible_movement',
            'confidence_score': 0.98
        })
        transaction_id_counter += 1
    
    # ============================================
    # PATTERN 3: Rapid-Fire Bot Attack (Bot Saldırısı)
    # Saniyeler içinde ardışık küçük işlemler.
    # ============================================
    for i in range(np.random.randint(10, 30)):
        fraud_transactions.append({
            'transaction_id': f'FRAUD_{transaction_id_counter:08d}',
            'user_id': user_id,
            'amount': round(np.random.randint(50, 500), 2),
            'timestamp': (fraud_date + timedelta(seconds=i * 15)).isoformat(),
            'recipient_id': f'USER_{np.random.randint(0, NUM_USERS):05d}',
            'channel': 'Mobile',
            'location': city,
            'fraud_label': 1,
            'fraud_type': 'rapid_fire_bot',
            'confidence_score': 0.99
        })
        transaction_id_counter += 1
    
    # ============================================
    # PATTERN 4: Profile Mismatch (Profil Uyumsuzluğu)
    # Profille uyuşmayan yüksek tutarlı işlem.
    # ============================================
    if idx % 3 == 0:  # Her 3. dolandırıcı
        fraud_transactions.append({
            'transaction_id': f'FRAUD_{transaction_id_counter:08d}',
            'user_id': user_id,
            'amount': round(monthly_income * 50, 2),  # Devasa miktar
            'timestamp': (fraud_date + timedelta(days=1)).isoformat(),
            'recipient_id': f'USER_{np.random.randint(0, NUM_USERS):05d}',
            'channel': 'Crypto',
            'location': city,
            'fraud_label': 1,
            'fraud_type': 'profile_mismatch',
            'confidence_score': 0.92
        })
        transaction_id_counter += 1

print(f"✅ {len(fraud_transactions)} dolandırıcı işlem oluşturuldu")

# =============================================
# 4. TÜM İŞLEMLERİ BİRLEŞTİR VE KAYDET
#    Normal + fraud işlemleri zaman sırasına göre kaydet.
# =============================================
print("\n[İŞLEMLER BİRLEŞTİRİLİYOR...]")

all_transactions = pd.DataFrame(normal_transactions + fraud_transactions)
all_transactions = all_transactions.sort_values('timestamp').reset_index(drop=True)

# CSV'ye Kaydet
all_transactions.to_csv('data/transactions.csv', index=False)

print("\n" + "=" * 60)
print("✅ VERİ ÜRETIMI BAŞARIYLA TAMAMLANDI!")
print("=" * 60)
print(f"\n📊 ÖZET İSTATİSTİKLER:")
print(f"  • Toplam İşlem: {len(all_transactions):,}")
print(f"  • Normal İşlem: {(all_transactions['fraud_label'] == 0).sum():,}")
print(f"  • Dolandırıcı İşlem: {(all_transactions['fraud_label'] == 1).sum():,}")
print(f"  • Fraud Oranı: {(all_transactions['fraud_label'] == 1).sum() / len(all_transactions) * 100:.2f}%")

print(f"\n📁 ÇIKTI DOSYALARI:")
print(f"  • data/users.csv ({len(user_df)} satır)")
print(f"  • data/transactions.csv ({len(all_transactions)} satır)")

print(f"\n🚀 Sonraki adım: producer.py scriptini çalıştır")
print("=" * 60)
