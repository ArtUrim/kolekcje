import mariadb
import sys

def connect_to_db():
    try:
        conn = mariadb.connect(
            user="example",
            password="example",
            host="kolekcje-db-1",
            port=3306,
            database="katalog"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

def get_all_books_with_details(conn):
    """Get all books with their details including authors, publisher, and series"""
    try:
        cur = conn.cursor()
        query = """
        SELECT 
            b.title,
            GROUP_CONCAT(a.name) as authors,
            p.name as publisher,
            b.release_date,
            s.name as series_name
        FROM Books b
        LEFT JOIN bookAuthors ba ON b.id = ba.book_id
        LEFT JOIN Authors a ON ba.author_id = a.id
        LEFT JOIN publisher p ON b.publisher_id = p.id
        LEFT JOIN series s ON b.series_id = s.id
        GROUP BY b.id, b.title, p.name, b.release_date, s.name
        """
        cur.execute(query)
        results = cur.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error: {e}")
        return None

def get_books_in_series(conn):
    """Get only books that belong to a series"""
    try:
        cur = conn.cursor()
        query = """
        SELECT 
            b.title,
            GROUP_CONCAT(a.name) as authors,
            p.name as publisher,
            b.release_date,
            s.name as series_name
        FROM Books b
        INNER JOIN series s ON b.series_id = s.id
        LEFT JOIN bookAuthors ba ON b.id = ba.book_id
        LEFT JOIN Authors a ON ba.author_id = a.id
        LEFT JOIN publisher p ON b.publisher_id = p.id
        GROUP BY b.id, b.title, p.name, b.release_date, s.name
        """
        cur.execute(query)
        results = cur.fetchall()
        return results
    except mariadb.Error as e:
        print(f"Error: {e}")
        return None

def display_results(results):
    """Display the query results in a formatted way"""
    if not results:
        print("No results found")
        return

    print("\n{:<50} {:<30} {:<20} {:<15} {:<20}".format(
        "Title", "Author(s)", "Publisher", "Release Date", "Series Name"))
    print("-" * 135)
    print("-" * 135)

    for row in results:
        title, authors, publisher, release_date, series_name = row
        # Handle NULL values
        authors = authors if authors else "Unknown"
        publisher = publisher if publisher else "Unknown"
        release_date = release_date if release_date else "Unknown"
        series_name = series_name if series_name else "N/A"

        print("{:<50} {:<30} {:<20} {:<15} {:<20}".format(
            title[:47] + "..." if len(title) > 47 else title,
            authors[:27] + "..." if len(authors) > 27 else authors,
            publisher[:17] + "..." if len(publisher) > 17 else publisher,
            release_date,
            series_name[:17] + "..." if len(series_name) > 17 else series_name
        ))

def main():
    conn = connect_to_db()
    if not conn:
        return

    try:
        while True:
            print("\nBook Catalog Query System")
            print("1. Show all books with details")
            print("2. Show only books in series")
            print("3. Exit")

            choice = input("\nEnter your choice (1-3): ")

            if choice == "1":
                results = get_all_books_with_details(conn)
                display_results(results)
            elif choice == "2":
                results = get_books_in_series(conn)
                display_results(results)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
