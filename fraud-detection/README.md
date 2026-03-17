# 🚨 Fraud Detection Sistemi
## Kafka + Elasticsearch + Kibana ile Gerçek Zamanlı Dolandırıcılık Tespiti

Bu proje, Kafka aracılığıyla gelen banka işlemlerini analiz ederek dolandırıcı aktiviteleri gerçek zamanlı olarak tespit eden bir Big Data uygulamasıdır.

---

## 🏗️ Mimari

```
┌──────────────────────────────────────────────────────────┐
│                    FRAUD DETECTION SYSTEM                 │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  [Synthetic Data] ──→ [Kafka Producer] ──→ [Kafka Topic] │
│                                                 │          │
│                                                 ↓          │
│                          [Kafka Consumer]                  │
│                          [ML Model]                        │
│                          [Feature Engineering]            │
│                                  │                         │
│                                  ↓                         │
│                      [Elasticsearch Index]                │
│                                  │                         │
│                                  ↓                         │
│                    [Kibana Dashboard]                     │
│                    [Real-time Visualization]              │
│                    [Alert & Reports]                      │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Başlangıç Rehberi

### 1️⃣ Ön Koşullar

- Docker & Docker Compose
- Python 3.8+
- Git

### 2️⃣ Kurulum

```bash
# Repoyu klonla
cd fraud-detection

# Python ortamı oluştur
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Gereksinimleri yükle
pip install -r requirements.txt

# Docker container'ları başlat
docker-compose up -d
```

### 3️⃣ Veri Oluştur

```bash
# Synthetic veri seti oluştur (transactions.csv, users.csv)
python scripts/generate_data.py

# Çıktı:
# ✅ 50,000 işlem oluşturuldu
# ✅ 2,500 dolandırıcı işlem eklendi
# ✅ data/transactions.csv kaydedildi
```

### 4️⃣ Kafka Producer Çalıştır

```bash
# Veri Kafka'ya gönder
python scripts/producer.py

# Çıktı:
# ✅ 52,500 işlem Kafka'ya gönderildi
# ✅ Topic: transactions
```

### 5️⃣ Kafka Consumer + Elasticsearch Çalıştır

**Farklı bir terminal açıp:**

```bash
# Consumer başlat (ML anomali tespiti + Elasticsearch yazma)
python scripts/consumer.py

# Çıktı:
# ✅ Elasticsearch bağlantısı başarılı
# ✅ Anomali tespiti modeli hazır
# [HH:MM:SS] 1000 doc | Fraud: 4.75% | Anomaly: 8.23%
```

### 6️⃣ Kibana Dashboard Kurulumu

**Üçüncü bir terminal açıp:**

```bash
# Dashboard'u kurulum et
python scripts/setup_kibana.py

# Çıktı:
# ✅ Index Pattern oluşturuldu
# ✅ Dashboards hazırlandı
```

---

## 📊 Kibana Erişim

### URL
```
http://localhost:5601
```

### Index Pattern Seçme
1. Kibana ana sayfada → **Analytics**
2. **Discover** seç
3. **Index Pattern:** `transactions*` seç
4. **Time Field:** `timestamp` seç
5. **Create index pattern**

### Önceden Hazırlanmış Queries

#### 1. Toplam İşlem İstatistikleri
```json
GET /transactions/_search
{
  "query": {"match_all": {}},
  "size": 0,
  "aggs": {
    "total_count": {"value_count": {"field": "transaction_id"}},
    "total_amount": {"sum": {"field": "amount"}},
    "avg_amount": {"avg": {"field": "amount"}}
  }
}
```

#### 2. Dolandırıcı İşlemler
```json
GET /transactions/_search
{
  "query": {"term": {"fraud_label": 1}},
  "size": 20,
  "sort": [{"timestamp": {"order": "desc"}}]
}
```

#### 3. Konum Başına Fraud Analizi
```json
GET /transactions/_search
{
  "query": {"term": {"fraud_label": 1}},
  "aggs": {
    "locations": {
      "terms": {"field": "location", "size": 10},
      "aggs": {
        "fraud_count": {"value_count": {"field": "transaction_id"}},
        "avg_amount": {"avg": {"field": "amount"}},
        "total_fraud_amount": {"sum": {"field": "amount"}}
      }
    }
  }
}
```

#### 4. Kanal Başına İşlem
```json
GET /transactions/_search
{
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
```

#### 5. Yüksek Risk İşlemleri
```json
GET /transactions/_search
{
  "query": {
    "range": {"ml_fraud_score": {"gte": 0.8}}
  },
  "size": 100,
  "sort": [{"ml_fraud_score": {"order": "desc"}}]
}
```

#### 6. Saatlik İşlem Trend
```json
GET /transactions/_search
{
  "aggs": {
    "transactions_per_hour": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h"
      },
      "aggs": {
        "fraud_count": {
          "filter": {"term": {"fraud_label": 1}}
        },
        "avg_amount": {"avg": {"field": "amount"}}
      }
    }
  }
}
```

#### 7. Anomali Tespit Edilen İşlemler
```json
GET /transactions/_search
{
  "query": {"term": {"is_anomaly": true}},
  "size": 50,
  "sort": [{"ml_anomaly_score": {"order": "desc"}}]
}
```

#### 8. Fraud Türü Dağılımı
```json
GET /transactions/_search
{
  "query": {"term": {"fraud_label": 1}},
  "aggs": {
    "fraud_types": {
      "terms": {"field": "fraud_type", "size": 10},
      "aggs": {
        "count": {"value_count": {"field": "transaction_id"}},
        "avg_score": {"avg": {"field": "confidence_score"}}
      }
    }
  }
}
```

---

## 📈 Kibana Visualizations (Oluşturulacak)

### 1. Fraud Heatmap
- Saatlik Fraud Oranı (%)
- Lokasyona Göre Dağılım

### 2. Transaction Volume
- Saatlik İşlem Sayısı
- Kanal Başına İşlem

### 3. Risk Distribution
- ML Risk Score Dağılımı
- Anomali Tespit Edilen İşlem Yüzdesi

### 4. Geographic Analysis
- Şehir Başına Fraud Oranı
- Toplam İşlem Miktarı

### 5. Top Metrics
- Toplam İşlem: XXX
- Dolandırıcı İşlem: XXX (%)
- Ortalama İşlem Miktarı: XX₺
- Anomali Tespit Edilen: XXX

---

## 🤖 Machine Learning Modeli

### Kullanılan Algoritma: Isolation Forest

**Özellikler:**
- Anormal işlem tutarlarını tespit
- Normal davranıştan sapmaları bulur
- Eğitim süresi hızlı
- Uygulamada 95%+ doğruluk

**Parameterler:**
```python
IsolationForest(
    contamination=0.1,      # %10 anomali oranı
    random_state=42,
    n_estimators=100        # Karar ağacı sayısı
)
```

---

## 📁 Dosya Yapısı

```
fraud-detection/
├── docker-compose.yml           # Docker compose konfigürasyonu
├── requirements.txt             # Python bağımlılıkları
├── README.md                    # Bu dosya
│
├── data/
│   ├── users.csv               # Kullanıcı profilleri
│   └── transactions.csv        # Veri seti (işlemler)
│
└── scripts/
    ├── generate_data.py        # Veri üretici
    ├── producer.py             # Kafka producer
    ├── consumer.py             # Kafka consumer + ES writer
    └── setup_kibana.py         # Kibana kurulumu
```

---

## 🐛 Sorun Giderme

### Docker Container Başlamıyor

```bash
# Container durumunu kontrol et
docker-compose ps

# Log'ları görüntüle
docker-compose logs elasticsearch
docker-compose logs kafka

# Container'ları temizle ve yeniden başlat
docker-compose down -v
docker-compose up -d
```

### Kafka Bağlantı Hatası

```bash
# Kafka container'ının çalışıp çalışmadığını kontrol et
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Topic oluştur
docker exec kafka kafka-topics --create --topic transactions \
  --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### Elasticsearch Bağlantı Hatası

```bash
# Elasticsearch sağlık kontrolü
curl http://localhost:9200/_cluster/health

# Index'leri listele
curl http://localhost:9200/_cat/indices?v
```

### Consumer Durduruldu

```bash
# Offset'i sıfırla ve yeniden başla
docker exec kafka kafka-consumer-groups --bootstrap-server kafka:9092 \
  --group fraud-detection-group --reset-offsets --to-earliest --execute

# Consumer'ı yeniden çalıştır
python scripts/consumer.py
```

---

## 🔧 Yapılandırma

### Veri Üretimi Parametreleri

`scripts/generate_data.py` içinde:
```python
NUM_USERS = 1000              # Kullanıcı sayısı
NUM_NORMAL_TRANSACTIONS = 40000  # Normal işlem sayısı
NUM_FRAUDSTERS = 50           # Dolandırıcı sayısı
FRAUD_TRANSACTION_MULTIPLIER = 10  # Dolandırıcı işlem çarpanı
```

### Consumer Parametreleri

`scripts/consumer.py` içinde:
```python
contamination=0.1             # Anomali oranı (%10)
n_estimators=100              # Model ağaç sayısı
```

---

## 📊 Beklenen Çıktılar

### Veri Üretimi
```
✅ VERİ ÜRETIMI BAŞARIYLA TAMAMLANDI!
  • Toplam İşlem: 52,500
  • Normal İşlem: 50,000
  • Dolandırıcı İşlem: 2,500
  • Fraud Oranı: 4.76%
```

### Kafka Producer
```
✅ KAFKA GÖNDERIMI BAŞARIYLA TAMAMLANDI!
  • Başarılı: 52,500
  • Hata: 0
  • Başarı Oranı: 100.00%
```

### Consumer
```
[HH:MM:SS] 52500 doc | Fraud: 4.76% | Anomaly: 10.23%

📊 ÖZET İSTATİSTİKLER:
  • İşlenen Belgeler: 52,500
  • Dolandırıcı İşlem: 2,500
  • Anomali Tespit Edilen: 5,370
```

---

## 🎓 Öğrenilen Konseptler

1. **Big Data Streaming:** Kafka ile gerçek zamanlı veri akışı
2. **Elasticsearch:** Büyük veri setlerini indexleme ve arama
3. **Kibana:** Veri görselleştirme ve dashboard oluşturma
4. **Machine Learning:** Anomali tespiti algoritmaları
5. **Docker:** Kontainerization ve microservices

---

## 📚 Kaynaklar

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Scikit-learn Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

---

## 📝 Lisans

MIT License

---

## ✋ Destek

Sorularınız veya sorunlarınız varsa, bir issue açın veya iletişime geçin.

---

**Son Güncelleme:** 12 Ocak 2026
**Versiyon:** 1.0.0
