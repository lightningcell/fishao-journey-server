import json
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.models import db
from app.models.area.area import Area
from app.models.area.special_location import SpecialLocation
from config import create_app

def load_areas_from_json():
    """Load areas and special locations from area.json file"""
    
    # Get the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'area.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            areas_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find area.json file at {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in area.json: {e}")
        return
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            areas_created = 0
            special_locations_created = 0
            
            # Process each area in the JSON
            for area_id_str, area_data in areas_data.items():
                area_id = int(area_id_str)
                
                # Check if area already exists
                existing_area = Area.query.filter_by(id=area_id).first()
                if existing_area:
                    print(f"Area with ID {area_id} already exists, skipping...")
                    continue
                
                # Create main area
                area = Area(
                    id=area_id,
                    name=area_data['name'],
                    badge_id=area_data.get('badge_id'),
                    is_sub_area=False
                )
                
                db.session.add(area)
                areas_created += 1
                print(f"Created area: {area.name} (ID: {area_id})")
                
                # Process special locations if they exist
                if 'special_location' in area_data:
                    special_locations = area_data['special_location']
                    
                    for location_name, location_title in special_locations.items():
                        # Skip the "All" entries as they are just collections
                        if location_name.endswith(' (All)'):
                            continue
                        
                        # Check if special location already exists
                        existing_special_location = SpecialLocation.query.filter_by(
                            name=location_name, 
                            area_id=area_id
                        ).first()
                        
                        if existing_special_location:
                            print(f"Special location '{location_name}' already exists for area {area_id}, skipping...")
                            continue
                        
                        # Create special location
                        special_location = SpecialLocation(
                            name=location_name,
                            title=str(location_title),  # Convert to string in case it's a number
                            area_id=area_id
                        )
                        
                        db.session.add(special_location)
                        special_locations_created += 1
                        print(f"  Created special location: {location_name} -> {location_title}")
                
                # Process subareas if they exist
                if 'sublocations' in area_data:
                    sublocations = area_data['sublocations']
                    
                    for subarea_name, subarea_id in sublocations.items():
                        # Skip the "All" entries as they are just collections
                        if subarea_name == 'All':
                            continue
                        
                        # Check if subarea already exists
                        existing_subarea = Area.query.filter_by(id=subarea_id).first()
                        if existing_subarea:
                            print(f"Subarea with ID {subarea_id} already exists, skipping...")
                            continue
                        
                        # Create subarea
                        subarea = Area(
                            id=subarea_id,
                            name=subarea_name,
                            is_sub_area=True,
                            parent_area_id=area_id
                        )
                        
                        db.session.add(subarea)
                        areas_created += 1
                        print(f"  Created subarea: {subarea_name} (ID: {subarea_id}) under {area.name}")
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n✅ Migration completed successfully!")
            print(f"   Areas created: {areas_created}")
            print(f"   Special locations created: {special_locations_created}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            raise

if __name__ == '__main__':
    print("Starting area data migration...")
    load_areas_from_json()