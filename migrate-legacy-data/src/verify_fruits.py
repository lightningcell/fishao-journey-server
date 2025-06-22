import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.item.fruit import Fruit
from config import create_app

def verify_fruits():
    """Verify fruits data in the database"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Get all fruits
            fruits = Fruit.query.all()
            
            print(f"📊 Fruit Verification Report")
            print(f"=" * 50)
            print(f"Total fruits in database: {len(fruits)}")
            print()
            
            if not fruits:
                print("❌ No fruits found in database!")
                return
            
            # Display all fruits
            print("🍎 Fruits List:")
            print("-" * 30)
            for fruit in sorted(fruits, key=lambda x: x.id):
                print(f"  ID {fruit.id:2d}: {fruit.name}")
            
            print()
            
            # Check for expected fruits from the migration
            expected_fruits = [
                "Banana", "Coconut", "Kiwi", "Lemon", "Mango", 
                "Orange", "Papaya", "Pineapple", "Pitaya"
            ]
            
            existing_fruit_names = [fruit.name for fruit in fruits]
            missing_fruits = [fruit for fruit in expected_fruits if fruit not in existing_fruit_names]
            unexpected_fruits = [fruit for fruit in existing_fruit_names if fruit not in expected_fruits]
            
            if missing_fruits:
                print(f"⚠️  Missing expected fruits: {', '.join(missing_fruits)}")
            
            if unexpected_fruits:
                print(f"ℹ️  Additional fruits found: {', '.join(unexpected_fruits)}")
            
            if not missing_fruits and not unexpected_fruits:
                print("✅ All expected fruits are present and no unexpected fruits found!")
            
            # Check for duplicates
            fruit_names = [fruit.name for fruit in fruits]
            duplicates = []
            for name in set(fruit_names):
                if fruit_names.count(name) > 1:
                    duplicates.append(name)
            
            if duplicates:
                print(f"⚠️  Duplicate fruit names found: {', '.join(duplicates)}")
            else:
                print("✅ No duplicate fruit names found!")
                
        except Exception as e:
            print(f"❌ Error during verification: {e}")

if __name__ == '__main__':
    print("Starting fruit data verification...")
    verify_fruits()
