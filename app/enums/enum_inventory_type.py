from enum import Enum

class InventoryType(Enum):
    # Only Amount
    Shell = "Shell"
    Fishbucks = "Fishbucks"
    Fishcoins = "Fishcoins"
    Energy = "Energy"
    
    # Amount and Type
    Fruit = "Fruit"
    Look = "Look"
    Bait = "Bait"
    Rod = "Rod"
    Decoration = "Decoration"
    
    # Only Type
    Fish = "Fish"
    
    # Special Types
    Fishbox = "Fishbox"
    
    def is_only_amount(self):
        return self in {InventoryType.Shell, InventoryType.Fishbucks, InventoryType.Fishcoins, InventoryType.Energy}
    
    def is_amount_and_type(self):
        return self in {InventoryType.Fruit, InventoryType.Look, InventoryType.Bait, InventoryType.Rod, InventoryType.Decoration}
    
    def is_only_type(self):
        return self in {InventoryType.Fish, InventoryType.Fishbox}
    
    def is_special_type(self):
        return self == InventoryType.Fishbox
