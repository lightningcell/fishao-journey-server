# Fishao Journey Server

Flask-Migrate has been integrated into this project. You can now manage database changes safely.

## Flask-Migrate Usage

### Installation
```bash
pip install -r requirements.txt
```

### Migration Commands

#### 1. Initial setup (only once)
```bash
flask db init
```

#### 2. Create migration after model changes
```bash
flask db migrate -m "Descriptive message"
```

#### 3. Apply migration to database
```bash
flask db upgrade
```

#### 4. Rollback (downgrade)
```bash
flask db downgrade
```

#### 5. View migration history
```bash
flask db history
```

#### 6. Check current revision
```bash
flask db current
```

### Development Process

1. **Make model changes**: Edit files in the `models/` folder
2. **Create migration**: `flask db migrate -m "change description"`
3. **Review migration**: Check the generated file in `migrations/versions/` folder
4. **Apply**: `flask db upgrade`

### Important Notes

- No need to delete database files anymore
- Don't forget to create migrations after every model change
- Add migration files to version control (git)
- Apply migrations carefully in production

### Current File Structure

```
project/
├── app.py              # Main Flask application file
├── models/             # All models
├── migrations/         # Migration files (auto-generated)
│   ├── versions/       # Migration versions
│   └── alembic.ini     # Alembic configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Example Workflow

```bash
# After making model changes
flask db migrate -m "Added new field to Player model"

# Apply changes
flask db upgrade

# If you want to rollback
flask db downgrade
```

This way you can safely manage your database schema and stay synchronized with your team members. 