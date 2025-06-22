import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import db
from models.item.rod import Rod
from models.item.bait import Bait
from models.item.bait_category import BaitCategory
from enums.enum_rod_sizes import RodSizes
from config import create_app

def verify_rods_and_baits():
    """Verify that the rod and bait migrations worked correctly"""
    app = create_app()
    
    with app.app_context():
        # Count total records
        total_rods = Rod.query.count()
        total_baits = Bait.query.count()
        total_bait_categories = BaitCategory.query.count()
        
        print(f"📊 Rod & Bait Migration Verification Results:")
        print(f"   Total Rods: {total_rods}")
        print(f"   Total Baits: {total_baits}")
        print(f"   Total Bait Categories: {total_bait_categories}")
        print()
        
        # Show rods by size
        print("🎣 Rods by Size:")
        for size in RodSizes:
            count = Rod.query.filter_by(size=size).count()
            print(f"   {size.value}: {count} rods")
        print()
        
        # Show top rods by quality
        print("⭐ Top Rods by Quality:")
        top_rods = Rod.query.order_by(Rod.length_quality.desc()).limit(5).all()
        for rod in top_rods:
            print(f"   - {rod.name}: {rod.length_quality} quality ({rod.size.value})")
        print()
        
        # Show bait categories with counts
        print("🪱 Bait Categories:")
        bait_categories = BaitCategory.query.all()
        for category in bait_categories:
            bait_count = category.baits.count()
            print(f"   - {category.name}: {bait_count} baits")
        print()
        
        # Show sample baits from each category
        print("🔍 Sample Baits by Category:")
        for category in bait_categories:
            sample_baits = category.baits.limit(3).all()
            bait_names = [bait.name for bait in sample_baits]
            if bait_names:
                print(f"   {category.name}: {', '.join(bait_names)}")
        print()
        
        # Show all rods
        print("🎣 All Rods:")
        all_rods = Rod.query.order_by(Rod.length_quality.asc()).all()
        for rod in all_rods:
            print(f"   - {rod.name}: {rod.length_quality} quality ({rod.size.value})")

if __name__ == '__main__':
    print("Verifying rod and bait data migration...")
    verify_rods_and_baits()
