from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from flask_sqlalchemy import SQLAlchemy
from database import User, Ad, notification, UserFavorites, db

app = Flask(__name__, template_folder='app/templates')
app.secret_key = 'uma_chave_secreta_aleatoria' # Inicialize o objeto db com esse aplicativo Flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']    
        is_db = User.login_user(email, password)
        if not is_db:
            return "Usuário ou senha incorreta"
        else:
            # Se o login for bem-sucedido, redirecionar para outra página
            
            session['current_user'] = User.get_id_by_email(email)
            session['username'] = User.get_username_by_email(email)
            return redirect(url_for('home'))
    return render_template('login.html')
        
        
@app.route('/home', methods = ['GET', 'POST'])
def home():
    username = session.get('username', 'Convidado')
    ads = Ad.query.all()
    notifications = notification.query.all()
    return render_template('home.html',username=username, ads=ads, notifications=notifications)


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
            User.add_user(name, email, password)
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
        value = request.form.get('value')
        # Verifica se todos os campos estão preenchidos
        user_id = session.get('user')
        if title and description and category and value:
            Ad.add_ad(user_id, title, description, category, value)
            notification.add_notification("Novo anúncio criado")
            success_message = "Anúncio criado com sucesso!"
            return redirect(url_for('home'))
        else:
            error_message = "Por favor, preencha todos os campos!"
    return render_template('create_ad.html',success_message=success_message, error_message=error_message)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    user_id = request.form.get('user_id')
    ad_id = request.form.get('ad_id')
    
    UserFavorites.add_favorites(user_id, ad_id)
    return jsonify(status='success')

@app.route('/edit_user', methods=['POST', 'GET'])
def edit_user():
    if request.method == 'POST':
        
    
    return render_template('edit_user.html')



if __name__ == '__main__':
    app.run(debug=True)    