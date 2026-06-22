\# Library Management System



Bu proje, FastAPI kullanılarak geliştirilmiş bir Kütüphane Yönetim Sistemi API projesidir.



\## Özellikler



\- Kitap ekleme, listeleme, güncelleme ve silme

\- Kaggle Books Dataset içe aktarma

\- Kullanıcı kayıt ve giriş sistemi

\- JWT tabanlı kimlik doğrulama

\- Rol bazlı yetkilendirme

\- Kitap ödünç alma ve iade işlemleri

\- Kitap rezervasyon sistemi

\- Raporlama ve analitik endpointleri

\- Docker ile backend, frontend ve PostgreSQL container yapısı



\## Kullanılan Teknolojiler



\- Python

\- FastAPI

\- SQLAlchemy

\- PostgreSQL

\- SQLite

\- Docker

\- Docker Compose

\- Nginx

\- JWT Authentication



\## Proje Yapısı



```text

library-management-system/

│

├── backend/

│   ├── app/

│   │   ├── routers/

│   │   ├── data/

│   │   ├── auth.py

│   │   ├── database.py

│   │   ├── import\_books.py

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

├── .gitignore

└── README.md



Docker ile Çalıştırma



Projeyi Docker ile çalıştırmak için:



docker compose up --build



Backend API:



http://localhost:8000



Swagger API dokümantasyonu:



http://localhost:8000/docs



Frontend:



http://localhost:3000



Health check:



http://localhost:8000/health

Dataset Kullanımı



Bu projede Kaggle Books Dataset kullanılmıştır:



https://www.kaggle.com/datasets/saurabhbagchi/books-dataset



Dataset indirildikten sonra books.csv dosyası şu klasöre yerleştirilmelidir:



backend/app/data/books.csv



Dataset’i veritabanına aktarmak için:



python -m app.import\_books



Docker container içinde aktarmak için:



docker compose exec backend python -m app.import\_books


## Kullanıcı Rolleri ve Test Kullanıcısı

Bu projede kullanıcı kayıt işlemi güvenli hale getirilmiştir. Yeni kayıt olan kullanıcılar otomatik olarak `member` rolüyle oluşturulur. Kullanıcı kayıt formunda rol seçimi bulunmaz.

### Yeni Kullanıcı Oluşturma

`/auth/register` endpointi ile yeni kullanıcı oluşturma örneği:

```json
{
  "username": "member1",
  "email": "member1@example.com",
  "password": "123456"
}
```

Bu kullanıcı sistemde otomatik olarak `member` rolüyle kaydedilir.

### Giriş Yapma

`/auth/login` endpointi ile giriş örneği:

```json
{
  "username": "member1",
  "password": "123456"
}
```

Başarılı girişten sonra JWT token alınır ve frontend tarafında kullanıcının adı ve rolü görüntülenir.

### Admin Test Kullanıcısı

Frontend üzerindeki admin yetkili alanları test etmek için geliştirme ortamında aşağıdaki admin kullanıcısı kullanılmıştır:

* Kullanıcı adı: `admin3`
* Şifre: `123456`
* Rol: `admin`

Bu kullanıcı ile giriş yapıldığında frontend üzerinde `Kitap Ekle` ve `Raporlar` bölümleri görünür.

> Not: Güvenlik nedeniyle yeni kayıt olan kullanıcılar otomatik olarak `member` rolüyle oluşturulur. Temiz kurulumda admin kullanıcısı yoksa, önce normal kullanıcı oluşturulup test amacıyla veritabanı üzerinden rolü `admin` olarak güncellenmelidir.

### Rol Bazlı Görünürlük

* `member` rolündeki kullanıcılar kitap arayabilir, ödünç alma ve iade işlemlerini kullanabilir.
* `admin` ve `librarian` rolündeki kullanıcılar ek olarak `Kitap Ekle` ve `Raporlar` bölümlerini görebilir.
* Frontend tarafında admin/librarian olmayan kullanıcılara `Kitap Ekle` ve `Raporlar` panelleri gösterilmez.
* Backend tarafında yeni kayıt olan kullanıcıların rolü otomatik olarak `member` yapılır.

Geliştirici




Gülse Özdek

