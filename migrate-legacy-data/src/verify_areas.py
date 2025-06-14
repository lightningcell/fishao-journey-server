import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.area.area import Area
from models.area.special_location import SpecialLocation
from config import create_app

def verify_migration():
    """Verify that the migration worked correctly"""
    app = create_app()
    
    with app.app_context():
        # Count total areas
        total_areas = Area.query.count()
        main_areas = Area.query.filter_by(is_sub_area=False).count()
        sub_areas = Area.query.filter_by(is_sub_area=True).count()
        total_special_locations = SpecialLocation.query.count()
        
        print(f"📊 Migration Verification Results:")
        print(f"   Total Areas: {total_areas}")
        print(f"   Main Areas: {main_areas}")
        print(f"   Sub Areas: {sub_areas}")
        print(f"   Special Locations: {total_special_locations}")
        print()
        
        # Show some example data
        print("🔍 Sample Areas:")
        sample_areas = Area.query.filter_by(is_sub_area=False).limit(5).all()
        for area in sample_areas:
            print(f"   - {area.name} (ID: {area.id}, Badge: {area.badge_id})")
            
            # Show subareas if any
            subareas = area.sub_areas.all()
            if subareas:
                for subarea in subareas:
                    print(f"     └─ {subarea.name} (ID: {subarea.id})")
            
            # Show special locations if any
            special_locs = area.special_locations.all()
            if special_locs:
                for loc in special_locs:
                    print(f"     🏆 {loc.name} -> {loc.title}")
        print()
        
        # Show areas with most special locations
        print("🎯 Areas with Special Locations:")
        areas_with_specials = Area.query.join(SpecialLocation).distinct().all()
        for area in areas_with_specials:
            special_count = area.special_locations.count()
            print(f"   - {area.name}: {special_count} special locations")

if __name__ == '__main__':
    print("Verifying area data migration...")
    verify_migration()
