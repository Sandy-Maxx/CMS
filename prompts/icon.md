(venv) PS D:\CMS\CMS> python main.py
Traceback (most recent call last):
  File "D:\CMS\CMS\main.py", line 3, in <module>
    from features.work_management.main_window import MainWindow
  File "D:\CMS\CMS\features\work_management\main_window.py", line 9, in <module>
    from features.variation.Variation_report import VariationReportDialog
  File "D:\CMS\CMS\features\variation\Variation_report.py", line 6, in <module>
    from features.variation.variation_data_exporter import export_variation_data_to_excel
  File "D:\CMS\CMS\features\variation\variation_data_exporter.py", line 3, in <module>
    from features.variation.variation_excel_structure import get_variation_table_columns, write_variation_excel_headers
  File "D:\CMS\CMS\features\variation\variation_excel_structure.py", line 1, in <module>
    from xlsxwriter.utility import xl_col_to_name       
ModuleNotFoundError: No module named 'xlsxwriter'       
(venv) PS D:\CMS\CMS> 