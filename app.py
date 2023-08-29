from flask import Flask, render_template, request, redirect, url_for, session
from database import add_user, create_table, get_user, add_ad
import sqlite3

app = Flask(__name__, template_folder='app/templates')
app.secret_key = 'uma_chave_secreta_aleatoria'
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
            session['username'] = email
            return redirect(url_for('home'))
    return render_template('login.html')
        
        
@app.route('/home', methods = ['GET', 'POST'])
def home():
    username = session.get('username', 'Convidado')
    return render_template('home.html',username=username)


@app.route('/create_account',  methods = ['GET', 'POST'])
def create_account():
    error = None
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not name or not email or not password:
            error = 'Todos os campos devem ser preenchidos!'
        else:
            add_user(name, email, password)
            return(redirect(url_for('login')))
    return render_template('sing.html', error=error)


@app.route('/create_ad', methods = ['GET', 'POST'])
def create_ad():
    success_message = None
    error_message = None
    # get resquets of post
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        # Verifica se todos os campos estão preenchidos
        if title and description and category:
            add_ad(title, description, category)
            success_message = "Anúncio criado com sucesso!"
        else:
            error_message = "Por favor, preencha todos os campos!"
    return render_template('create_ad.html',success_message=success_message, error_message=error_message)







if __name__ == '__main__':
    app.run(debug=True)    