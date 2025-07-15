import pandas as pd
from datetime import datetime

def export_variation_report(work_details, schedule_items, firm_rates_by_item, updated_quantities, output_path):
    try:
        data = []
        for item in schedule_items:
            item_id = item['item_id']
            original_qty = item['quantity']
            new_qty = float(updated_quantities.get(str(item_id), original_qty))
            firm_rates = firm_rates_by_item.get(item_id, [])
            for rate in firm_rates:
                firm_name = rate['firm_name']
                unit_rate = rate['unit_rate']
                original_cost = original_qty * unit_rate
                new_cost = new_qty * unit_rate
                data.append({
                    'Item ID': item_id,
                    'Item Name': item['item_name'],
                    'Unit': item['unit'],
                    'Original Quantity': original_qty,
                    'New Quantity': new_qty,
                    'Firm Name': firm_name,
                    'Unit Rate': unit_rate,
                    'Original Cost': original_cost,
                    'New Cost': new_cost,
                    'Variation': new_cost - original_cost
                })
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Vitiation Report', index=False)
            worksheet = writer.sheets['Vitiation Report']
            for col in worksheet.columns:
                max_length = max(len(str(cell.value)) for cell in col)
                worksheet.column_dimensions[col[0].column_letter].width = max_length + 2
        return True, "Report generated successfully"
    except Exception as e:
        return False, f"Error generating report: {str(e)}"

def export_work_to_excel(work_details, schedule_items, firm_rates_by_item, output_path):
    try:
        data = []
        for item in schedule_items:
            item_id = item['item_id']
            quantity = item['quantity']
            firm_rates = firm_rates_by_item.get(item_id, [])
            for rate in firm_rates:
                firm_name = rate['firm_name']
                unit_rate = rate['unit_rate']
                total_cost = quantity * unit_rate
                data.append({
                    'Work Name': work_details['work_name'],
                    'Item ID': item_id,
                    'Item Name': item['item_name'],
                    'Unit': item['unit'],
                    'Quantity': quantity,
                    'Firm Name': firm_name,
                    'Unit Rate': unit_rate,
                    'Total Cost': total_cost
                })
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Work Details', index=False)
            worksheet = writer.sheets['Work Details']
            for col in worksheet.columns:
                max_length = max(len(str(cell.value)) for cell in col)
                worksheet.column_dimensions[col[0].column_letter].width = max_length + 2
        return True, "Work details exported successfully"
    except Exception as e:
        return False, f"Error exporting work details: {str(e)}"