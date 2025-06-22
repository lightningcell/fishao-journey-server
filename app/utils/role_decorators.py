"""
Role-based access control decorators for Flask routes.

Bu modül, Flask route'larında rol tabanlı erişim kontrolü için decorator'lar sağlar.
RoleService ile entegre çalışarak kullanıcı yetkilendirmelerini kolaylaştırır.

Kullanım Örnekleri:
    @require_role('Admin')
    def admin_only_route():
        pass
        
    @require_privileged()
    def privileged_route():
        pass
        
    @require_any_role(['Admin', 'Moderator'])
    def admin_or_moderator_route():
        pass
"""

from functools import wraps
from flask import request, jsonify, session, g
from services import RoleService
from app import db


def require_role(role_name):
    """
    Belirtilen role sahip kullanıcıların erişebileceği route'lar için decorator.
    
    Args:
        role_name (str): Gerekli rol adı (örn: 'Admin', 'Player', 'Moderator')
        
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/admin/panel')
        @require_role('Admin')
        def admin_panel():
            return "Admin Panel"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Kullanıcı ID'sini farklı kaynaklardan al
            user_id = _get_current_user_id()
            
            if not user_id:
                return jsonify({'error': 'Oturum gerekli'}), 401
            
            role_service = RoleService(db)
            
            if not role_service._has_role(user_id, role_name):
                return jsonify({'error': f'{role_name} yetkisi gerekli'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_privileged():
    """
    Yetkili kullanıcıların (Admin, Developer, Moderator) erişebileceği route'lar için decorator.
    
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/moderate/content')
        @require_privileged()
        def moderate_content():
            return "Moderasyon Paneli"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = _get_current_user_id()
            
            if not user_id:
                return jsonify({'error': 'Oturum gerekli'}), 401
                
            role_service = RoleService(db)
            
            if not role_service.is_privileged_user(user_id):
                return jsonify({'error': 'Yetkili kullanıcı gerekli'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_any_role(role_list):
    """
    Belirtilen rollerden herhangi birine sahip kullanıcıların erişebileceği route'lar için decorator.
    
    Args:
        role_list (list): Gerekli rollerden herhangi biri (örn: ['Admin', 'Moderator'])
        
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/admin-or-mod')
        @require_any_role(['Admin', 'Moderator'])
        def admin_or_moderator_only():
            return "Admin veya Moderator Paneli"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = _get_current_user_id()
            
            if not user_id:
                return jsonify({'error': 'Oturum gerekli'}), 401
                
            role_service = RoleService(db)
            
            if not role_service.has_any_role(user_id, role_list):
                roles_str = ', '.join(role_list)
                return jsonify({'error': f'Şu rollerden birine sahip olmanız gerekli: {roles_str}'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_all_roles(role_list):
    """
    Belirtilen tüm rollere sahip kullanıcıların erişebileceği route'lar için decorator.
    
    Args:
        role_list (list): Gerekli tüm roller (örn: ['Admin', 'Player'])
        
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/special-admin')
        @require_all_roles(['Admin', 'Player'])
        def special_admin_route():
            return "Hem Admin hem Player olan kullanıcılar için"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = _get_current_user_id()
            
            if not user_id:
                return jsonify({'error': 'Oturum gerekli'}), 401
                
            role_service = RoleService(db)
            
            if not role_service.has_all_roles(user_id, role_list):
                roles_str = ', '.join(role_list)
                return jsonify({'error': f'Şu rollerin tümüne sahip olmanız gerekli: {roles_str}'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_admin():
    """
    Sadece Admin rolüne sahip kullanıcıların erişebileceği route'lar için kısayol decorator.
    
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/admin/users')
        @require_admin()
        def admin_users():
            return "Admin Kullanıcı Yönetimi"
    """
    return require_role('Admin')


def require_moderator():
    """
    Sadece Moderator rolüne sahip kullanıcıların erişebileceği route'lar için kısayol decorator.
    
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/moderate/reports')
        @require_moderator()
        def moderate_reports():
            return "Moderator Rapor Yönetimi"
    """
    return require_role('Moderator')


def require_developer():
    """
    Sadece Developer rolüne sahip kullanıcıların erişebileceği route'lar için kısayol decorator.
    
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/dev/debug')
        @require_developer()
        def dev_debug():
            return "Developer Debug Paneli"
    """
    return require_role('Developer')


def require_player():
    """
    Sadece Player rolüne sahip kullanıcıların erişebileceği route'lar için kısayol decorator.
    
    Returns:
        decorator: Flask route decorator'ı
        
    Example:
        @app.route('/player/profile')
        @require_player()
        def player_profile():
            return "Oyuncu Profili"
    """
    return require_role('Player')


def _get_current_user_id():
    """
    Mevcut kullanıcının ID'sini farklı kaynaklardan almaya çalışır.
    
    Öncelik sırası:
    1. Flask g objesi
    2. Session
    3. Request headers
    4. Request args/form
    
    Returns:
        int|None: Kullanıcı ID'si veya None
    """
    # Flask g objesi (genellikle middleware tarafından set edilir)
    if hasattr(g, 'user_id'):
        return g.user_id
    
    # Session
    if 'user_id' in session:
        return session['user_id']
    
    # Request object'inde user_id attribute'u (custom middleware tarafından set edilebilir)
    if hasattr(request, 'user_id'):
        return request.user_id
    
    # Headers
    user_id = request.headers.get('X-User-ID')
    if user_id:
        try:
            return int(user_id)
        except (ValueError, TypeError):
            pass
    
    # JSON body
    if request.is_json and request.json:
        user_id = request.json.get('user_id')
        if user_id:
            try:
                return int(user_id)
            except (ValueError, TypeError):
                pass
    
    # Form data veya args
    user_id = request.form.get('user_id') or request.args.get('user_id')
    if user_id:
        try:
            return int(user_id)
        except (ValueError, TypeError):
            pass
    
    return None


def get_current_user_roles():
    """
    Mevcut kullanıcının rollerini getirir.
    
    Returns:
        list: Kullanıcının rolleri listesi veya boş liste
    """
    user_id = _get_current_user_id()
    if not user_id:
        return []
    
    role_service = RoleService(db)
    response = role_service.get_user_roles(user_id)
    
    if response.success:
        return response.data
    
    return []


def check_user_permission(user_id, required_role):
    """
    Belirtilen kullanıcının gerekli role sahip olup olmadığını kontrol eder.
    
    Args:
        user_id (int): Kullanıcı ID'si
        required_role (str): Gerekli rol adı
        
    Returns:
        bool: Kullanıcı gerekli role sahipse True, değilse False
    """
    if not user_id:
        return False
        
    role_service = RoleService(db)
    return role_service._has_role(user_id, required_role)
