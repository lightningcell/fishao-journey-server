import json
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.models import db
from app.models.home.decoration import Decoration
from app.models.home.decoration_category import DecorationCategory
from app.models.collection.collection import Collection
from app.enums.enum_collection_type import CollectionType
from config import create_app

def verify_decorations():
    """Verify decoration data migration by comparing with original decoration.json"""
    
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
    
    app = create_app()
    
    with app.app_context():
        # Get all decorations from database
        db_decorations = {d.id: d for d in Decoration.query.all()}
        db_categories = {c.name: c for c in DecorationCategory.query.all()}
        db_collections = {c.name: c for c in Collection.query.filter_by(type=CollectionType.Decoration).all()}
        
        print("🔍 DECORATION VERIFICATION REPORT")
        print("=" * 60)
        print(f"📊 JSON file contains: {len(decoration_data)} decorations")
        print(f"📊 Database contains: {len(db_decorations)} decorations")
        print(f"📊 Database contains: {len(db_categories)} decoration categories")
        print(f"📊 Database contains: {len(db_collections)} decoration collections")
        print()
        
        missing_in_db = []
        mismatched_data = []
        missing_categories = []
        missing_collections = []
        
        # Check each decoration from JSON
        for decoration_item in decoration_data:
            decoration_id = decoration_item.get('id')
            if not decoration_id:
                continue
                
            decoration_id = int(decoration_id)
            
            # Check if decoration exists in database
            if decoration_id not in db_decorations:
                missing_in_db.append(decoration_id)
                continue
            
            db_decoration = db_decorations[decoration_id]
            
            # Verify basic fields
            json_name = decoration_item.get('name', '')
            json_home_points = decoration_item.get('homePoints', 0)
            
            try:
                json_home_points = int(json_home_points)
            except (ValueError, TypeError):
                json_home_points = 0
                
            mismatches = []
            
            if db_decoration.name != json_name:
                mismatches.append(f"name: DB='{db_decoration.name}' vs JSON='{json_name}'")
                
            if db_decoration.homepoints != json_home_points:
                mismatches.append(f"homepoints: DB={db_decoration.homepoints} vs JSON={json_home_points}")
            
            # Check category
            json_category = decoration_item.get('category')
            if json_category:
                if not db_decoration.category:
                    mismatches.append(f"category: DB=None vs JSON='{json_category}'")
                elif db_decoration.category.name != json_category:
                    mismatches.append(f"category: DB='{db_decoration.category.name}' vs JSON='{json_category}'")
                
                # Check if category exists in database
                if json_category not in db_categories:
                    missing_categories.append(json_category)
              # Check collections (now a list)
            json_collections = decoration_item.get('collection', [])
            
            # Handle both string and list formats for backwards compatibility
            if isinstance(json_collections, str):
                json_collections = [json_collections]
            elif not isinstance(json_collections, list):
                json_collections = []
            
            if json_collections:
                decoration_collections = [c.name for c in db_decoration.collections]
                
                for json_collection in json_collections:
                    if json_collection not in decoration_collections:
                        mismatches.append(f"collection: '{json_collection}' not found in DB collections {decoration_collections}")
                    
                    # Check if collection exists in database
                    if json_collection not in db_collections:
                        missing_collections.append(json_collection)
            
            if mismatches:
                mismatched_data.append({
                    'id': decoration_id,
                    'name': json_name,
                    'mismatches': mismatches
                })
        
        # Check for decorations in DB that are not in JSON
        extra_in_db = []
        for db_id in db_decorations.keys():
            if not any(int(item.get('id', 0)) == db_id for item in decoration_data):
                extra_in_db.append(db_id)
        
        # Print results
        if missing_in_db:
            print(f"❌ MISSING IN DATABASE ({len(missing_in_db)}):")
            for decoration_id in missing_in_db[:10]:
                json_decoration = next((item for item in decoration_data if int(item.get('id', 0)) == decoration_id), None)
                if json_decoration:
                    print(f"   ID {decoration_id}: {json_decoration.get('name', 'Unknown')}")
            if len(missing_in_db) > 10:
                print(f"   ... and {len(missing_in_db) - 10} more")
            print()
        
        if extra_in_db:
            print(f"⚠️  EXTRA IN DATABASE ({len(extra_in_db)}):")
            for decoration_id in extra_in_db[:10]:
                db_decoration = db_decorations[decoration_id]
                print(f"   ID {decoration_id}: {db_decoration.name}")
            if len(extra_in_db) > 10:
                print(f"   ... and {len(extra_in_db) - 10} more")
            print()
        
        if mismatched_data:
            print(f"⚠️  DATA MISMATCHES ({len(mismatched_data)}):")
            for mismatch in mismatched_data[:10]:
                print(f"   ID {mismatch['id']} ({mismatch['name']}):")
                for issue in mismatch['mismatches']:
                    print(f"     - {issue}")
            if len(mismatched_data) > 10:
                print(f"   ... and {len(mismatched_data) - 10} more mismatches")
            print()
        
        if missing_categories:
            unique_missing_categories = list(set(missing_categories))
            print(f"❌ MISSING CATEGORIES ({len(unique_missing_categories)}):")
            for category in unique_missing_categories:
                print(f"   - {category}")
            print()
        
        if missing_collections:
            unique_missing_collections = list(set(missing_collections))
            print(f"❌ MISSING COLLECTIONS ({len(unique_missing_collections)}):")
            for collection in unique_missing_collections:
                print(f"   - {collection}")
            print()
        
        # Summary
        total_issues = len(missing_in_db) + len(mismatched_data) + len(missing_categories) + len(missing_collections)
        
        if total_issues == 0:
            print("✅ VERIFICATION PASSED!")
            print("All decorations from JSON are correctly stored in the database.")
        else:
            print(f"⚠️  VERIFICATION ISSUES FOUND: {total_issues}")
            print("Please review the issues above.")
        
        print("\n📈 DATABASE STATISTICS:")
        print(f"   Total decorations: {len(db_decorations)}")
        print(f"   Total categories: {len(db_categories)}")
        print(f"   Total collections: {len(db_collections)}")
        
        # Category distribution
        category_counts = {}
        for decoration in db_decorations.values():
            cat_name = decoration.category.name if decoration.category else 'No Category'
            category_counts[cat_name] = category_counts.get(cat_name, 0) + 1
        
        print(f"\n🏷️  TOP CATEGORIES:")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {category}: {count} decorations")
        
        # Collection distribution
        collection_counts = {}
        for decoration in db_decorations.values():
            for collection in decoration.collections:
                collection_counts[collection.name] = collection_counts.get(collection.name, 0) + 1
        
        if collection_counts:
            print(f"\n📚 TOP COLLECTIONS:")
            for collection, count in sorted(collection_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   {collection}: {count} decorations")

if __name__ == '__main__':
    print("🔍 Starting decoration verification...")
    verify_decorations()
    print("✅ Decoration verification completed!")
