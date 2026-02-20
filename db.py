import requests
import sqlite3
from utils import *

def get_connection():
    return sqlite3.connect(DB_FILE)

### Création des tables
def create_tables():
    connection = get_connection()
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    ### BOOKS
    query = '''CREATE TABLE IF NOT EXISTS Books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT NOT NULL,
                author TEXT,
                publish_year YEAR,
                available BOOLEAN)
            '''
    cursor.execute(query)
    print("'Books' table : done")

    ### USERS
    query = '''
                CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)
            '''
    cursor.execute(query)
    print("'Users' table : done")

    ### LOANS
    query = '''                
                CREATE TABLE IF NOT EXISTS Loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER, 
                book_id INTEGER, 
                date DATE,
                return_date DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (book_id) REFERENCES Books(book_id))
            '''
    cursor.execute(query)
    print("'Loans' table : done")

    ### TRIGGER book_loan
    query = '''
            CREATE TRIGGER IF NOT EXISTS book_loan
            AFTER INSERT ON Loans 
            BEGIN
                UPDATE Books 
                SET available = False 
                WHERE book_id = NEW.book_id;
            END
            '''

    cursor.execute(query)
    print("'update_loaned_book' trigger: done")

    ### TRIGGER book_return
    query = '''
            CREATE TRIGGER IF NOT EXISTS book_return
            AFTER UPDATE ON Loans
            WHEN NEW.return_date IS NOT NULL
            BEGIN
                UPDATE Books
                SET available = True
                WHERE book_id = NEW.book_id;
            END
            '''
    cursor.execute(query)
    print("'update_loaned_book' trigger: done")

    ###
    connection.commit()
    cursor.close()
    connection.close()
    print("Done")

### Requêtes à l'API Open Library
def fetch_books(query, limit=10):
    url = "https://openlibrary.org/search.json"
    params = {
        "q" : query,
        "limit": limit
        }    
    response = requests.get(url, params=params)
    if response.ok : 
        return response.json()['docs']
    else: 
        return []

    
### Ajout de livres à la base de données
def add_books(books):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO Books (title, author, publish_year, available) VALUES (?, ?, ?, True)"
    for book in books : 
        cursor.execute(query, [book.get("title"), book.get("author_name")[0], book.get("first_publish_year")])
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    clear_screen()
    print(StrStyle.BOLD + "Création de la base de données" + StrStyle.RESET)
    create_tables()
    while True:
        query = input("Requête à l'API Open Library : ")
        if query == "":
            break
        limit = int(input("nombre de livres à récupérer : "))
        books = fetch_books(query, limit)
        #for book in books:
        #   print(book.get("title"))
        add_books(books)
    



