import requests
import sqlite3

API_URL = "https://www.googleapis.com/books/v1/volumes?q=python"


def fetch_books():
    try:
        response=requests.get(API_URL, timeout=10)
        
        if response.status_code !=200:
            print("Failed to fetch", response.status_code)
            
        data =response.json()
        
        items = data.get("items")

        if not items or not isinstance(items, list):
           print("No book items found in API response")
           return []

        return items
    
    except requests.exceptions.RequestException as e:
        print("API req failed", e)
        return []
    
    
def val_books(books):
    valid_books = []

    for book in books:
        volume = book.get("volumeInfo", {})

        title = volume.get("title")
        authors = volume.get("authors")
        published_date = volume.get("publishedDate")

        if not title or not authors or not published_date:
            continue

        author = authors[0]  

        try:
            year = int(published_date[:4])
        except:
            continue

        valid_books.append((title, author, year))

    return valid_books



def create_database():
    conn=sqlite3.connect("books.db")
    cursor=conn.cursor()
    
    cursor.execute("""
                   
                   CREATE TABLE IF NOT EXISTS books(
                       
                       if INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       author TEXT NOT NULL,
                       publication_year INTEGER,
                       UNIQUE(title,author)
                       )
                   
                   """)
    
    conn.commit()
    conn.close()
    
def insert_books(books):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT OR IGNORE INTO books (title, author, publication_year) VALUES (?, ?, ?)",
        books
    )

    conn.commit()
    conn.close()
    
def display_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, author, publication_year FROM books")
    rows = cursor.fetchall()

    conn.close()

    print("\nStored Books:\n")
    for title, author, year in rows:
        print(f"Title: {title} | Author: {author} | Year: {year}")

def main():


    create_database()

    raw_books = fetch_books()
    clean_books = val_books(raw_books)
    print("Books fetched:", len(raw_books))
    print("Books after validation:", len(clean_books))


    if clean_books:
        insert_books(clean_books)

    display_books()


if __name__ == "__main__":
    main()
