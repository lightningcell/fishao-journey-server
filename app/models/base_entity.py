from . import db

class BaseEntity(db.Model):
    """
    Tüm persistable entity'lerin miras alacağı temel sınıf
    Mendix tarzı Entity yaklaşımını implement eder
    
    Bu sınıf 4 temel aksiyonu sağlar:
    - Create: Entity oluşturma
    - Commit: Entity'yi veritabanına kaydetme  
    - Delete: Entity silme
    - Change: Entity özelliklerini değiştirme
    """
    __abstract__ = True  # Bu sınıfın kendi tablosu oluşturulmasın
    
    def create(self, commit=True):
        """
        Entity oluşturma
        
        Args:
            commit (bool): Otomatik olarak veritabanına kaydedilsin mi
            
        Returns:
            BaseEntity: Bu entity instance'ı
        """
        db.session.add(self)
        if commit:
            return self.commit()
        return self
    
    def commit(self):
        """
        Entity'yi veritabanına kaydetme
        
        Returns:
            BaseEntity: Bu entity instance'ı
            
        Raises:
            Exception: Veritabanı hatası durumunda
        """
        try:
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, commit=True):
        """
        Entity silme
        
        Args:
            commit (bool): Otomatik olarak veritabanından silinsin mi
            
        Returns:
            BaseEntity: Bu entity instance'ı
        """
        db.session.delete(self)
        if commit:
            return self.commit()
        return self
    
    def change(self, **kwargs):
        """
        Entity özelliklerini değiştirme
        
        Args:
            **kwargs: Değiştirilecek alan-değer çiftleri
            
        Returns:
            BaseEntity: Bu entity instance'ı
            
        Example:
            player.change(level=5, xp=1000)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
