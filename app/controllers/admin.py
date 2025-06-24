"""
Admin Panel Controller
Yönetici işlemleri için controller sınıfı
"""

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from utils.role_decorators import require_admin
from models.area.area import Area
from models.fishing.fish import Fish
from models import db
import math

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 7  # Her sayfada 7 veri
        search = request.args.get('search', '').strip()
        
        # Base query
        query = Area.query
        
        # Search filter
        if search:
            query = query.filter(
                Area.name.ilike(f'%{search}%')
            )
        
        # Pagination
        pagination_result = query.order_by(Area.id.asc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Serialize areas
        areas_data = []
        for area in pagination_result.items:
            areas_data.append({
                'id': area.id,
                'name': area.name,
                'area_id': area.area_id,
                'level_requirement': area.level_requirement,
                'is_sub_area': area.is_sub_area,
                'badge_id': area.badge_id,
                'parent_area_name': area.parent_area.name if area.parent_area else None,
                'sub_areas_count': area.sub_areas.count(),
                'fishes_count': len(area.fishes),
                'special_locations_count': area.special_locations.count()
            })
        
        return jsonify({
            'success': True,
            'data': {
                'items': areas_data,
                'pagination': {
                    'page': pagination_result.page,
                    'per_page': pagination_result.per_page,
                    'total': pagination_result.total,
                    'pages': pagination_result.pages,
                    'has_prev': pagination_result.has_prev,
                    'has_next': pagination_result.has_next,
                    'prev_num': pagination_result.prev_num,
                    'next_num': pagination_result.next_num
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        }), 500

@admin_bp.route('/fish')
@require_admin()
def fish():
    """Fish overview sayfası"""
    return render_template('admin/fish.html')

@admin_bp.route('/api/fish')
@require_admin()
def api_fish():
    """Fish listesi için API endpoint"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 7  # Her sayfada 7 veri
        search = request.args.get('search', '').strip()
        
        # Base query
        query = Fish.query
        
        # Search filter
        if search:
            query = query.filter(
                Fish.name.ilike(f'%{search}%')
            )
        
        # Pagination
        pagination_result = query.order_by(Fish.id.asc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Serialize fish
        fish_data = []
        for fish in pagination_result.items:
            fish_data.append({
                'id': fish.id,
                'name': fish.name,
                'star_rate': fish.star_rate,
                'rarity_factor': fish.rarity_factor,
                'min_length': fish.min_length,
                'average_length': fish.average_length,
                'max_length': fish.max_length,
                'price': fish.price,
                'club_points': fish.club_points,
                'fishcoins_to_unlock': fish.fishcoins_to_unlock,
                'breed_duration_hours': fish.breed_duration_hours,
                'breed_cost': fish.breed_cost,
                'breed_success_rate': fish.breed_success_rate,
                'areas_count': len(fish.areas),
                'special_locations_count': len(fish.special_locations),
                'bait_categories_count': len(fish.bait_categories)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'items': fish_data,
                'pagination': {
                    'page': pagination_result.page,
                    'per_page': pagination_result.per_page,
                    'total': pagination_result.total,
                    'pages': pagination_result.pages,
                    'has_prev': pagination_result.has_prev,
                    'has_next': pagination_result.has_next,
                    'prev_num': pagination_result.prev_num,
                    'next_num': pagination_result.next_num
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        }), 500

@admin_bp.route('/decorations')
@require_admin()
def decorations():
    """Decorations overview sayfası"""
    return render_template('admin/decorations.html')
