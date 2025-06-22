import pyotp
import qrcode
import io
import base64
import json
import secrets
from .base import BaseService, ServiceResponse
from models.player import Account


class TwoFactorService(BaseService):
    def generate_secret_key(self):
        """Generate a new TOTP secret key"""
        return pyotp.random_base32()
    
    def generate_qr_code(self, account, secret_key):
        """Generate QR code for TOTP setup"""
        try:
            # Create TOTP URI for the account
            totp_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
                name=account.email,
                issuer_name="FishAO Journey"
            )
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            
            # Create QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 string
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return ServiceResponse(True, data={
                'qr_code': f"data:image/png;base64,{img_base64}",
                'secret_key': secret_key,
                'totp_uri': totp_uri
            })
            
        except Exception as e:
            return ServiceResponse(False, message="Failed to generate QR code", error=str(e))
    
    def verify_totp_code(self, secret_key, user_code):
        """Verify TOTP code entered by user"""
        try:
            totp = pyotp.TOTP(secret_key)
            
            # Increase time window for better tolerance
            is_valid = totp.verify(user_code, valid_window=2)  # Allow 2 windows (±60 seconds)
            
            # Debug information
            current_code = totp.now()
            print(f"Debug - User code: {user_code}, Current expected: {current_code}, Valid: {is_valid}")
            
            return is_valid
        except Exception as e:
            print(f"TOTP verification error: {e}")
            return False
    
    def enable_2fa(self, account_id, totp_code, secret_key):
        """Enable 2FA for an account after verifying TOTP code"""
        try:
            account = Account.get(account_id)
            if not account:
                return ServiceResponse(False, message="Account not found")
            
            if account.is2fa_enabled:
                return ServiceResponse(False, message="2FA is already enabled")
            
            # Verify the TOTP code with the provided secret
            if not secret_key:
                return ServiceResponse(False, message="No setup in progress. Please start 2FA setup again.")
            
            if not self.verify_totp_code(secret_key, totp_code):
                return ServiceResponse(False, message="Invalid verification code")
            
            # Generate backup codes
            backup_codes = [secrets.token_hex(4).upper() for _ in range(10)]
            
            # Save to database
            account.change(
                totp_secret=secret_key,
                backup_codes=json.dumps(backup_codes),
                is2fa_enabled=True
            ).commit()
            
            return ServiceResponse(True, data={
                'backup_codes': backup_codes,
                'message': "2FA enabled successfully"
            })
            
        except Exception as e:
            self.db.session.rollback()
            return ServiceResponse(False, message="Failed to enable 2FA", error=str(e))
    def disable_2fa(self, account_id, password, totp_code_or_backup):
        """Disable 2FA for an account"""
        try:
            account = Account.get(account_id)
            if not account:
                return ServiceResponse(False, message="Account not found")
            
            if not account.is2fa_enabled:
                return ServiceResponse(False, message="2FA is not enabled")
            
            # Verify password first
            from werkzeug.security import check_password_hash
            if not check_password_hash(account.password_hash, password):
                return ServiceResponse(False, message="Invalid password")
            
            # Verify TOTP code or backup code
            is_valid = False
            used_backup_code = None
            
            # Try TOTP first
            if self.verify_totp_code(account.totp_secret, totp_code_or_backup):
                is_valid = True
            else:
                # Try backup codes
                backup_codes = json.loads(account.backup_codes or '[]')
                if totp_code_or_backup.upper() in backup_codes:
                    is_valid = True
                    used_backup_code = totp_code_or_backup.upper()
                    backup_codes.remove(used_backup_code)
                    account.backup_codes = json.dumps(backup_codes)
            
            if not is_valid:
                return ServiceResponse(False, message="Invalid verification code or backup code")
              # Disable 2FA
            account.change(
                is2fa_enabled=False,
                totp_secret=None,
                backup_codes=None
            ).commit()
            
            return ServiceResponse(True, message="2FA disabled successfully")
            
        except Exception as e:
            self.db.session.rollback()
            return ServiceResponse(False, message="Failed to disable 2FA", error=str(e))
    
    def setup_2fa(self, account_id):
        """Start 2FA setup process"""
        try:
            account = Account.get(account_id)
            if not account:
                return ServiceResponse(False, message="Account not found")
            
            if account.is2fa_enabled:
                return ServiceResponse(False, message="2FA is already enabled")
            
            # Generate secret key
            secret_key = self.generate_secret_key()
            
            # Generate QR code
            qr_result = self.generate_qr_code(account, secret_key)
            
            if qr_result.success:
                # Return secret_key so it can be stored in session
                return ServiceResponse(True, data={
                    **qr_result.data,
                    'account_id': account_id
                })
            else:
                return qr_result
                
        except Exception as e:
            return ServiceResponse(False, message="Failed to setup 2FA", error=str(e))
    
    def verify_2fa_login(self, account_id, totp_code_or_backup):
        """Verify 2FA code during login"""
        try:
            account = Account.get(account_id)
            if not account:
                return ServiceResponse(False, message="Account not found")
            
            if not account.is2fa_enabled:
                return ServiceResponse(True, message="2FA not required")
              # Try TOTP first
            if self.verify_totp_code(account.totp_secret, totp_code_or_backup):
                return ServiceResponse(True, data=account, message="2FA verification successful")
            
            # Try backup codes
            backup_codes = json.loads(account.backup_codes or '[]')
            if totp_code_or_backup.upper() in backup_codes:
                # Use backup code (remove it)
                backup_codes.remove(totp_code_or_backup.upper())
                account.backup_codes = json.dumps(backup_codes)
                self.db.session.commit()
                
                return ServiceResponse(True, data=account, message="2FA verification successful (backup code used)")
            
            return ServiceResponse(False, message="Invalid verification code")
            
        except Exception as e:
            return ServiceResponse(False, message="2FA verification failed", error=str(e))
