# Role Service Kullanım Örnekleri

## Role Service Nasıl Kullanılır

```python
from app.services import RoleService
from app import db

# Service instance'ı oluştur
role_service = RoleService(db)

# Kullanıcının Admin olup olmadığını kontrol et
user_id = 1
if role_service.is_admin(user_id):
    print("Kullanıcı Admin!")

# Kullanıcının Developer olup olmadığını kontrol et
if role_service.is_developer(user_id):
    print("Kullanıcı Developer!")

# Kullanıcının Player olup olmadığını kontrol et
if role_service.is_player(user_id):
    print("Kullanıcı Player!")

# Kullanıcının Moderator olup olmadığını kontrol et
if role_service.is_moderator(user_id):
    print("Kullanıcı Moderator!")

# Kullanıcının tüm rollerini getir
response = role_service.get_user_roles(user_id)
if response.success:
    print(f"Kullanıcının rolleri: {response.data}")
else:
    print(f"Hata: {response.message}")

# Kullanıcıya rol ata
response = role_service.add_role_to_user(user_id, "Admin")
if response.success:
    print("Rol başarıyla atandı!")
else:
    print(f"Rol atanamadı: {response.message}")

# Kullanıcıdan rol kaldır
response = role_service.remove_role_from_user(user_id, "Player")
if response.success:
    print("Rol başarıyla kaldırıldı!")
else:
    print(f"Rol kaldırılamadı: {response.message}")

# Kullanıcının belirtilen rollerden herhangi birine sahip olup olmadığını kontrol et
if role_service.has_any_role(user_id, ["Admin", "Developer"]):
    print("Kullanıcı Admin veya Developer!")

# Kullanıcının belirtilen tüm rollere sahip olup olmadığını kontrol et
if role_service.has_all_roles(user_id, ["Admin", "Player"]):
    print("Kullanıcı hem Admin hem de Player!")

# Kullanıcının yetkili (privileged) olup olmadığını kontrol et
if role_service.is_privileged_user(user_id):
    print("Kullanıcı yetkili bir kullanıcı!")

# Kullanıcının en yüksek rolünü getir
highest_role = role_service.get_user_highest_role(user_id)
if highest_role:
    print(f"Kullanıcının en yüksek rolü: {highest_role}")
```

## Controller'da Kullanım Örneği

```python
from flask import request, jsonify
from app.services import RoleService
from app import db

role_service = RoleService(db)

@app.route('/admin/panel')
def admin_panel():
    user_id = request.user_id  # Oturumdaki kullanıcı ID'si
    
    if not role_service.is_admin(user_id):
        return jsonify({'error': 'Admin yetkisi gerekli'}), 403
    
    return jsonify({'message': 'Admin paneline hoş geldiniz!'})

@app.route('/api/user/<int:user_id>/roles')
def get_user_roles(user_id):
    current_user_id = request.user_id
    
    # Sadece admin veya aynı kullanıcı kendi rollerini görebilir
    if not (role_service.is_admin(current_user_id) or current_user_id == user_id):
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    response = role_service.get_user_roles(user_id)
    if response.success:
        return jsonify({'roles': response.data})
    else:
        return jsonify({'error': response.message}), 400

@app.route('/api/user/<int:user_id>/roles', methods=['POST'])
def assign_role(user_id):
    current_user_id = request.user_id
    
    # Sadece admin rol atayabilir
    if not role_service.is_admin(current_user_id):
        return jsonify({'error': 'Admin yetkisi gerekli'}), 403
    
    role_name = request.json.get('role_name')
    response = role_service.add_role_to_user(user_id, role_name)
    
    if response.success:
        return jsonify({'message': response.message})
    else:
        return jsonify({'error': response.message}), 400
```

## Decorator Kullanımı için Örnek

```python
from functools import wraps
from flask import request, jsonify

def require_role(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = request.user_id  # Oturumdaki kullanıcı ID'si
            role_service = RoleService(db)
            
            if not role_service._has_role(user_id, role_name):
                return jsonify({'error': f'{role_name} yetkisi gerekli'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_privileged():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = request.user_id
            role_service = RoleService(db)
            
            if not role_service.is_privileged_user(user_id):
                return jsonify({'error': 'Yetkili kullanıcı gerekli'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Kullanım
@app.route('/admin/users')
@require_role('Admin')
def admin_users():
    return jsonify({'users': []})

@app.route('/moderate/content')
@require_privileged()
def moderate_content():
    return jsonify({'message': 'Moderasyon paneli'})
```
