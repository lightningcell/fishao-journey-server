from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from forms import LoginForm, RegisterForm
from models.player import Account, Player
from models import db
from werkzeug.security import check_password_hash, generate_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ana sayfa - Giriş sayfası"""
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with WTForms integration"""
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        
        # Find account by username
        account = Account.query.filter_by(username=username).first()
        
        if account and check_password_hash(account.password_hash, password):
            # Login successful
            session['user_id'] = account.id
            session['username'] = account.username
            
            if remember:
                session.permanent = True
            
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page with WTForms integration"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Create new account
        try:
            account = Account(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            account.create()
            
            # Create player profile
            player = Player(
                id=account.id,
                fishbucks=1000,  # Starting fishbucks
                fishcash=0,
                level=1,
                experience=0
            )
            player.create()
            
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('main.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html', form=form)

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page - requires login"""
    if 'user_id' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('main.login'))
    
    player = Player.query.get(session['user_id'])
    return render_template('dashboard.html', player=player)

@main_bp.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))
