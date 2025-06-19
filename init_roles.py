#!/usr/bin/env python3
"""
Role initialization script for Fishao Journey Server
This script creates the default roles in the system: Admin, Moderator, Player, Developer
"""

from app import create_app
from app.models import db
from app.models.player import AccountRole


def init_roles():
    """Initialize default roles in the system"""
    
    # Create Flask app instance
    app = create_app()
    
    # List of default roles to create
    default_roles = [
        "Admin",
        "Moderator", 
        "Player",
        "Developer"
    ]
    
    with app.app_context():
        print("Initializing roles...")
        
        for role_name in default_roles:
            # Check if role already exists
            existing_role = AccountRole.query.filter_by(name=role_name).first()
            
            if existing_role:
                print(f"Role '{role_name}' already exists, skipping...")
            else:
                # Create new role
                new_role = AccountRole(name=role_name)
                new_role.create(commit=False)
                print(f"Created role: {role_name}")
        
        # Commit all changes
        try:
            db.session.commit()
            print("All roles have been successfully initialized!")
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while initializing roles: {e}")
            raise


if __name__ == "__main__":
    init_roles()
