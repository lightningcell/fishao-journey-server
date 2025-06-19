import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.models import db
from app.models.item.fruit import Fruit
from app.models.fishing.fruit_combination import FruitCombination
from app.models.item.rod import Rod
from app.models.fishing.fish import Fish
from app.enums.enum_inventory_type import InventoryType
from config import create_app

# Fruit combination data from the provided table
FRUIT_COMBINATIONS = [
    {"id": 1, "reward": {"type": "Energy", "amount": 5}, "fruits": ["Coconut", "Coconut", "Coconut"]},
    {"id": 2, "reward": {"type": "Energy", "amount": 10}, "fruits": ["Lemon", "Orange", "Lemon"]},
    {"id": 3, "reward": {"type": "Bait", "amount": 50, "name": "shad"}, "fruits": ["Papaya", "Papaya", "Mango"]},
    {"id": 4, "reward": {"type": "Rod", "amount": 1, "name": "Simple rod (brown)"}, "fruits": ["Coconut", "Banana", "Banana"]},
    {"id": 5, "reward": {"type": "Fishbucks", "amount": 500}, "fruits": ["Kiwi", "Kiwi", "Kiwi"]},
    {"id": 6, "reward": {"type": "Fish", "amount": 1, "name": "Trumpetfish"}, "fruits": ["Pitaya", "Banana", "Banana"]},
    {"id": 7, "reward": {"type": "Fish", "amount": 1, "name": "Queen Parrotfish"}, "fruits": ["Papaya", "Orange", "Pitaya"]},
    {"id": 8, "reward": {"type": "Fish", "amount": 1, "name": "Spanish Hogfish"}, "fruits": ["Banana", "Lemon", "Lemon"]},
    {"id": 9, "reward": {"type": "Fish", "amount": 1, "name": "Yellow Tang"}, "fruits": ["Lemon", "Lemon", "Lemon"]},
    {"id": 10, "reward": {"type": "Fish", "amount": 1, "name": "Fantail Filefish"}, "fruits": ["Pitaya", "Papaya", "Pitaya"]},
    {"id": 11, "reward": {"type": "Fish", "amount": 1, "name": "Hogfish"}, "fruits": ["Coconut", "Coconut", "Orange"]},
    {"id": 12, "reward": {"type": "Fish", "amount": 1, "name": "Blackbar Soldierfish"}, "fruits": ["Orange", "Pineapple", "Orange"]},
    {"id": 13, "reward": {"type": "Fish", "amount": 1, "name": "Yellowhead Wrasse"}, "fruits": ["Mango", "Papaya", "Pineapple"]},
    {"id": 14, "reward": {"type": "Fish", "amount": 1, "name": "Bluespotted Grouper"}, "fruits": ["Kiwi", "Pitaya", "Kiwi"]},
    {"id": 15, "reward": {"type": "Fish", "amount": 1, "name": "Blue Parrotfish"}, "fruits": ["Pitaya", "Mango", "Papaya"]},
    {"id": 16, "reward": {"type": "Fish", "amount": 1, "name": "Picasso Triggerfish"}, "fruits": ["Orange", "Pitaya", "Banana"]},
    {"id": 17, "reward": {"type": "Fish", "amount": 1, "name": "Yellowtail Wrasse"}, "fruits": ["Lemon", "Coconut", "Coconut"]},
    {"id": 18, "reward": {"type": "Fish", "amount": 1, "name": "Pinktail Triggerfish"}, "fruits": ["Orange", "Orange", "Pitaya"]},
    {"id": 19, "reward": {"type": "Fish", "amount": 1, "name": "Peacock Flounder"}, "fruits": ["Pitaya", "Pineapple", "Pineapple"]},
    {"id": 20, "reward": {"type": "Fish", "amount": 1, "name": "Midnight Parrotfish"}, "fruits": ["Pitaya", "Coconut", "Coconut"]},
    {"id": 21, "reward": {"type": "Fish", "amount": 1, "name": "Titan Triggerfish"}, "fruits": ["Pineapple", "Banana", "Papaya"]},
    {"id": 22, "reward": {"type": "Fish", "amount": 1, "name": "Bluestripe Snapper"}, "fruits": ["Banana", "Pineapple", "Banana"]},
    {"id": 23, "reward": {"type": "Fish", "amount": 1, "name": "Orange-banded Pipefish"}, "fruits": ["Orange", "Orange", "Banana"]},
]

def load_fruit_combinations():
    """Load fruit combinations data into the database"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            fruits_created = 0
            combinations_created = 0
            warnings = []
            
            # First, create all required fruits
            print("🍎 Creating fruits...")
            unique_fruit_names = set()
            for combo in FRUIT_COMBINATIONS:
                unique_fruit_names.update(combo["fruits"])
            
            fruit_mapping = {}
            for fruit_name in unique_fruit_names:
                existing_fruit = Fruit.query.filter_by(name=fruit_name).first()
                if not existing_fruit:
                    fruit = Fruit(name=fruit_name)
                    db.session.add(fruit)
                    fruits_created += 1
                    print(f"  Created fruit: {fruit_name}")
                    fruit_mapping[fruit_name] = fruit
                else:
                    print(f"  Fruit '{fruit_name}' already exists")
                    fruit_mapping[fruit_name] = existing_fruit
            
            # Commit fruits first
            db.session.commit()
            
            # Refresh fruit mapping with IDs
            for fruit_name in fruit_mapping:
                if not hasattr(fruit_mapping[fruit_name], 'id') or not fruit_mapping[fruit_name].id:
                    fruit_mapping[fruit_name] = Fruit.query.filter_by(name=fruit_name).first()
            
            print(f"\n🍹 Creating fruit combinations...")
            
            # Create fruit combinations
            for combo_data in FRUIT_COMBINATIONS:
                try:
                    combo_id = combo_data["id"]
                    
                    # Check if combination already exists
                    existing_combo = FruitCombination.query.filter_by(id=combo_id).first()
                    if existing_combo:
                        print(f"Fruit combination {combo_id} already exists, skipping...")
                        continue
                    
                    # Get fruit IDs
                    fruit1 = fruit_mapping[combo_data["fruits"][0]]
                    fruit2 = fruit_mapping[combo_data["fruits"][1]]
                    fruit3 = fruit_mapping[combo_data["fruits"][2]]
                    
                    if not fruit1.id or not fruit2.id or not fruit3.id:
                        warnings.append(f"Could not find fruit IDs for combination {combo_id}")
                        continue
                    
                    # Prepare reward data
                    reward = combo_data["reward"]
                    reward_type = reward["type"]
                    
                    # Map reward type to InventoryType
                    inventory_type_mapping = {
                        "Energy": InventoryType.Energy,
                        "Fishbucks": InventoryType.Fishbucks,
                        "Fishcoins": InventoryType.Fishcoins,
                        "Bait": InventoryType.Bait,
                        "Rod": InventoryType.Rod,
                        "Fish": InventoryType.Fish,
                    }
                    
                    if reward_type not in inventory_type_mapping:
                        warnings.append(f"Unknown reward type '{reward_type}' for combination {combo_id}")
                        continue
                    
                    inventory_type = inventory_type_mapping[reward_type]
                    
                    # Create reward data JSON
                    reward_data = {
                        "item_type": inventory_type.value,
                        "amount": reward["amount"],
                        "type": reward.get("name", reward_type)
                    }
                    
                    # Create fruit combination
                    fruit_combination = FruitCombination(
                        id=combo_id,
                        fruit1_id=fruit1.id,
                        fruit2_id=fruit2.id,
                        fruit3_id=fruit3.id,
                        reward_data=reward_data
                    )
                    
                    # Validate reward data
                    is_valid, validation_message = fruit_combination.validate_reward_data()
                    if not is_valid:
                        warnings.append(f"Invalid reward data for combination {combo_id}: {validation_message}")
                        continue
                    
                    db.session.add(fruit_combination)
                    combinations_created += 1
                    
                    fruits_str = f"{fruit1.name}-{fruit2.name}-{fruit3.name}"
                    reward_desc = fruit_combination.get_reward_description()
                    print(f"  Created combination {combo_id}: {fruits_str} → {reward_desc}")
                
                except Exception as e:
                    warnings.append(f"Error processing combination {combo_data.get('id', 'unknown')}: {e}")
                    continue
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n✅ Fruit combination migration completed successfully!")
            print(f"   Fruits created: {fruits_created}")
            print(f"   Fruit combinations created: {combinations_created}")
            
            if warnings:
                print(f"\n⚠️  {len(warnings)} warnings occurred:")
                for warning in warnings:
                    print(f"   - {warning}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            raise

if __name__ == '__main__':
    print("Starting fruit combination data migration...")
    load_fruit_combinations()
