from .base import BaseService, ServiceResponse
from models.player.account_role import AccountRole
from models.player.account import Account

class RoleService(BaseService):
    """
    Role (Rol) yönetimi için servis sınıfı
    Kullanıcının rollerini kontrol etme ve yönetme işlevlerini sağlar
    """
    
    # Rol sabitleri
    ADMIN = 'Admin'
    DEVELOPER = 'Developer' 
    PLAYER = 'Player'
    MODERATOR = 'Moderator'
    
    def __init__(self, db):
        super().__init__(db)
    
    def is_admin(self, account_id):
        """
        Kullanıcının Admin rolü olup olmadığını kontrol eder
        
        Args:
            account_id (int): Kullanıcı ID'si
            
        Returns:
            bool: Admin ise True, değilse False
        """
        return self._has_role(account_id, self.ADMIN)
    
    def is_developer(self, account_id):
        """
        Kullanıcının Developer rolü olup olmadığını kontrol eder
        
        Args:
            account_id (int): Kullanıcı ID'si
            
        Returns:
            bool: Developer ise True, değilse False
        """
        return self._has_role(account_id, self.DEVELOPER)
    
    def is_player(self, account_id):
        """
        Kullanıcının Player rolü olup olmadığını kontrol eder
        
        Args:
            account_id (int): Kullanıcı ID'si
            
        Returns:
            bool: Player ise True, değilse False
        """
        return self._has_role(account_id, self.PLAYER)
    
    def is_moderator(self, account_id):
        """
        Kullanıcının Moderator rolü olup olmadığını kontrol eder
        
        Args:
            account_id (int): Kullanıcı ID'si
            
        Returns:
            bool: Moderator ise True, değilse False
        """
        return self._has_role(account_id, self.MODERATOR)
    
    def get_user_roles(self, account_id):
        """
        Kullanıcının tüm rollerini getirir
        
        Args:
            account_id (int): Kullanıcı ID'si
            
        Returns:
            ServiceResponse: Kullanıcının rolleri listesini içeren response
        """
        try:
            account = Account.get(account_id)
            if not account:
                return ServiceResponse(
                    success=False,
                    message="Kullanıcı bulunamadı",
                    error="ACCOUNT_NOT_FOUND"
                )
            
            roles = [role.name for role in account.roles]
            return ServiceResponse(
                success=True,
                data=roles,
                message="Kullanıcı rolleri başarıyla getirildi"
            )
        except Exception as e:
            return ServiceResponse(
                success=False,
                message="Kullanıcı rolleri getirilemedi",
                error=str(e)
            )
    
    def add_role_to_user(self, account_id, role_name):
        """
        Kullanıcıya rol atar
        
        Args:
            account_id (int): Kullanıcı ID'si
            role_name (str): Atanacak rol adı
            
        Returns:
            ServiceResponse: İşlem sonucu
        """
        try:
            account = Account.get(account_id)
            if not account:
                return ServiceResponse(
                    success=False,
                    message="Kullanıcı bulunamadı",
                    error="ACCOUNT_NOT_FOUND"
                )
            
            role = AccountRole.query.filter_by(name=role_name).first()
            if not role:
                return ServiceResponse(
                    success=False,
                    message="Rol bulunamadı",
                    error="ROLE_NOT_FOUND"
                )
            
            # Kullanıcının zaten bu rolü var mı kontrol et
            if role in account.roles:
                return ServiceResponse(
                    success=False,
                    message="Kullanıcının zaten bu rolü mevcut",
                    error="ROLE_ALREADY_EXISTS"
                )
            
            account.roles.append(role)
            account.commit()
            
            return ServiceResponse(
                success=True,
                message=f"{role_name} rolü başarıyla atandı"
            )
        except Exception as e:
            return ServiceResponse(
                success=False,
                message="Rol atanamadı",
                error=str(e)
            )
    
    def remove_role_from_user(self, account_id, role_name):
        """
        Kullanıcıdan rol kaldırır
        
        Args:
            account_id (int): Kullanıcı ID'si
            role_name (str): Kaldırılacak rol adı
            
        Returns:
            ServiceResponse: İşlem sonucu
        """
        try:
            account = Account.get(account_id)
            if not account:
                return ServiceResponse(
                    success=False,
                    message="Kullanıcı bulunamadı",
                    error="ACCOUNT_NOT_FOUND"
                )
            
            role = AccountRole.query.filter_by(name=role_name).first()
            if not role:
                return ServiceResponse(
                    success=False,
                    message="Rol bulunamadı",
                    error="ROLE_NOT_FOUND"
                )
            
            # Kullanıcının bu rolü var mı kontrol et
            if role not in account.roles:
                return ServiceResponse(
                    success=False,
                    message="Kullanıcının bu rolü mevcut değil",
                    error="ROLE_NOT_EXISTS"
                )
            
            account.roles.remove(role)
            account.commit()
            
            return ServiceResponse(
                success=True,
                message=f"{role_name} rolü başarıyla kaldırıldı"
            )
        except Exception as e:
            return ServiceResponse(
                success=False,
                message="Rol kaldırılamadı",
                error=str(e)
            )
    
    def has_any_role(self, account_id, role_names):
        """
        Kullanıcının belirtilen rollerden herhangi birine sahip olup olmadığını kontrol eder
        
        Args:
            account_id (int): Kullanıcı ID'si
            role_names (list): Kontrol edilecek rol adları listesi
            
        Returns:
            bool: Herhangi bir role sahipse True, değilse False
        """
        try:
            account = Account.get(account_id)
            if not account:
                return False
            
            user_roles = [role.name for role in account.roles]
            return any(role in user_roles for role in role_names)
        except Exception:
            return False
    
    def has_all_roles(self, account_id, role_names):
        """
        Kullanıcının belirtilen tüm rollere sahip olup olmadığını kontrol eder
        
        Args:
            account_id (int): Kullanıcı ID'si
            role_names (list): Kontrol edilecek rol adları listesi
            
        Returns:
            bool: Tüm rollere sahipse True, değilse False
        """
        try:
            account = Account.get(account_id)
            if not account:
                return False
            
            user_roles = [role.name for role in account.roles]
            return all(role in user_roles for role in role_names)
        except Exception:
            return False
    
    def is_privileged_user(self, account_id):
        """
        Kullanıcının yetkili (Admin, Developer, Moderator) olup olmadığını kontrol eder
        
        Args:
            account_id (int): Kullanıcı ID'si
            
        Returns:
            bool: Yetkili ise True, değilse False
        """
        privileged_roles = [self.ADMIN, self.DEVELOPER, self.MODERATOR]
        return self.has_any_role(account_id, privileged_roles)
    
    def get_user_highest_role(self, account_id):
        """
        Kullanıcının en yüksek yetkili rolünü getirir
        Hiyerarşi: Admin > Developer > Moderator > Player
        
        Args:
            account_id (int): Kullanıcı ID'si
            
        Returns:
            str: En yüksek rol adı veya None
        """
        role_hierarchy = [self.ADMIN, self.DEVELOPER, self.MODERATOR, self.PLAYER]
        
        try:
            account = Account.get(account_id)
            if not account:
                return None
            
            user_roles = [role.name for role in account.roles]
            
            for role in role_hierarchy:
                if role in user_roles:
                    return role
            
            return None
        except Exception:
            return None
    
    def _has_role(self, account_id, role_name):
        """
        Kullanıcının belirtilen role sahip olup olmadığını kontrol eden yardımcı metod
        
        Args:
            account_id (int): Kullanıcı ID'si
            role_name (str): Kontrol edilecek rol adı
            
        Returns:
            bool: Role sahipse True, değilse False
        """
        try:
            account = Account.get(account_id)
            if not account:
                return False
            
            return any(role.name == role_name for role in account.roles)
        except Exception:
            return False
