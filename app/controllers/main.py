from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ana sayfa - Giriş sayfası"""
    return render_template('index.html')

@main_bp.route('/home')
def home():
    """Home sayfası"""
    return render_template('home.html')

@main_bp.route('/blog')
def blog():
    """Blog sayfası"""
    return render_template('blog.html')
