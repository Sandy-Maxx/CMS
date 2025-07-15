import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from utils.helpers import format_currency_inr, number_to_indian_words

def evaluate_special_placeholder(placeholder_name, data):
    # Handle COST variations
    if placeholder_name.startswith("COST"):
        parts = placeholder_name.split("_")
        base_cost_key = parts[0] # e.g., "COST"

        # Get the base cost value
        base_value = data.get(base_cost_key)
        if base_value is None or base_value == "":
            return f"{{{{{placeholder_name}}}}}" # Return original if base not found or empty

        try:
            result = Decimal(str(base_value))
        except Exception:
            return f"{{{{{placeholder_name}}}}}" # Return original if base is not numeric

        format_as_words = False
        round_to_nearest = None

        for part in parts[1:]:
            if part == "IN" and "WORDS" in parts: # Check for IN_WORDS
                format_as_words = True
            elif part.replace('.', '', 1).isdigit(): # Check for numeric multiplier
                result *= Decimal(part)
            elif part.isdigit() and len(part) == 2 and part.endswith("00"): # Check for rounding to nearest 100
                round_to_nearest = Decimal(100)
            elif part.isdigit() and len(part) == 2 and part.endswith("0"): # Check for rounding to nearest 10
                round_to_nearest = Decimal(10)

        if round_to_nearest:
            # Custom rounding to nearest multiple, always rounding up for .5
            # This handles cases like 125.68 rounding to 130 for nearest 10
            # and 125.68 rounding to 200 for nearest 100
            if result > 0 and result < round_to_nearest and result % round_to_nearest != 0:
                result = round_to_nearest
            else:
                result = (result / round_to_nearest).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * round_to_nearest

        if format_as_words:
            return number_to_indian_words(result)
        else:
            return format_currency_inr(result)

    # Default: return value from data if exists, otherwise original placeholder
    return data.get(placeholder_name, f"{{{{{placeholder_name}}}}}")
