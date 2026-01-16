# 🎯 SUNUM SIRASINDA ÇALIŞTIRMASI GEREKEN KOMUTLAR

## 📁 Proje Dizinine Git

```powershell
cd C:\Users\Mehmet\visualstudio\buyukveri\fraud-detection
```

---

## 1️⃣ Docker Servislerini Başlat (Kafka, Elasticsearch, Kibana)

```powershell
docker-compose up -d
```

**Açıklama:** "4 servis başlatıyorum: Zookeeper, Kafka, Elasticsearch ve Kibana"

**Kontrol et:**

```powershell
docker-compose ps
```

**Açıklama:** "Tüm servisler çalışıyor mu kontrol ediyorum"

---

## 2️⃣ Sentetik Veri Üret

```powershell
. .\venv\Scripts\Activate.ps1
python scripts/generate_data.py
```

**Açıklama:** "29,472 bankacılık işlemi üretiyorum - bunların %5.5'i fraud işlem. 4 farklı fraud pattern var: Money Laundering, Impossible Movement, Rapid-Fire Bot, Profile Mismatch"

---

## 3️⃣ Kafka Producer - Veriyi Kafka'ya Gönder

```powershell
python scripts/producer.py
```

**Açıklama:** "Verileri Kafka'ya real-time stream olarak gönderiyorum. Her 100 işlemde progress gösterecek, yaklaşık 2-3 dakika sürer"

---

## 4️⃣ Kafka Consumer - Elasticsearch'e Yaz

**Yeni terminal aç ve:**

```powershell
cd C:\Users\Mehmet\visualstudio\buyukveri\fraud-detection
. .\venv\Scripts\Activate.ps1
python scripts/consumer.py
```

**Açıklama:** "Consumer Kafka'dan verileri okuyor, ML modeliyle anomaly tespiti yapıyor ve Elasticsearch'e yazıyor. Her 100 belgede progress göreceksiniz"

---

## 5️⃣ Kibana Dashboard - Sonuçları Göster

**Tarayıcıda:**

```
http://localhost:5601
```

**Açıklama:** "Kibana'da verileri görselleştiriyorum:"
- Sol menü → **Discover** → `transactions*` index pattern
- Fraud işlemleri filtrele: `fraud_label: 1`
- ML anomaly'ler göster: `is_anomaly: true`

---

## 6️⃣ (Opsiyonel) Elasticsearch Veri Kontrolü

```powershell
python -c "from elasticsearch import Elasticsearch; es = Elasticsearch(['http://localhost:9200']); total = es.count(index='transactions')['count']; fraud = es.count(index='transactions', body={'query': {'term': {'fraud_label': 1}}})['count']; print(f'Toplam: {total:,}'); print(f'Fraud: {fraud:,} ({fraud/total*100:.2f}%)')"
```

**Açıklama:** "Elasticsearch'teki toplam işlem ve fraud oranını gösteriyorum"

---

## 7️⃣ Test Sistemi - Health Check

```powershell
python test_system.py
```

**Açıklama:** "Tüm servislerin sağlık kontrolünü yapıyorum"

---

# 🎬 SUNUM AKIŞI ÖNERİSİ

1. **"Projeyi tanıtayım:"** README.md'yi göster
2. **"Altyapıyı başlatıyorum:"** `docker-compose up -d`
3. **"Veri üretiyorum:"** `generate_data.py`
4. **"Kafka'ya streaming başlatıyorum:"** `producer.py` (progress izle)
5. **"Consumer ML modeliyle işliyor:"** `consumer.py` (2 terminal yan yana)
6. **"Kibana'da sonuçları gösteriyorum:"** Dashboard visualizations
7. **"Fraud işlem örneği göstereyim:"** Discover'da fraud filtrele

---

# 📊 KIBANA'DA GÖSTERECEKLERİN

1. **Discover** → Tüm işlemler
2. **Filter:** `fraud_label: 1` → Sadece fraud'lar
3. **Filter:** `is_anomaly: true` → ML anomaly tespitleri
4. **Visualize** → Pie chart (fraud oranı)
5. **Tag Cloud** → Şehir dağılımı

---

# 🛑 SUNUM SONRASI KAPAT

```powershell
docker-compose down
```

---

# 💡 HOCAYA SÖYLEYEBİLECEKLERİN

## Proje Özellikleri:
- ✅ **Real-time streaming** - Kafka ile sürekli veri akışı
- ✅ **Machine Learning** - Isolation Forest ile anomaly detection
- ✅ **Scalable Architecture** - Docker containerization
- ✅ **Production-ready** - Error handling, logging, monitoring
- ✅ **Data Pipeline** - Producer → Kafka → Consumer → Elasticsearch → Kibana

## Teknik Detaylar:
- **Veri:** 29,472 sentetik bankacılık işlemi
- **Fraud Rate:** %5.61 (1,626 fraud transaction)
- **ML Accuracy:** %5.05 anomaly detection
- **4 Fraud Pattern:**
  1. Fan-Out Money Laundering (aynı anda çok kişiye para)
  2. Impossible Movement (coğrafi olarak imkansız hareketler)
  3. Rapid-Fire Bot (saniyeler içinde çok işlem)
  4. Profile Mismatch (kullanıcı profiline uymayan işlemler)

## Stack:
- **Apache Kafka:** Message streaming
- **Elasticsearch:** Search & analytics engine
- **Kibana:** Data visualization
- **Python:** Data processing & ML
- **Docker:** Containerization
- **scikit-learn:** Machine Learning (Isolation Forest)

---

**Tüm komutlar hazır! Sunum başarılar! 🚀**
