from db import get_connection
from classes import *
import bcrypt

### Encodage du mot de passe

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(entry, stored):
    return bcrypt.checkpw(entry.encode('utf-8'), stored)



### Requêtes SQL 

def add_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO Users (username, password) VALUES (?, ?)"
    cursor.execute(query, (username, hash_password(password)))
    connection.commit()
    cursor.close()
    connection.close()

def get_user(username) :
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT user_id, username, password FROM Users WHERE Users.username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    print(result)
    if len(result) == 1 : 
        return User(id=result[0][0], username=result[0][1], password=result[0][2])
    return None

def add_loan(user_id, book_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO Loans (user_id, book_id, start_date, end_date, ongoing) VALUES (?, ?, date('now'), date('now', '+7 days'), True)"
    cursor.execute(query, (user_id, book_id))
    query = "UPDATE Books SET available=False WHERE book_id=?"
    cursor.execute(query, (book_id,))
    connection.commit()
    cursor.close()
    connection.close()


def get_books(filter):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT book_id, title, author, publish_year, available FROM Books " + filter.to_sql() + " ORDER BY Books.title ASC"
    print(query)
    cursor.execute(query)
    books = []
    for row in cursor.fetchall():
        print(row)
        books += [Book(id=row[0], title=row[1], author=row[2], year=row[3], status=row[4])]
    cursor.close()
    connection.close()
    return books

def get_user_books(user_id) :
    connection = get_connection()
    cursor = connection.cursor()
    query = '''
            SELECT Books.book_id, Books.title, Books.author, Books.publish_year FROM Books
            INNER JOIN Loans
            ON Books.book_id = Loans.book_id
            WHERE Loans.user_id = ? 
            ORDER BY Books.title ASC
            ''' 
    cursor.execute(query, (user_id,))
    books = []
    for row in cursor.fetchall():
        books += [Book(id=row[0], title=row[1], author=row[2], year=row[3])]
    cursor.close()
    connection.close()
    return books

def return_book(user_id, book_id) : 
    #TODO
    print("not implemented yet")
    return


""""
def return_book(userId, bookId) : 
    connection = get_connection()
    cursor = connection.cursor()
    query1 = "UPDATE Loans SET status=0 WHERE user_id=%s AND book_id=%s"
    query2 = "UPDATE Books SET status=1 WHERE id=%s"
    cursor.execute(query1, [userId, bookId])
    cursor.execute(query2, [bookId])
    connection.commit()
    cursor.close()
    connection.close()
"""   








