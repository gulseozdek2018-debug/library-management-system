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

Test Kullanıcısı



Örnek admin kullanıcı oluşturmak için /auth/register endpointi kullanılabilir:



{

&#x20; "username": "admin2",

&#x20; "email": "admin2@example.com",

&#x20; "password": "123456",

&#x20; "role": "admin"

}



Giriş için:



{

&#x20; "username": "admin2",

&#x20; "password": "123456"

}

Geliştirici



Gülse Özdek

