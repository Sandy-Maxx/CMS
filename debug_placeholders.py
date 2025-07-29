#!/usr/bin/env python3

"""
Debug script to test placeholder generation for the help section
"""

from features.template_engine.work_data_provider import WorkDataProvider
from datetime import datetime

try:
    print("Testing WorkDataProvider.get_available_placeholders_static()...")
    placeholders = WorkDataProvider.get_available_placeholders_static()
    
    print(f"✓ Successfully retrieved {len(placeholders)} placeholders")
    
    # Create formatted placeholder text dynamically
    work_placeholders = []
    firm_placeholders = []
    special_placeholders = []
    
    for key, desc in placeholders.items():
        if key.startswith('[') and key.endswith(']'):
            if key in ('[CURRENT_DATE]', '[CURRENT_TIME]', '[FIRM_PG_DETAILS]', '[ALL_FIRMS_PG_DETAILS]'):
                special_placeholders.append(f"*   **{key}**: {desc}")
            else:
                work_placeholders.append(f"*   **{key}**: {desc}")
        elif key.startswith('<<') and key.endswith('>>'):
            firm_placeholders.append(f"*   **{key}**: {desc}")
    
    work_placeholders_text = "\n".join(work_placeholders)
    firm_placeholders_text = "\n".join(firm_placeholders) 
    special_placeholders_text = "\n".join(special_placeholders)
    
    # Generate dynamic placeholder list answer
    dynamic_placeholder_answer = f"""Here is the comprehensive list of all available placeholders for the AutoDocGen template system (auto-generated from current database schema):

**WORK DETAILS (use [PLACEHOLDER] format):**
{work_placeholders_text}

**FIRM DETAILS (use <<PLACEHOLDER>> format):**
{firm_placeholders_text}

**SPECIAL PLACEHOLDERS:**
{special_placeholders_text}

**TEMPLATE ENGINE PLACEHOLDERS (use {{{{PLACEHOLDER}}}} format):**
*   **{{{{any_placeholder_name}}}}** - For manual input fields
*   **{{{{COST}}}}** - Base cost value with mathematical operations
*   **{{{{COST_1.1}}}}** - Cost multiplied by 1.1
*   **{{{{COST_IN_WORDS}}}}** - Cost converted to words
*   **{{{{COST_00}}}}** - Cost rounded to nearest 100
*   **{{{{DATE_field}}}}** - Any date field with date picker

**💡 This list is automatically updated when new database fields are added!

(Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"""
    
    print("\n" + "="*80)
    print("GENERATED PLACEHOLDER CONTENT:")
    print("="*80)
    print(dynamic_placeholder_answer)
    
    print(f"\n✓ Generated content length: {len(dynamic_placeholder_answer)} characters")
    print(f"✓ Work placeholders: {len(work_placeholders)}")
    print(f"✓ Firm placeholders: {len(firm_placeholders)}")
    print(f"✓ Special placeholders: {len(special_placeholders)}")
    
    # Test if content is blank/empty
    if not dynamic_placeholder_answer.strip():
        print("❌ ERROR: Generated content is blank!")
    else:
        print("✓ Content is not blank")

except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
