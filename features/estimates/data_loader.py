# features/estimates/data_loader.py

import os
from datetime import datetime
from database import db_manager

def load_data(work_id, firm_name):
    """
    Loads data for the estimate report from the database based on work_id and firm_name.
    All fields are optional and can be missing or None.
    """
    all_data = []

    # Fetch work details for the 'A' row
    work_details = db_manager.get_work_by_id(work_id)
    if work_details:
        all_data.append({
            "sr_no": "A",
            "description": work_details.get('description', ''),
            "qty": None,
            "rate": None,
            "unit": None,
            "to_be_maintained": None,
            "labour_rate": None,
            "labour_amount": None,
            "total_in_rs": None,
            "remarks": work_details.get('description', ''),
        })

    # Fetch schedule items and firm rates
    schedule_items = db_manager.get_schedule_items(work_id)
    for i, item in enumerate(schedule_items):
        firm_rate = db_manager.get_firm_rate_for_item(item['item_id'], firm_name)
        
        # Ensure numeric values are floats for calculations
        qty = float(item.get('quantity')) if item.get('quantity') is not None else None
        rate = float(firm_rate.get('rate')) if firm_rate and firm_rate.get('rate') is not None else None
        labour_rate = float(firm_rate.get('labour_rate')) if firm_rate and firm_rate.get('labour_rate') is not None else None

        all_data.append({
            "sr_no": i + 1,
            "description": item.get('item_name'),
            "qty": qty,
            "rate": rate,
            "unit": item.get('unit'),
            "to_be_maintained": None, # Calculated field
            "labour_rate": labour_rate,
            "labour_amount": None, # Will be calculated by Excel formula
            "total_in_rs": None,    # Will be calculated by Excel formula
            "remarks": item.get('remarks'),
        })
    return all_data
