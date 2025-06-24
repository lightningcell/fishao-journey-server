"""
Admin Panel Controller
Yönetici işlemleri için controller sınıfı
"""

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from utils.role_decorators import require_admin
from services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Service instance
admin_service = AdminService()

@admin_bp.route('/dashboard')
@require_admin()
def dashboard():
    """Admin dashboard ana sayfası"""
    return render_template('admin/dashboard.html')

@admin_bp.route('/areas')
@require_admin()
def areas():
    """Area overview sayfası"""
    return render_template('admin/areas.html')

@admin_bp.route('/api/areas')
@require_admin()
def api_areas():
    """Area listesi için API endpoint"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    result = admin_service.get_areas_paginated(page=page, search=search)
    
    if result.success:
        return jsonify(result.to_dict())
    else:
        return jsonify(result.to_dict()), 500

@admin_bp.route('/fish')
@require_admin()
def fish():
    """Fish overview sayfası"""
    return render_template('admin/fish.html')

@admin_bp.route('/api/fish')
@require_admin()
def api_fish():
    """Fish listesi için API endpoint"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    result = admin_service.get_fish_paginated(page=page, search=search)
    
    if result.success:
        return jsonify(result.to_dict())
    else:
        return jsonify(result.to_dict()), 500

@admin_bp.route('/decorations')
@require_admin()
def decorations():
    """Decorations overview sayfası"""
    return render_template('admin/decorations.html')

@admin_bp.route('/api/decorations')
@require_admin()
def api_decorations():
    """Decoration listesi için API endpoint"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    result = admin_service.get_decorations_paginated(page=page, search=search)
    
    if result.success:
        return jsonify(result.to_dict())
    else:
        return jsonify(result.to_dict()), 500

@admin_bp.route('/api/decoration-categories')
@require_admin()
def api_decoration_categories():
    """Decoration kategorileri için API endpoint"""
    result = admin_service.get_decoration_categories()
    
    if result.success:
        return jsonify(result.to_dict())
    else:
        return jsonify(result.to_dict()), 500

@admin_bp.route('/api/dashboard-stats')
@require_admin()
def api_dashboard_stats():
    """Dashboard istatistikleri için API endpoint"""
    result = admin_service.get_dashboard_stats()
    
    if result.success:
        return jsonify(result.to_dict())
    else:
        return jsonify(result.to_dict()), 500
