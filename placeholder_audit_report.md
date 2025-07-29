# Placeholder & Template-Merge Code Audit Report

## Executive Summary

This audit identifies all modules and classes that handle placeholder mapping and text replacement within the CMS application. The system uses multiple placeholder systems with different syntaxes and hard-coded mappings distributed across several modules.

## 1. Placeholder Mapping Systems

### 1.1 Work Data Provider (`features/template_engine/work_data_provider.py`)

**Primary placeholder mapping location - CRITICAL for refactoring**

**Hard-coded mappings:**
```python
# Lines 9-23: Main placeholder_map dictionary
self.placeholder_map = {
    'ID': 'work_id',
    'NAME': 'work_name', 
    'DESCRIPTION': 'description',
    'JUSTIFICATION': 'justification',
    'SECTION': 'section',
    'WORK_TYPE': 'work_type',
    'FILE_NO': 'file_no',
    'ESTIMATE_NO': 'estimate_no',
    'TENDER_COST': 'tender_cost',
    'TENDER_OPENING_DATE': 'tender_opening_date',
    'LOA_NO': 'loa_no',
    'LOA_DATE': 'loa_date',
    'WORK_COMMENCE_DATE': 'work_commence_date',
}
```

**Additional hard-coded logic:**
- Line 29: Special case for `'firm_pg_details'` placeholder
- Lines 42-55: Hard-coded field mapping for firm document data (tuple indices to dictionary keys)
- Lines 74-88: Duplicate field mapping in `get_firm_pg_details_block()`

### 1.2 AutodocGen Constants (`features/AutodocGen/constants.py`)

**Hard-coded placeholder patterns:**
```python
# Lines 11-22: Regex patterns for different placeholder types
USER_PLACEHOLDER_PATTERN = r"\{\{([a-zA-Z0-9_.]+)\}\}"          # {{placeholder}}
WORK_DATA_PLACEHOLDER_PATTERN = r"\[([a-zA-Z0-9_]+)\]"          # [PLACEHOLDER]
FIRM_PLACEHOLDER_PATTERN = r"<<([a-zA-Z0-9_]+)>>"              # <<PLACEHOLDER>>
ALL_FIRMS_PG_DETAILS_PATTERN = r"\[ALL_FIRMS_PG_DETAILS\]"     # Special case
```

### 1.3 AutodocGen Document Generator (`features/AutodocGen/document_generator.py`)

**Hard-coded mapping logic:**
- Lines 78-90: Date placeholder parsing with hard-coded format conversion
- Lines 96-116: Firm-specific placeholder mapping with hard-coded field names:
  ```python
  # Line 105-116: Hard-coded firm field mappings
  if lookup_key == 'firm_name':
      replacement_value = current_firm_name
  elif lookup_key == 'pg_submitted':
      replacement_value = "submitted the PG No." if firm_document_data.get('pg_submitted') == 1 else "did not submit the PG"
  elif lookup_key == 'indemnity_bond_submitted':
      replacement_value = "submitted the Indemnity Bond" if firm_document_data.get('indemnity_bond_submitted') == 1 else "did not submit the Indemnity Bond"
  ```

## 2. Text Replacement Engines

### 2.1 Template Processor (`features/template_engine/template_processor.py`)

**Main text replacement engine for {{placeholder}} syntax**

**Key methods performing text replacement:**
- `extract_placeholders()` (Lines 10-67): Extracts placeholders from Word documents
- `replace_placeholders()` (Lines 103-144): Main replacement coordinator
- `_replace_in_paragraph()` (Lines 146-185): Core text replacement logic

**Hard-coded logic:**
- Lines 57-64: Hard-coded rules for derived placeholder detection:
  ```python
  if p_name.startswith(("COST", "COSTAMC", "COSTRP", "COSTCON", "COSTCAMC")):
      if re.search(r"_([0-9.]+)$|_IN_WORDS$|_0$|_00$", p_name):
          is_derived = True
  ```
- Line 150: Hard-coded regex pattern for user input placeholders

### 2.2 Special Placeholder Handler (`features/template_engine/special_placeholder_handler.py`)

**Handles COST-based placeholder transformations**

**Hard-coded transformation rules:**
- Lines 10-43: Complex logic for COST placeholder variations
- Lines 28-35: Hard-coded suffix processing:
  ```python
  if part == "IN" and "WORDS" in parts:     # IN_WORDS handling
      format_as_words = True
  elif part.strip() == "00":                 # Rounding to 100
      round_to_nearest = Decimal(100)
  elif part.strip() == "0":                  # Rounding to 10
      round_to_nearest = Decimal(10)
  ```

### 2.3 AutodocGen Document Generator Text Replacement

**Handles [PLACEHOLDER] and <<PLACEHOLDER>> syntax**

**Key replacement method:**
- `_replace_placeholders_in_paragraph()` (Lines 49-127)

**Hard-coded logic:**
- Line 51: Hard-coded regex pattern for placeholder detection
- Lines 57-64: Special case handling for `[ALL_FIRMS_PG_DETAILS]`
- Lines 78-90: Hard-coded date format conversion logic

## 3. Supporting Modules with Hard-coded Mappings

### 3.1 PG Details Formatter (`features/AutodocGen/pg_details_formatter.py`)

**Hard-coded field access patterns:**
- Lines 14-30: Hard-coded tuple index mappings:
  ```python
  firm_name = doc_tuple[2]        # Index 2 = firm_name
  pg_submitted = doc_tuple[11]    # Index 11 = pg_submitted
  pg_no = doc_tuple[3]           # Index 3 = pg_no
  # ... more hard-coded indices
  ```

### 3.2 Template Data Manager (`database/managers/template_data_manager.py`)

**Database-based placeholder storage (less critical for immediate refactoring)**
- Stores placeholder values in database
- No hard-coded mappings, but manages template-specific placeholder data

## 4. Template Processing Flow

### 4.1 Template Engine Flow ({{placeholder}} syntax)
1. `TemplateProcessor.extract_placeholders()` → finds all {{placeholders}}
2. `TemplateProcessor.replace_placeholders()` → coordinates replacement
3. `WorkDataProvider.get_data()` → maps placeholder to database field
4. `evaluate_special_placeholder()` → handles COST transformations
5. `TemplateProcessor._replace_in_paragraph()` → performs text replacement

### 4.2 AutodocGen Flow ([PLACEHOLDER] and <<PLACEHOLDER>> syntax)
1. `PlaceholderParser.extract_placeholders()` → finds all placeholders by type
2. `DocumentGenerator.generate()` → coordinates document generation
3. `DocumentGenerator._replace_placeholders_in_paragraph()` → performs replacements
4. `WorkDataProvider.get_data()` → provides work data
5. Direct field mapping for firm-specific placeholders

## 5. Critical Areas Requiring Refactoring

### 5.1 **HIGH PRIORITY - Must Remove/Refactor**

1. **`WorkDataProvider.placeholder_map`** (Lines 9-23)
   - Central mapping dictionary
   - Controls all work-related placeholder resolution

2. **Hard-coded tuple index mappings** in multiple files:
   - `WorkDataProvider.get_firm_document_data()` (Lines 42-55)
   - `WorkDataProvider.get_firm_pg_details_block()` (Lines 74-88)
   - `PGDetailsFormatter.format_pg_details()` (Lines 14-30)

3. **Firm field mapping logic** in `DocumentGenerator` (Lines 105-116)
   - Hard-coded field name to display text conversions

### 5.2 **MEDIUM PRIORITY - Consider Refactoring**

1. **COST placeholder processing** in `SpecialPlaceholderHandler`
   - Hard-coded suffix rules (Lines 28-35)
   - Could be made configurable

2. **Placeholder pattern definitions** in `constants.py`
   - Currently hard-coded regex patterns
   - Could be made configurable for future extensibility

3. **Derived placeholder detection** in `TemplateProcessor`
   - Hard-coded rules for COST variations (Lines 57-64)

### 5.3 **LOW PRIORITY - Documentation/Reference**

1. **Placeholder documentation** in `placeholders_list.txt`
   - Reference documentation
   - Should be updated after refactoring

## 6. Recommendations

1. **Create a centralized configuration system** to replace hard-coded mappings
2. **Implement dynamic field mapping** based on database schema
3. **Replace tuple index access** with named field access (dictionaries/dataclasses)
4. **Consolidate placeholder processing** into a single, extensible system
5. **Add validation** for placeholder-to-field mappings
6. **Create migration path** for existing templates

## 7. Files Requiring Modification

### Critical Files (Must Modify):
- `features/template_engine/work_data_provider.py`
- `features/AutodocGen/document_generator.py`
- `features/AutodocGen/pg_details_formatter.py`

### Important Files (Should Modify):
- `features/template_engine/special_placeholder_handler.py`
- `features/template_engine/template_processor.py`
- `features/AutodocGen/constants.py`

### Reference Files (Update After Changes):
- `placeholders_list.txt`
- Documentation and help files

---

**Total files with hard-coded mappings identified: 6 critical files**
**Total hard-coded mapping instances: 15+ distinct locations**
