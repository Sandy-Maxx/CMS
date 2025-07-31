import os

# Base directory for templates
BASE_TEMPLATE_DIR = os.path.join("Templates")

# Specific template subdirectories
LETTERS_TEMPLATE_DIR = os.path.join(BASE_TEMPLATE_DIR, "Letters")
OFFICE_NOTES_TEMPLATE_DIR = os.path.join(BASE_TEMPLATE_DIR, "OfficeNotes")

# Placeholder patterns
# User input placeholders (e.g., {{placeholder_name}})
USER_PLACEHOLDER_PATTERN = r"\{\{([a-zA-Z0-9_.]+)\}\}"

# Work data placeholders (e.g., [WORK_NAME])
WORK_DATA_PLACEHOLDER_PATTERN = r"\[([a-zA-Z0-9_]+)\]"

# Firm-specific placeholders (e.g., <<FIRM_ADDRESS>>)
FIRM_PLACEHOLDER_PATTERN = r"<<([a-zA-Z0-9_]+)>>"
ALL_FIRMS_PG_DETAILS_PATTERN = r"\[ALL_FIRMS_PG_DETAILS\]"

# Combined regex for all placeholder types
ALL_PLACEHOLDER_PATTERN = r"(\{\{([a-zA-Z0-9_.]+)\}\}\]|\[([a-zA-Z0-9_]+)\]|<<([a-zA-Z0-9_]+)>>|(\[ALL_FIRMS_PG_DETAILS\]))"
