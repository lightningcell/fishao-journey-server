import json
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.models import db
from app.models.item.fruit import Fruit
from config import create_app

def load_fruits_from_json():
    """Load fruits from fruit.json file"""
    
    # Get the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'fruit.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            fruits_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find fruit.json file at {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in fruit.json: {e}")
        return
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            fruits_created = 0
            fruits_updated = 0
            
            # Process each fruit in the JSON
            for fruit_data in fruits_data:
                fruit_id = fruit_data['id']
                fruit_name = fruit_data['name']
                
                # Check if fruit already exists
                existing_fruit = Fruit.query.filter_by(id=fruit_id).first()
                if existing_fruit:
                    # Update existing fruit if name is different
                    if existing_fruit.name != fruit_name:
                        existing_fruit.name = fruit_name
                        fruits_updated += 1
                        print(f"Updated fruit: {fruit_name} (ID: {fruit_id})")
                    else:
                        print(f"Fruit with ID {fruit_id} already exists with same data, skipping...")
                    continue
                
                # Create new fruit
                fruit = Fruit(
                    id=fruit_id,
                    name=fruit_name
                )
                
                db.session.add(fruit)
                fruits_created += 1
                print(f"Created fruit: {fruit_name} (ID: {fruit_id})")
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n✅ Migration completed successfully!")
            print(f"   Fruits created: {fruits_created}")
            print(f"   Fruits updated: {fruits_updated}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            raise

def verify_fruits():
    """Verify that all fruits were loaded correctly"""
    app = create_app()
    
    with app.app_context():
        try:
            fruits = Fruit.query.all()
            print(f"\n📊 Verification Report:")
            print(f"   Total fruits in database: {len(fruits)}")
            print(f"   Fruit list:")
            
            for fruit in sorted(fruits, key=lambda x: x.id):
                print(f"     - ID {fruit.id}: {fruit.name}")
                
        except Exception as e:
            print(f"❌ Error during verification: {e}")

if __name__ == '__main__':
    print("Starting fruit data migration...")
    load_fruits_from_json()
    verify_fruits()
