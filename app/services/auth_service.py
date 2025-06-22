from models.player import Account, Player
from models import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from .base import BaseService, ServiceResponse
from .two_factor_service import TwoFactorService


class AuthService(BaseService):
    def __init__(self, db):
        super().__init__(db)
        self.two_factor_service = TwoFactorService(db)

    def authenticate_user(self, username, password=None, totp_code=None):
        """
        Authenticate user with username and password, and optionally 2FA code
        """
        account = Account.query.filter_by(username=username).first()
        
        if not account:
            return ServiceResponse(False, message="Invalid username or password.")
        
        # If password is provided, verify it (first step of login)
        if password is not None:
            if not check_password_hash(account.password_hash, password):
                return ServiceResponse(False, message="Invalid username or password.")
        
        # Check if 2FA is enabled
        if account.is2fa_enabled:
            if not totp_code:
                return ServiceResponse(False, message="2FA code required.", data={'requires_2fa': True, 'account_id': account.id})
            
            # Verify 2FA code
            totp_result = self.two_factor_service.verify_2fa_login(account.id, totp_code)
            if not totp_result.success:
                return ServiceResponse(False, message=totp_result.message)
        
        # Update last login
        account.last_login = datetime.utcnow()
        self.db.session.commit()
        
        return ServiceResponse(True, data=account, message="Login successful.")
    
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

    def verify_2fa_for_login(self, account_id, totp_code):
        """
        Verify 2FA code for an already password-authenticated account
        """
        try:
            account = Account.query.get(account_id)
            if not account:
                return ServiceResponse(False, message="Account not found")
            
            if not account.is2fa_enabled:
                return ServiceResponse(True, data=account, message="2FA not required")
            
            # Verify 2FA code
            totp_result = self.two_factor_service.verify_2fa_login(account.id, totp_code)
            if not totp_result.success:
                return ServiceResponse(False, message=totp_result.message)
            
            # Update last login
            account.last_login = datetime.utcnow()
            self.db.session.commit()
            
            return ServiceResponse(True, data=account, message="2FA verification successful")
            
        except Exception as e:
            return ServiceResponse(False, message="2FA verification failed", error=str(e))
