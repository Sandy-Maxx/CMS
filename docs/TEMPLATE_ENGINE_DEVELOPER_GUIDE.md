# Template Engine Developer Guide

This document provides comprehensive technical documentation for developers working with the CMS Template Engine and Placeholder System.

## Architecture Overview

The template engine consists of several key components:

1. **Database Layer**: Dynamic column discovery and data retrieval
2. **Placeholder Generation**: Automatic placeholder creation from database schema
3. **Template Processing**: Multi-pass placeholder replacement
4. **Special Handlers**: Computed and custom placeholder logic

## Core Components

### 1. Database Schema Discovery

**File**: `database/managers/database_utils.py`

The system dynamically discovers database columns using SQLite's `PRAGMA table_info()`:

```python
def get_work_columns():
    """Get all column names from the works table dynamically."""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.execute("PRAGMA table_info(works)")
        columns = [row[1] for row in cursor.fetchall()]
        return columns
    finally:
        conn.close()
```

**Key Benefits**:
- New columns are immediately available as placeholders
- No code changes required for simple database additions
- Maintains schema flexibility

### 2. Placeholder Generation

**File**: `features/template_engine/work_data_provider.py`

The `WorkDataProvider` class generates placeholders in three categories:

#### Work-Level Placeholders (`[PLACEHOLDER]`)
```python
# Generate work placeholders: [COLUMN_NAME] format
work_placeholders = {}
if self.work_details:
    for column in work_columns:
        work_placeholders[f'[{column.upper()}]'] = self.work_details.get(column)
```

#### Firm-Level Placeholders (`<<PLACEHOLDER>>`)
```python
# Generate firm placeholders: <<COLUMN_NAME>> format
firm_placeholders = {}
for firm_doc in self.firm_documents:
    for column in firm_columns:
        firm_placeholders[f'<<{column.upper()}>'] = firm_doc.get(column)
```

#### Special Placeholders
```python
special_placeholders = {
    '[CURRENT_DATE]': datetime.now().strftime("%Y-%m-%d"),
    '[CURRENT_TIME]': datetime.now().strftime("%H:%M:%S"),
    '[FIRM_PG_DETAILS]': self._generate_firm_pg_details(),
    '[ALL_FIRMS_PG_DETAILS]': self._generate_all_firms_pg_details()
}
```

### 3. Database Migration System

**File**: `database/db_manager.py`

The application uses a simple but effective migration pattern:

```python
def create_tables():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create base table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    # Add new columns if they don't exist
    columns_to_add = {
        "justification": "TEXT",
        "section": "TEXT",
        "work_type": "TEXT",
        "file_no": "TEXT",
        "estimate_no": "TEXT",
        "tender_cost": "REAL",
        # ... more columns
    }

    for column, col_type in columns_to_add.items():
        try:
            cursor.execute(f"ALTER TABLE works ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                raise
    
    conn.commit()
    conn.close()
```

**Migration Workflow**:
1. Application starts → `create_tables()` is called
2. Base table is created if it doesn't exist
3. New columns are added via `ALTER TABLE` statements
4. Duplicate column errors are ignored
5. New placeholders become immediately available

### 4. Template Processing Pipeline

**File**: `features/template_engine/template_processor.py`

The template processing follows a three-pass approach:

#### Pass 1: Work-Level Data (`[PLACEHOLDER]`)
```python
def replace_work_placeholders(self, content, work_data):
    """Replace [PLACEHOLDER] tokens with work data."""
    pattern = r'\[([A-Z_]+)\]'
    
    def replace_func(match):
        placeholder_key = match.group(1)
        return str(work_data.get(placeholder_key, match.group(0)))
    
    return re.sub(pattern, replace_func, content)
```

#### Pass 2: Firm-Level Data (`<<PLACEHOLDER>>`)
```python
def replace_firm_placeholders(self, content, firm_data):
    """Replace <<PLACEHOLDER>> tokens with firm data."""
    pattern = r'<<([A-Z_]+)>>'
    
    def replace_func(match):
        placeholder_key = match.group(1)
        return str(firm_data.get(placeholder_key, match.group(0)))
    
    return re.sub(pattern, replace_func, content)
```

#### Pass 3: User Input (`{{placeholder}}`)
```python
def replace_user_placeholders(self, content, user_data):
    """Replace {{placeholder}} tokens with user input."""
    pattern = r'\{\{([a-zA-Z0-9_.]+)\}\}'
    
    def replace_func(match):
        placeholder_key = match.group(1)
        return str(user_data.get(placeholder_key, match.group(0)))
    
    return re.sub(pattern, replace_func, content)
```

### 5. Special Placeholder Handler

**File**: `features/template_engine/special_placeholder_handler.py`

Handles computed placeholders with custom logic:

```python
def evaluate_special_placeholder(placeholder_name, data):
    # Only process placeholders starting with "COST"
    if placeholder_name.startswith("COST"):
        parts = placeholder_name.split("_")
        base_cost_key = parts[0]  # e.g., "COST"

        # Get the base cost value
        base_value = data.get(base_cost_key)
        if base_value is None or base_value == "":
            return f"{{{{{placeholder_name}}}}}"  # Return original if base not found

        try:
            result = Decimal(str(base_value))
        except Exception:
            return f"{{{{{placeholder_name}}}}}"  # Return original if not numeric

        format_as_words = False
        round_to_nearest = None

        for part in parts[1:]:
            if part == "IN" and "WORDS" in parts:
                format_as_words = True
            elif part.strip() == "00":  # Round to nearest 100
                round_to_nearest = Decimal(100)
            elif part.strip() == "0":   # Round to nearest 10
                round_to_nearest = Decimal(10)
            elif part.replace('.', '', 1).isdigit():  # Numeric multiplier
                result *= Decimal(part)

        if round_to_nearest:
            result = (result / round_to_nearest).to_integral_value(rounding=ROUND_HALF_UP) * round_to_nearest

        if format_as_words:
            return number_to_indian_words(float(result))
        else:
            return format_currency_inr(result)

    # If not a COST-based placeholder, return from data or leave unchanged
    return data.get(placeholder_name, f"{{{{{placeholder_name}}}}}")
```

## Adding New Features

### Adding a New Database Column

1. **Update the migration dictionary**:
   ```python
   columns_to_add = {
       # ... existing columns ...
       "contract_duration": "INTEGER",
       "project_manager": "TEXT",
   }
   ```

2. **The placeholders become automatically available**:
   - `[CONTRACT_DURATION]`
   - `[PROJECT_MANAGER]`

3. **Add descriptions (optional)**:
   ```python
   work_descriptions = {
       # ... existing descriptions ...
       'contract_duration': 'Duration of contract in months',
       'project_manager': 'Name of the project manager',
   }
   ```

### Creating Custom Special Placeholders

1. **Modify `special_placeholder_handler.py`**:
   ```python
   def evaluate_special_placeholder(placeholder_name, data):
       # Add your custom logic
       if placeholder_name.startswith("CUSTOM"):
           parts = placeholder_name.split("_")
           if len(parts) > 1 and parts[1] == "UPPER":
               base_value = data.get("CUSTOM")
               return str(base_value).upper() if base_value else ""
       
       # Existing COST logic...
   ```

2. **Use in templates**:
   ```
   {{CUSTOM}} = "hello world"
   {{CUSTOM_UPPER}} = "HELLO WORLD"
   ```

### Adding New Placeholder Categories

1. **Extend the constants**:
   ```python
   # In features/AutodocGen/constants.py
   PROJECT_PLACEHOLDER_PATTERN = r"%%([a-zA-Z0-9_]+)%%"
   ```

2. **Update the placeholder parser**:
   ```python
   # In features/AutodocGen/placeholder_parser.py
   project_placeholders = set()
   project_placeholders.update(re.findall(PROJECT_PLACEHOLDER_PATTERN, text_content))
   ```

3. **Add processing logic**:
   ```python
   # In template processor
   def replace_project_placeholders(self, content, project_data):
       pattern = r'%%([A-Z_]+)%%'
       # ... replacement logic
   ```

## Best Practices

### Database Design
- Use descriptive column names that make sense as placeholders
- Follow `snake_case` convention for column names
- Avoid special characters that might break placeholder parsing
- Consider the placeholder name when designing the schema

### Performance Considerations
- Database column discovery is cached at the class level
- Use `SELECT *` judiciously - it's used for dynamic column handling
- Consider indexing frequently accessed columns
- Keep special placeholder logic efficient

### Error Handling
- Unknown placeholders are left untouched for debugging
- Invalid numeric values in special placeholders return the original placeholder
- Database connection errors are handled gracefully
- Log meaningful error messages for troubleshooting

### Testing
- Test new placeholders with actual data
- Verify special placeholder logic with edge cases
- Test database migrations on different schema versions
- Validate placeholder parsing with complex templates

## Debugging Guide

### Common Issues

1. **Placeholder not replaced**:
   - Check case sensitivity (must be ALL CAPS for `[]` and `<<>>`)
   - Verify column exists in database: `PRAGMA table_info(table_name)`
   - Check placeholder syntax (brackets, spelling)

2. **Special placeholder not working**:
   - Ensure base placeholder exists in data
   - Check special placeholder handler logic
   - Verify syntax follows the expected pattern

3. **Database column not appearing**:
   - Check if migration ran successfully
   - Verify column was added to the correct table
   - Restart application if using cached column lists

### Debugging Tools

1. **Database inspection**:
   ```python
   # Check table structure
   cursor.execute("PRAGMA table_info(works)")
   columns = cursor.fetchall()
   print(columns)
   ```

2. **Placeholder inspection**:
   ```python
   # List all available placeholders
   provider = WorkDataProvider(work_id)
   placeholders = provider.get_available_placeholders()
   for key, desc in placeholders.items():
       print(f"{key}: {desc}")
   ```

3. **Template testing**:
   - Use simple templates to test individual placeholders
   - Check generated documents for untouched placeholders
   - Enable debug logging in template processor

## Security Considerations

- User input is not directly executed as code
- SQL injection is prevented through parameterized queries
- File paths are validated before template processing
- Special placeholder logic has input validation

## Future Enhancements

Potential areas for improvement:

1. **Conditional Placeholders**: `{{IF condition}}...{{ENDIF}}`
2. **Loop Placeholders**: `{{FOR item IN list}}...{{ENDFOR}}`
3. **Date Formatting**: `{{date:YYYY-MM-DD}}`
4. **Mathematical Expressions**: `{{COST * 1.1 + TAX}}`
5. **Template Inheritance**: Base templates with overrides
6. **Placeholder Validation**: Schema-based validation
7. **Multi-language Support**: Localized placeholder names

## Migration from Legacy Systems

When migrating from older placeholder systems:

1. **Audit existing templates** for placeholder usage
2. **Map legacy placeholders** to new database columns
3. **Create aliases** for backward compatibility
4. **Update documentation** and user training materials
5. **Provide migration tools** for bulk template updates
