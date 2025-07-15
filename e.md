C:\Users\MY PC\AppData\Roaming\Python\Python313\site-packages\xlsxwriter\worksheet.py:2243: UserWarning: Can't merge single cell
  warn("Can't merge single cell")
Error in export_vitiation_data_to_excel: 'Workbook' object has no attribute 'xl_col_to_name'  
Traceback (most recent call last):
  File "D:\CMS\CMS\features\vitiation\vitiation_data_exporter.py", line 84, in export_vitiation_data_to_excel
    unit_rate_col_letter = workbook.xl_col_to_name(col_idx - 1) # Unit Rate is one column to the left
                           ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'Workbook' object has no attribute 'xl_col_to_name'
PS D:\CMS\CMS>