import csv
import os

from .database import SessionLocal, engine, Base
from . import models

Base.metadata.create_all(bind=engine)

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "books.csv")


def clean_text(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def clean_year(value):
    try:
        year = int(str(value).strip())
        if 0 < year <= 2026:
            return year
    except:
        return None
    return None


def get_column(row, *names):
    for name in names:
        if name in row:
            return row[name]
    return None


def import_books():
    db = SessionLocal()

    if not os.path.exists(CSV_PATH):
        print("books.csv bulunamadı:", CSV_PATH)
        return

    existing_isbns = {
        item[0] for item in db.query(models.Book.isbn).all()
    }

    added_count = 0
    skipped_count = 0
    batch = []

    with open(CSV_PATH, "r", encoding="latin-1", errors="ignore") as file:
        sample = file.read(4096)
        file.seek(0)

        delimiter = ";" if sample.count(";") > sample.count(",") else ","

        reader = csv.DictReader(file, delimiter=delimiter)

        for row in reader:
            isbn = clean_text(get_column(row, "ISBN", "isbn"))
            title = clean_text(get_column(row, "Book-Title", "title", "Title"))
            author = clean_text(get_column(row, "Book-Author", "author", "Author"))
            publisher = clean_text(get_column(row, "Publisher", "publisher"))
            publication_year = clean_year(
                get_column(row, "Year-Of-Publication", "publication_year", "year")
            )

            if not isbn or not title or not author:
                skipped_count += 1
                continue

            if isbn in existing_isbns:
                skipped_count += 1
                continue

            book = models.Book(
                isbn=isbn,
                title=title,
                author=author,
                publisher=publisher,
                publication_year=publication_year,
                total_copies=1,
                available_copies=1
            )

            batch.append(book)
            existing_isbns.add(isbn)
            added_count += 1

            if len(batch) >= 1000:
                db.bulk_save_objects(batch)
                db.commit()
                batch = []
                print(f"{added_count} kitap aktarıldı...")

    if batch:
        db.bulk_save_objects(batch)
        db.commit()

    db.close()

    print("Aktarma tamamlandı.")
    print("Eklenen kitap sayısı:", added_count)
    print("Atlanan kayıt sayısı:", skipped_count)


if __name__ == "__main__":
    import_books()