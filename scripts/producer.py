# -*- coding: utf-8 -*-
"""
Fraud Detection Sistemi - Kafka Producer
CSV'deki işlemleri Kafka 'transactions' topic'ine akıtır.
"""

import json
import pandas as pd
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

print("=" * 60)
print("KAFKA PRODUCER BAŞLANIYOR...")
print("=" * 60)

# Kafka Producer Bağlantısı
try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all',
        retries=3,
        request_timeout_ms=30000,
        api_version=(0, 10)
    )
    print("✅ Kafka'ya bağlantı başarılı!")
except Exception as e:
    print(f"❌ Kafka bağlantı hatası: {e}")
    print("\n💡 Docker container'lar çalışıyor mu? Kontrol et:")
    print("   docker-compose up -d")
    exit(1)

# Veri Yükle
try:
    transactions = pd.read_csv('data/transactions.csv')
    print(f"✅ {len(transactions)} işlem yüklendi")
except FileNotFoundError:
    print("❌ data/transactions.csv bulunamadı!")
    print("   Önce: python scripts/generate_data.py çalıştır")
    exit(1)

print("\n" + "=" * 60)
print("VERİLER KAFKA'YA GÖNDERILIYOR...")
print("=" * 60)

# Kafka'ya Gönder
success_count = 0
error_count = 0
batch_size = 1000

for idx, row in transactions.iterrows():
    try:
        # Veri Hazırla (CSV satırını JSON mesaja çevir)
        message = {
            'transaction_id': str(row['transaction_id']),
            'user_id': str(row['user_id']),
            'amount': float(row['amount']),
            'timestamp': str(row['timestamp']),
            'recipient_id': str(row['recipient_id']),
            'channel': str(row['channel']),
            'location': str(row['location']),
            'fraud_label': int(row['fraud_label']),
            'fraud_type': str(row['fraud_type']) if pd.notna(row['fraud_type']) else None,
            'confidence_score': float(row['confidence_score'])
        }
        
        # Kafka Topic'e Gönder
        future = producer.send('transactions', value=message, partition=0)
        record_metadata = future.get(timeout=30)
        
        success_count += 1
        
        # Progress Bar (her batch'te bir göster)
        if (idx + 1) % batch_size == 0:
            percentage = ((idx + 1) / len(transactions)) * 100
            print(f"  [{percentage:5.1f}%] {idx + 1:6d}/{len(transactions)} işlem gönderildi")
        
        # Simülasyon: gerçek zamanlı akış gibi hız ayarla
        if idx % 100 == 0:
            time.sleep(0.1)  # Her 100 işlemde 100ms bekle
    
    except Exception as e:
        error_count += 1
        print(f"❌ Hata (işlem {idx}): {e}")

# Producer'ı Kapat
producer.flush(timeout=10)
producer.close()

print("\n" + "=" * 60)
print("✅ KAFKA GÖNDERIMI BAŞARIYLA TAMAMLANDI!")
print("=" * 60)
print(f"\n📊 ÖZET:")
print(f"  • Başarılı: {success_count:,}")
print(f"  • Hata: {error_count:,}")
print(f"  • Başarı Oranı: {(success_count / len(transactions) * 100):.2f}%")

print(f"\n🚀 Sonraki adım: consumer.py scriptini çalıştır")
print("=" * 60)
