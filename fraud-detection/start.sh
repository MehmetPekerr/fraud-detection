#!/bin/bash
# Fraud Detection Sistemi - Otomatik Başlatma Betiği

echo "=================================================="
echo "FRAUD DETECTION SISTEM BAŞLATILIYOR..."
echo "=================================================="

# Renk tanımları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# =====================================================
# 1. Docker Container'ları Başlat
# =====================================================
echo -e "\n${YELLOW}[1/6] Docker container'ları başlatılıyor...${NC}"
docker-compose up -d

# Container'ların hazır olmasını bekle
echo "Bekleniyor..."
sleep 10

# =====================================================
# 2. Python Ortamını Kontrol Et
# =====================================================
echo -e "\n${YELLOW}[2/6] Python ortamı kontrol ediliyor...${NC}"
if [ ! -d "venv" ]; then
    echo "Virtual environment oluşturuluyor..."
    python -m venv venv
fi

# Activate venv
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# =====================================================
# 3. Bağımlılıkları Yükle
# =====================================================
echo -e "\n${YELLOW}[3/6] Bağımlılıklar yükleniyor...${NC}"
pip install -q -r requirements.txt

# =====================================================
# 4. Veri Oluştur
# =====================================================
echo -e "\n${YELLOW}[4/6] Synthetic veri üretiliyor...${NC}"
python scripts/generate_data.py

# =====================================================
# 5. Kafka Producer Çalıştır
# =====================================================
echo -e "\n${YELLOW}[5/6] Kafka Producer başlatılıyor...${NC}"
timeout 30 python scripts/producer.py &
sleep 5

# =====================================================
# 6. Consumer + Elasticsearch Kurulumu
# =====================================================
echo -e "\n${YELLOW}[6/6] Consumer + Elasticsearch başlatılıyor...${NC}"
python scripts/consumer.py &
CONSUMER_PID=$!

# Setup Kibana
sleep 5
python scripts/setup_kibana.py

echo -e "\n${GREEN}=================================================="
echo "✅ SİSTEM BAŞARIYLA KURULDU!"
echo "==================================================${NC}"

echo -e "\n${GREEN}🌐 KIBANA ARAYÜZÜ:${NC}"
echo "  http://localhost:5601"

echo -e "\n${GREEN}📊 ELASTICSEARCH:${NC}"
echo "  http://localhost:9200"

echo -e "\n${GREEN}📡 KAFKA BROKER:${NC}"
echo "  localhost:9092"

echo -e "\n${YELLOW}💡 SONRAKI ADIMLAR:${NC}"
echo "  1. Kibana arayüzüne gidin: http://localhost:5601"
echo "  2. Index Pattern oluşturun: transactions*"
echo "  3. Discover sekmesinde verileri görüntüleyin"
echo "  4. Visualizations oluşturun"
echo "  5. Dashboard'lar hazırlayın"

echo -e "\n${YELLOW}🛑 SİSTEMİ DURDURMAK İÇİN:${NC}"
echo "  docker-compose down -v"

echo -e "\n${GREEN}=================================================="
echo "Consumer çalışıyor (PID: $CONSUMER_PID)"
echo "Durdurmak için: Ctrl+C"
echo "==================================================${NC}\n"

# Consumer'ı ön planda çalıştır
wait $CONSUMER_PID
