# Library Management System

Bu proje, FastAPI, PostgreSQL, Docker ve modern bir frontend arayüzü kullanılarak geliştirilmiş bir **Kütüphane Yönetim Sistemi** projesidir.

Sistem; kullanıcı kaydı, kullanıcı girişi, rol tabanlı erişim kontrolü, kitap yönetimi, kitap ödünç alma/iade, rezervasyon, işlem geçmişi, son teslim tarihi takibi ve raporlama özelliklerini desteklemektedir.

---

## Proje Özellikleri

### Kullanıcı Yönetimi

* Kullanıcı kaydı
* Kullanıcı girişi
* Kullanıcı çıkışı
* JWT tabanlı kimlik doğrulama
* Güvenli parola saklama
* Parolaların hashlenerek veritabanında tutulması
* Rol tabanlı erişim kontrolü

Desteklenen roller:

* `admin` = Yönetici
* `librarian` = Kütüphaneci
* `student` = Öğrenci

Yeni kayıt olan kullanıcılar otomatik olarak `student` rolüyle oluşturulur. Kullanıcı kayıt formunda rol seçimi bulunmaz.

---

## Kitap Yönetim Sistemi

Yetkili kullanıcılar (`admin` ve `librarian`) aşağıdaki işlemleri yapabilir:

* Kitap ekleme
* Kitap bilgilerini güncelleme
* Kitap silme
* Kitap arama
* Kitap uygunluk durumunu görüntüleme

Normal kullanıcılar (`student`) kitapları arayabilir ve uygunluk durumunu görüntüleyebilir fakat kitap ekleyemez, güncelleyemez veya silemez.

Kitap arama sistemi şu alanlara göre çalışmaktadır:

* Kitap başlığı
* ISBN
* Yazar
* Yayınevi

Kitap kartlarında şu bilgiler gösterilir:

* ISBN
* Kitap adı
* Yazar
* Yayınevi
* Yayın yılı
* Toplam kopya
* Mevcut kopya
* Uygunluk durumu

Uygunluk durumu:

* `available_copies > 0` ise kitap **Müsait**
* `available_copies = 0` ise kitap **Müsait değil**

---

## Ödünç Alma ve İade Sistemi

Sistem aşağıdaki işlemleri destekler:

* Kitap ödünç alma
* Kitap iade etme
* Geçmiş işlemleri görüntüleme
* Son teslim tarihlerini takip etme
* Gecikmiş kitapları takip etme

Ödünç alma kuralları:

* Kullanıcı giriş yapmadan kitap ödünç alamaz.
* Kitap ödünç alındığında `BorrowTransaction` kaydı oluşturulur.
* Kitabın `available_copies` değeri 1 azalır.
* `available_copies` hiçbir zaman 0’ın altına düşmez.
* Aynı kullanıcı aynı kitabı aktif olarak ikinci kez ödünç alamaz.
* Kitap müsait değilse kullanıcı rezervasyon oluşturabilir.

Aynı kullanıcı aynı kitabı tekrar ödünç almaya çalışırsa sistem şu hatayı döndürür:

```text
You already borrowed this book
```

Kitap müsait değilse sistem şu hatayı döndürür:

```text
Book is not available. You can create a reservation.
```

İade kuralları:

* Kullanıcı ödünç aldığı kitabı iade edebilir.
* İade işleminde transaction durumu `returned` yapılır.
* `return_date` güncellenir.
* Kitabın `available_copies` değeri 1 artar.
* `available_copies`, `total_copies` değerini geçemez.
* Zaten iade edilmiş bir işlem tekrar iade edilemez.

Zaten iade edilmiş işlem tekrar iade edilmeye çalışılırsa sistem şu hatayı döndürür:

```text
This book has already been returned
```

Frontend tarafında kullanıcılar **Ödünç Geçmişim** bölümünden geçmiş işlemlerini görebilir. Bu bölümde kitap adı, ISBN, yazar, ödünç alma tarihi, son teslim tarihi, iade tarihi ve durum bilgileri gösterilir.

---

## Rezervasyon Sistemi

Bir kitap mevcut değilse kullanıcı rezervasyon oluşturabilir.

Rezervasyon kuralları:

* Kullanıcı giriş yapmadan rezervasyon oluşturamaz.
* Kullanıcı yalnızca `available_copies = 0` olan kitaplar için rezervasyon oluşturabilir.
* Kitap müsaitse rezervasyon oluşturulamaz.
* Aynı kullanıcı aynı kitap için ikinci aktif/pending rezervasyon oluşturamaz.
* Rezervasyon durumu takip edilir.
* Kullanıcı kendi rezervasyonlarını görüntüleyebilir.
* Kullanıcı aktif rezervasyonunu iptal edebilir.
* İptal edilen rezervasyon yeni rezervasyon oluşturmaya engel olmaz.

Rezervasyon durumları:

* `active` veya `pending` = Aktif rezervasyon
* `cancelled` = İptal edildi
* `fulfilled` = Tamamlandı

Kitap müsaitken rezervasyon oluşturulmaya çalışılırsa sistem şu hatayı döndürür:

```text
Book is available, reservation is not needed
```

Aynı kullanıcı aynı kitap için tekrar aktif rezervasyon oluşturmaya çalışırsa sistem şu hatayı döndürür:

```text
You already have an active or pending reservation for this book
```

Frontend tarafında kullanıcılar **Rezervasyonlarım** bölümünden rezervasyonlarını görüntüleyebilir.

---

## Raporlama ve Analitik

Sistem aşağıdaki raporları destekler:

* En çok ödünç alınan kitaplar
* Aktif kullanıcılar
* Ödünç alınmış kitaplar
* Gecikmiş kitaplar
* Aylık ödünç alma istatistikleri

Raporlar yalnızca `admin` ve `librarian` rollerine sahip kullanıcılar tarafından görüntülenebilir. `student` rolündeki kullanıcılar raporları göremez.

Yetkisiz kullanıcı rapor endpointlerine erişmeye çalışırsa sistem şu hatayı döndürür:

```text
You do not have permission to perform this action.
```

Frontend tarafında raporlar modern kart/tablo yapısı ile gösterilmektedir.

---

## Kullanılan Teknolojiler

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* SQLite
* Docker
* Docker Compose
* Nginx
* HTML
* CSS
* JavaScript
* JWT Authentication
* Git
* GitHub

---

## Proje Klasör Yapısı

```text
library-management-system/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── books.py
│   │   │   ├── auth.py
│   │   │   ├── borrow.py
│   │   │   ├── reservations.py
│   │   │   └── reports.py
│   │   ├── data/
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── import_books.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── Dockerfile
│   └── index.html
│
├── docker-compose.yml
├── README.md
├── .gitignore
└── .dockerignore
```

---

## Dataset Kullanımı

Projede Kaggle üzerinde bulunan Books Dataset kullanılmıştır.

Dataset bağlantısı:

```text
https://www.kaggle.com/datasets/saurabhbagchi/books-dataset
```

Dataset indirildikten sonra `books.csv` dosyası şu klasöre yerleştirilmelidir:

```text
backend/app/data/books.csv
```

Dataset’i veritabanına aktarmak için:

```bash
python -m app.import_books
```

Docker container içinde aktarmak için:

```bash
docker compose exec backend python -m app.import_books
```

Import işlemi sonucunda proje veritabanına 271.378 kitap aktarılmıştır.

---

## Docker ile Çalıştırma

Projeyi çalıştırmak için:

```bash
docker compose up --build
```

Arka planda çalıştırmak için:

```bash
docker compose up --build -d
```

Containerları durdurmak için:

```bash
docker compose down
```

> Not: `docker compose down -v` komutu veritabanı volume’unu siler. Bu komut çalıştırılırsa veritabanındaki kullanıcılar, kitap importları ve test verileri silinebilir.

---

## Uygulama Adresleri

Frontend:

```text
http://localhost:3000
```

Backend API:

```text
http://localhost:8000
```

Swagger API dokümantasyonu:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

Beklenen çıktı:

```json
{
  "status": "ok"
}
```

---

## API Endpointleri

### Auth Endpointleri

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Books Endpointleri

```text
POST   /books/
GET    /books/
GET    /books/{isbn}
PUT    /books/{isbn}
DELETE /books/{isbn}
```

### Borrow / Return Endpointleri

```text
POST /borrow
POST /return
GET  /borrow/history
```

### Reservation Endpointleri

```text
POST   /reservations/
GET    /reservations/
DELETE /reservations/{reservation_id}
```

### Reports Endpointleri

```text
GET /reports/
GET /reports/most-borrowed-books
GET /reports/active-users
GET /reports/borrowed-books
GET /reports/overdue-books
GET /reports/monthly-borrow-stats
```

---

## Test Kullanıcıları

### Öğrenci Kullanıcı

Yeni kayıt olan kullanıcılar otomatik olarak `student` rolüyle oluşturulur.

Örnek kayıt isteği:

```json
{
  "username": "student1",
  "email": "student1@example.com",
  "password": "123456"
}
```

Giriş örneği:

```json
{
  "username": "student1",
  "password": "123456"
}
```

`student` rolündeki kullanıcılar:

* Kitap arayabilir.
* Kitap uygunluk durumunu görüntüleyebilir.
* Kitap ödünç alabilir.
* Kitap iade edebilir.
* Ödünç geçmişini görüntüleyebilir.
* Rezervasyon oluşturabilir.
* Kendi rezervasyonlarını görüntüleyebilir.

Ancak `student` kullanıcılar:

* Kitap ekleyemez.
* Kitap güncelleyemez.
* Kitap silemez.
* Raporları görüntüleyemez.

### Admin Test Kullanıcısı

Frontend üzerindeki yetkili alanları test etmek için geliştirme ortamında aşağıdaki admin kullanıcısı kullanılmıştır:

* Kullanıcı adı: `admin3`
* Şifre: `123456`
* Rol: `admin`

Bu kullanıcı ile giriş yapıldığında frontend üzerinde şu bölümler görünür:

* Kitap Ekle
* Kitap Güncelle
* Kitap Sil
* Raporlar

> Not: Temiz kurulumda admin kullanıcısı yoksa önce normal kullanıcı oluşturulup test amacıyla veritabanı üzerinden rolü `admin` veya `librarian` olarak güncellenmelidir.

---

## Rol Bazlı Erişim Kontrolü

Yetkili kullanıcılar:

* `admin`
* `librarian`

Normal kullanıcı:

* `student`

`admin` ve `librarian` rolleri:

* Kitap ekleyebilir.
* Kitap güncelleyebilir.
* Kitap silebilir.
* Raporları görüntüleyebilir.

`student` rolü:

* Kitap arayabilir.
* Kitap ödünç alabilir.
* Kitap iade edebilir.
* Rezervasyon oluşturabilir.
* Kendi geçmiş işlemlerini görüntüleyebilir.

Yetkisiz erişimlerde sistem şu hata mesajını döndürür:

```text
You do not have permission to perform this action.
```

---

## Test Edilen Senaryolar

Proje geliştirme sürecinde aşağıdaki senaryolar test edilmiştir:

* Kullanıcı kaydı yapıldı.
* Kullanıcı girişi yapıldı.
* JWT token ile korumalı endpointlere erişildi.
* Yeni kayıt olan kullanıcının otomatik `student` rolü aldığı doğrulandı.
* Student kullanıcının Kitap Ekle, Güncelle, Sil ve Raporlar bölümlerini göremediği doğrulandı.
* Admin kullanıcının Kitap Ekle, Güncelle, Sil ve Raporlar bölümlerini görebildiği doğrulandı.
* Başlığa göre kitap arama test edildi.
* ISBN’e göre kitap arama test edildi.
* Yazara göre kitap arama test edildi.
* Yayınevine göre kitap arama test edildi.
* Kitap uygunluk durumu görüntülendi.
* Müsait kitap ödünç alındı.
* Kitap ödünç alındığında `available_copies` değerinin azaldığı doğrulandı.
* Aynı kullanıcının aynı kitabı ikinci kez aktif olarak ödünç alamadığı doğrulandı.
* Kitap iade edildi.
* İade sonrası `available_copies` değerinin arttığı doğrulandı.
* Aynı transaction’ın ikinci kez iade edilemediği doğrulandı.
* Kullanıcının ödünç geçmişini görebildiği doğrulandı.
* Son teslim tarihi ve gecikme durumu görüntülendi.
* Stokta olmayan kitap için rezervasyon oluşturuldu.
* Müsait kitap için rezervasyon oluşturulmasının engellendiği doğrulandı.
* Aynı kullanıcı tarafından aynı kitap için tekrar aktif rezervasyon oluşturulmasının engellendiği doğrulandı.
* Rezervasyon iptali test edildi.
* Raporlama endpointleri test edildi.
* Docker ile backend, frontend ve database containerlarının çalıştığı doğrulandı.

---

## GitHub Bağlantısı

```text
https://github.com/gulseozdek2018-debug/library-management-system
```

---

## Geliştirici

**Gülse Özdek**
