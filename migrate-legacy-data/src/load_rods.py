import json
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.item.rod import Rod
from enums.enum_rod_sizes import RodSizes
from config import create_app

def load_rods_from_json():
    """Load rod data from rod.json file"""
    
    # Get the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'rod.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            rods_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find rod.json file at {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in rod.json: {e}")
        return
    
    if not isinstance(rods_data, list):
        print("Error: Expected rod.json to contain a list of rod objects")
        return
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            rods_created = 0
            warnings = []
            
            # Process each rod in the JSON
            for i, rod_data in enumerate(rods_data):
                try:
                    # Validate required fields
                    if 'name' not in rod_data:
                        warnings.append(f"Rod at index {i} missing 'name' field, skipping...")
                        continue
                    
                    if 'size' not in rod_data:
                        warnings.append(f"Rod '{rod_data.get('name', 'unknown')}' missing 'size' field, skipping...")
                        continue
                    
                    if 'length_quality' not in rod_data:
                        warnings.append(f"Rod '{rod_data.get('name', 'unknown')}' missing 'length_quality' field, skipping...")
                        continue
                    
                    # Check if rod already exists (by name)
                    existing_rod = Rod.query.filter_by(name=rod_data['name']).first()
                    if existing_rod:
                        print(f"Rod '{rod_data['name']}' already exists, skipping...")
                        continue
                    
                    # Validate and convert size enum
                    size_str = rod_data['size']
                    try:
                        rod_size = RodSizes(size_str)
                    except ValueError:
                        warnings.append(f"Invalid rod size '{size_str}' for rod '{rod_data['name']}', skipping...")
                        continue
                    
                    # Create rod
                    rod = Rod(
                        name=rod_data['name'],
                        size=rod_size,
                        length_quality=int(rod_data['length_quality'])
                    )
                    
                    db.session.add(rod)
                    rods_created += 1
                    print(f"Created rod: {rod.name} (Size: {rod.size.value}, Quality: {rod.length_quality})")
                
                except Exception as e:
                    warnings.append(f"Error processing rod at index {i}: {e}")
                    continue
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n✅ Rod migration completed successfully!")
            print(f"   Rods created: {rods_created}")
            
            if warnings:
                print(f"\n⚠️  {len(warnings)} warnings occurred:")
                for warning in warnings:
                    print(f"   - {warning}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            raise

if __name__ == '__main__':
    print("Starting rod data migration...")
    load_rods_from_json()
