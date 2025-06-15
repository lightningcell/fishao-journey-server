import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.fishing.fish import Fish
from models.fishing.caught_time import CaughtTime
from models.fishing.caught_date import CaughtDate
from models.fishing.fruit_combination import FruitCombination
from models.item.bait_category import BaitCategory
from models.area.area import Area
from models.area.special_location import SpecialLocation
from config import create_app

def verify_fish_migration():
    """Verify that the fish migration worked correctly"""
    app = create_app()
    
    with app.app_context():        # Count total records
        total_fish = Fish.query.count()
        total_bait_categories = BaitCategory.query.count()
        total_caught_times = CaughtTime.query.count()
        total_caught_dates = CaughtDate.query.count()
        fish_with_fruit_combinations = Fish.query.filter(Fish.fruit_combination_id.isnot(None)).count()
        
        print(f"📊 Fish Migration Verification Results:")
        print(f"   Total Fish: {total_fish}")
        print(f"   Total Bait Categories: {total_bait_categories}")
        print(f"   Total Caught Times: {total_caught_times}")
        print(f"   Total Caught dates: {total_caught_dates}")
        print(f"   Fish with Fruit Combination Requirements: {fish_with_fruit_combinations}")
        print()
        
        # Show bait categories
        print("🎣 Bait Categories:")
        bait_categories = BaitCategory.query.all()
        for bait in bait_categories:
            fish_count = bait.fishes.count() if hasattr(bait, 'fishes') else 0
            print(f"   - {bait.name}: {fish_count} fish")
        print()
          # Show fish by rating
        print("⭐ Fish by Rating:")
        for rating in range(1, 6):
            count = Fish.query.filter_by(star_rate=rating).count()
            print(f"   {rating} star: {count} fish")
        print()
        
        # Show fish with fruit combination requirements
        if fish_with_fruit_combinations > 0:
            print("🍹 Fish with Fruit Combination Requirements:")
            fish_with_fruit_req = Fish.query.filter(Fish.fruit_combination_id.isnot(None)).limit(10).all()
            for fish in fish_with_fruit_req:
                if fish.fruit_combination:
                    fruits_str = f"{fish.fruit_combination.fruit1.name}-{fish.fruit_combination.fruit2.name}-{fish.fruit_combination.fruit3.name}"
                    print(f"   - {fish.name}: requires combination {fish.fruit_combination_id} ({fruits_str})")
                else:
                    print(f"   - {fish.name}: requires combination {fish.fruit_combination_id} (combination not found)")
            if fish_with_fruit_combinations > 10:
                print(f"   ... and {fish_with_fruit_combinations - 10} more")
            print()
        # Show sample fish with relationships
        print("🔍 Sample Fish with Details:")
        sample_fish = Fish.query.limit(3).all()
        for fish in sample_fish:
            print(f"   - {fish.name} (ID: {fish.id}, Rating: {fish.star_rate}⭐)")
            print(f"     Price: {fish.price}, Rarity: {fish.rarity_factor}")
            print(f"     Length: {fish.min_length}-{fish.max_length}cm (avg: {fish.average_length})")
            
            # Show areas
            areas_count = fish.areas.count() if hasattr(fish, 'areas') else 0
            if areas_count > 0:
                area_names = [area.name for area in fish.areas[:3]]
                print(f"     Areas ({areas_count}): {', '.join(area_names)}")
            
            # Show bait categories
            bait_count = fish.bait_categories.count() if hasattr(fish, 'bait_categories') else 0
            if bait_count > 0:
                bait_names = [bait.name for bait in fish.bait_categories[:3]]
                print(f"     Baits ({bait_count}): {', '.join(bait_names)}")
            
            # Show caught times
            time_count = fish.caught_times.count()
            if time_count > 0:
                times = [f"{ct.starttime}-{ct.endtime}" for ct in fish.caught_times[:2]]
                print(f"     Catch Times ({time_count}): {', '.join(times)}")
            
            # Show caught dates
            date_count = fish.caught_dates.count()
            if date_count > 0:
                dates = [f"{cd.startdate}-{cd.enddate}" for cd in fish.caught_dates[:2]]
                print(f"     Catch Dates ({date_count}): {', '.join(dates)}")
              # Show special requirements
            special_reqs = []
            if fish.club_points:
                special_reqs.append(f"Club Points: {fish.club_points}")
            if fish.fishcoins_to_unlock:
                special_reqs.append(f"Fishcoins: {fish.fishcoins_to_unlock}")
            if fish.fruit_combination_id:
                special_reqs.append(f"Fruit Combination: {fish.fruit_combination_id}")
            
            if special_reqs:
                print(f"     Special Requirements: {', '.join(special_reqs)}")
            
            print()
        
        # Show fish with most areas
        print("🌍 Fish with Most Areas:")
        fish_with_areas = Fish.query.join(Fish.areas).distinct().all()
        fish_area_counts = [(fish, fish.areas.count()) for fish in fish_with_areas]
        fish_area_counts.sort(key=lambda x: x[1], reverse=True)
        
        for fish, area_count in fish_area_counts[:5]:
            print(f"   - {fish.name}: {area_count} areas")
        print()
        
        # Show most expensive fish
        print("💰 Most Expensive Fish:")
        expensive_fish = Fish.query.order_by(Fish.price.desc()).limit(5).all()
        for fish in expensive_fish:
            print(f"   - {fish.name}: {fish.price} coins ({fish.star_rate}⭐)")

if __name__ == '__main__':
    print("Verifying fish data migration...")
    verify_fish_migration()
