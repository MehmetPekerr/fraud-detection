"""
Fraud Detection Sistemi - Configuration
"""

# ==================================================
# KAFKA AYARLARI
# ==================================================
KAFKA_CONFIG = {
    'bootstrap_servers': ['kafka:9092'],
    'topic': 'transactions',
    'group_id': 'fraud-detection-group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
}

# ==================================================
# ELASTICSEARCH AYARLARI
# ==================================================
ELASTICSEARCH_CONFIG = {
    'hosts': ['elasticsearch:9200'],
    'index_name': 'transactions',
    'alias': 'fraud-detection'
}

# ==================================================
# MACHINE LEARNING AYARLARI
# ==================================================
ML_CONFIG = {
    'model_type': 'isolation_forest',
    'contamination': 0.1,      # %10 anomali
    'n_estimators': 100,       # Karar ağaç sayısı
    'random_state': 42,
    'max_samples': 'auto'
}

# ==================================================
# VERİ AYARLARI
# ==================================================
DATA_CONFIG = {
    'num_users': 1000,
    'num_normal_transactions': 40000,
    'num_fraudsters': 50,
    'fraud_transaction_multiplier': 10
}

# ==================================================
# FEATURE AYARLARI
# ==================================================
FEATURES = [
    'amount',
    'timestamp',
    'channel',
    'location',
    'fraud_type'
]

# ==================================================
# FRAUD PATTERN'LERI
# ==================================================
FRAUD_PATTERNS = {
    'fan_out_money_laundering': {
        'description': 'Tek hesaptan birçok hesaba para transferi',
        'confidence': 0.95,
        'recipients_threshold': 5,
        'multiplier': 10
    },
    'impossible_movement': {
        'description': 'Fiziksel olarak imkansız coğrafi hareket',
        'confidence': 0.98,
        'distance_threshold': 5000,  # km
        'time_threshold': 3  # saat
    },
    'rapid_fire_bot': {
        'description': 'Bot tarafından yapılan hızlı ardışık işlemler',
        'confidence': 0.99,
        'transaction_count': 20,
        'time_window': 300  # saniye
    },
    'profile_mismatch': {
        'description': 'Kullanıcı profiline uymayan işlem',
        'confidence': 0.92,
        'amount_multiplier': 50  # Normal işlemin 50x'i
    }
}

# ==================================================
# CHANNELs
# ==================================================
TRANSACTION_CHANNELS = [
    'ATM',
    'Online',
    'Branch',
    'Mobile',
    'Crypto',
    'Wire'
]

# ==================================================
# ŞEHIRLER
# ==================================================
CITIES = [
    'Istanbul',
    'Ankara',
    'Izmir',
    'Bursa',
    'Antalya',
    'Gaziantep',
    'Konya',
    'Kayseri'
]

# ==================================================
# MESLEKLER
# ==================================================
PROFESSIONS = [
    'Mühendis',
    'Öğretmen',
    'Öğrenci',
    'Hizmetçi',
    'İşletmeci',
    'Doktor',
    'Hemşire',
    'Satışçı'
]

# ==================================================
# İNDEKS MAPPINGS
# ==================================================
INDEX_MAPPING = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
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

# ==================================================
# KIBANA QUERIES
# ==================================================
KIBANA_QUERIES = {
    "total_transactions": {
        "name": "Toplam İşlem Sayısı",
        "query": {
            "query": {"match_all": {}},
            "size": 0,
            "aggs": {
                "count": {"value_count": {"field": "transaction_id"}}
            }
        }
    },
    "fraud_rate": {
        "name": "Dolandırıcılık Oranı",
        "query": {
            "query": {"match_all": {}},
            "size": 0,
            "aggs": {
                "total": {"value_count": {"field": "transaction_id"}},
                "fraud": {
                    "filter": {"term": {"fraud_label": 1}},
                    "aggs": {"count": {"value_count": {"field": "transaction_id"}}}
                }
            }
        }
    },
    "by_location": {
        "name": "Konuma Göre Fraud",
        "query": {
            "query": {"term": {"fraud_label": 1}},
            "aggs": {
                "locations": {
                    "terms": {"field": "location", "size": 10},
                    "aggs": {
                        "count": {"value_count": {"field": "transaction_id"}},
                        "total_amount": {"sum": {"field": "amount"}}
                    }
                }
            }
        }
    },
    "by_channel": {
        "name": "Kanala Göre Fraud",
        "query": {
            "aggs": {
                "channels": {
                    "terms": {"field": "channel", "size": 10},
                    "aggs": {
                        "fraud_rate": {"avg": {"field": "fraud_label"}},
                        "count": {"value_count": {"field": "transaction_id"}}
                    }
                }
            }
        }
    },
    "high_risk": {
        "name": "Yüksek Risk İşlemleri",
        "query": {
            "query": {
                "range": {
                    "ml_fraud_score": {"gte": 0.8}
                }
            },
            "size": 100,
            "sort": [{"ml_fraud_score": {"order": "desc"}}]
        }
    }
}

if __name__ == "__main__":
    print("Fraud Detection Configuration")
    print("=" * 50)
    print(f"\nKafka: {KAFKA_CONFIG['bootstrap_servers']}")
    print(f"Elasticsearch: {ELASTICSEARCH_CONFIG['hosts']}")
    print(f"ML Model: {ML_CONFIG['model_type']}")
    print(f"Data: {DATA_CONFIG['num_users']} users, {DATA_CONFIG['num_fraudsters']} fraudsters")
    print(f"\nFraud Patterns: {len(FRAUD_PATTERNS)}")
    for pattern_name in FRAUD_PATTERNS:
        print(f"  • {pattern_name}")
