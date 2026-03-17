"""
Fraud Detection - Kibana Dashboard Setup
Index pattern ve dashboard oluştur
"""

import requests
import json
from elasticsearch import Elasticsearch

KIBANA_URL = "http://localhost:5601"
ES_URL = "http://localhost:9200"

print("=" * 60)
print("KIBANA DASHBOARD KURULUMU")
print("=" * 60)

# =============================================
# INDEX PATTERN OLUŞTUR
# =============================================
print("\n[1/3] Index Pattern oluşturuluyor...")

index_pattern_body = {
    "attributes": {
        "title": "transactions*",
        "timeFieldName": "processed_at"
    }
}

try:
    response = requests.post(
        f"{KIBANA_URL}/api/saved_objects/index-pattern/transactions",
        json=index_pattern_body,
        headers={"kbn-xsrf": "true"}
    )
    if response.status_code in [200, 201]:
        print("✅ Index Pattern 'transactions*' oluşturuldu")
    else:
        print(f"⚠️  Index Pattern zaten var veya hata: {response.status_code}")
except Exception as e:
    print(f"❌ Index Pattern hatası: {e}")

# =============================================
# ELASTICSEARCH VERİ KONTROLÜ
# =============================================
print("\n[2/3] Elasticsearch verileri kontrol ediliyor...")

try:
    es = Elasticsearch([ES_URL])
    
    # Toplam belge sayısı
    total = es.count(index='transactions')['count']
    print(f"✅ Toplam Belge: {total:,}")
    
    # Fraud belgeler
    fraud_count = es.count(
        index='transactions',
        body={'query': {'term': {'fraud_label': 1}}}
    )['count']
    fraud_rate = (fraud_count / total * 100) if total > 0 else 0
    print(f"✅ Fraud İşlemler: {fraud_count:,} ({fraud_rate:.2f}%)")
    
    # Anomaly belgeler
    anomaly_count = es.count(
        index='transactions',
        body={'query': {'term': {'is_anomaly': True}}}
    )['count']
    anomaly_rate = (anomaly_count / total * 100) if total > 0 else 0
    print(f"✅ ML Anomaly: {anomaly_count:,} ({anomaly_rate:.2f}%)")
    
except Exception as e:
    print(f"❌ Elasticsearch bağlantı hatası: {e}")

# =============================================
# DASHBOARD BİLGİSİ
# =============================================
print("\n[3/3] Dashboard bilgisi...")
print(f"""
📊 KİBANA DASHBOARD ERİŞİM:
   URL: {KIBANA_URL}
   
🔍 YAPILACAKLAR:
   1. Sol menüden 'Discover' tıkla
   2. Index pattern: 'transactions*' seç
   3. Verileri görüntüle ve filtrele
   
📈 ÖNERİLEN VİZUALİZASYONLAR:
   • Zaman bazlı transaction sayısı (Time Series)
   • Fraud oranı (Pie Chart: fraud_label)
   • Anomaly dağılımı (Pie Chart: is_anomaly)
   • Şehir bazlı işlemler (Tag Cloud: location)
   • En yüksek tutarlar (Data Table: amount DESC)
   • ML Fraud Score dağılımı (Histogram: ml_fraud_score)
""")

print("=" * 60)
print("✅ KURULUM TAMAMLANDI!")
print("=" * 60)
