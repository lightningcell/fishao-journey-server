import json
import os
import sys
from datetime import datetime, time, date

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.models import db
from app.models.fishing.fish import Fish
from app.models.fishing.caught_time import CaughtTime
from app.models.fishing.caught_date import CaughtDate
from app.models.fishing.fruit_combination import FruitCombination
from app.models.item.bait_category import BaitCategory
from app.models.area.area import Area
from app.models.area.special_location import SpecialLocation
from config import create_app

def parse_time_range(time_str):
    """Parse time range string like '21:00-08:00' into start and end time objects"""
    try:
        start_str, end_str = time_str.split('-')
        start_time = datetime.strptime(start_str, '%H:%M').time()
        end_time = datetime.strptime(end_str, '%H:%M').time()
        return start_time, end_time
    except ValueError as e:
        print(f"Warning: Could not parse time range '{time_str}': {e}")
        return None, None

def parse_date_range(date_str):
    """Parse date range string like '07.01-09.30' into start and end date objects"""
    try:
        start_str, end_str = date_str.split('-')
        
        # Parse dates assuming current year
        current_year = datetime.now().year
        start_date = datetime.strptime(f"{current_year}.{start_str}", '%Y.%m.%d').date()
        end_date = datetime.strptime(f"{current_year}.{end_str}", '%Y.%m.%d').date()
        
        return start_date, end_date
    except ValueError as e:
        print(f"Warning: Could not parse date range '{date_str}': {e}")
        return None, None

def load_fish_from_json():
    """Load fish data from fish.json file"""
    
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
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            fish_created = 0
            bait_categories_created = 0
            caught_times_created = 0
            caught_dates_created = 0
            fruit_combination_links = 0
            warnings = []
            
            # Get all existing areas, special locations, and fruit combinations for validation
            existing_areas = {area.id: area for area in Area.query.all()}
            existing_special_locations = {sl.title: sl for sl in SpecialLocation.query.all()}
            existing_fruit_combinations = {fc.id: fc for fc in FruitCombination.query.all()}
            
            print(f"Found {len(existing_areas)} existing areas")
            print(f"Found {len(existing_special_locations)} existing special locations")
            print(f"Found {len(existing_fruit_combinations)} existing fruit combinations")
            
            # Process each fish in the JSON
            for i, fish_data_item in enumerate(fish_data):
                try:
                    fish_id = int(fish_data_item.get('id', 0))
                    
                    # Skip if no valid ID
                    if not fish_id:
                        print(f"Warning: Fish at index {i} has no valid ID, skipping...")
                        continue
                      # Check if fish already exists
                    existing_fish = Fish.query.filter_by(id=fish_id).first()
                    if existing_fish:
                        # Update existing fish with fruit combination if needed
                        catch_req = fish_data_item.get('catch_req', {})
                        if 'fruit_combinations_done' in catch_req:
                            fruit_combo_ids = catch_req['fruit_combinations_done']
                            if fruit_combo_ids and len(fruit_combo_ids) > 0:
                                fruit_combo_id = fruit_combo_ids[0]
                                if fruit_combo_id in existing_fruit_combinations:
                                    if existing_fish.fruit_combination_id != fruit_combo_id:
                                        existing_fish.fruit_combination_id = fruit_combo_id
                                        fruit_combination_links += 1
                                        print(f"Updated existing fish {existing_fish.name} with fruit combination {fruit_combo_id}")
                                else:
                                    warnings.append(f"Fruit combination {fruit_combo_id} not found for existing fish {existing_fish.name}")
                        continue
                    
                    # Create main fish object with safe value handling
                    fish = Fish(
                        id=fish_id,
                        name=fish_data_item.get('name', ''),
                        star_rate=int(fish_data_item.get('rating', 1)),
                        rarity_factor=float(fish_data_item.get('rarity_factor', 1.0)),
                        min_length=int(fish_data_item.get('min_length', 0)),
                        average_length=int(fish_data_item.get('avg_length', 0)),
                        max_length=int(fish_data_item.get('max_length', 0)),
                        breed_duration_hours=int(fish_data_item.get('breed_duration', 0) or 0),
                        breed_cost=int(fish_data_item.get('breed_cost', 0) or 0),
                        breed_success_rate=float(fish_data_item.get('breed_success_rate', 0.0) or 0.0),
                        hue_shift_of_shiny=int(fish_data_item.get('hue_shift_of_shiny', 0) or 0),
                        price=fish_data_item.get('price', 0) or 0
                    )
                    
                    # Handle optional fields from catch_req
                    catch_req = fish_data_item.get('catch_req', {})
                    
                    if 'club_points' in catch_req:
                        fish.club_points = catch_req['club_points']
                    
                    if 'club_unlock_by_fishcoins' in catch_req:
                        fish.fishcoins_to_unlock = catch_req['club_unlock_by_fishcoins']
                    
                    # Handle fruit combination requirement
                    if 'fruit_combinations_done' in catch_req:
                        fruit_combo_ids = catch_req['fruit_combinations_done']
                        if fruit_combo_ids and len(fruit_combo_ids) > 0:
                            # Take the first (and typically only) fruit combination ID
                            fruit_combo_id = fruit_combo_ids[0]
                            if fruit_combo_id in existing_fruit_combinations:
                                fish.fruit_combination_id = fruit_combo_id
                                fruit_combination_links += 1
                                print(f"  Linked fish {fish.name} to fruit combination {fruit_combo_id}")
                            else:
                                warnings.append(f"Fruit combination {fruit_combo_id} not found for fish {fish.name}")
                    
                    db.session.add(fish)
                    fish_created += 1
                    print(f"Created fish: {fish.name} (ID: {fish_id})")
                    
                    # Process location_ids (Areas)
                    if 'location_ids' in catch_req:
                        for area_id in catch_req['location_ids']:
                            if area_id not in existing_areas:
                                warning_msg = f"Area with ID {area_id} not found for fish {fish.name} (ID: {fish_id})"
                                warnings.append(warning_msg)
                                print(f"WARNING: {warning_msg}")
                            else:
                                fish.areas.append(existing_areas[area_id])
                    
                    # Process bait_category
                    if 'bait_category' in catch_req:
                        for bait_name in catch_req['bait_category']:
                            # Check if bait category exists, create if not
                            bait_category = BaitCategory.query.filter_by(name=bait_name).first()
                            if not bait_category:
                                bait_category = BaitCategory(name=bait_name)
                                db.session.add(bait_category)
                                bait_categories_created += 1
                                print(f"  Created bait category: {bait_name}")
                            
                            fish.bait_categories.append(bait_category)
                    
                    # Process fishing_place (Special Locations)
                    if 'fishing_place' in catch_req:
                        for place_title in catch_req['fishing_place']:
                            if place_title not in existing_special_locations:
                                warning_msg = f"Special location '{place_title}' not found for fish {fish.name} (ID: {fish_id})"
                                warnings.append(warning_msg)
                                print(f"WARNING: {warning_msg}")
                            else:
                                fish.special_locations.append(existing_special_locations[place_title])
                    
                    # Process caught_time
                    if 'caught_time' in catch_req:
                        for time_range in catch_req['caught_time']:
                            start_time, end_time = parse_time_range(time_range)
                            if start_time and end_time:
                                caught_time = CaughtTime(
                                    starttime=start_time,
                                    endtime=end_time,
                                    fish_id=fish_id
                                )
                                db.session.add(caught_time)
                                caught_times_created += 1
                                print(f"  Created caught time: {time_range}")
                    
                    # Process caught_date
                    if 'caught_date' in catch_req:
                        for date_range in catch_req['caught_date']:
                            start_date, end_date = parse_date_range(date_range)
                            if start_date and end_date:
                                caught_date = CaughtDate(
                                    startdate=start_date,
                                    enddate=end_date,
                                    fish_id=fish_id
                                )
                                db.session.add(caught_date)
                                caught_dates_created += 1
                                print(f"  Created caught date: {date_range}")
                
                except Exception as e:
                    print(f"❌ Error processing fish at index {i} (ID: {fish_data_item.get('id', 'unknown')}): {e}")
                    print(f"   Fish data: {fish_data_item}")
                    continue  # Skip this fish and continue with the next one
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n✅ Fish migration completed successfully!")
            print(f"   Fish created: {fish_created}")
            print(f"   Bait categories created: {bait_categories_created}")
            print(f"   Caught times created: {caught_times_created}")
            print(f"   Caught dates created: {caught_dates_created}")
            print(f"   Fruit combination links: {fruit_combination_links}")
            
            if warnings:
                print(f"\n⚠️  {len(warnings)} warnings occurred:")
                for warning in warnings[:10]:  # Show first 10 warnings
                    print(f"   - {warning}")
                if len(warnings) > 10:
                    print(f"   ... and {len(warnings) - 10} more warnings")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            raise

if __name__ == '__main__':
    print("Starting fish data migration...")
    load_fish_from_json()
