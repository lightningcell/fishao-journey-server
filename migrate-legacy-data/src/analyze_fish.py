import json
import os

def analyze_fish_json():
    """Analyze fish.json file and extract all possible keys with example data"""
    
    # Get the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'fish.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            fish_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find fish.json file at {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in fish.json: {e}")
        return
    
    if not isinstance(fish_data, list):
        print("Error: Expected fish.json to contain a list of fish objects")
        return
    
    print(f"🐟 Total fish count: {len(fish_data)}")
    print("=" * 60)
    
    # Collect all unique keys and their data types
    all_keys = {}
    catch_req_keys = {}
    
    for i, fish in enumerate(fish_data):
        if not isinstance(fish, dict):
            print(f"Warning: Fish at index {i} is not a dictionary")
            continue
        
        # Analyze main fish keys
        for key, value in fish.items():
            if key not in all_keys:
                all_keys[key] = {
                    'type': type(value).__name__,
                    'example': value,
                    'count': 1,
                    'values': set()
                }
            else:
                all_keys[key]['count'] += 1
            
            # For specific keys, collect all unique values
            if key in ['rating', 'breed_duration', 'breed_cost']:
                if isinstance(value, (str, int, float)):
                    all_keys[key]['values'].add(str(value))
            
            # Special handling for catch_req nested object
            if key == 'catch_req' and isinstance(value, dict):
                for catch_key, catch_value in value.items():
                    if catch_key not in catch_req_keys:
                        catch_req_keys[catch_key] = {
                            'type': type(catch_value).__name__,
                            'example': catch_value,
                            'count': 1,
                            'values': set()
                        }
                    else:
                        catch_req_keys[catch_key]['count'] += 1
                    
                    # Collect unique values for some keys
                    if catch_key in ['bait_category', 'caught_time', 'caught_date']:
                        if isinstance(catch_value, list):
                            for item in catch_value:
                                catch_req_keys[catch_key]['values'].add(str(item))
                        else:
                            catch_req_keys[catch_key]['values'].add(str(catch_value))
    
    # Print main keys analysis
    print("📊 MAIN FISH KEYS ANALYSIS:")
    print("-" * 40)
    for key, info in sorted(all_keys.items()):
        print(f"Key: '{key}'")
        print(f"  Type: {info['type']}")
        print(f"  Count: {info['count']} / {len(fish_data)} fish")
        print(f"  Example: {info['example']}")
        if info['values'] and len(info['values']) < 20:
            print(f"  Unique values: {sorted(list(info['values']))}")
        print()
    
    # Print catch_req keys analysis
    if catch_req_keys:
        print("🎣 CATCH_REQ NESTED KEYS ANALYSIS:")
        print("-" * 40)
        for key, info in sorted(catch_req_keys.items()):
            print(f"Key: '{key}'")
            print(f"  Type: {info['type']}")
            print(f"  Count: {info['count']} fish have this key")
            print(f"  Example: {info['example']}")
            if info['values'] and len(info['values']) < 30:
                print(f"  Unique values: {sorted(list(info['values']))}")
            print()
    
    # Create example JSON structure
    example_fish = {
        "id": "string - unique identifier",
        "rating": "string - fish rating (1-5)",
        "rarity_factor": "string - decimal value",
        "min_length": "string - minimum length",
        "avg_length": "string - average length", 
        "max_length": "string - maximum length",
        "breed_duration": "string - breeding time",
        "breed_cost": "string - breeding cost",
        "breed_success_rate": "string - decimal success rate",
        "hue_shift_of_shiny": "string - color shift for shiny variant",
        "name": "string - fish name",
        "price": "integer - base price",
        "price_shiny": "integer - shiny variant price"
    }
    
    example_catch_req = {
        "location_ids": "array - list of area IDs where fish can be caught",
        "bait_category": "array - types of bait that work",
        "caught_time": "array - time ranges when fish can be caught (optional)",
        "caught_date": "array - date ranges when fish can be caught (optional)"
    }
    
    print("📋 EXAMPLE JSON STRUCTURE:")
    print("-" * 40)
    print("Main Fish Object:")
    print(json.dumps(example_fish, indent=2, ensure_ascii=False))
    print("\nCatch Requirements Object:")
    print(json.dumps(example_catch_req, indent=2, ensure_ascii=False))
    
    # Show some real examples
    print("\n🔍 REAL EXAMPLES:")
    print("-" * 40)
    
    # Show first 3 fish as examples
    for i in range(min(3, len(fish_data))):
        print(f"Fish #{i+1}:")
        print(json.dumps(fish_data[i], indent=2, ensure_ascii=False))
        print()
    
    # Find fish with different catch_req structures
    print("🌟 FISH WITH DIFFERENT CATCH_REQ STRUCTURES:")
    print("-" * 50)
    
    unique_catch_structures = {}
    for fish in fish_data:
        if 'catch_req' in fish:
            keys_tuple = tuple(sorted(fish['catch_req'].keys()))
            if keys_tuple not in unique_catch_structures:
                unique_catch_structures[keys_tuple] = fish
    
    for i, (keys, fish_example) in enumerate(unique_catch_structures.items()):
        print(f"Structure #{i+1} - Keys: {list(keys)}")
        print(f"Example from fish '{fish_example.get('name', 'Unknown')}':")
        print(json.dumps(fish_example['catch_req'], indent=2, ensure_ascii=False))
        print()

if __name__ == '__main__':
    print("🔍 Analyzing fish.json file...")
    analyze_fish_json()
