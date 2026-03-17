"""
Elasticsearch Index ve Mapping Kurulumu
"""

import requests
import json
import time

ES_URL = "http://localhost:9200"

print("=" * 60)
print("ELASTICSEARCH INDEX KURULUMU")
print("=" * 60)

# Elasticsearch hazır mı kontrol et
print("\n[1/3] Elasticsearch durumu kontrol ediliyor...")
for i in range(30):
    try:
        response = requests.get(f"{ES_URL}/_cluster/health", timeout=5)
        if response.status_code == 200:
            print("✅ Elasticsearch hazır!")
            break
    except:
        if i < 29:
            print(f"  ⏳ Bekleniyor... ({i+1}/30)")
            time.sleep(1)
        else:
            print("❌ Elasticsearch yanıt vermiyor")
            exit(1)

# Index Mapping
print("\n[2/3] Index mapping ayarlanıyor...")

index_name = "transactions"

mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "standard"
                }
            }
        },
        "index.max_result_window": 50000
    },
    "mappings": {
        "properties": {
            "transaction_id": {
                "type": "keyword",
                "ignore_above": 256
            },
            "user_id": {
                "type": "keyword",
                "ignore_above": 256
            },
            "amount": {
                "type": "float"
            },
            "timestamp": {
                "type": "date",
                "format": "strict_date_time||epoch_millis"
            },
            "recipient_id": {
                "type": "keyword",
                "ignore_above": 256
            },
            "channel": {
                "type": "keyword",
                "ignore_above": 256
            },
            "location": {
                "type": "keyword",
                "ignore_above": 256
            },
            "fraud_label": {
                "type": "integer"
            },
            "fraud_type": {
                "type": "keyword",
                "ignore_above": 256
            },
            "confidence_score": {
                "type": "float"
            },
            "ml_fraud_score": {
                "type": "float"
            },
            "ml_anomaly_score": {
                "type": "float"
            },
            "is_anomaly": {
                "type": "boolean"
            },
            "processed_at": {
                "type": "date",
                "format": "strict_date_time||epoch_millis"
            }
        }
    }
}

try:
    # Index silinmiş mi kontrol et
    response = requests.head(f"{ES_URL}/{index_name}")
    if response.status_code == 200:
        print(f"ℹ️  Index '{index_name}' zaten var")
        # Sil
        requests.delete(f"{ES_URL}/{index_name}")
        print(f"✅ Eski index silindi")
    
    # Index oluştur
    response = requests.put(
        f"{ES_URL}/{index_name}",
        json=mapping
    )
    
    if response.status_code in [200, 201]:
        print(f"✅ Index '{index_name}' oluşturuldu")
        print(f"   Shards: 1, Replicas: 0")
    else:
        print(f"❌ Hata: {response.status_code}")
        print(response.json())

except Exception as e:
    print(f"❌ Hata: {e}")
    exit(1)

# Alias oluştur
print("\n[3/3] Alias ayarlanıyor...")

alias_config = {
    "actions": [
        {
            "add": {
                "index": index_name,
                "alias": "fraud-detection"
            }
        }
    ]
}

try:
    response = requests.post(
        f"{ES_URL}/_aliases",
        json=alias_config
    )
    
    if response.status_code in [200, 201]:
        print("✅ Alias 'fraud-detection' oluşturuldu")
    else:
        print(f"❌ Hata: {response.status_code}")

except Exception as e:
    print(f"❌ Hata: {e}")

# Index bilgilerini göster
print("\n" + "=" * 60)
print("INDEX BİLGİLERİ")
print("=" * 60)

try:
    response = requests.get(f"{ES_URL}/{index_name}/_stats")
    if response.status_code == 200:
        stats = response.json()
        index_stats = stats['indices'][index_name]
        
        print(f"\n📊 İstatistikler:")
        print(f"  • Index: {index_name}")
        print(f"  • Primaries (docs): {index_stats['primaries']['docs']['count']}")
        print(f"  • Store Size: {index_stats['primaries']['store']['size_in_bytes']} bytes")
        print(f"  • Status: {response.json()}")

except Exception as e:
    print(f"ℹ️  İstatistikler henüz kullanılabilir değil (normal)")

print("\n" + "=" * 60)
print("✅ ELASTICSEARCH KURULUMU TAMAMLANDI!")
print("=" * 60)
