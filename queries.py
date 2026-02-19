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
    query = '''
            INSERT INTO Users (username, password) 
            VALUES (?, ?)
            '''
    cursor.execute(query, (username, hash_password(password)))
    connection.commit()
    cursor.close()
    connection.close()

def get_user(username) :
    connection = get_connection()
    cursor = connection.cursor()
    query = '''
            SELECT user_id, username, password 
            FROM Users 
            WHERE Users.username = ?
            '''
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(result) == 1 : 
        return User(id=result[0][0], username=result[0][1], password=result[0][2])
    return None

def add_loan(user_id, book_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = '''
            INSERT INTO Loans (user_id, book_id, date) 
            VALUES (?, ?, date('now'))
            '''
    cursor.execute(query, (user_id, book_id))
    connection.commit()
    cursor.close()
    connection.close()


def get_books():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT book_id, title, author, publish_year, available FROM Books ORDER BY Books.title ASC"
    cursor.execute(query)
    books = []
    for row in cursor.fetchall():
        books += [Book(id=row[0], title=row[1], author=row[2], year=row[3], status=row[4])]
    cursor.close()
    connection.close()
    return books

def get_loans(user_id) :
    connection = get_connection()
    cursor = connection.cursor()
    query = '''
            SELECT UsrLoans.loan_id, UsrLoans.date, Books.book_id, Books.title, Books.author, Books.publish_year 
            FROM (
                SELECT * 
                FROM Loans 
                WHERE return_date IS NULL
                        AND Loans.user_id = ?
                ) as UsrLoans
            INNER JOIN Books
            ON Books.book_id = UsrLoans.book_id
            ORDER BY Books.title ASC
            ''' 
    cursor.execute(query, (user_id,))
    loans = []
    for row in cursor.fetchall():
        loans += [Loan(row[0], row[1], Book(id=row[2], title=row[3], author=row[4], year=row[5]))]
    cursor.close()
    connection.close()
    return loans

def return_book(loan_id) : 
    connection = get_connection()
    cursor = connection.cursor()
    query = '''
            UPDATE Loans
            SET return_date = date('now')
            WHERE Loans.loan_id = ? 
            '''
    cursor.execute(query, (loan_id,))
    connection.commit()
    cursor.close()
    connection.close()









