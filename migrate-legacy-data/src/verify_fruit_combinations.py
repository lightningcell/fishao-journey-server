import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.item.fruit import Fruit
from models.fishing.fruit_combination import FruitCombination
from enums.enum_inventory_type import InventoryType
from config import create_app

def verify_fruit_combinations():
    """Verify that the fruit combination migration worked correctly"""
    app = create_app()
    
    with app.app_context():
        # Count total records
        total_fruits = Fruit.query.count()
        total_combinations = FruitCombination.query.count()
        
        print(f"📊 Fruit Combination Migration Verification Results:")
        print(f"   Total Fruits: {total_fruits}")
        print(f"   Total Fruit Combinations: {total_combinations}")
        print()
        
        # Show all fruits
        print("🍎 All Fruits:")
        fruits = Fruit.query.order_by(Fruit.name).all()
        for fruit in fruits:
            print(f"   - {fruit.name} (ID: {fruit.id})")
        print()
        
        # Show combinations by reward type
        print("🎁 Combinations by Reward Type:")
        reward_types = {}
        combinations = FruitCombination.query.all()
        
        for combo in combinations:
            reward_type = combo.reward_data.get('item_type', 'Unknown')
            if reward_type not in reward_types:
                reward_types[reward_type] = []
            reward_types[reward_type].append(combo)
        
        for reward_type, combos in reward_types.items():
            print(f"   {reward_type}: {len(combos)} combinations")
        print()
        
        # Show sample combinations from each reward type
        print("🔍 Sample Combinations by Reward Type:")
        for reward_type, combos in reward_types.items():
            print(f"\n   {reward_type} Rewards:")
            for combo in combos[:3]:  # Show first 3 of each type
                fruits_str = f"{combo.fruit1.name}-{combo.fruit2.name}-{combo.fruit3.name}"
                reward_desc = combo.get_reward_description()
                print(f"     {combo.id}: {fruits_str} → {reward_desc}")
            if len(combos) > 3:
                print(f"     ... and {len(combos) - 3} more")
        
        print("\n🍹 All Fruit Combinations:")
        print("-" * 60)
        all_combinations = FruitCombination.query.order_by(FruitCombination.id).all()
        for combo in all_combinations:
            fruits_str = f"{combo.fruit1.name}-{combo.fruit2.name}-{combo.fruit3.name}"
            reward_desc = combo.get_reward_description()
            validation_result = combo.validate_reward_data()
            status = "✅" if validation_result[0] else "❌"
            print(f"   {status} {combo.id:2d}: {fruits_str:25} → {reward_desc}")
        
        # Fruit usage statistics
        print(f"\n📈 Fruit Usage Statistics:")
        fruit_usage = {}
        for combo in all_combinations:
            for fruit in [combo.fruit1, combo.fruit2, combo.fruit3]:
                if fruit.name not in fruit_usage:
                    fruit_usage[fruit.name] = 0
                fruit_usage[fruit.name] += 1
        
        # Sort by usage
        sorted_usage = sorted(fruit_usage.items(), key=lambda x: x[1], reverse=True)
        for fruit_name, count in sorted_usage:
            print(f"   {fruit_name:12}: used in {count:2d} combinations")

if __name__ == '__main__':
    print("Verifying fruit combination data migration...")
    verify_fruit_combinations()
