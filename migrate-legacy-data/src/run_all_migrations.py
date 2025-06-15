import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def run_all_migrations():
    """Run all migration scripts in the correct order"""
    
    print("🚀 Starting complete data migration process...")
    print("=" * 60)    # Import migration functions
    from load_areas import load_areas_from_json
    from load_rods import load_rods_from_json
    from load_baits import load_baits_from_json
    from load_fruit_combinations import load_fruit_combinations
    from load_fish import load_fish_from_json
    from load_fruits import load_fruits_from_json
    from load_decorations import load_decorations_from_json
    
    try:
        # Step 1: Load areas (required for fish)
        print("\n📍 Step 1: Loading Areas...")
        print("-" * 30)
        load_areas_from_json()
        
        # Step 2: Load rods
        print("\n🎣 Step 2: Loading Rods...")
        print("-" * 30)
        load_rods_from_json()
          # Step 3: Load baits (and bait categories)
        print("\n🪱 Step 3: Loading Baits...")
        print("-" * 30)
        load_baits_from_json()
        
        # Step 4: Load fruit combinations
        print("\n🍹 Step 4: Loading Fruit Combinations...")
        print("-" * 30)
        load_fruit_combinations()
          # Step 5: Load fish (depends on areas and bait categories)
        print("\n🐟 Step 5: Loading Fish...")
        print("-" * 30)
        load_fish_from_json()
        
        # Step 5: Load fruits
        print("\n🍎 Step 5: Loading Fruits...")
        print("-" * 30)
        load_fruits_from_json()
        
        # Step 6: Load decorations
        print("\n🏠 Step 6: Loading Decorations...")
        print("-" * 30)
        load_decorations_from_json()
        
        print("\n" + "=" * 60)
        print("✅ All migrations completed successfully!")
        
        # Run verification
        print("\n🔍 Running verification...")
        print("-" * 30)
        
        from verify_areas import verify_migration as verify_areas
        from verify_rods_baits import verify_rods_and_baits
        from verify_fruit_combinations import verify_fruit_combinations
        from verify_fish import verify_fish_migration
        from verify_decorations import verify_decorations
        
        verify_areas()
        print()
        verify_rods_and_baits()
        print()
        verify_fruit_combinations()
        print()
        verify_fish_migration()
        print()
        verify_decorations()
        
    except Exception as e:
        print(f"\n❌ Migration process failed: {e}")
        raise

if __name__ == '__main__':
    run_all_migrations()
