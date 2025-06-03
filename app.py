from flask import Flask
from flask_migrate import Migrate
from models import db
import os

def create_app():
    app = Flask(__name__)
    
    # Veritabanı yapılandırması
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fishao.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # SQLAlchemy'yi başlat
    db.init_app(app)
    
    # Flask-Migrate'i başlat
    migrate = Migrate(app, db)
    
    # Blueprint'leri burada ekleyebilirsiniz
    # app.register_blueprint(your_blueprint)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 