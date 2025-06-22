from models.player import Account, Player
from models import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from .base import BaseService, ServiceResponse


class AuthService(BaseService):
    def authenticate_user(self, username, password):
        """
        Authenticate user with username and password
        Returns the account if successful, None otherwise
        """
        account = Account.query.filter_by(username=username).first()
        
        if account and check_password_hash(account.password_hash, password):
            account.last_login = datetime.utcnow()
            self.db.session.commit()
            return ServiceResponse(True, data=account, message="Login successful.")
        
        return ServiceResponse(False, message="Invalid username or password.")
    
    def register_player(self, username, email, password):
        """
        Register a new player account
        Returns the created player if successful, raises exception otherwise
        """
        try:
            # Check if username or email already exists
            existing_account = Account.query.filter(
                (Account.username == username) | (Account.email == email)
            ).first()
            
            if existing_account:
                if existing_account.username == username:
                    return ServiceResponse(False, message="Username already exists")
                else:
                    return ServiceResponse(False, message="Email already exists")
            
            # Create new player (which inherits from Account)
            player = Player(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                created_date=datetime.utcnow(),
                is_active=True,
                # Player specific fields
                fishbucks=1000,  # Starting fishbucks
                fishcoins=0,
                energy=100,  # Starting energy
                level=1,
                xp=0,
                online=False
            )
            self.db.session.add(player)
            self.db.session.commit()
            return ServiceResponse(True, data=player, message="Registration successful.")
            
        except Exception as e:
            self.db.session.rollback()
            return ServiceResponse(False, message="Registration failed.", error=str(e))

    def get_player_by_id(self, player_id):
        """
        Get player by ID
        """
        player = Player.query.get(player_id)
        if player:
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def is_username_available(self, username):
        """
        Check if username is available
        """
        exists = Account.query.filter_by(username=username).first() is not None
        return ServiceResponse(not exists)

    def is_email_available(self, email):
        """
        Check if email is available
        """
        exists = Account.query.filter_by(email=email).first() is not None
        return ServiceResponse(not exists)
