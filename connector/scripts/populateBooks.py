import mariadb
import random
from datetime import datetime

# Database configuration
DB_CONFIG = {
        "user": "example",
        "password": "example",
        "host": "db",
        "port": 3306,
        "database": "katalog"
}

try:
    conn = mariadb.connect(**DB_CONFIG)
    cursor = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")

# Read titles from title.txt
with open('title.txt', 'r', encoding='utf-8') as file:
    titles = file.read().splitlines()

# Function to generate a random 13-digit ISBN
def generate_isbn():
    return ''.join([str(random.randint(0, 9)) for _ in range(13)])

# Function to generate a random year between 1960 and 2024
def generate_year():
    return random.randint(1960, 2024)

# Function to generate a random format
def generate_format():
    formats = ['unknown', 'hardback', 'paperback', 'ebook']
    return random.choice(formats)

# Function to generate a random number of pages between 100 and 321
def generate_pages():
    return random.randint(100, 321)

# Function to assign random authors to a book
def assign_authors():
    # 12 books with 1 author, 6 with 2 authors, 2 with 3 authors
    if len(assigned_books) < 12:
        return [random.randint(1, 12)]
    elif len(assigned_books) < 18:
        return random.sample(range(1, 13), 2)
    else:
        return random.sample(range(1, 13), 3)

# Function to assign random genres to a book
def assign_genres():
    return random.sample(range(1, 13), random.randint(1, 3))

# Insert books into the database
assigned_books = []
for title in titles:
    isbn = generate_isbn()
    release_date = generate_year()
    format = generate_format()
    pages = generate_pages()
    publisher_id = random.randint(1, 6)
    series_id = random.choice([None, 1, 2]) if len(assigned_books) < 14 else random.choice([1, 2])
    language_id = 'pl_'

    # Insert into Books table
    add_book = ("INSERT INTO Books "
                "(isbn, title, release_date, first_polish_release_date, format, publisher_id, pages, language_id, series_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_book = (isbn, title, release_date, release_date, format, publisher_id, pages, language_id, series_id)
    cursor.execute(add_book, data_book)
    book_id = cursor.lastrowid

    # Assign authors
    authors = assign_authors()
    for author_id in authors:
        add_book_author = ("INSERT INTO bookAuthors "
                          "(book_id, author_id) "
                          "VALUES (%s, %s)")
        data_book_author = (book_id, author_id)
        cursor.execute(add_book_author, data_book_author)

    # Assign genres
    genres = assign_genres()
    for genre_id in genres:
        add_book_genre = ("INSERT INTO bookGenres "
                          "(book_id, genre_id) "
                          "VALUES (%s, %s)")
        data_book_genre = (book_id, genre_id)
        cursor.execute(add_book_genre, data_book_genre)

    assigned_books.append(book_id)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
