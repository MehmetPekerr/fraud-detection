@echo off
REM Fraud Detection Sistemi - Otomatik Başlatma (Windows)

echo ==================================================
echo FRAUD DETECTION SISTEM BASLATILIYOR...
echo ==================================================

REM =====================================================
REM 1. Docker Container'larini Basla
REM =====================================================
echo.
echo [1/6] Docker container'lari baslatiliyor...
docker-compose up -d

echo Bekleniyor...
timeout /t 10 /nobreak

REM =====================================================
REM 2. Python Ortamini Kontrol Et
REM =====================================================
echo.
echo [2/6] Python ortami kontrol ediliyor...
if not exist "venv" (
    echo Virtual environment olusturuluyor...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM =====================================================
REM 3. Bagliliklar Yukle
REM =====================================================
echo.
echo [3/6] Bagliliklar yukleniyor...
pip install -q -r requirements.txt

REM =====================================================
REM 4. Veri Olustur
REM =====================================================
echo.
echo [4/6] Synthetic veri uretiliyor...
python scripts\generate_data.py

REM =====================================================
REM 5. Kafka Producer Calistir
REM =====================================================
echo.
echo [5/6] Kafka Producer baslatiliyor...
start /B python scripts\producer.py

timeout /t 5 /nobreak

REM =====================================================
REM 6. Consumer + Elasticsearch Kurulumu
REM =====================================================
echo.
echo [6/6] Consumer + Elasticsearch baslatiliyor...
start /B python scripts\consumer.py

REM Setup Kibana
timeout /t 5 /nobreak
python scripts\setup_kibana.py

echo.
echo ==================================================
echo OK SISTEM BASARIYLA KURULDU!
echo ==================================================

echo.
echo WEB ARAYUZLERI:
echo   - Kibana:      http://localhost:5601
echo   - Elasticsearch: http://localhost:9200

echo.
echo SONRAKI ADIMLAR:
echo   1. Kibana acin: http://localhost:5601
echo   2. Index Pattern olusturun: transactions*
echo   3. Discover sekmesinde verileri gorun
echo   4. Visualizations olusturun
echo   5. Dashboard hazirlayin

echo.
echo SISTEMI DURDURMAK ICIN:
echo   docker-compose down -v

echo.
echo ==================================================
echo Komut satirina donuluyor...
echo ==================================================
