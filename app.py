from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'instance/to_do_app.db'

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (task) VALUES (?)', (request.form['task'],))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
