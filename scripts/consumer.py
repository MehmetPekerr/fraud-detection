"""
Fraud Detection Sistemi - Kafka Consumer + Elasticsearch Writer
Kafka 'transactions' topic'inden veriyi alır, ML anomaly skoru ekler, Elasticsearch'e yazar.
"""

import json
import pandas as pd
import numpy as np
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime
import time
import warnings

warnings.filterwarnings('ignore')

# ML libraries - optional
try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import IsolationForest
    HAS_ML = True
except ImportError:
    HAS_ML = False
    print("⚠️  scikit-learn kullanılamıyor (ML devre dışı)")

print("=" * 60)
print("KAFKA CONSUMER + ELASTICSEARCH WRITER BAŞLANIYOR...")
print("=" * 60)

# =============================================
# ELASTICSEARCH BAĞLANTISI
# ES hazır mı kontrol et, değilse çık.
# =============================================
try:
    es = Elasticsearch(['http://localhost:9200'])
    es.info()
    print("✅ Elasticsearch bağlantısı başarılı!")
except Exception as e:
    print(f"❌ Elasticsearch bağlantı hatası: {e}")
    exit(1)

# =============================================
# INDEX OLUŞTUR
# =============================================
index_name = "transactions"

# Index Mapping
mapping = {
    "mappings": {
        "properties": {
            "transaction_id": {"type": "keyword"},
            "user_id": {"type": "keyword"},
            "amount": {"type": "float"},
            "timestamp": {"type": "date"},
            "recipient_id": {"type": "keyword"},
            "channel": {"type": "keyword"},
            "location": {"type": "keyword"},
            "fraud_label": {"type": "integer"},
            "fraud_type": {"type": "keyword"},
            "confidence_score": {"type": "float"},
            "ml_fraud_score": {"type": "float"},
            "ml_anomaly_score": {"type": "float"},
            "is_anomaly": {"type": "boolean"},
            "processed_at": {"type": "date"}
        }
    }
}

if es.indices.exists(index=index_name):
    print(f"ℹ️  Index '{index_name}' zaten var")
else:
    es.indices.create(index=index_name, body=mapping)
    print(f"✅ Index '{index_name}' oluşturuldu")

# =============================================
# KAFKA CONSUMER
# Kafka'ya abone ol, earliest offset'ten oku.
# =============================================
try:
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='fraud-detection-final',
        enable_auto_commit=True,
        session_timeout_ms=60000,
        max_poll_records=500,
        request_timeout_ms=90000
    )
    print("✅ Kafka Consumer bağlantısı başarılı!")
except Exception as e:
    print(f"❌ Kafka bağlantı hatası: {e}")
    exit(1)

print("\n" + "=" * 60)
print("KAFKA'DAN VERİ OKUNUYOR...")
print("=" * 60)

# =============================================
# ISOLATION FOREST MODELİ
# Basit tek-feature (amount) modeli eğit, skorla.
# =============================================
if HAS_ML:
    # Örnek veri ile model eğit
    transactions_df = pd.read_csv('data/transactions.csv')
    amounts = transactions_df['amount'].values.reshape(-1, 1)
    
    scaler = StandardScaler()
    amounts_scaled = scaler.fit_transform(amounts)
    
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    iso_forest.fit(amounts_scaled)
    print("✅ ML Anomali Tespiti Modeli hazır")
else:
    iso_forest = None
    scaler = None
    print("ℹ️  ML modeli devre dışı (scikit-learn yok)")

# =============================================
# VERİ İŞLEME DÖNGÜSÜ
# Kafka'dan batch pull, ML skorla, ES'ye yaz, ilerleme raporla.
# =============================================
doc_count = 0
fraud_count = 0
anomaly_count = 0
empty_polls = 0
MAX_EMPTY_POLLS = 60  # 60 * 5 saniye = 5 dakika

try:
    print("\n✅ Consumer başladı. Veriler bekleniyor...\n")
    
    while True:
        messages = consumer.poll(timeout_ms=5000, max_records=500)
        
        if not messages:
            empty_polls += 1
            if empty_polls >= MAX_EMPTY_POLLS:
                print(f"\n✅ Tüm veriler işlendi. Toplam: {doc_count} belge")
                break
            continue
        
        empty_polls = 0
        
        for topic_partition, records in messages.items():
            for message in records:
                try:
                    data = message.value
                    
                    # ML Anomali Skoru Hesapla (IsolationForest varsa)
                    ml_anomaly_score = 0.0
                    is_anomaly = False
                    ml_fraud_score = float(data.get('confidence_score', 0))
                    
                    if iso_forest is not None:
                        try:
                            amount_scaled = scaler.transform([[float(data['amount'])]])
                            anomaly_pred = iso_forest.predict(amount_scaled)[0]
                            anomaly_score = iso_forest.score_samples(amount_scaled)[0]
                            
                            is_anomaly = anomaly_pred == -1
                            ml_anomaly_score = 1.0 / (1.0 + np.exp(-(-anomaly_score)))
                        except:
                            pass
                    
                    # Elasticsearch Document
                    doc = {
                        'transaction_id': data.get('transaction_id'),
                        'user_id': data.get('user_id'),
                        'amount': float(data.get('amount', 0)),
                        'timestamp': data.get('timestamp'),
                        'recipient_id': data.get('recipient_id'),
                        'channel': data.get('channel'),
                        'location': data.get('location'),
                        'fraud_label': int(data.get('fraud_label', 0)),
                        'fraud_type': data.get('fraud_type'),
                        'confidence_score': float(data.get('confidence_score', 0)),
                        'ml_fraud_score': ml_fraud_score,
                        'ml_anomaly_score': ml_anomaly_score,
                        'is_anomaly': is_anomaly,
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    # Elasticsearch'e Yazma
                    es.index(index=index_name, body=doc)
                    
                    doc_count += 1
                    if data.get('fraud_label') == 1:
                        fraud_count += 1
                    if is_anomaly:
                        anomaly_count += 1
                    
                    # Progress
                    if doc_count % 100 == 0:
                        fraud_rate = (fraud_count / doc_count) * 100
                        anomaly_rate = (anomaly_count / doc_count) * 100
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {doc_count:6d} doc | "
                              f"Fraud: {fraud_rate:5.2f}% | Anomaly: {anomaly_rate:5.2f}%")
                
                except Exception as e:
                    print(f"❌ Belge işleme hatası: {e}")

except KeyboardInterrupt:
    print("\n⏹️  Consumer durduruldu (Ctrl+C)")
except Exception as e:
    print(f"❌ Consumer hatası: {e}")

finally:
    consumer.close()

# =============================================
# ÖZET
# =============================================
print("\n" + "=" * 60)
print("✅ VERİ İŞLEME TAMAMLANDI!")
print("=" * 60)

try:
    es_count = es.count(index=index_name)['count']
    fraud_rate = (fraud_count / doc_count * 100) if doc_count > 0 else 0
    anomaly_rate = (anomaly_count / doc_count * 100) if doc_count > 0 else 0
    
    print(f"\n📊 ÖZET İSTATİSTİKLER:")
    print(f"  • İşlenen Belgeler: {doc_count}")
    print(f"  • Dolandırıcı İşlem: {fraud_count} ({fraud_rate:.2f}%)")
    print(f"  • Anomali Tespit Edilen: {anomaly_count} ({anomaly_rate:.2f}%)")
    
    print(f"\n🔍 ELASTICSEARCH INDEX:")
    print(f"  • Index: {index_name}")
    print(f"  • Belge Sayısı: {es_count}")
    
    print(f"\n📊 Kibana Dashboard'u görüntülemek için:")
    print(f"  • http://localhost:5601")
except:
    pass

print("=" * 60)
