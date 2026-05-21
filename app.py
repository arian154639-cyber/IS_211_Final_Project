from flask import Flask, render_template, redirect, session, request, g
import sqlite3

app = Flask(__name__)

app.secret_key = '5c3163dddf232f6684f8a176de1157124073ebbc8f94a44c9d5c90a49b1f9338'

DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def main_controller():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard_controller():
    error = None

    try:
        db = get_db()

        posts = db.execute('SELECT * FROM posts ORDER BY post_date DESC').fetchall()

        return render_template('dashboard_page.html', posts=posts, error=error)
    
    except Exception: 
        error='Error detected. Please try again.'
        return render_template('dashboard_page.html', posts=[], error=error)

def valid_login(username, password):
    return username == 'admin' and password == 'password'

@app.route('/login', methods=['GET', 'POST'])
def login_controller():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if valid_login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            error = 'Invalid username/password.'

    return render_template('login_form.html', error=error)

@app.route('/logout')
def logout_controller():
    session.pop('username', None)
    return redirect('/dashboard')

@app.route('/create', methods=['GET', 'POST'])
def create_controller():
    if 'username' not in session:
        return redirect('/login')
    error = None

    try:
        if request.method == 'POST':
            title = request.form['post_title']
            author = request.form['post_author']
            content = request.form['post_content']

            if not title or not author or not content:    
                error = 'Missing required field.'  
                return render_template('create.html', error=error)
            
            db = get_db()

            db.execute(
                'INSERT INTO posts (post_title, post_author, post_content) VALUES (?, ?, ?)',
                (title, author, content)
            )
            
            db.commit()

            return redirect('/dashboard')

    except Exception:
        error = 'Error detected. Please try again.'
        return render_template('create.html', error=error)

    return render_template('create.html', error=error)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_controller(post_id):
    if 'username' not in session:
        return redirect('/login')
    error = None

    try:
        db = get_db()

        post = db.execute('SELECT * FROM posts WHERE post_id = ?', (post_id,)).fetchone()

        if request.method == 'POST':
            title = request.form['post_title']
            author = request.form['post_author']
            content = request.form['post_content']

            if not title or not author or not content:
                error = 'Missing required field.'
                return render_template('edit.html', post=post, error=error)

            db.execute(
                'UPDATE posts SET post_title = ?, post_date = CURRENT_TIMESTAMP, post_author = ?, post_content = ? WHERE post_id = ?',
                (title, author, content, post_id)
            )

            db.commit()

            return redirect('/dashboard')

    except Exception:
        error = 'Error detected. Please try again.'
        return render_template('edit.html', post=post, error=error)

    return render_template('edit.html', post=post, error=error)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_controller(post_id):
    if 'username' not in session:
        return redirect('/login')

    try:
        db = get_db()

        db.execute('DELETE FROM posts WHERE post_id = ?', (post_id,))

        db.commit()
    
    except Exception:
        return redirect('/dashboard')

    return redirect('/dashboard')

if __name__ == '__main__':
    app.run()