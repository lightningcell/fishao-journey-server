"""
Admin Service
Admin panel için iş mantığı katmanı
"""

from services.base import BaseService, ServiceResponse
from models.area.area import Area
from models.fishing.fish import Fish
from models.home.decoration import Decoration
from models.home.decoration_category import DecorationCategory
from models import db
from sqlalchemy import func


class AdminService(BaseService):
    """Admin panel için servis katmanı"""
    
    def __init__(self):
        super().__init__(db)
    
    # Area Operations
    def get_areas_paginated(self, page=1, per_page=7, search=None):
        """Sayfalanmış area listesi döndürür"""
        try:
            query = Area.query
            
            if search:
                query = query.filter(Area.name.ilike(f'%{search}%'))
            
            pagination_result = query.order_by(Area.id.asc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
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
            
            return ServiceResponse(
                success=True,
                data={
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
            )
            
        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f'Areas yüklenirken hata oluştu: {str(e)}'
            )
    
    # Fish Operations
    def get_fish_paginated(self, page=1, per_page=7, search=None):
        """Sayfalanmış fish listesi döndürür"""
        try:
            query = Fish.query
            
            if search:
                query = query.filter(Fish.name.ilike(f'%{search}%'))
            
            pagination_result = query.order_by(Fish.id.asc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
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
            
            return ServiceResponse(
                success=True,
                data={
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
            )
            
        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f'Fish yüklenirken hata oluştu: {str(e)}'
            )
    
    # Decoration Operations
    def get_decorations_paginated(self, page=1, per_page=7, search=None):
        """Sayfalanmış decoration listesi döndürür"""
        try:
            query = Decoration.query
            
            if search:
                query = query.filter(Decoration.name.ilike(f'%{search}%'))
            
            pagination_result = query.order_by(Decoration.id.asc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            decorations_data = []
            for decoration in pagination_result.items:
                decorations_data.append({
                    'id': decoration.id,
                    'name': decoration.name,
                    'homepoints': decoration.homepoints,
                    'category_id': decoration.category_id,
                    'category_name': decoration.category.name if decoration.category else None,
                    'decoration_items_count': decoration.decoration_items.count(),
                    'collections_count': decoration.collections.count(),
                    'has_item': decoration.item is not None
                })
            
            return ServiceResponse(
                success=True,
                data={
                    'items': decorations_data,
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
            )
            
        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f'Decorations yüklenirken hata oluştu: {str(e)}'
            )
    
    def get_decoration_categories(self):
        """Decoration kategorilerini döndürür"""
        try:
            categories = DecorationCategory.query.order_by(DecorationCategory.name.asc()).all()
            categories_data = []
            
            for category in categories:
                categories_data.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description
                })
            
            return ServiceResponse(
                success=True,
                data=categories_data
            )
            
        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f'Kategoriler yüklenirken hata oluştu: {str(e)}'
            )
    
    # Dashboard Statistics
    def get_dashboard_stats(self):
        """Dashboard istatistiklerini döndürür"""
        try:
            stats = {
                'areas_count': Area.query.count(),
                'fish_count': Fish.query.count(),
                'decorations_count': Decoration.query.count(),
                'decoration_categories_count': DecorationCategory.query.count()
            }
            
            return ServiceResponse(
                success=True,
                data=stats
            )
            
        except Exception as e:
            return ServiceResponse(
                success=False,
                message=f'İstatistikler yüklenirken hata oluştu: {str(e)}'
            )
