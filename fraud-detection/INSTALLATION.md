# 📚 DETAYLI KURULUM REHBERI

## 🎯 Hedef

Bu proje, Kafka üzerinden gelen banka işlemlerini **gerçek zamanlı olarak** analiz ederek:
- ✅ Dolandırıcı aktiviteleri tespit etme
- ✅ Anomali algılama (ML)
- ✅ Elasticsearch'e veri indexleme
- ✅ Kibana dashboard'unda görselleştirme

---

## 🔧 Kurulum Adımları

### 1. Ön Koşulları Kontrol Et

**Windows:**
```bash
# Git
git --version

# Python 3.8+
python --version

# Docker Desktop
docker --version
docker-compose --version
```

**Linux/Mac:**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose python3 python3-pip git
```

### 2. Projeyi Klonla veya İndir

```bash
cd c:\Users\Mehmet\visualstudio\buyukveri
```

Proje zaten orada: `fraud-detection/`

### 3. Docker Container'ları Başlat

```bash
cd fraud-detection
docker-compose up -d
```

**Kontrol et:**
```bash
docker-compose ps
```

Beklenen çıktı:
```
NAME            STATUS
zookeeper       Up 10 seconds
kafka           Up 9 seconds
elasticsearch   Up 8 seconds
kibana          Up 7 seconds
```

### 4. Python Sanal Ortamı Oluştur

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 6. Sistem Kontrol Et

```bash
python test_system.py
```

Çıktı:
```
✅ DOCKER          OK
✅ ELASTICSEARCH   OK
✅ KAFKA           OK
✅ KIBANA          OK
✅ PACKAGES        OK
```

---

## 🚀 Uygulamayı Çalıştır

### Terminal 1: Veri Üret

```bash
python scripts/generate_data.py
```

**Çıktı örneği:**
```
[1/3] Kullanıcı profilleri oluşturuluyor...
✅ 1000 kullanıcı profili oluşturuldu

[2/3] Normal işlemler oluşturuluyor...
✅ 50000 normal işlem oluşturuldu

[3/3] Dolandırıcı işlemleri oluşturuluyor...
✅ 2500 dolandırıcı işlem oluşturuldu

✅ VERİ ÜRETIMI BAŞARIYLA TAMAMLANDI!
  • Toplam İşlem: 52,500
  • Normal İşlem: 50,000
  • Dolandırıcı İşlem: 2,500
  • Fraud Oranı: 4.76%
```

### Terminal 2: Producer Çalıştır

```bash
python scripts/producer.py
```

**Çıktı örneği:**
```
✅ Kafka'ya bağlantı başarılı!
✅ 52500 işlem yüklendi

[20.0%] 10500/52500 işlem gönderildi
[40.0%] 21000/52500 işlem gönderildi
[60.0%] 31500/52500 işlem gönderildi
[80.0%] 42000/52500 işlem gönderildi
[100.0%] 52500/52500 işlem gönderildi

✅ KAFKA GÖNDERIMI BAŞARIYLA TAMAMLANDI!
```

### Terminal 3: Consumer Çalıştır

```bash
python scripts/consumer.py
```

**Çıktı örneği:**
```
✅ Elasticsearch bağlantısı başarılı!
✅ Index 'transactions' oluşturuldu
✅ ML Anomali Tespiti Modeli hazır

✅ Consumer başladı. Veriler bekleniyor...

[14:30:45] 1000 doc | Fraud: 4.75% | Anomaly: 8.23%
[14:31:15] 2000 doc | Fraud: 4.76% | Anomaly: 8.19%
[14:31:45] 3000 doc | Fraud: 4.75% | Anomaly: 8.21%
...
[14:45:30] 52500 doc | Fraud: 4.76% | Anomaly: 8.22%

✅ VERİ İŞLEME TAMAMLANDI!
```

---

## 🌐 Kibana'da Veri Görüntüleme

### 1. Kibana Aç

Browser'da aç: **http://localhost:5601**

### 2. Index Pattern Oluştur

1. Sol menüde **Analytics** → **Discover**
2. **Create data view** tıkla
3. Name: `transactions`
4. Index pattern: `transactions*`
5. Timestamp field: `timestamp`
6. **Save data view**

### 3. Verileri Görüntüle

1. **Discover** sekmesinde
2. Index: `transactions*` seç
3. **Refresh** butonuna tıkla
4. Veriler listelenmeye başlar

### 4. Visualizations Oluştur

**Örnek 1: Kanal Başına Fraud Oranı**

```
1. Analytics → Visualizations → Create visualization
2. Data: transactions
3. Visualization type: Donut
4. Buckets → Slice by: channel (Top 5 terms)
5. Split slices: fraud_label (percentage)
```

**Örnek 2: Saatlik İşlem Trend**

```
1. Create visualization
2. Type: Line chart
3. X-axis: timestamp (Date histogram, hourly)
4. Y-axis: Count of records
5. Split series: fraud_label
```

**Örnek 3: Konum Başına Fraud**

```
1. Create visualization
2. Type: Bar chart
3. X-axis: location (Top 10 terms)
4. Y-axis: Percentage of fraud_label:1
```

---

## 📊 Elasticsearch Queries (Console'da)

Kibana'da **Dev Tools** → **Console** aç ve şunları çalıştır:

### Query 1: Toplam Statistikler

```json
GET /transactions/_search
{
  "query": {"match_all": {}},
  "size": 0,
  "aggs": {
    "total_transactions": {"value_count": {"field": "transaction_id"}},
    "total_amount": {"sum": {"field": "amount"}},
    "avg_amount": {"avg": {"field": "amount"}},
    "max_amount": {"max": {"field": "amount"}},
    "min_amount": {"min": {"field": "amount"}}
  }
}
```

### Query 2: Fraud Rate

```json
GET /transactions/_search
{
  "size": 0,
  "aggs": {
    "fraud_rate": {
      "terms": {"field": "fraud_label", "size": 2},
      "aggs": {
        "count": {"value_count": {"field": "transaction_id"}}
      }
    }
  }
}
```

### Query 3: Fraud Türü Dağılımı

```json
GET /transactions/_search
{
  "query": {"term": {"fraud_label": 1}},
  "size": 0,
  "aggs": {
    "fraud_types": {
      "terms": {"field": "fraud_type", "size": 10},
      "aggs": {
        "count": {"value_count": {"field": "transaction_id"}},
        "avg_confidence": {"avg": {"field": "confidence_score"}}
      }
    }
  }
}
```

### Query 4: Konum Analizi

```json
GET /transactions/_search
{
  "query": {"term": {"fraud_label": 1}},
  "size": 0,
  "aggs": {
    "locations": {
      "terms": {"field": "location", "size": 20},
      "aggs": {
        "fraud_count": {"value_count": {"field": "transaction_id"}},
        "total_amount": {"sum": {"field": "amount"}},
        "avg_amount": {"avg": {"field": "amount"}}
      }
    }
  }
}
```

### Query 5: Kanal Analizi

```json
GET /transactions/_search
{
  "size": 0,
  "aggs": {
    "channels": {
      "terms": {"field": "channel", "size": 10},
      "aggs": {
        "total_transactions": {"value_count": {"field": "transaction_id"}},
        "fraud_transactions": {
          "filter": {"term": {"fraud_label": 1}},
          "aggs": {"count": {"value_count": {"field": "transaction_id"}}}
        },
        "fraud_rate": {"avg": {"field": "fraud_label"}}
      }
    }
  }
}
```

### Query 6: Yüksek Risk İşlemleri (ML)

```json
GET /transactions/_search
{
  "query": {
    "bool": {
      "should": [
        {"range": {"ml_fraud_score": {"gte": 0.8}}},
        {"range": {"ml_anomaly_score": {"gte": 0.7}}}
      ]
    }
  },
  "size": 50,
  "sort": [
    {"ml_fraud_score": {"order": "desc"}},
    {"timestamp": {"order": "desc"}}
  ]
}
```

### Query 7: Saatlik Trend

```json
GET /transactions/_search
{
  "size": 0,
  "aggs": {
    "transactions_per_hour": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h",
        "min_doc_count": 0
      },
      "aggs": {
        "total_amount": {"sum": {"field": "amount"}},
        "fraud_count": {
          "filter": {"term": {"fraud_label": 1}},
          "aggs": {"count": {"value_count": {"field": "transaction_id"}}}
        },
        "normal_count": {
          "filter": {"term": {"fraud_label": 0}},
          "aggs": {"count": {"value_count": {"field": "transaction_id"}}}
        }
      }
    }
  }
}
```

---

## ⚙️ Yapılandırma Dosyaları

### config.py

Ana konfigürasyon dosyası. Değiştirebilirsiniz:

```python
# Veri parametreleri
NUM_USERS = 1000
NUM_FRAUDSTERS = 50

# ML Model
contamination = 0.1  # %10 anomali

# Kafka
bootstrap_servers = ['kafka:9092']

# Elasticsearch
hosts = ['elasticsearch:9200']
```

### docker-compose.yml

Container'ları başlatır. Portları değiştirebilirsiniz:

```yaml
elasticsearch:
  ports:
    - "9200:9200"  # Elasticsearch port

kibana:
  ports:
    - "5601:5601"  # Kibana port

kafka:
  ports:
    - "9092:9092"  # Kafka port
```

---

## 🐛 Sorun Giderme

### Problem 1: "Connection refused" hatası

**Sebep:** Container'lar çalışmıyor

**Çözüm:**
```bash
docker-compose ps  # Durum kontrol et
docker-compose up -d  # Tekrar başlat
docker-compose logs elasticsearch  # Logs'ı gör
```

### Problem 2: Kafka topic bulunamadı

**Sebep:** Topic otomatik oluşturulmadı

**Çözüm:**
```bash
docker exec kafka kafka-topics --create \
  --topic transactions \
  --bootstrap-server kafka:9092 \
  --partitions 1 \
  --replication-factor 1
```

### Problem 3: Kibana verisi görmüyor

**Sebep:** Consumer çalışmıyor veya index boş

**Çözüm:**
```bash
# Consumer çalışıyor mu kontrol et
ps aux | grep consumer.py

# Elasticsearch'de kaç belge var kontrol et
curl http://localhost:9200/transactions/_count
```

### Problem 4: Python paket hatası

**Sebep:** Bağımlılıklar yüklenmedi

**Çözüm:**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📈 Beklenen Sonuçlar

**Generator Çıktısı:**
```
✅ 52,500 işlem
   • 50,000 normal
   • 2,500 fraud (%4.76)
```

**Producer Çıktısı:**
```
✅ 52,500/52,500 işlem gönderildi
```

**Consumer Çıktısı:**
```
✅ 52,500 belge işlendi
   • 2,500 fraud işlem
   • ~4,200 anomali tespit
```

**Kibana:**
```
✅ 52,500 belge indexlendi
✅ 8 fields
✅ Query zamanı: <100ms
```

---

## 📚 Öğrenilen Kavramlar

1. **Apache Kafka:** Gerçek zamanlı veri streaming
2. **Elasticsearch:** Büyük veri setlerinin indexlenmesi ve araması
3. **Kibana:** Veri görselleştirme ve analitik dashboard
4. **Machine Learning:** Isolation Forest anomali tespiti
5. **Docker:** Containerization ve microservices
6. **Big Data Pipeline:** End-to-end veri işleme

---

## 🎓 Gelişmiş Konular (İsteğe Bağlı)

### Elasticsearch Performance Tuning

```json
PUT /transactions/_settings
{
  "index": {
    "number_of_replicas": 0,
    "refresh_interval": "30s"
  }
}
```

### Kibana Custom Dashboard

1. **Canvas** aracı ile özel dashboard oluştur
2. **Alerts** kur (yüksek fraud rate'de bildirim)
3. **Reporting** ile PDF rapor oluştur

### Production Deployment

- Docker Swarm veya Kubernetes kullan
- SSL/TLS aktif et
- Monitoring (Prometheus, Grafana) ekle
- Backup stratejisi uygula

---

## 📞 İletişim & Destek

- **Belgeler:** README.md, QUICKSTART.md
- **Kod:** scripts/ klasöründe
- **Config:** config.py

---

**Başarılar! 🚀**

Son güncelleme: 12 Ocak 2026
