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

                # Write SN, Description, Quantity Before, Quantity After, Increased Qty, Unit
                worksheet.write(excel_row, 0, item_data['sr_no'], cell_format)  # SN
                worksheet.write(excel_row, 1, item_data['item_name'], cell_format)  # Description
                worksheet.write(excel_row, 2, item_data['quantity'], numeric_format)  # Quantity Before Variation
                worksheet.write(excel_row, 3, qty_after_variation, numeric_format)  # Quantity After Variation
                # Increased Qty formula: After - Before
                formula_increased_qty = f"={get_col_letter(3)}{excel_row + 1}-{get_col_letter(2)}{excel_row + 1}"
                worksheet.write_formula(excel_row, 4, formula_increased_qty, numeric_format)  # Increased Qty
                worksheet.write(excel_row, 5, item_data['unit'], cell_format)  # Unit

                col_offset = 6 # Start column for firm-specific data (updated from 5 to 6)
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
                    
                    # Increased Cost = Total Cost After - Total Cost Before
                    formula_increased_cost = f"={get_col_letter(col_offset + 2)}{excel_row + 1}-{get_col_letter(col_offset + 1)}{excel_row + 1}"
                    worksheet.write_formula(excel_row, col_offset + 3, formula_increased_cost, currency_format_inr)
                    
                    col_offset += 4  # Updated from 3 to 4

            # Calculate and write summary rows
            summary_row_start = 3 + len(schedule_items)
            summary_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            summary_numeric_format = workbook.add_format({'bold': True, 'border': 1, 'num_format': '#,##0.00', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

            firm_col_start_idx = 6 # Updated starting column
            start_data_excel_row = 4 # Excel first data row
            end_data_excel_row = 3 + len(schedule_items) # Excel last data row

            # Unified Subtotal Row
            subtotal_row = summary_row_start
            worksheet.merge_range(subtotal_row, 0, subtotal_row, 5, "Subtotal:", summary_format)
            for i, firm_name in enumerate(selected_firms):
                base_col = firm_col_start_idx + (i * 4)
                # Subtotal Before
                formula_subtotal_before = f"=SUM({get_col_letter(base_col + 1)}{start_data_excel_row}:{get_col_letter(base_col + 1)}{end_data_excel_row})"
                worksheet.write_formula(subtotal_row, base_col + 1, formula_subtotal_before, currency_format_inr)
                
                # Subtotal After
                formula_subtotal_after = f"=SUM({get_col_letter(base_col + 2)}{start_data_excel_row}:{get_col_letter(base_col + 2)}{end_data_excel_row})"
                worksheet.write_formula(subtotal_row, base_col + 2, formula_subtotal_after, currency_format_inr)
                
                # Subtotal Increased
                formula_subtotal_increased = f"=SUM({get_col_letter(base_col + 3)}{start_data_excel_row}:{get_col_letter(base_col + 3)}{end_data_excel_row})"
                worksheet.write_formula(subtotal_row, base_col + 3, formula_subtotal_increased, currency_format_inr)

            # Unified GST Row
            gst_row = subtotal_row + 1
            worksheet.merge_range(gst_row, 0, gst_row, 5, "GST @ 18%:", summary_format)
            for i, firm_name in enumerate(selected_firms):
                base_col = firm_col_start_idx + (i * 4)
                # GST Before
                formula_gst_before = f"={get_col_letter(base_col + 1)}{subtotal_row + 1}*0.18"
                worksheet.write_formula(gst_row, base_col + 1, formula_gst_before, currency_format_inr)

                # GST After
                formula_gst_after = f"={get_col_letter(base_col + 2)}{subtotal_row + 1}*0.18"
                worksheet.write_formula(gst_row, base_col + 2, formula_gst_after, currency_format_inr)

                # GST Increased
                formula_gst_increased = f"={get_col_letter(base_col + 3)}{subtotal_row + 1}*0.18"
                worksheet.write_formula(gst_row, base_col + 3, formula_gst_increased, currency_format_inr)

            # Unified Total Cost Row
            total_cost_row = gst_row + 1
            worksheet.merge_range(total_cost_row, 0, total_cost_row, 5, "Total Cost (with GST):", summary_format)
            for i, firm_name in enumerate(selected_firms):
                base_col = firm_col_start_idx + (i * 4)
                # Total Before
                formula_total_before_gst = f"={get_col_letter(base_col + 1)}{subtotal_row + 1}+{get_col_letter(base_col + 1)}{gst_row + 1}"
                worksheet.write_formula(total_cost_row, base_col + 1, formula_total_before_gst, currency_format_inr)

                # Total After
                formula_total_after_gst = f"={get_col_letter(base_col + 2)}{subtotal_row + 1}+{get_col_letter(base_col + 2)}{gst_row + 1}"
                worksheet.write_formula(total_cost_row, base_col + 2, formula_total_after_gst, currency_format_inr)

                # Total Increased
                formula_total_increased_gst = f"={get_col_letter(base_col + 3)}{subtotal_row + 1}+{get_col_letter(base_col + 3)}{gst_row + 1}"
                worksheet.write_formula(total_cost_row, base_col + 3, formula_total_increased_gst, currency_format_inr)

            # Unified Inter Se Position Row
            inter_se_row = total_cost_row + 1
            worksheet.merge_range(inter_se_row, 0, inter_se_row, 5, "Inter Se Position:", summary_format)

            # Calculate ranks using Excel's RANK.EQ function
            for i, firm_name in enumerate(selected_firms):
                base_col = firm_col_start_idx + (i * 4)
                
                # Build the range string for RANK.EQ formula for 'Before Variation'
                rank_range_str_before = ",".join([f"${get_col_letter(firm_col_start_idx + (j * 4) + 1)}${total_cost_row + 1}" for j in range(len(selected_firms))])
                formula_rank_before = f"=\"L-\"&RANK.EQ({get_col_letter(base_col + 1)}{total_cost_row + 1},({rank_range_str_before}),1)"
                worksheet.write_formula(inter_se_row, base_col + 1, formula_rank_before, summary_format)

                # Build the range string for RANK.EQ formula for 'After Variation'
                rank_range_str_after = ",".join([f"${get_col_letter(firm_col_start_idx + (j * 4) + 2)}${total_cost_row + 1}" for j in range(len(selected_firms))])
                formula_rank_after = f"=\"L-\"&RANK.EQ({get_col_letter(base_col + 2)}{total_cost_row + 1},({rank_range_str_after}),1)"
                worksheet.write_formula(inter_se_row, base_col + 2, formula_rank_after, summary_format)

        return True, "Report generated successfully"
    except Exception as e:
        print(f"Error in export_vitiation_data_to_excel: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error generating report: {str(e)}"