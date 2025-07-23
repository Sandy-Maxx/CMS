# features/estimates/constants.py

COLUMN_HEADERS = [
    "Sr. No.",
    "Description",
    "Qty",
    "Rate in Rs",
    "Unit",
    "To be Maintained",
    "Labour rate in Rs.",
    "Labour Amount",
    "Total in Rs",
    "Remarks",
]

# Mapping of column headers to their corresponding keys in the data dictionaries
COLUMN_MAPPING = {
    "Sr. No.": "sr_no",
    "Description": "description",
    "Qty": "qty",
    "Rate in Rs": "rate",
    "Unit": "unit",
    "To be Maintained": "to_be_maintained",
    "Labour rate in Rs.": "labour_rate",
    "Labour Amount": "labour_amount",
    "Total in Rs": "total_in_rs",
    "Remarks": "remarks",
}

GST_RATE = 0.18

# Custom number format for displaying 0 or empty as '--'
# Format: Positive;Negative;Zero;Text
INDIAN_CURRENCY_FORMAT = '₹#,##,##0.00;[Red]-₹#,##,##0.00;"--";"--"'
NUMBER_FORMAT = '#,##0.00;[Red]-#,##0.00;"--";"--"'

# Column styles (e.g., for number formatting)
COLUMN_STYLES = {
    "Qty": {'format': NUMBER_FORMAT},
    "Rate in Rs": {'format': INDIAN_CURRENCY_FORMAT},
    "To be Maintained": {'format': NUMBER_FORMAT},
    "Labour rate in Rs.": {'format': INDIAN_CURRENCY_FORMAT},
    "Labour Amount": {'format': INDIAN_CURRENCY_FORMAT},
    "Total in Rs": {'format': INDIAN_CURRENCY_FORMAT},
}
