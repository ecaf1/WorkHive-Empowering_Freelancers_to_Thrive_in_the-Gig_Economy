from flask import Flask, render_template, request, redirect, url_for
from database import add_user, create_table, get_user
import sqlite3

app = Flask(__name__, template_folder='app/templates')

create_table()

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        
        is_db = get_user(email, password)
        print(is_db)
        if not is_db:
            return "Usuário ou senha incorreta"
        else:
            # Se o login for bem-sucedido, redirecionar para outra página
            return redirect(url_for('dashboard'))
    return render_template('login.html')
        
        
@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    return render_template('home.html')


@app.route('/create_account',  methods = ['GET', 'POST'])
def create_account():
    if request.method == "POST":
        name = request.form[name]
        email = request.form[email]
        password = request.form[password]
        conn = sqlite3.connect('users.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO user  (name, email, password) VALUES (?,?,?)', (name, email, password))
        conn.commit()
        conn.close()
    return render_template('sing.html')


@app.route('/create_ad', methods = ['GET', 'POST'])
def create_ad():
    return render_template('create_ad.html')







if __name__ == '__main__':
    app.run(debug=True)    