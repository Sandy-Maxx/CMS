import pandas as pd
from database import db_manager
from features.variation.variation_excel_structure import get_variation_table_columns, write_variation_excel_report
from xlsxwriter.utility import xl_col_to_name

def export_variation_data_to_excel(work_details, schedule_items, output_path, selected_firms):
    try:
        total_cost_before_all_items = sum(item['total_cost_before'] for item in schedule_items)
        total_cost_after_all_items = sum(item['total_cost_after'] for item in schedule_items)

        percentage_change = 0.0
        if total_cost_before_all_items != 0:
            percentage_change = ((total_cost_after_all_items - total_cost_before_all_items) / total_cost_before_all_items) * 100

        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Variation Report')

            # Write multi-level headers and data
            write_variation_excel_report(
                worksheet,
                workbook,
                work_details,
                schedule_items,
                selected_firms,
                total_cost_before_all_items,
                total_cost_after_all_items,
                percentage_change
            )

        return True, "Report generated successfully"
    except Exception as e:
        print(f"Error in export_variation_data_to_excel: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error generating report: {str(e)}"
