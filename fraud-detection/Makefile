.PHONY: help setup up down logs clean test data produce consume setup-elasticsearch setup-kibana

# Renk tanımları
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "$(BLUE)===============================================$(NC)"
	@echo "$(BLUE)Fraud Detection Sistemi - Komutlar$(NC)"
	@echo "$(BLUE)===============================================$(NC)"
	@echo ""
	@echo "$(GREEN)setup$(NC)              - Sistemi tamamen kur"
	@echo "$(GREEN)up$(NC)                 - Docker container'larını başlat"
	@echo "$(GREEN)down$(NC)               - Docker container'larını durdur"
	@echo "$(GREEN)clean$(NC)              - Sistemi temizle (veriler silinir)"
	@echo ""
	@echo "$(GREEN)data$(NC)               - Synthetic veri oluştur"
	@echo "$(GREEN)produce$(NC)            - Kafka Producer çalıştır"
	@echo "$(GREEN)consume$(NC)            - Kafka Consumer çalıştır"
	@echo ""
	@echo "$(GREEN)elasticsearch$(NC)      - Elasticsearch kurulumu"
	@echo "$(GREEN)kibana$(NC)             - Kibana kurulumu"
	@echo "$(GREEN)test$(NC)               - Sistem testi yap"
	@echo ""
	@echo "$(GREEN)logs-kafka$(NC)         - Kafka log'larını göster"
	@echo "$(GREEN)logs-elasticsearch$(NC) - Elasticsearch log'larını göster"
	@echo "$(GREEN)logs-kibana$(NC)        - Kibana log'larını göster"
	@echo ""

setup:
	@echo "$(BLUE)[1/5]$(NC) Docker container'larını başlatıyor..."
	docker-compose up -d
	@sleep 5
	@echo "$(BLUE)[2/5]$(NC) Virtual environment oluşturuluyor..."
	python -m venv venv || python3 -m venv venv
	@echo "$(BLUE)[3/5]$(NC) Bağımlılıklar yükleniyor..."
	pip install -r requirements.txt
	@echo "$(BLUE)[4/5]$(NC) Elasticsearch indexleme..."
	python scripts/setup_elasticsearch.py
	@echo "$(BLUE)[5/5]$(NC) Kibana kurulumu..."
	python scripts/setup_kibana.py
	@echo "$(GREEN)✅ Kurulum tamamlandı!$(NC)"
	@echo "URL: http://localhost:5601"

up:
	@echo "$(BLUE)Docker container'larını başlatıyor...$(NC)"
	docker-compose up -d
	@docker-compose ps

down:
	@echo "$(BLUE)Docker container'larını durduruyor...$(NC)"
	docker-compose down

clean:
	@echo "$(RED)Sistemi temizliyor (Veriler silinecek!)$(NC)"
	docker-compose down -v
	rm -rf data/*.csv
	rm -rf __pycache__/
	rm -rf scripts/__pycache__/

test:
	@echo "$(BLUE)Sistem testi yapılıyor...$(NC)"
	python test_system.py

logs:
	@docker-compose logs -f

logs-kafka:
	@docker-compose logs -f kafka

logs-elasticsearch:
	@docker-compose logs -f elasticsearch

logs-kibana:
	@docker-compose logs -f kibana

data:
	@echo "$(BLUE)Synthetic veri üretiliyor...$(NC)"
	python scripts/generate_data.py

produce:
	@echo "$(BLUE)Kafka Producer başlatılıyor...$(NC)"
	python scripts/producer.py

consume:
	@echo "$(BLUE)Kafka Consumer başlatılıyor...$(NC)"
	python scripts/consumer.py

elasticsearch:
	@echo "$(BLUE)Elasticsearch indexleme...$(NC)"
	python scripts/setup_elasticsearch.py

kibana:
	@echo "$(BLUE)Kibana kurulumu...$(NC)"
	python scripts/setup_kibana.py

# Docker desktop komutları (Mac)
docker-start:
	@open -a Docker

# Status kontrol
status:
	@echo "$(BLUE)Sistem Durumu:$(NC)"
	@docker-compose ps
	@echo ""
	@echo "$(BLUE)Elasticsearch Status:$(NC)"
	@curl -s http://localhost:9200/_cluster/health | grep -o '"status":"[^"]*"' || echo "Çalışmıyor"
	@echo ""
	@echo "$(BLUE)Kibana Status:$(NC)"
	@curl -s http://localhost:5601/api/status | grep -o '"state":"[^"]*"' || echo "Çalışmıyor"

# Hızlı başlama
quick-start:
	@echo "$(GREEN)Hızlı başlama modunda...$(NC)"
	make clean
	make up
	@sleep 5
	make data
	@echo "$(GREEN)✅ Veri oluşturuldu$(NC)"
	@echo "$(BLUE)Üç farklı terminal'de çalıştır:$(NC)"
	@echo "1. make produce"
	@echo "2. make consume"
	@echo "3. make kibana"

# URL açma (Mac/Linux)
open-kibana:
	@echo "$(BLUE)Kibana açılıyor...$(NC)"
	open http://localhost:5601 || xdg-open http://localhost:5601

open-elasticsearch:
	@echo "$(BLUE)Elasticsearch açılıyor...$(NC)"
	open http://localhost:9200 || xdg-open http://localhost:9200

# İstatistikler
stats:
	@echo "$(BLUE)Elasticsearch İstatistikleri:$(NC)"
	@curl -s http://localhost:9200/transactions/_count | python -m json.tool 2>/dev/null || echo "İstatistik alınamadı"

# Yardım mesajı
.PHONY: help
all: help
