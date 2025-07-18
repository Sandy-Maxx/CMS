PS D:\CMS\CMS> python main.py
Error in export_variation_data_to_excel: name 'summary_row_start' is not defined
Traceback (most recent call last):
  File "D:\CMS\CMS\features\variation\variation_data_exporter.py", line 20, in export_variation_data_to_excel
    write_variation_excel_report(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        worksheet,
        ^^^^^^^^^^
    ...<6 lines>...
        percentage_change        
        ^^^^^^^^^^^^^^^^^        
    )
    ^
  File "D:\CMS\CMS\features\variation\variation_excel_structure.py", line 85, in write_variation_excel_report
    subtotal_row_before = summary_row_start
                          ^^^^^^^^^^^^^^^^^
NameError: name 'summary_row_start' is not defined
