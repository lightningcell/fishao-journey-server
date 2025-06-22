import json
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.item.bait import Bait
from models.item.bait_category import BaitCategory
from config import create_app

def load_baits_from_json():
    """Load bait data from bait.json file"""
    
    # Get the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'bait.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            baits_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find bait.json file at {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in bait.json: {e}")
        return
    
    if not isinstance(baits_data, list):
        print("Error: Expected bait.json to contain a list of bait objects")
        return
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            baits_created = 0
            bait_categories_created = 0
            warnings = []
            
            # Process each bait in the JSON
            for i, bait_data in enumerate(baits_data):
                try:
                    # Validate required fields
                    if 'id' not in bait_data:
                        warnings.append(f"Bait at index {i} missing 'id' field, skipping...")
                        continue
                    
                    if 'name' not in bait_data:
                        warnings.append(f"Bait at index {i} missing 'name' field, skipping...")
                        continue
                    
                    if 'category' not in bait_data:
                        warnings.append(f"Bait '{bait_data.get('name', 'unknown')}' missing 'category' field, skipping...")
                        continue
                    
                    bait_id = int(bait_data['id'])
                    
                    # Check if bait already exists
                    existing_bait = Bait.query.filter_by(bait_id=bait_id).first()
                    if existing_bait:
                        print(f"Bait with ID {bait_id} already exists, skipping...")
                        continue
                    
                    # Get or create bait category
                    category_name = bait_data['category']
                    bait_category = BaitCategory.query.filter_by(name=category_name).first()
                    if not bait_category:
                        bait_category = BaitCategory(name=category_name)
                        db.session.add(bait_category)
                        bait_categories_created += 1
                        print(f"  Created bait category: {category_name}")
                    
                    # Create bait
                    bait = Bait(
                        name=bait_data['name'],
                        bait_id=bait_id,
                        category=bait_category
                    )
                    
                    db.session.add(bait)
                    baits_created += 1
                    print(f"Created bait: {bait.name} (ID: {bait_id}, Category: {category_name})")
                
                except Exception as e:
                    warnings.append(f"Error processing bait at index {i} (ID: {bait_data.get('id', 'unknown')}): {e}")
                    continue
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n✅ Bait migration completed successfully!")
            print(f"   Baits created: {baits_created}")
            print(f"   Bait categories created: {bait_categories_created}")
            
            if warnings:
                print(f"\n⚠️  {len(warnings)} warnings occurred:")
                for warning in warnings:
                    print(f"   - {warning}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            raise

if __name__ == '__main__':
    print("Starting bait data migration...")
    load_baits_from_json()
