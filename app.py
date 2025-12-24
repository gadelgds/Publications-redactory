from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@app.route('/articles')
def articles():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute("SELECT * FROM articles ORDER BY date DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('articles.html', articles=articles)

@app.route('/articles/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if title and content:
            conn = sqlite3.connect('articles.db')
            c = conn.cursor()
            c.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            return redirect('/articles')
    
    return render_template('create.html')

@app.route('/articles/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        c.execute("UPDATE articles SET title=?, content=? WHERE id=?", (title, content, id))
        conn.commit()
        conn.close()
        return redirect('/articles')
    
    c.execute("SELECT * FROM articles WHERE id=?", (id,))
    article = c.fetchone()
    conn.close()
    
    if article:
        return render_template('edit.html', article=article)
    else:
        return "Статья не найдена", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)