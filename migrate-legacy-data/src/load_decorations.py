import json
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.home.decoration import Decoration
from models.home.decoration_category import DecorationCategory
from models.collection.collection import Collection
from enums.enum_collection_type import CollectionType
from config import create_app

def load_decorations_from_json():
    """Load decoration data from decoration.json file"""
    
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
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            decorations_created = 0
            decorations_updated = 0
            categories_created = 0
            collections_created = 0
            warnings = []
            
            # Keep track of created categories and collections to avoid duplicates
            category_cache = {}
            collection_cache = {}
            
            # Get existing categories and collections
            existing_categories = {cat.name: cat for cat in DecorationCategory.query.all()}
            existing_collections = {col.name: col for col in Collection.query.filter_by(type=CollectionType.Decoration).all()}
            
            print(f"Found {len(existing_categories)} existing decoration categories")
            print(f"Found {len(existing_collections)} existing decoration collections")
            print(f"Processing {len(decoration_data)} decorations...")
            print("-" * 50)
            
            # Process each decoration in the JSON
            for i, decoration_item in enumerate(decoration_data):
                try:
                    decoration_id = decoration_item.get('id')
                    
                    # Skip if no valid ID
                    if not decoration_id:
                        warnings.append(f"Decoration at index {i} has no valid ID, skipping...")
                        continue
                    
                    decoration_id = int(decoration_id)
                    
                    # Check if decoration already exists
                    existing_decoration = Decoration.query.filter_by(id=decoration_id).first()
                    
                    # Get or create category
                    category = None
                    category_name = decoration_item.get('category')
                    if category_name:
                        # Check cache first
                        if category_name in category_cache:
                            category = category_cache[category_name]
                        # Check existing categories
                        elif category_name in existing_categories:
                            category = existing_categories[category_name]
                            category_cache[category_name] = category
                        else:
                            # Create new category
                            category = DecorationCategory(name=category_name)
                            category.create(commit=False)
                            category_cache[category_name] = category
                            existing_categories[category_name] = category
                            categories_created += 1
                            print(f"Created new decoration category: '{category_name}'")
                      # Get or create collections (now a list)
                    collections = []
                    collection_names = decoration_item.get('collection', [])
                    
                    # Handle both string and list formats for backwards compatibility
                    if isinstance(collection_names, str):
                        collection_names = [collection_names]
                    elif not isinstance(collection_names, list):
                        collection_names = []
                    
                    for collection_name in collection_names:
                        if collection_name:
                            collection = None
                            # Check cache first
                            if collection_name in collection_cache:
                                collection = collection_cache[collection_name]
                            # Check existing collections
                            elif collection_name in existing_collections:
                                collection = existing_collections[collection_name]
                                collection_cache[collection_name] = collection
                            else:
                                # Create new collection
                                collection = Collection(
                                    name=collection_name,
                                    type=CollectionType.Decoration
                                )
                                collection.create(commit=False)
                                collection_cache[collection_name] = collection
                                existing_collections[collection_name] = collection
                                collections_created += 1
                                print(f"Created new decoration collection: '{collection_name}'")
                            
                            if collection:
                                collections.append(collection)
                    
                    # Convert homePoints to integer
                    home_points = decoration_item.get('homePoints')
                    if home_points is not None:
                        try:
                            home_points = int(home_points)
                        except (ValueError, TypeError):
                            home_points = 0
                            warnings.append(f"Invalid homePoints value for decoration ID {decoration_id}")
                    else:
                        home_points = 0
                    
                    if existing_decoration:                        # Update existing decoration
                        existing_decoration.name = decoration_item.get('name', existing_decoration.name)
                        existing_decoration.homepoints = home_points
                        if category:
                            existing_decoration.category = category
                        
                        # Add to collections if specified
                        for collection in collections:
                            if collection not in existing_decoration.collections:
                                existing_decoration.collections.append(collection)
                        
                        decorations_updated += 1
                        print(f"Updated decoration: {existing_decoration.name} (ID: {decoration_id})")
                        
                    else:
                        # Create new decoration
                        decoration = Decoration(
                            id=decoration_id,
                            name=decoration_item.get('name', f'Decoration {decoration_id}'),
                            homepoints=home_points
                        )
                          # Set category relationship
                        if category:
                            decoration.category = category
                        
                        decoration.create(commit=False)
                        
                        # Add to collections if specified
                        for collection in collections:
                            decoration.collections.append(collection)
                        
                        decorations_created += 1
                        print(f"Created decoration: {decoration.name} (ID: {decoration_id})")
                
                except Exception as e:
                    error_msg = f"Error processing decoration at index {i}: {str(e)}"
                    warnings.append(error_msg)
                    print(f"Warning: {error_msg}")
                    continue
            
            # Commit all changes
            try:
                db.session.commit()
                print(f"\n✅ Successfully committed all changes!")
            except Exception as e:
                db.session.rollback()
                print(f"\n❌ Error committing changes: {e}")
                return
            
            # Print summary
            print("\n" + "=" * 60)
            print("🏠 DECORATION MIGRATION SUMMARY")
            print("=" * 60)
            print(f"📦 Decorations created: {decorations_created}")
            print(f"🔄 Decorations updated: {decorations_updated}")
            print(f"🏷️  Categories created: {categories_created}")
            print(f"📚 Collections created: {collections_created}")
            
            if warnings:
                print(f"\n⚠️  WARNINGS ({len(warnings)}):")
                for warning in warnings[:10]:  # Show first 10 warnings
                    print(f"   - {warning}")
                if len(warnings) > 10:
                    print(f"   ... and {len(warnings) - 10} more warnings")
            
            print(f"\n🎯 Total decorations in database: {Decoration.query.count()}")
            print(f"🏷️  Total decoration categories: {DecorationCategory.query.count()}")
            print(f"📚 Total decoration collections: {Collection.query.filter_by(type=CollectionType.Decoration).count()}")
            
        except Exception as e:
            print(f"❌ Fatal error during decoration migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("🔄 Starting decoration migration from decoration.json...")
    load_decorations_from_json()
    print("✅ Decoration migration completed!")
