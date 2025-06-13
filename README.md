# NOSQL-LAB-PYTHON

Bu repository, NoSQL veritabanlarının (Redis, Hazelcast, MongoDB) performansını karşılaştırmak için geliştirilen bir laboratuvar ödevi projesini içerir. Proje, Docker konteynerleri kullanılarak kurulan veritabanlarıyla bir FastAPI uygulaması aracılığıyla test edilmiş ve Siege ile yük testi, PowerShell script’leriyle zaman testi yapılmıştır.

---

## 📖 İçindekiler
- [Proje Amacı](#proje-amaci)
- [Kurulum](#kurulum)
- [Proje Yapısı](#proje-yapisi)
- [Test Süreçleri](#test-surecleri)
- [Test Sonuçlar](#test-sonuclar)
- [Karşılaşılan Zorluklar ve Çözümler](#karsilasilan-zorluklar-ve-cozumler)
- [Tartışma](#tartisma)

---

## 📌 Proje Amacı

Bu ödevin amacı, farklı NoSQL veritabanlarının (Redis, Hazelcast, MongoDB) performansını ölçmek ve karşılaştırmaktır. Performans, 1000 istekle yük testi (Siege) ve 100 istekle zaman testi (PowerShell script’leri) kullanılarak değerlendirilmiştir. Proje, veritabanlarının okuma/yazma hızlarını ve eşzamanlı işlem kapasitelerini analiz etmeyi hedefler.

---

## ⚙️ Kurulum

### Gereksinimler
- Docker ve Docker Compose (en son sürüm)
- Python 3.8+
- PowerShell (Windows için)
- Git

### Adımlar

1. **Repository’i Klonla**:
   ```bash
   git clone hhttps://github.com/KeremTingir/nosql-lab-python.git
   cd nosql-lab-python

2. **Sanal Ortamı Kur**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate

3. **Bağımlılıkları Yükle**:
    ```bash
    pip install -r requirements.txt

4. **Docker Konteynerlerini Başlat**:
    ```bash
    docker-compose up -d

5. **Uygulamayı Çalıştır**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

---

## 🗂️ Proje Yapısı

- **Proje Dizini**
    ```bash
    NOSQL-LAB-PYTHON/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                          # FastAPI uygulaması
    │   ├── model/                           # Veri modelleri
    │   │   ├── __init__.py
    │   │   └── student.py
    │   └── store/                           # Veritabanı sınıfları
    │       ├── __init__.py
    │       ├── hazelcast_store.py
    │       ├── mongo_store.py
    │       └── redis_store.py
    ├── venv/                                # Sanal ortam klasörü
    │   ├── Include/
    │   ├── Lib/
    │   └── Scripts/
    ├── .gitignore
    ├── docker-compose.yml                  # Tüm NoSQL veritabanları için Docker tanımı
    ├── Dockerfile.siege                    # Siege için özel Dockerfile
    ├── hz-siege.results                    # Hazelcast Siege testi sonucu
    ├── hz-time.ps1                         # Hazelcast zaman testi script'i
    ├── hz-time.results                     # Hazelcast zaman testi sonucu
    ├── mongodb-siege.results               # MongoDB Siege testi sonucu
    ├── mongodb-time.ps1                    # MongoDB zaman testi script'i
    ├── mongodb-time.results                # MongoDB zaman testi sonucu
    ├── redis-siege.results                 # Redis Siege testi sonucu
    ├── redis-time.ps1                      # Redis zaman testi script'i
    ├── redis-time.results                  # Redis zaman testi sonucu
    ├── requirements.txt                    # Python bağımlılıkları
    └── README.md

---

## 🧪 Test Süreçleri

### ⚔️ Siege Testleri

- **Amaç**: 1000 istekle veritabanı performansını ölçmek.
- **Komut**: Özel `local/siege` imajı kullanılarak:
- **Bash Kodu**
    ```bash
    docker run --rm -v ${PWD}:/results local/siege -H "Accept: application/json" -c10 -r100 "http://<IP_ADRESI>:8080/nosql-lab-<db>/ogrenci_no=2025000001" > <db>-siege.results

---

## Test Sonuçları

Aşağıdaki tablo, test sonuçlarını özetler:

| Veritabanı | Siege Elapsed Time (sn) | Siege Response Time (sn) | Siege Transaction Rate (trans/sec) | Time Test Süresi (sn) |
|------------|---------------------------|--------------------------|------------------------------------|-----------------------|
| Redis      | 1.99                      | 0.02                     | 502.51                             | 0.0749879             |
| Hazelcast  | 2.09                      | 0.02                     | 478.47                             | 0.0793079             |
| MongoDB    | 17.50                     | 0.12                     | 57.14                              | 0.0921126             |

*   **Redis**: En hızlı veritabanı, düşük yanıt süresi ve yüksek işlem oranı.
*   **Hazelcast**: Redis’e yakın performans, dengeli sonuçlar.
*   **MongoDB**: Diğerlerinden çok daha yavaş, Elapsed Time ve Longest Transaction (15.86 sn) değerleri anormal.

---

## Karşılaşılan Zorluklar ve Çözümler

### Port Çakışması (6379):
*   **Sorun**: Yerel Redis kurulumunun 6379 portunu işgal etmesi.
*   **Çözüm**: `taskkill` komutu ile çakışan işlemi sonlandırdık.

### Siege İmajı Sorunu:
*   **Sorun**: `yokogawa/siege` ve `cytopia/siege` imajlarının uyumsuzluğu, Alpine’de `siege` paketinin olmaması.
*   **Çözüm**: `debian:bullseye-slim` tabanlı `Dockerfile.siege` ile özelleştirilmiş imaj oluşturuldu.

### Ağ Erişim Sorunları:
*   **Sorun**: `host.docker.internal` zaman aşımı, `localhost` ile "Connection refused" hatası.
*   **Çözüm**: `vEthernet (WSL (Hyper-V firewall))` IP adresi kullanıldı.

### PowerShell Hatası:
*   **Sorun**: `-Parallel` parametresinin PowerShell 5.1’de desteklenmemesi.
*   **Çözüm**: Script paralel olmadan çalıştırıldı, sonuçlar yine de alındı.

---

## 💬 Tartışma

### Performans Farkları
- **Redis**: Düşük yanıt süresi ve yüksek işlem oranıyla en üstün performansı sergiledi.
- **Hazelcast**: Redis’e yakın, dengeli bir performans gösterdi.
- **MongoDB**: 17.50 saniye Elapsed Time ve 15.86 saniye Longest Transaction ile diğerlerinden belirgin şekilde yavaş. Bu anomali, işlemlerin paralel gerçekleştirilememesinden kaynaklanıyor.

### Sınırlamalar
- PowerShell 5.1 kullanımı, paralel test süreçlerini etkiledi; ancak sonuçlar geçerli kabul edildi.
- MongoDB’nin düşük performansı için ek inceleme önerilir.

### İyileştirme Önerileri
- PowerShell 7.x’e geçiş yaparak paralel test performansını artırma.
- MongoDB konteyner yapılandırmasını optimize etme.
- Yazma işlemleri gibi ek test senaryoları ile kapsamlı analiz.

---