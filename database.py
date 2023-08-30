from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    ads = db.relationship('Ad', backref='user', lazy=True, cascade="all, delete")
    favorite_ads = db.relationship('Ad', secondary='user_favorites')


    @classmethod
    def add_user(cls, username, email, password):
        new_user = cls(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
    @classmethod
    def login_user(cls, email, password):
        login = cls.query.filter_by(email=email, password=password).first()
        return True if login else False

    @classmethod
    def get_username_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user.username
        return None

    @classmethod
    def get_id_by_email(cls,email):
        user = cls.query.filter_by(email = email).first()
        return user.user_id


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer)
    favorite_ads = db.relationship('User', secondary='user_favorites')

    
    @classmethod
    def add_ad(cls,user_id, title, description, category, value):
        new_ad = cls(user_id=user_id, title=title, description=description, category=category, value=value)
        db.session.add(new_ad)
        db.session.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

class UserFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'))
    
    @classmethod
    def add_favotites(cls, user_id, ad_id):
        new_favorite = cls(user_id= user_id,  ad_id=ad_id)
        db.session.add(new_favorite)
        db.session.commit()
        
class notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.String, nullable=False)
    
    @classmethod
    def add_notification(cls, texto):
        new_noti = cls(texto = texto)
        db.session.add(new_noti)
        db.session.commit()
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
