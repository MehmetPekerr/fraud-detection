"""
Sistem Kontrol Aracı - Tüm Bileşenleri Test Et
"""

import subprocess
import requests
import time
from kafka import KafkaAdminClient, KafkaClient
from kafka.admin import NewTopic

print("=" * 60)
print("FRAUD DETECTION SİSTEMİ KONTROL")
print("=" * 60)

# Kontrol sonuçları
results = {}

# =====================================================
# 1. Docker Kontrol
# =====================================================
print("\n[1/5] Docker kontrol ediliyor...")

try:
    result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Docker kurulu")
        results['docker'] = True
    else:
        print("❌ Docker kurulu değil")
        results['docker'] = False
except:
    print("❌ Docker bulunamadı")
    results['docker'] = False

# =====================================================
# 2. Elasticsearch Kontrol
# =====================================================
print("\n[2/5] Elasticsearch kontrol ediliyor...")

try:
    response = requests.get("http://localhost:9200/_cluster/health", timeout=5)
    if response.status_code == 200:
        health = response.json()
        print(f"✅ Elasticsearch çalışıyor")
        print(f"   Status: {health['status']}")
        print(f"   Nodes: {health['number_of_nodes']}")
        results['elasticsearch'] = True
    else:
        print(f"❌ Elasticsearch yanıt hatası: {response.status_code}")
        results['elasticsearch'] = False
except Exception as e:
    print(f"❌ Elasticsearch bağlanamadı: {e}")
    results['elasticsearch'] = False

# =====================================================
# 3. Kafka Kontrol
# =====================================================
print("\n[3/5] Kafka kontrol ediliyor...")

try:
    admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'], client_id='test-client')
    
    # Topic'i kontrol et
    topics = admin_client.list_topics()
    
    print("✅ Kafka çalışıyor")
    print(f"   Topics: {len(topics)}")
    
    if 'transactions' in topics:
        print("✅ Topic 'transactions' mevcut")
    else:
        print("⚠️  Topic 'transactions' bulunamadı (oluşturulması gerekiyor)")
    
    results['kafka'] = True
    admin_client.close()
    
except Exception as e:
    print(f"❌ Kafka bağlanamadı: {str(e)}")
    results['kafka'] = False

# =====================================================
# 4. Kibana Kontrol
# =====================================================
print("\n[4/5] Kibana kontrol ediliyor...")

try:
    response = requests.get("http://localhost:5601/api/status", timeout=5)
    if response.status_code == 200:
        print("✅ Kibana çalışıyor")
        results['kibana'] = True
    else:
        print(f"❌ Kibana yanıt hatası: {response.status_code}")
        results['kibana'] = False
except Exception as e:
    print(f"❌ Kibana bağlanamadı: {e}")
    results['kibana'] = False

# =====================================================
# 5. Python Paketleri Kontrol
# =====================================================
print("\n[5/5] Python paketleri kontrol ediliyor...")

required_packages = {'pandas': 'pandas', 'numpy': 'numpy', 'kafka': 'kafka', 'elasticsearch': 'elasticsearch', 'scikit-learn': 'sklearn'}
missing_packages = []

for package, import_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"✅ {package} kurulu")
    except ImportError:
        print(f"❌ {package} kurulu değil")
        missing_packages.append(package)

results['packages'] = len(missing_packages) == 0

# =====================================================
# ÖZET
# =====================================================
print("\n" + "=" * 60)
print("KONTROL ÖZETI")
print("=" * 60)

all_ok = all(results.values())

for service, status in results.items():
    symbol = "✅" if status else "❌"
    print(f"{symbol} {service.upper():20s} {'OK' if status else 'PROBLEM'}")

print("\n" + "=" * 60)

if all_ok:
    print("✅ SİSTEM HAZIR! Başlatabilirsiniz.")
    print("\n🚀 Başlatmak için:")
    print("   python scripts/generate_data.py")
    print("   python scripts/producer.py")
    print("   python scripts/consumer.py  (farklı terminal)")
else:
    print("❌ PROBLEM VAR! Yukarıdaki hataları düzelt.")
    print("\n💡 Yardım:")
    if not results.get('elasticsearch'):
        print("   • Elasticsearch başlat: docker-compose up -d elasticsearch")
    if not results.get('kafka'):
        print("   • Kafka başlat: docker-compose up -d kafka zookeeper")
    if not results.get('kibana'):
        print("   • Kibana başlat: docker-compose up -d kibana")
    if not results.get('packages'):
        print(f"   • Paket yükle: pip install {' '.join(missing_packages)}")

print("=" * 60)
