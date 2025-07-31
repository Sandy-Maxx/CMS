import pandas as pd
from database import db_manager
from features.price_variation.price_variation_excel_structure import write_price_variation_excel_report
from features.price_variation.price_variation_data_manager import calculate_price_variation_costs

def export_price_variation_data_to_excel(work_details, schedule_items, output_path, selected_firms, variation_type):
    try:
        processed_schedule_items = []
        total_cost_before_all_items = 0
        total_cost_after_all_items = 0

        for sr_no, item in enumerate(schedule_items, 1):
            item['sr_no'] = sr_no  # Add serial number to the item
            original_quantity = item['quantity']
            # Fetch new_quantity from schedule_item_variations
            variations = db_manager.get_schedule_item_variations(item['item_id'])
            new_quantity = variations.get(variation_type, original_quantity)
            item['new_quantity'] = new_quantity # Add new_quantity to the item dictionary

            # Fetch unit_rate for the selected firm
            firm_rates = db_manager.get_firm_rates(item['item_id'])
            unit_rate = 0
            if selected_firms and firm_rates:
                for rate in firm_rates:
                    if rate['firm_name'] == selected_firms[0]: # Assuming only one firm is selected
                        unit_rate = rate['unit_rate']
                        break
            if unit_rate == 0:
                # Fallback if no specific firm rate is found or selected_firms is empty
                # This might need more robust error handling or a default behavior
                unit_rate = item.get('unit_rate', 0) # Use existing unit_rate if available, else 0
            item['unit_rate'] = unit_rate # Add unit_rate to the item dictionary

            # Calculate costs based on price variation logic
            calculated_costs = calculate_price_variation_costs(original_quantity, new_quantity, unit_rate)
            
            item['total_cost_before'] = original_quantity * unit_rate
            item['total_cost_after'] = calculated_costs['total_cost_after']
            item['quantity_upto_125'] = calculated_costs['quantity_upto_125']
            item['quantity_upto_140'] = calculated_costs['quantity_upto_140']
            item['quantity_upto_150'] = calculated_costs['quantity_upto_150']
            item['cost_upto_125'] = calculated_costs['cost_upto_125']
            item['cost_upto_140'] = calculated_costs['cost_upto_140']
            item['cost_upto_150'] = calculated_costs['cost_upto_150']
            
            processed_schedule_items.append(item)
            total_cost_before_all_items += item['total_cost_before']
            total_cost_after_all_items += item['total_cost_after']

        percentage_change = 0.0
        if total_cost_before_all_items != 0:
            percentage_change = ((total_cost_after_all_items - total_cost_before_all_items) / total_cost_before_all_items) * 100

        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Price Variation Report')

            write_price_variation_excel_report(
                worksheet,
                workbook,
                work_details,
                processed_schedule_items,
                selected_firms,
                total_cost_before_all_items,
                total_cost_after_all_items,
                percentage_change
            )

        return True, "Price Variation Report generated successfully"
    except Exception as e:
        print(f"Error in export_price_variation_data_to_excel: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error generating report: {str(e)}"
