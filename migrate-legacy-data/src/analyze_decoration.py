import json
import os

def analyze_decoration_json():
    """Analyze decoration.json file and extract all possible keys with example data"""
    
    # Get the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'decoration.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            decoration_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find decoration.json file at {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in decoration.json: {e}")
        return
    
    if not isinstance(decoration_data, list):
        print("Error: Expected decoration.json to contain a list of decoration objects")
        return
    
    print(f"🏠 Total decoration count: {len(decoration_data)}")
    print("=" * 60)
    
    # Collect all unique keys and their data types
    all_keys = {}
    
    for i, decoration in enumerate(decoration_data):
        if not isinstance(decoration, dict):
            print(f"Warning: Decoration at index {i} is not a dictionary")
            continue
        
        # Analyze main decoration keys
        for key, value in decoration.items():
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
            if key in ['category', 'collection', 'season', 'rarity', 'howToGet']:
                if isinstance(value, (str, int, float)):
                    all_keys[key]['values'].add(str(value))
    
    # Print main keys analysis
    print("📊 DECORATION KEYS ANALYSIS:")
    print("-" * 40)
    for key, info in sorted(all_keys.items()):
        print(f"Key: '{key}'")
        print(f"  Type: {info['type']}")
        print(f"  Count: {info['count']} / {len(decoration_data)} decorations")
        print(f"  Example: {info['example']}")
        if info['values'] and len(info['values']) < 30:
            print(f"  Unique values: {sorted(list(info['values']))}")
        elif info['values']:
            print(f"  Unique values count: {len(info['values'])}")
        print()
      # Create example JSON structure
    example_decoration = {
        "id": "integer - unique identifier",
        "category": "string - decoration category",
        "name": "string - decoration name",
        "collection": "array - list of collection names (can be multiple)",
        "homePoints": "integer - home points value",
        "level": "integer - required level",
        "season": "string - season availability",
        "rarity": "string - rarity level",
        "howToGet": "string - how to obtain",
        "vasiliy74": "integer - unknown field (possibly price or cost)"
    }
    
    print("📋 EXAMPLE JSON STRUCTURE:")
    print("-" * 40)
    print("Decoration Object:")
    print(json.dumps(example_decoration, indent=2, ensure_ascii=False))
    
    # Show some real examples
    print("\n🔍 REAL EXAMPLES:")
    print("-" * 40)
    
    # Show first 3 decorations as examples
    for i in range(min(3, len(decoration_data))):
        print(f"Decoration #{i+1}:")
        print(json.dumps(decoration_data[i], indent=2, ensure_ascii=False))
        print()
      # Analyze collections (now can be a list)
    print("🎨 COLLECTION ANALYSIS:")
    print("-" * 40)
    collections = {}
    for decoration in decoration_data:
        decoration_collections = decoration.get('collection', [])
        
        # Handle both string and list formats
        if isinstance(decoration_collections, str):
            decoration_collections = [decoration_collections]
        elif not isinstance(decoration_collections, list):
            decoration_collections = ['No Collection']
        
        if not decoration_collections:
            decoration_collections = ['No Collection']
            
        for collection in decoration_collections:
            if collection not in collections:
                collections[collection] = 0
            collections[collection] += 1
    
    for collection, count in sorted(collections.items(), key=lambda x: x[1], reverse=True):
        print(f"'{collection}': {count} decorations")
    
    # Analyze categories
    print("\n🏷️ CATEGORY ANALYSIS:")
    print("-" * 40)
    categories = {}
    for decoration in decoration_data:
        category = decoration.get('category', 'No Category')
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"'{category}': {count} decorations")
    
    # Analyze rarities
    print("\n💎 RARITY ANALYSIS:")
    print("-" * 40)
    rarities = {}
    for decoration in decoration_data:
        rarity = decoration.get('rarity', 'No Rarity')
        if rarity not in rarities:
            rarities[rarity] = 0
        rarities[rarity] += 1
    
    for rarity, count in sorted(rarities.items(), key=lambda x: x[1], reverse=True):
        print(f"'{rarity}': {count} decorations")
    
    # Analyze seasons
    print("\n🌸 SEASON ANALYSIS:")
    print("-" * 40)
    seasons = {}
    for decoration in decoration_data:
        season = decoration.get('season', 'No Season')
        if season not in seasons:
            seasons[season] = 0
        seasons[season] += 1
    
    for season, count in sorted(seasons.items(), key=lambda x: x[1], reverse=True):
        print(f"'{season}': {count} decorations")
    
    # Analyze howToGet
    print("\n🎁 HOW TO GET ANALYSIS:")
    print("-" * 40)
    how_to_get = {}
    for decoration in decoration_data:
        method = decoration.get('howToGet', 'Unknown')
        if method not in how_to_get:
            how_to_get[method] = 0
        how_to_get[method] += 1
    
    for method, count in sorted(how_to_get.items(), key=lambda x: x[1], reverse=True):
        print(f"'{method}': {count} decorations")
    
    # Home points analysis
    print("\n🏡 HOME POINTS ANALYSIS:")
    print("-" * 40)
    home_points = [d.get('homePoints', 0) for d in decoration_data if 'homePoints' in d]
    if home_points:
        print(f"Min home points: {min(home_points)}")
        print(f"Max home points: {max(home_points)}")
        print(f"Average home points: {sum(home_points) / len(home_points):.2f}")
    
    # Level analysis
    print("\n🔢 LEVEL ANALYSIS:")
    print("-" * 40)
    levels = [d.get('level', 0) for d in decoration_data if 'level' in d]
    if levels:
        print(f"Min level: {min(levels)}")
        print(f"Max level: {max(levels)}")
        print(f"Average level: {sum(levels) / len(levels):.2f}")

if __name__ == '__main__':
    print("🔍 Analyzing decoration.json file...")
    analyze_decoration_json()
