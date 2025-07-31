import pandas as pd
from database import db_manager
from features.vitiation import vitiation_excel_structure
from xlsxwriter.utility import xl_col_to_name

def get_col_letter(col_idx):
    return xl_col_to_name(col_idx)

def export_vitiation_data_to_excel(work_details, schedule_items, output_path, selected_firms, selected_variation_name):
    try:
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet('Vitiation Report')

            # Define formats
            currency_format_inr = workbook.add_format({'num_format': '₹ #,##,##0.00', 'border': 1})
            cell_format = workbook.add_format({'border': 1})
            numeric_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})

            # Write multi-level headers
            vitiation_excel_structure.write_vitiation_excel_headers(worksheet, workbook, selected_firms)

            # Write data rows manually
            for row_idx, item_data in enumerate(schedule_items):
                excel_row = 3 + row_idx # Data starts at Excel row 4 (0-indexed row 3)
                
                # Get quantity after variation from the selected variation column
                qty_after_variation = item_data['variations'].get(selected_variation_name, 0)

                # Write SN, Description, Quantity Before, Quantity After, Unit
                worksheet.write(excel_row, 0, item_data['sr_no'], cell_format)
                worksheet.write(excel_row, 1, item_data['item_name'], cell_format)
                worksheet.write(excel_row, 2, item_data['quantity'], numeric_format) # Quantity Before Variation
                worksheet.write(excel_row, 3, qty_after_variation, numeric_format) # Quantity After Variation
                worksheet.write(excel_row, 4, item_data['unit'], cell_format)

                col_offset = 5 # Start column for firm-specific data
                for firm_name in selected_firms:
                    # Find the firm rate for this item and firm
                    unit_rate = 0.0
                    for rate_entry in item_data['firm_rates']:
                        if rate_entry['firm_name'] == firm_name:
                            unit_rate = rate_entry['unit_rate']
                            break

                    # Write Unit Rate
                    worksheet.write(excel_row, col_offset, unit_rate, currency_format_inr)

                    # Total Cost Before Variation (formula: original_qty * unit_rate)
                    # original_qty is in column 2 (C), unit_rate is in current col_offset
                    formula_total_cost_before_item = f"={get_col_letter(2)}{excel_row + 1}*{get_col_letter(col_offset)}{excel_row + 1}"
                    worksheet.write_formula(excel_row, col_offset + 1, formula_total_cost_before_item, currency_format_inr)

                    # Total Cost After Variation (formula: qty_after_variation * unit_rate)
                    # qty_after_variation is in column 3 (D), unit_rate is in current col_offset
                    formula_total_cost_after_item = f"={get_col_letter(3)}{excel_row + 1}*{get_col_letter(col_offset)}{excel_row + 1}"
                    worksheet.write_formula(excel_row, col_offset + 2, formula_total_cost_after_item, currency_format_inr)
                    
                    col_offset += 3

            # Calculate and write summary rows
            summary_row_start = 3 + len(schedule_items)
            summary_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            summary_numeric_format = workbook.add_format({'bold': True, 'border': 1, 'num_format': '#,##0.00', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

            # Subtotal Before/After Variation
            worksheet.merge_range(summary_row_start, 0, summary_row_start, 4, "Subtotal Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 1, 0, summary_row_start + 1, 4, "Subtotal After Variation", summary_format)

            firm_col_start_idx = 5 # Column index where firm data starts
            for i, firm_name in enumerate(selected_firms):
                subtotal_before_col = firm_col_start_idx + 1 + (i * 3) # Total Cost (Before) column for this firm
                start_data_excel_row = 4 # Excel row for the first data item
                end_data_excel_row = 3 + len(schedule_items) # Excel row for the last data item

                formula_subtotal_before = f"=SUM({get_col_letter(subtotal_before_col)}{start_data_excel_row}:{get_col_letter(subtotal_before_col)}{end_data_excel_row})"
                worksheet.write_formula(summary_row_start, subtotal_before_col, formula_subtotal_before, currency_format_inr)

                subtotal_after_col = firm_col_start_idx + 2 + (i * 3) # Total Cost (After) column for this firm
                formula_subtotal_after = f"=SUM({get_col_letter(subtotal_after_col)}{start_data_excel_row}:{get_col_letter(subtotal_after_col)}{end_data_excel_row})"
                worksheet.write_formula(summary_row_start + 1, subtotal_after_col, formula_subtotal_after, currency_format_inr)

            # GST @ 18% Before/After Variation
            worksheet.merge_range(summary_row_start + 2, 0, summary_row_start + 2, 4, "GST @ 18% Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 3, 0, summary_row_start + 3, 4, "GST @ 18% After Variation", summary_format)

            for i, firm_name in enumerate(selected_firms):
                gst_before_col = firm_col_start_idx + 1 + (i * 3)
                formula_gst_before = f"={get_col_letter(gst_before_col)}{summary_row_start + 1}*0.18"
                worksheet.write_formula(summary_row_start + 2, gst_before_col, formula_gst_before, currency_format_inr)

                gst_after_col = firm_col_start_idx + 2 + (i * 3)
                formula_gst_after = f"={get_col_letter(gst_after_col)}{summary_row_start + 2}*0.18"
                worksheet.write_formula(summary_row_start + 3, gst_after_col, formula_gst_after, currency_format_inr)

            # Total Cost Before/After Variation
            worksheet.merge_range(summary_row_start + 4, 0, summary_row_start + 4, 4, "Total Cost Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 5, 0, summary_row_start + 5, 4, "Total Cost After Variation", summary_format)

            for i, firm_name in enumerate(selected_firms):
                total_cost_before_col = firm_col_start_idx + 1 + (i * 3)
                formula_total_cost_before = f"={get_col_letter(total_cost_before_col)}{summary_row_start + 1}+{get_col_letter(total_cost_before_col)}{summary_row_start + 3}"
                worksheet.write_formula(summary_row_start + 4, total_cost_before_col, formula_total_cost_before, currency_format_inr)

                total_cost_after_col = firm_col_start_idx + 2 + (i * 3)
                formula_total_cost_after = f"={get_col_letter(total_cost_after_col)}{summary_row_start + 2}+{get_col_letter(total_cost_after_col)}{summary_row_start + 4}"
                worksheet.write_formula(summary_row_start + 5, total_cost_after_col, formula_total_cost_after, currency_format_inr)

            # Inter Per Se Position Before/After Variation
            worksheet.merge_range(summary_row_start + 6, 0, summary_row_start + 6, 4, "Inter Per Se Position Before Variation", summary_format)
            worksheet.merge_range(summary_row_start + 7, 0, summary_row_start + 7, 4, "Inter Per Se Position After Variation", summary_format)

            # Calculate ranks using Excel's RANK.EQ function
            for i, firm_name in enumerate(selected_firms):
                col_before = firm_col_start_idx + 1 + (i * 3)
                col_after = firm_col_start_idx + 2 + (i * 3)

                # Build the range string for RANK.EQ formula for 'Before Variation'
                rank_range_str_before = ",".join([f"${get_col_letter(firm_col_start_idx + 1 + (j * 3))}${summary_row_start + 4 + 1}" for j in range(len(selected_firms))])
                formula_rank_before = f"=\"L-\"&RANK.EQ({get_col_letter(col_before)}{summary_row_start + 4 + 1},({rank_range_str_before}),1)"
                worksheet.write_formula(summary_row_start + 6, col_before, formula_rank_before, summary_format)

                # Build the range string for RANK.EQ formula for 'After Variation'
                rank_range_str_after = ",".join([f"${get_col_letter(firm_col_start_idx + 2 + (j * 3))}${summary_row_start + 5 + 1}" for j in range(len(selected_firms))])
                formula_rank_after = f"=\"L-\"&RANK.EQ({get_col_letter(col_after)}{summary_row_start + 5 + 1},({rank_range_str_after}),1)"
                worksheet.write_formula(summary_row_start + 7, col_after, formula_rank_after, summary_format)

        return True, "Report generated successfully"
    except Exception as e:
        print(f"Error in export_vitiation_data_to_excel: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error generating report: {str(e)}"