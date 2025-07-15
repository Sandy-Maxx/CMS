import pandas as pd
from database import db_manager
from features.vitiation.vitiation_excel_structure import get_vitiation_table_columns

def export_vitiation_data_to_excel(work_details, schedule_items, output_path, selected_firms):
    try:
        # Get the MultiIndex columns for the report
        columns = get_vitiation_table_columns(selected_firms)

        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Vitiation Report')

            # Write multi-level headers
            from features.vitiation.vitiation_excel_structure import write_vitiation_excel_headers
            from xlsxwriter.utility import xl_col_to_name
            write_vitiation_excel_headers(worksheet, workbook, columns, selected_firms)

            # Write data rows manually
            for row_idx, item_data in enumerate(schedule_items):
                excel_row = 3 + row_idx # Data starts at Excel row 4 (0-indexed row 3)
                cell_format = workbook.add_format({'border': 1})
                numeric_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})

                # Write SN, Description, Quantity Before, Quantity After, Unit
                worksheet.write(excel_row, 0, item_data['sr_no'], cell_format)
                worksheet.write(excel_row, 1, item_data['item_name'], cell_format)
                worksheet.write(excel_row, 2, item_data['quantity'], numeric_format)
                worksheet.write(excel_row, 3, item_data['new_quantity'], numeric_format)
                worksheet.write(excel_row, 4, item_data['unit'], cell_format)

                col_offset = 5 # Start column for firm-specific data
                for firm_name in selected_firms:
                    # Find the firm rate for this item and firm
                    unit_rate = 0.0
                    for rate_entry in item_data['firm_rates']:
                        if rate_entry['firm_name'] == firm_name:
                            unit_rate = rate_entry['unit_rate']
                            break

                    total_cost_before = item_data['quantity'] * unit_rate
                    total_cost_after = item_data['new_quantity'] * unit_rate

                    worksheet.write(excel_row, col_offset, unit_rate, numeric_format)
                    worksheet.write(excel_row, col_offset + 1, total_cost_before, numeric_format)
                    worksheet.write(excel_row, col_offset + 2, total_cost_after, numeric_format)
                    col_offset += 3

            # Calculate and write summary rows
            summary_row_start = 3 + len(schedule_items)
            summary_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            summary_numeric_format = workbook.add_format({'bold': True, 'border': 1, 'num_format': '#,##0.00', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

            # Helper to get column letter for formulas
            def get_col_letter(col_idx):
                return xl_col_to_name(col_idx)

            # Subtotal Before/After Variation
            worksheet.merge_range(summary_row_start, 0, summary_row_start, 4, "Subtotal Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 1, 0, summary_row_start + 1, 4, "Subtotal After Variation", summary_format)

            firm_col_start_idx = 5 # Column index where firm data starts
            for i, firm_name in enumerate(selected_firms):
                # Subtotal Before Variation
                subtotal_before_col = firm_col_start_idx + 1 + (i * 3) # Total Cost (Before) column for this firm
                formula_subtotal_before = f"=SUM({get_col_letter(subtotal_before_col)}{4}:{get_col_letter(subtotal_before_col)}{3 + len(schedule_items)})"
                worksheet.write_formula(summary_row_start, subtotal_before_col, formula_subtotal_before, summary_numeric_format)

                # Subtotal After Variation
                subtotal_after_col = firm_col_start_idx + 2 + (i * 3) # Total Cost (After) column for this firm
                formula_subtotal_after = f"=SUM({get_col_letter(subtotal_after_col)}{4}:{get_col_letter(subtotal_after_col)}{3 + len(schedule_items)})"
                worksheet.write_formula(summary_row_start + 1, subtotal_after_col, formula_subtotal_after, summary_numeric_format)

            # GST @ 18% Before/After Variation
            worksheet.merge_range(summary_row_start + 2, 0, summary_row_start + 2, 4, "GST @ 18% Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 3, 0, summary_row_start + 3, 4, "GST @ 18% After Variation", summary_format)

            for i, firm_name in enumerate(selected_firms):
                gst_before_col = firm_col_start_idx + 1 + (i * 3)
                formula_gst_before = f"={get_col_letter(gst_before_col)}{summary_row_start + 1}*0.18"
                worksheet.write_formula(summary_row_start + 2, gst_before_col, formula_gst_before, summary_numeric_format)

                gst_after_col = firm_col_start_idx + 2 + (i * 3)
                formula_gst_after = f"={get_col_letter(gst_after_col)}{summary_row_start + 2}*0.18"
                worksheet.write_formula(summary_row_start + 3, gst_after_col, formula_gst_after, summary_numeric_format)

            # Total Cost Before/After Variation
            worksheet.merge_range(summary_row_start + 4, 0, summary_row_start + 4, 4, "Total Cost Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 5, 0, summary_row_start + 5, 4, "Total Cost After Variation", summary_format)

            for i, firm_name in enumerate(selected_firms):
                total_cost_before_col = firm_col_start_idx + 1 + (i * 3)
                formula_total_cost_before = f"={get_col_letter(total_cost_before_col)}{summary_row_start + 1}+{get_col_letter(total_cost_before_col)}{summary_row_start + 3}"
                worksheet.write_formula(summary_row_start + 4, total_cost_before_col, formula_total_cost_before, summary_numeric_format)

                total_cost_after_col = firm_col_start_idx + 2 + (i * 3)
                formula_total_cost_after = f"={get_col_letter(total_cost_after_col)}{summary_row_start + 2}+{get_col_letter(total_cost_after_col)}{summary_row_start + 4}"
                worksheet.write_formula(summary_row_start + 5, total_cost_after_col, formula_total_cost_after, summary_numeric_format)

            # Inter Per Se Position Before/After Variation
            worksheet.merge_range(summary_row_start + 6, 0, summary_row_start + 6, 4, "Inter Per Se Position Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 7, 0, summary_row_start + 7, 4, "Inter Per Se Position After Variation", summary_format)

            # Calculate ranks for Inter Per Se Position
            # For Before Variation, rank based on Total Cost Before Variation
            total_costs_before = []
            for i, firm_name in enumerate(selected_firms):
                col = firm_col_start_idx + 1 + (i * 3)
                total_costs_before.append((worksheet.read_formula(summary_row_start + 4, col), firm_name)) # Read formula result
            total_costs_before.sort(key=lambda x: x[0]) # Sort by total cost
            ranks_before = {firm: rank + 1 for rank, (cost, firm) in enumerate(total_costs_before)}

            # For After Variation, rank based on Total Cost After Variation
            total_costs_after = []
            for i, firm_name in enumerate(selected_firms):
                col = firm_col_start_idx + 2 + (i * 3)
                total_costs_after.append((worksheet.read_formula(summary_row_start + 5, col), firm_name)) # Read formula result
            total_costs_after.sort(key=lambda x: x[0]) # Sort by total cost
            ranks_after = {firm: rank + 1 for rank, (cost, firm) in enumerate(total_costs_after)}

            for i, firm_name in enumerate(selected_firms):
                col_before = firm_col_start_idx + 1 + (i * 3)
                col_after = firm_col_start_idx + 2 + (i * 3)
                worksheet.write(summary_row_start + 6, col_before, f"L{ranks_before.get(firm_name, '')}", summary_format)
                worksheet.write(summary_row_start + 7, col_after, f"L{ranks_after.get(firm_name, '')}", summary_format)

        return True, "Report generated successfully"
    except Exception as e:
        print(f"Error in export_vitiation_data_to_excel: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error generating report: {str(e)}"
        # Get the MultiIndex columns for the report
        columns = get_vitiation_table_columns(selected_firms)

        # Get column names to map to indices for formula generation
        # This is a flat list of the lowest level headers
        flat_columns = [col[2] if col[2] else col[1] if col[1] else col[0] for col in columns]

        # Map column names to their indices
        col_name_to_idx = {name: idx for idx, name in enumerate(flat_columns)}

        # Get the base column indices for quantities
        original_qty_col_idx = col_name_to_idx['Before Variation'] # This is the Qty Before Variation column
        new_qty_col_idx = col_name_to_idx['After Variation'] # This is the Qty After Variation column

        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Vitiation Report')

            # Write multi-level headers
            from features.vitiation.vitiation_excel_structure import write_vitiation_excel_headers
            from xlsxwriter.utility import xl_col_to_name
            write_vitiation_excel_headers(worksheet, workbook, columns, selected_firms)

            # Write data rows manually
            for row_idx, item_data in enumerate(schedule_items):
                excel_row = 3 + row_idx # Data starts at Excel row 4 (0-indexed row 3)
                cell_format = workbook.add_format({'border': 1})
                numeric_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})

                # Write SN, Description, Quantity Before, Quantity After, Unit
                worksheet.write(excel_row, 0, item_data['sr_no'], cell_format)
                worksheet.write(excel_row, 1, item_data['item_name'], cell_format)
                worksheet.write(excel_row, 2, item_data['quantity'], numeric_format)
                worksheet.write(excel_row, 3, item_data['new_quantity'], numeric_format)
                worksheet.write(excel_row, 4, item_data['unit'], cell_format)

                col_offset = 5 # Start column for firm-specific data
                for firm_name in selected_firms:
                    # Find the firm rate for this item and firm
                    unit_rate = 0.0
                    for rate_entry in item_data['firm_rates']:
                        if rate_entry['firm_name'] == firm_name:
                            unit_rate = rate_entry['unit_rate']
                            break

                    total_cost_before = item_data['quantity'] * unit_rate
                    total_cost_after = item_data['new_quantity'] * unit_rate

                    worksheet.write(excel_row, col_offset, unit_rate, numeric_format)
                    worksheet.write(excel_row, col_offset + 1, total_cost_before, numeric_format)
                    worksheet.write(excel_row, col_offset + 2, total_cost_after, numeric_format)
                    col_offset += 3

            # Calculate and write summary rows
            summary_row_start = 3 + len(schedule_items)
            summary_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            summary_numeric_format = workbook.add_format({'bold': True, 'border': 1, 'num_format': '#,##0.00', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

            # Helper to get column letter for formulas
            def get_col_letter(col_idx):
                return xl_col_to_name(col_idx)

            # Subtotal Before/After Variation
            worksheet.merge_range(summary_row_start, 0, summary_row_start, 4, "Subtotal Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 1, 0, summary_row_start + 1, 4, "Subtotal After Variation", summary_format)

            firm_col_start_idx = 5 # Column index where firm data starts
            for i, firm_name in enumerate(selected_firms):
                # Subtotal Before Variation
                subtotal_before_col = firm_col_start_idx + 1 + (i * 3) # Total Cost (Before) column for this firm
                formula_subtotal_before = f"=SUM({get_col_letter(subtotal_before_col)}{4}:{get_col_letter(subtotal_before_col)}{3 + len(schedule_items)})"
                worksheet.write_formula(summary_row_start, subtotal_before_col, formula_subtotal_before, summary_numeric_format)

                # Subtotal After Variation
                subtotal_after_col = firm_col_start_idx + 2 + (i * 3) # Total Cost (After) column for this firm
                formula_subtotal_after = f"=SUM({get_col_letter(subtotal_after_col)}{4}:{get_col_letter(subtotal_after_col)}{3 + len(schedule_items)})"
                worksheet.write_formula(summary_row_start + 1, subtotal_after_col, formula_subtotal_after, summary_numeric_format)

            # GST @ 18% Before/After Variation
            worksheet.merge_range(summary_row_start + 2, 0, summary_row_start + 2, 4, "GST @ 18% Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 3, 0, summary_row_start + 3, 4, "GST @ 18% After Variation", summary_format)

            for i, firm_name in enumerate(selected_firms):
                gst_before_col = firm_col_start_idx + 1 + (i * 3)
                formula_gst_before = f"={get_col_letter(gst_before_col)}{summary_row_start + 1}*0.18"
                worksheet.write_formula(summary_row_start + 2, gst_before_col, formula_gst_before, summary_numeric_format)

                gst_after_col = firm_col_start_idx + 2 + (i * 3)
                formula_gst_after = f"={get_col_letter(gst_after_col)}{summary_row_start + 2}*0.18"
                worksheet.write_formula(summary_row_start + 3, gst_after_col, formula_gst_after, summary_numeric_format)

            # Total Cost Before/After Variation
            worksheet.merge_range(summary_row_start + 4, 0, summary_row_start + 4, 4, "Total Cost Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 5, 0, summary_row_start + 5, 4, "Total Cost After Variation", summary_format)

            for i, firm_name in enumerate(selected_firms):
                total_cost_before_col = firm_col_start_idx + 1 + (i * 3)
                formula_total_cost_before = f"={get_col_letter(total_cost_before_col)}{summary_row_start + 1}+{get_col_letter(total_cost_before_col)}{summary_row_start + 3}"
                worksheet.write_formula(summary_row_start + 4, total_cost_before_col, formula_total_cost_before, summary_numeric_format)

                total_cost_after_col = firm_col_start_idx + 2 + (i * 3)
                formula_total_cost_after = f"={get_col_letter(total_cost_after_col)}{summary_row_start + 2}+{get_col_letter(total_cost_after_col)}{summary_row_start + 4}"
                worksheet.write_formula(summary_row_start + 5, total_cost_after_col, formula_total_cost_after, summary_numeric_format)

            # Inter Per Se Position Before/After Variation
            worksheet.merge_range(summary_row_start + 6, 0, summary_row_start + 6, 4, "Inter Per Se Position Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 7, 0, summary_row_start + 7, 4, "Inter Per Se Position After Variation", summary_format)

            # Calculate ranks for Inter Per Se Position
            # For Before Variation, rank based on Total Cost Before Variation
            total_costs_before = []
            for i, firm_name in enumerate(selected_firms):
                col = firm_col_start_idx + 1 + (i * 3)
                total_costs_before.append((worksheet.read_formula(summary_row_start + 4, col), firm_name)) # Read formula result
            total_costs_before.sort(key=lambda x: x[0]) # Sort by total cost
            ranks_before = {firm: rank + 1 for rank, (cost, firm) in enumerate(total_costs_before)}

            # For After Variation, rank based on Total Cost After Variation
            total_costs_after = []
            for i, firm_name in enumerate(selected_firms):
                col = firm_col_start_idx + 2 + (i * 3)
                total_costs_after.append((worksheet.read_formula(summary_row_start + 5, col), firm_name)) # Read formula result
            total_costs_after.sort(key=lambda x: x[0]) # Sort by total cost
            ranks_after = {firm: rank + 1 for rank, (cost, firm) in enumerate(total_costs_after)}

            for i, firm_name in enumerate(selected_firms):
                col_before = firm_col_start_idx + 1 + (i * 3)
                col_after = firm_col_start_idx + 2 + (i * 3)
                worksheet.write(summary_row_start + 6, col_before, f"L{ranks_before.get(firm_name, '')}", summary_format)
                worksheet.write(summary_row_start + 7, col_after, f"L{ranks_after.get(firm_name, '')}", summary_format)

        

        return True, "Report generated successfully"
    except Exception as e:
        print(f"Error in export_vitiation_data_to_excel: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error generating report: {str(e)}"
