import json
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from config import create_app
from models import db
from models.player.account_role import AccountRole

def init_roles():
    """Initialize default roles in the database"""
    app = create_app()
    
    with app.app_context():
        # Define default roles
        default_roles = [
            "Admin",
            "Moderator", 
            "Player",
            "Developer"
        ]
        
        for role_name in default_roles:
            # Check if role already exists
            existing_role = AccountRole.query.filter_by(name=role_name).first()
            
            if not existing_role:
                # Create new role
                new_role = AccountRole(name=role_name)
                db.session.add(new_role)
                print(f"Created role: {role_name}")
            else:
                print(f"Role already exists: {role_name}")
        
        # Commit all changes
        try:
            db.session.commit()
            print("All roles initialized successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing roles: {e}")

if __name__ == "__main__":
    init_roles()