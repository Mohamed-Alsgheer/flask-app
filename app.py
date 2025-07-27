from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Set the database path relative to the project root
DATABASE = os.path.join(os.getcwd(), 'database.db')

# we want to create, update, delete, and read books 
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
init_db()


# Home page route #
@app.route('/')
def index():
    return render_template('index.html')


# Create Book Route #
@app.route('/createBook', methods=['GET', 'POST'])
def createBook():
    if request.method == 'GET':
        return render_template('createBook.html')
    
    elif request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        description = request.form['description']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, year, description) VALUES (?, ?, ?, ?)', [title, author, year, description])
        conn.commit()
        conn.close()
        
        return redirect('/viewBooks')


# View All Books Route #
@app.route('/viewBooks')
def viewBooks():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    
    return render_template('viewBooks.html', books=books)


# View Book Details Route #
@app.route('/viewBook/<int:id>')
def readBook(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', [id]).fetchone()
    conn.close()
    
    if book:
        return render_template('viewBook.html', book=book)
    else:
        return 'Book not found'
    

# Update Book Route #
@app.route('/updateBook/<int:id>', methods=['GET', 'POST'])
def updateBook(id):
    conn = get_db_connection()
    
    if request.method == 'GET':
        book = conn.execute('SELECT * FROM books WHERE id = ?', [id]).fetchone()
        conn.close()
        
        if book:
            return render_template('updateBook.html', book=book)
        else:
            return 'Book not found'
    
    elif request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        description = request.form['description']
        
        conn.execute('UPDATE books SET title = ?, author = ?, year = ?, description = ? WHERE id = ?', [title, author, year, description, id])
        conn.commit()
        conn.close()
        
        return redirect('/viewBooks')


# Delete Book Route #
@app.route('/deleteBook/<int:id>', methods=['POST'])
def deleteBook(id):
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('DELETE FROM books WHERE id = ?', [id])
        conn.commit()
        conn.close()
        return redirect('/viewBooks')


# Run the app #
if __name__ == '__main__':
    app.run()
