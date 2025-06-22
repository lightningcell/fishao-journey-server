from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from forms import LoginForm, RegisterForm
from services import AuthService, PlayerService
from models import db

main_bp = Blueprint('main', __name__)

auth_service = AuthService(db)
player_service = PlayerService(db)

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
        
        # Authenticate user using service
        result = auth_service.authenticate_user(username, password)
        
        if result.success:
            account = result.data
            session['user_id'] = account.id
            session['username'] = account.username
            
            if remember:
                session.permanent = True
            
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash(result.message or 'Invalid username or password.', 'error')
    
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page with WTForms integration"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Register new player using service
        result = auth_service.register_player(username, email, password)
        if result.success:
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash(result.message or 'Registration failed. Please try again.', 'error')
    
    return render_template('register.html', form=form)

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page - requires login"""
    if 'user_id' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('main.login'))
    
    player_result = player_service.get_player_by_id(session['user_id'])
    if not player_result.success:
        flash('Player not found. Please login again.', 'error')
        return redirect(url_for('main.logout'))
    player = player_result.data
    
    player_service.update_player_activity(player.id)
    
    return render_template('dashboard.html', player=player)

@main_bp.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))
