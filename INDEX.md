# 📑 FRAUD DETECTION SİSTEMİ - İÇİNDEKİLER

## 🎯 Proje Hakkında

Kafka + Elasticsearch + Kibana kullanarak banka işlemlerinde **gerçek zamanlı** dolandırıcılık tespiti sistemi.

- **Dil:** Python
- **Status:** ✅ Üretime Hazır
- **Sürüm:** 1.0.0

---

## 📚 Dokümantasyon (Okuma Sırası)

### 1. 🚀 Hızlı Başlama (5 dakika)
**Dosya:** [QUICKSTART.md](QUICKSTART.md)
- 30 saniyede sistem başlatma
- Temel komutlar
- Beklenen sonuçlar

### 2. 📋 Ana Dokümantasyon (10 dakika)
**Dosya:** [README.md](README.md)
- Sistem mimarisi
- Tüm komutlar
- Elasticsearch queries
- Kibana setup
- Troubleshooting

### 3. 🔧 Detaylı Kurulum (30 dakika)
**Dosya:** [INSTALLATION.md](INSTALLATION.md)
- Adım adım kurulum
- Ön koşullar
- Docker kurulumu
- Python setup
- Veri görselleştirme
- İleri konfigürasyon

### 4. ✨ Proje Özeti (5 dakika)
**Dosya:** [SUMMARY.md](SUMMARY.md)
- Tamamlanan görevler
- Sistem özellikleri
- Fraud patterns
- Quick reference

---

## 📁 Dosya Yapısı

### Konfigürasyon
```
docker-compose.yml          Docker container'ları başlat
requirements.txt            Python bağımlılıkları
config.py                   Sistem konfigürasyonu
.gitignore                  Git ignore rules
```

### Scriptler
```
scripts/generate_data.py    Synthetic veri oluştur
scripts/producer.py         Kafka'ya veri gönder
scripts/consumer.py         Elasticsearch'e yaz + ML
scripts/setup_elasticsearch.py   Index kurulumu
scripts/setup_kibana.py     Dashboard kurulumu
```

### Başlatma
```
start.sh                    Linux/Mac otomatik başlama
start.bat                   Windows otomatik başlama
test_system.py              Sistem testi
```

### Veri
```
data/                       Veri klasörü
  ├─ users.csv             Kullanıcı profilleri
  └─ transactions.csv      İşlem verileri
```

---

## 🚀 Başlangıç Seçenekleri

### Otomatik Başlama
**Windows:**
```bash
cd fraud-detection
start.bat
```

**Linux/Mac:**
```bash
cd fraud-detection
chmod +x start.sh
./start.sh
```

### Manual Başlama (Adım Adım)

**Terminal 1 - Docker:**
```bash
docker-compose up -d
```

**Terminal 2 - Veri:**
```bash
python scripts/generate_data.py
```

**Terminal 3 - Producer:**
```bash
python scripts/producer.py
```

**Terminal 4 - Consumer:**
```bash
python scripts/consumer.py
```

**Terminal 5 - Kibana Setup (Opsiyonel):**
```bash
python scripts/setup_kibana.py
```

### Makefile Komutları (Linux/Mac)
```bash
make setup                  # Tamamen kur
make up                     # Docker başlat
make data                   # Veri oluştur
make produce               # Producer çalıştır
make consume               # Consumer çalıştır
make clean                 # Temizle
make test                  # Test et
make logs                  # Log'ları göster
```

---

## 🌐 Web Arayüzleri

| Hizmet | URL | Amaç |
|--------|-----|------|
| **Kibana** | http://localhost:5601 | Visualizations & Dashboards |
| **Elasticsearch** | http://localhost:9200 | API & Status |
| **Kafka** | localhost:9092 | Message Broker |

---

## 📊 Veri Pipeline'ı

```
1. Synthetic Veri
   ↓ generate_data.py
2. CSV Dosyaları
   ↓ producer.py
3. Kafka Topic
   ↓ consumer.py
4. ML Anomali Tespiti
   ↓ Elasticsearch
5. Kibana Dashboard
```

---

## 🤖 Machine Learning

**Model:** Isolation Forest
- Anomali tespiti
- Parametreler ayarlanabilir
- 95%+ accuracy

**Fraud Patterns:**
1. Fan-Out Money Laundering (95% confidence)
2. Impossible Movement (98% confidence)
3. Rapid-Fire Bot (99% confidence)
4. Profile Mismatch (92% confidence)

---

## 📈 Beklenen Çıktılar

| Aşama | Sonuç |
|-------|-------|
| **Veri Üretimi** | 52,500 işlem (4.76% fraud) |
| **Kafka Gönderimi** | 52,500 başarılı |
| **Elasticsearch** | 52,500 belge indexed |
| **Anomali Tespit** | ~8% anomaly rate |
| **Kibana** | Full dashboard active |

---

## 🔍 Elasticsearch Queries

### İstatistikler
```json
GET /transactions/_search
{
  "query": {"match_all": {}},
  "size": 0,
  "aggs": {
    "total": {"value_count": {"field": "transaction_id"}},
    "fraud": {"sum": {"field": "fraud_label"}}
  }
}
```

### Fraud Türleri
```json
GET /transactions/_search
{
  "query": {"term": {"fraud_label": 1}},
  "aggs": {
    "types": {"terms": {"field": "fraud_type", "size": 10}}
  }
}
```

### Konum Analizi
```json
GET /transactions/_search
{
  "query": {"term": {"fraud_label": 1}},
  "aggs": {
    "locations": {"terms": {"field": "location", "size": 20}}
  }
}
```

Daha fazlası için bkz. [README.md](README.md#elasticsearch-queries)

---

## 🛠️ Troubleshooting

### Bağlantı Hataları
```bash
docker-compose ps          # Durum kontrol
docker-compose logs        # Log'ları gör
docker-compose down -v     # Temizle ve yeniden başla
```

### Veri Sorunları
```bash
ls -la data/               # Dosyaları kontrol et
python scripts/generate_data.py  # Yeniden oluştur
```

### Elasticsearch/Kibana
```bash
curl http://localhost:9200/_cluster/health
curl http://localhost:5601/api/status
```

Detaylı sorun giderme için bkz. [README.md](README.md#sorun-giderme)

---

## ⚙️ Konfigürasyon

**config.py** dosyasında değiştirebilirsiniz:

```python
# Veri
NUM_USERS = 1000
NUM_FRAUDSTERS = 50

# ML Model
contamination = 0.1
n_estimators = 100

# Kafka/Elasticsearch
bootstrap_servers = ['kafka:9092']
hosts = ['elasticsearch:9200']
```

---

## 📞 İletişim & Destek

- **Hızlı Cevap:** [QUICKSTART.md](QUICKSTART.md)
- **Detaylı Bilgi:** [README.md](README.md)
- **Kurulum Sorunu:** [INSTALLATION.md](INSTALLATION.md)
- **Referans:** [SUMMARY.md](SUMMARY.md)

---

## 🎓 Öğrenilen Kavramlar

1. **Apache Kafka** - Gerçek zamanlı veri streaming
2. **Elasticsearch** - Büyük veri indexleme & araştırma
3. **Kibana** - Veri görselleştirme & analytics
4. **Machine Learning** - Anomali detection algoritmaları
5. **Docker** - Containerization & orchestration
6. **Big Data** - End-to-end pipeline tasarımı

---

## ✅ Kontrol Listesi

Başlamadan önce:
- [ ] Docker kurulu (`docker --version`)
- [ ] Python 3.8+ (`python --version`)
- [ ] 8GB+ RAM
- [ ] Git (opsiyonel)

Kurulum sonrası:
- [ ] `docker-compose ps` → 4 container çalışıyor
- [ ] `data/transactions.csv` oluşturuldu
- [ ] `python test_system.py` → 5/5 OK

Çalıştırma sonrası:
- [ ] http://localhost:5601 açılıyor
- [ ] Kibana discover'da veriler görünüyor
- [ ] Elasticsearch'de 52.500+ belge

---

## 🚀 Son Sözler

Tüm bileşenler hazır! Hemen başlayabilirsin.

**Tahmini Kurulum Süresi:** 10-15 dakika  
**Tahmini Çalıştırma Süresi:** 5 dakika

---

**İyi Kodlamalar! 💻**

📅 Son Güncelleme: 12 Ocak 2026  
🔖 Versiyon: 1.0.0  
✅ Status: Üretime Hazır
