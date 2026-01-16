# 🚀 HIZLI BAŞLAMA REHBERI

## ⚡ 30 Saniyede Başla

### Windows
```bash
cd fraud-detection
start.bat
```

### Linux / Mac
```bash
cd fraud-detection
chmod +x start.sh
./start.sh
```

---

## 📋 Adım Adım

### 1. Docker Başlat
```bash
docker-compose up -d
```

**Beklenen:** Zookeeper, Kafka, Elasticsearch, Kibana çalışıyor

### 2. Venv Oluştur
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 4. Veri Oluştur
```bash
python scripts/generate_data.py
```

**Çıktı:**
```
✅ VERİ ÜRETIMI BAŞARIYLA TAMAMLANDI!
  • Toplam İşlem: 52,500
  • Normal İşlem: 50,000
  • Dolandırıcı İşlem: 2,500
```

### 5. Kafka Producer Çalıştır
```bash
python scripts/producer.py
```

**Çıktı:**
```
✅ KAFKA GÖNDERIMI BAŞARIYLA TAMAMLANDI!
  • Başarılı: 52,500
```

### 6. Consumer Çalıştır (Yeni Terminal)
```bash
python scripts/consumer.py
```

**Çıktı:**
```
✅ Consumer başladı. Veriler bekleniyor...
[14:30:45] 1000 doc | Fraud: 4.75% | Anomaly: 8.23%
```

### 7. Kibana Dashboard (Üçüncü Terminal)
```bash
python scripts/setup_kibana.py
```

**Çıktı:**
```
✅ KİBANA DASHBOARD KURULUMU TAMAMLANDI!
🌐 URL: http://localhost:5601
```

---

## 🌐 Web Arayüzleri

| Hizmet | URL | Kullanıcı Adı | Şifre |
|--------|-----|---------------|-------|
| **Kibana** | http://localhost:5601 | - | - |
| **Elasticsearch** | http://localhost:9200 | - | - |
| **Kafka** | localhost:9092 | - | - |

---

## 🔍 Kibana'da Veri Görüntüleme

### 1. Index Pattern Oluştur
- **Kibana** → **Management** → **Index Patterns**
- **Create index pattern**
- Pattern: `transactions*`
- Time field: `timestamp`
- **Create**

### 2. Discover
- **Analytics** → **Discover**
- Index: `transactions*`
- Verileri görmek için Refresh butonuna tıkla

### 3. Visualizations
```json
// Örnek: Kanal Başına Fraud Oranı
GET /transactions/_search
{
  "aggs": {
    "channels": {
      "terms": {"field": "channel", "size": 10},
      "aggs": {
        "fraud_pct": {"avg": {"field": "fraud_label"}}
      }
    }
  }
}
```

---

## ⚠️ Yaygın Sorunlar

### Problem: "Connection refused"
```bash
# Docker container'ları kontrol et
docker-compose ps

# Logs'ları görüntüle
docker-compose logs elasticsearch
```

### Problem: "Kafka topic not found"
```bash
# Topic oluştur
docker exec kafka kafka-topics --create --topic transactions \
  --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
```

### Problem: "Index not found"
- Veri Producer'ından Elasticsearch'e yazılmıştır
- Consumer'ın çalışıp çalışmadığını kontrol et
- Consumer log'ında `✅ 1000 doc` gibi sayı görülmeli

---

## 📊 Beklenen Sonuçlar

**Dolandırıcılık Oranı:** ~4-5%
**Anomali Tespit Oranı:** ~8-10%
**İşlem Başarısı:** 99-100%

---

## 🛑 Sistemi Durdur

```bash
# Tüm container'ları kapat
docker-compose down

# Verileri de sil (temiz başlama)
docker-compose down -v
```

---

## 💡 İpuçları

- **Real-time Monitoring:** Consumer'ı her zaman çalıştırmaya devam et
- **Kibana Refresh:** Dashboard'u düzenli refresh et
- **Log'ları Takip Et:** Producer ve Consumer çıktılarını izle
- **Veri Ölçeğini Artır:** `generate_data.py`'de NUM_USERS parametresini değiştir

---

## ✅ Kontrol Listesi

- [ ] Docker kurulu (`docker --version`)
- [ ] Python 3.8+ kurulu (`python --version`)
- [ ] Repo klonlandı (`cd fraud-detection`)
- [ ] Requirements yüklendi (`pip install -r requirements.txt`)
- [ ] Docker container'ları çalışıyor (`docker-compose ps`)
- [ ] Veri oluşturuldu (`data/transactions.csv` var mı?)
- [ ] Kafka'ya veri gönderildi (producer çalıştı mı?)
- [ ] Consumer çalışıyor (Elasticsearch yazıyor mu?)
- [ ] Kibana açılabiliyor (http://localhost:5601)
- [ ] Index pattern oluşturuldu (`transactions*`)

---

**Tamamlandı! 🎉 Sistem hazır.**

Sorularınız varsa README.md'yi kontrol edin.
