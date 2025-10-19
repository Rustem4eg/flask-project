import os
import csv
from urllib.parse import urlparse
import requests
from app import create_app, db
from app.models import Book, Genre

app = create_app()

COVERS_DIR = os.path.join(app.static_folder, 'covers')
os.makedirs(COVERS_DIR, exist_ok=True)

def download_cover(url, filename):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            filepath = os.path.join(COVERS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return f'covers/{filename}'
    except Exception as e:
        print(f"Не удалось скачать обложку {url}: {e}")
    return 'placeholder.jpg'

@app.cli.command()
def init_db():
    db.create_all()
    csv_path = os.path.join(os.path.dirname(__file__), 'book_catalog_sample.csv')
    if not os.path.exists(csv_path):
        print("❌ Файл book_catalog_sample.csv не найден!")
        return

    genre_cache = {}
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        books_to_add = []
        for i, row in enumerate(reader):
            genre_name = row['genre'].strip()
            if genre_name not in genre_cache:
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    genre = Genre(name=genre_name)
                    db.session.add(genre)
                    db.session.flush()
                genre_cache[genre_name] = genre
            genre = genre_cache[genre_name]

            cover_url = row['cover_url']
            cover_filename = f"book_{i+1}.jpg"
            local_cover = download_cover(cover_url, cover_filename)

            book = Book(
                title=row['title'],
                author=row['author'],
                price=float(row['price']),
                description=row['description'],
                rating=float(row['rating']) if row['rating'] else 0.0,
                year=int(row['year']) if row['year'] else None,
                cover=local_cover
            )
            book.genres.append(genre)
            books_to_add.append(book)

        db.session.add_all(books_to_add)
        db.session.commit()
    print(f"✅ Загружено {len(books_to_add)} книг и {len(genre_cache)} жанров.")

if __name__ == '__main__':
    app.run(debug=True)