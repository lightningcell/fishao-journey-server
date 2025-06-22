from . import db
from sqlalchemy import asc, desc

class PaginationResult:
    """
    Pagination sonuçlarını tutan sınıf
    """
    
    def __init__(self, items, total, pages, page, per_page, has_prev, has_next, prev_num, next_num):
        """
        PaginationResult oluşturucu
        
        Args:
            items: Sayfadaki entity'lerin listesi
            total (int): Toplam kayıt sayısı
            pages (int): Toplam sayfa sayısı
            page (int): Mevcut sayfa numarası
            per_page (int): Sayfa başına kayıt sayısı
            has_prev (bool): Önceki sayfa var mı
            has_next (bool): Sonraki sayfa var mı
            prev_num (int): Önceki sayfa numarası
            next_num (int): Sonraki sayfa numarası
        """
        self.items = items
        self.total = total
        self.pages = pages
        self.page = page
        self.per_page = per_page
        self.has_prev = has_prev
        self.has_next = has_next
        self.prev_num = prev_num
        self.next_num = next_num
    
    def to_dict(self):
        """
        PaginationResult'ı dictionary'ye çevir
        
        Returns:
            dict: Pagination bilgileri içeren dictionary
        """
        return {
            'items': self.items,
            'total': self.total,
            'pages': self.pages,
            'page': self.page,
            'per_page': self.per_page,
            'has_prev': self.has_prev,
            'has_next': self.has_next,
            'prev_num': self.prev_num,
            'next_num': self.next_num
        }
    
    def __repr__(self):
        return f"<PaginationResult page={self.page}/{self.pages}, total={self.total}, items={len(self.items)}>"

class BaseEntity(db.Model):
    """
    Tüm persistable entity'lerin miras alacağı temel sınıf
    Mendix tarzı Entity yaklaşımını implement eder
    
    Bu sınıf temel aksiyonları sağlar:
    - Create: Entity oluşturma
    - Commit: Entity'yi veritabanına kaydetme  
    - Delete: Entity silme
    - Change: Entity özelliklerini değiştirme
    - Get: Id ile entity getirme
    - GetAll: Tüm entity'leri getirme
    - GetPaginated: Pagination ile entity'leri getirme
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
            BaseEntity: Bu entity instance'ı        """
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
    
    @classmethod
    def get(cls, entity_id):
        """
        Id ile entity getirme
        
        Args:
            entity_id: Entity'nin id'si
            
        Returns:
            BaseEntity: Bulunan entity instance'ı veya None
        """
        return cls.query.get(entity_id)
    
    @classmethod
    def get_all(cls, order_by=None, order_desc=False):
        """
        Tüm entity'leri getirme
        
        Args:
            order_by (str): Sıralama yapılacak alan adı
            order_desc (bool): Azalan sıralama yapılsın mı
            
        Returns:
            list: Tüm entity'lerin listesi
        """
        query = cls.query
        
        if order_by and hasattr(cls, order_by):            
            order_column = getattr(cls, order_by)
            if order_desc:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))
        
        return query.all()
    
    @classmethod
    def get_paginated(cls, page=1, per_page=20, order_by=None, order_desc=False):
        """
        Pagination ile entity'leri getirme
        
        Args:
            page (int): Sayfa numarası (1'den başlar)
            per_page (int): Sayfa başına kayıt sayısı
            order_by (str): Sıralama yapılacak alan adı
            order_desc (bool): Azalan sıralama yapılsın mı
            
        Returns:
            PaginationResult: Pagination bilgileri içeren nesne
        """
        query = cls.query
        
        if order_by and hasattr(cls, order_by):
            order_column = getattr(cls, order_by)
            if order_desc:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))
        
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return PaginationResult(
            items=pagination.items,
            total=pagination.total,
            pages=pagination.pages,
            page=pagination.page,
            per_page=pagination.per_page,
            has_prev=pagination.has_prev,
            has_next=pagination.has_next,
            prev_num=pagination.prev_num,
            next_num=pagination.next_num
        )
    
    @classmethod
    def count(cls):
        """
        Toplam kayıt sayısını getirme
        
        Returns:
            int: Toplam kayıt sayısı
        """
        return cls.query.count()
