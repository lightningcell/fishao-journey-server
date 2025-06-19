from models import db, BaseEntity
from enums.enum_inventory_type import InventoryType
from sqlalchemy import JSON

# Association Table for Player-FruitCombination Many-to-Many relationship
player_fruit_combination = db.Table(
    'player_fruit_combination',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('fruit_combination_id', db.Integer, db.ForeignKey('fruit_combination.id'), primary_key=True)
)


class FruitCombination(BaseEntity):
    __tablename__ = 'fruit_combination'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Fruit references
    fruit1_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
    fruit2_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
    fruit3_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
    
    # Reward data stored as JSON
    # Structure: {
    #   "item_type": <InventoryType enum key>,
    #   "amount": <integer>,
    #   "type": <string>
    # }
    reward_data = db.Column(JSON, nullable=False)
    
    # Relationships
    fruit1 = db.relationship('Fruit', foreign_keys=[fruit1_id])
    fruit2 = db.relationship('Fruit', foreign_keys=[fruit2_id])
    fruit3 = db.relationship('Fruit', foreign_keys=[fruit3_id])
      # Many-to-Many relationship with Player
    players = db.relationship(
        'Player',
        secondary=player_fruit_combination,
        backref='fruit_combinations'
    )
    
    # Note: Fish relationship is defined in Fish model with backref='unlocked_fish'
    
    def __repr__(self):
        return f'<FruitCombination {self.id}: {self.fruit1.name if self.fruit1 else "?"}-{self.fruit2.name if self.fruit2 else "?"}-{self.fruit3.name if self.fruit3 else "?"}>'
    
    def get_reward_description(self):
        """Get a human-readable description of the reward"""
        if not self.reward_data:
            return "No reward"
        
        item_type = self.reward_data.get('item_type')
        amount = self.reward_data.get('amount', 1)
        reward_type = self.reward_data.get('type', 'Unknown')
        
        if item_type:
            return f"{amount} {item_type}"
        
        return f"{reward_type}: {amount}"
    
    def validate_reward_data(self):
        """Validate the reward_data structure"""
        if not self.reward_data:
            return False, "reward_data is required"
        
        required_fields = ['item_type', 'amount', 'type']
        for field in required_fields:
            if field not in self.reward_data:
                return False, f"Missing required field: {field}"
        
        # Validate item_type is a valid InventoryType
        item_type = self.reward_data.get('item_type')
        try:
            InventoryType(item_type)
        except ValueError:
            return False, f"Invalid item_type: {item_type}"
        
        # Validate amount is positive integer
        amount = self.reward_data.get('amount')
        if not isinstance(amount, int) or amount <= 0:
            return False, "amount must be a positive integer"
        
        return True, "Valid"
