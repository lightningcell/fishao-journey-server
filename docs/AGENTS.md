# AGENTS.md - OpenAI Codex Project Understanding Guide

This document provides comprehensive information about the Fishao Journey Server project structure and development processes to help AI coding agents understand and work with this codebase effectively.

## 🎮 Project Overview

**Fishao Journey Server** is a Flask-based backend application for a fishing simulation game. The project implements a comprehensive gaming ecosystem with players, fish, areas, equipment, social features, and game progression mechanics.

### Core Game Concepts
- **Players**: Registered users with profiles, stats, inventory, and progression
- **Fish**: Various fish species with different rarities, locations, and properties
- **Areas**: Game locations where players can fish, each with specific fish populations
- **Equipment**: Rods, baits, and other fishing gear affecting gameplay
- **Social Features**: Clubs, friends, chat, and player interactions
- **Home System**: Player housing with decorations and fish collections
- **Tasks & Progression**: Missions, achievements, and character advancement

## 🛠 Technology Stack

### Core Framework & Database
- **Flask 2.3.3**: Python web framework
- **SQLAlchemy 3.0.5**: ORM for database operations
- **Flask-Migrate 4.0.5**: Database migration management
- **SQLite**: Development database (fishao.db)

### Additional Dependencies
- **python-dotenv 1.0.0**: Environment variable management

## 📁 Project Structure

```
fishao-journey-server/
├── app.py                  # Main Flask application entry point
├── seed.py                 # Database seeding with initial data
├── requirements.txt        # Python dependencies
├── migrations/             # Flask-Migrate database migrations
│   ├── versions/          # Individual migration files
│   └── alembic.ini        # Alembic configuration
├── models/                # SQLAlchemy model definitions
│   ├── __init__.py        # Model imports and db initialization
│   ├── base_entity.py     # Base class for all entities
│   ├── player/            # Player-related models
│   ├── fishing/           # Fish and fishing-related models
│   ├── item/              # Items and inventory models
│   ├── area/              # Game areas and locations
│   ├── home/              # Player housing and decorations
│   ├── club/              # Social clubs and memberships
│   ├── task/              # Missions and achievements
│   ├── trade/             # Player trading system
│   ├── chat/              # Messaging and communication
│   ├── outfit/            # Player appearance and customization
│   ├── report/            # Moderation and reporting system
│   └── payment_integration/ # Payment processing
├── enums/                 # Enumeration definitions
├── docs/                  # Documentation files
└── instance/              # Instance-specific files (SQLite DB)
```

## 🏗 Architecture Patterns

### BaseEntity Pattern (Mendix-Inspired)
All database models inherit from `BaseEntity`, providing consistent CRUD operations:

```python
class BaseEntity(db.Model):
    def create(self, commit=True)    # Create and optionally save
    def commit(self)                 # Save changes to database
    def delete(self, commit=True)    # Delete and optionally commit
    def change(self, **kwargs)       # Update multiple attributes
```

**Usage Example:**
```python
player = Player(username='john', email='john@example.com')
player.create()  # Creates and saves to database
player.change(level=5, xp=1000).commit()  # Updates and saves
```

### Polymorphic Inheritance
- `Account` base class with `Player` subclass
- `Item` base class with `ShopItem` subclass
- Uses SQLAlchemy's polymorphic features for table inheritance

### Relationship Patterns
- **One-to-One**: Player ↔ PlayerSettings, Player ↔ MoneyTree
- **One-to-Many**: Player → Items, Area → Fish, Player → FishingLogs
- **Many-to-Many**: Fish ↔ Areas, Player ↔ Friends, Fish ↔ BaitCategories
- **Self-Referential**: Area parent/sub-areas, Player friendships

## 🗄 Database Migration Commands

### Essential Migration Workflow

#### 1. Initial Setup (one-time only)
```bash
flask db init
```
*Creates the migrations folder structure and configuration*

#### 2. Create Migration After Model Changes
```bash
flask db migrate -m "Descriptive message about changes"
```
*Generates a new migration file based on model changes*

#### 3. Apply Migrations to Database
```bash
flask db upgrade
```
*Executes pending migrations to update database schema*

#### 4. Rollback Changes
```bash
flask db downgrade
```
*Reverts the last migration*

#### 5. Migration History and Status
```bash
flask db history          # View migration history
flask db current          # Check current database revision
flask db show <revision>  # Show details of specific migration
```

### Development Best Practices

1. **Always create migrations after model changes**
2. **Review generated migration files before applying**
3. **Use descriptive migration messages**
4. **Test migrations in development before production**
5. **Include migration files in version control**
6. **Never edit applied migrations - create new ones instead**

### Common Migration Scenarios

```bash
# Adding new model or field
flask db migrate -m "Add player last_activity_date field"

# Modifying existing relationships
flask db migrate -m "Update fish-area relationship constraints"

# Adding indexes for performance
flask db migrate -m "Add index on player username and email"

# Data migrations (be careful with these)
flask db migrate -m "Migrate old player data to new format"
```

## 🎯 Key Models and Relationships

### Player Ecosystem
- **Player**: Core user entity with game stats and progression
- **PlayerSettings**: User preferences and configuration
- **PlayerStats**: Detailed gameplay statistics
- **Account**: Base authentication and profile information

### Fishing System
- **Fish**: Species with properties (rarity, length, breeding info)
- **Area**: Fishing locations with level requirements
- **FishingLog**: Records of caught fish with details
- **FishingLine**: Player's fishing equipment upgrades

### Inventory System
- **Item**: Polymorphic base for all inventory items
- **Bait**: Fishing bait with categories and effectiveness
- **Rod**: Fishing rods with sizes and quality ratings
- **Decoration**: Home decoration items
- **Look**: Cosmetic appearance items
- **Fruit**: Special items for various game mechanics

### Social Features
- **Club**: Player groups with leadership and membership
- **ClubPlayer**: Membership relationships
- **PM**: Private messaging between players
- **ChatLog**: Public chat message history

### Game Progression
- **Task**: Missions and objectives for players
- **TaskCompletion**: Player progress on specific tasks
- **TaskAward**: Rewards for completing tasks
- **UpgradeRecord**: History of player upgrades

## 🔧 Development Commands

### Database Operations
```bash
# Reset and seed database (development only)
python seed.py

# Start Flask development server
python app.py

# Create fresh migration after model changes
flask db migrate -m "Your change description"

# Apply migrations
flask db upgrade
```

### Project Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (if not done)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade

# Seed with sample data
python seed.py
```

## 📊 Data Initialization

The `seed.py` file provides comprehensive sample data including:
- Sample areas and special locations
- Fish species with properties and relationships
- Player accounts with complete profiles
- Inventory items and equipment
- Club structures and memberships
- Tasks and progression data
- Home decorations and plans

## 🔍 Common Code Patterns

### Entity Creation Pattern
```python
# Standard entity creation with relationships
area = Area(name='Test Area', level_requirement=1).create()
fish = Fish(name='Salmon').create()
AreaFish(area=area, fish=fish).create()
```

### Querying with Relationships
```python
# Get player with all related data
player = Player.query.filter_by(username='john').first()
player_items = player.items.all()
player_fishing_logs = player.fishing_logs.limit(10).all()
```

### Enumeration Usage
```python
from enums.enum_inventory_type import InventoryType
from enums.enum_rod_sizes import RodSizes

# Creating items with proper types
bait_item = Item(
    amount=5, 
    item_type=InventoryType.Bait,
    bait=bait,
    player=player
).create()
```

## ⚠️ Important Notes for AI Agents

1. **Always use BaseEntity methods** (`create()`, `commit()`, `delete()`, `change()`) for database operations
2. **Respect foreign key relationships** when creating or modifying entities
3. **Use enums consistently** for type safety and data integrity
4. **Follow migration workflow** for any schema changes
5. **Check existing relationships** before creating new ones to avoid duplicates
6. **Use lazy loading appropriately** for performance optimization
7. **Handle polymorphic inheritance** correctly when working with Account/Player and Item hierarchies

## 🚀 Quick Start for AI Agents

1. **Understand the domain**: This is a fishing game with complex social and progression mechanics
2. **Start with models**: Review the model definitions in `models/` to understand data structure
3. **Check relationships**: Pay attention to foreign keys and relationship configurations
4. **Use BaseEntity**: Leverage the consistent CRUD interface for all database operations
5. **Follow migration workflow**: Always create migrations for schema changes
6. **Test with seed data**: Use `seed.py` to populate development database with realistic data

## 📝 File Modification Guidelines

When modifying this project:

1. **Model Changes**: Always followed by `flask db migrate`
2. **New Models**: Add to appropriate `models/` subdirectory and update `__init__.py`
3. **New Enums**: Create in `enums/` directory with descriptive names
4. **Database Schema**: Use migrations, never direct SQL modifications
5. **Relationships**: Define both sides of relationships for proper ORM functionality

This documentation provides the foundation for understanding and working with the Fishao Journey Server codebase. The project follows Flask and SQLAlchemy best practices while implementing domain-specific patterns for game development.
