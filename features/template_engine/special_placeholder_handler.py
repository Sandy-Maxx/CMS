import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from utils.helpers import format_currency_inr, number_to_indian_words


def evaluate_special_placeholder(placeholder_name, data):

    # Only process placeholders starting with "COST"
    if placeholder_name.startswith("COST"):
        parts = placeholder_name.split("_")
        base_cost_key = parts[0]  # e.g., "COST"

        # Get the base cost value
        base_value = data.get(base_cost_key)
        if base_value is None or base_value == "":
            return f"[{placeholder_name}]"  # Return original if base not found or empty

        try:
            result = Decimal(str(base_value))
        except Exception:
            return f"[{placeholder_name}]"  # Return original if base is not numeric

        format_as_words = False
        round_to_nearest = None

        for part in parts[1:]:
            if part == "IN" and "WORDS" in parts: # Check for IN_WORDS
                format_as_words = True
            elif part.strip() == "00": # Check for rounding to nearest 100
                round_to_nearest = Decimal(100)
            elif part.strip() == "0": # Check for rounding to nearest 10
                round_to_nearest = Decimal(10)
            elif part.replace('.', '', 1).isdigit(): # Check for numeric multiplier
                result *= Decimal(part)

        if round_to_nearest:
            result = (result / round_to_nearest).to_integral_value(rounding=ROUND_HALF_UP) * round_to_nearest

        if format_as_words:
            return number_to_indian_words(float(result))
        else:
            return format_currency_inr(result)

    # If not a COST-based placeholder, return from data or leave unchanged
    result = data.get(placeholder_name, f"[{placeholder_name}]")
    return result
