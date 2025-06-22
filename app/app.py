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
    
    # Blueprint'leri kayıt et
    from controllers.main import main_bp
    from controllers.two_factor import two_factor_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(two_factor_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
