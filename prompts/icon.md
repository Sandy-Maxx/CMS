PS D:\CMS\CMS> python main.py
Traceback (most recent call last):
  File "D:\CMS\CMS\features\work_management\main_window.py", line 134, in _export_comparison_report
    exporter.export_to_excel(file_path)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "D:\CMS\CMS\features\comparison\comparison_exporter.py", line 37, in export_to_excel
    header_rows = excel_structure.get_excel_header_structure()
                  ^^^^^^^^^^^^^^^
NameError: name 'excel_structure' is not defined. Did you mean: 'self.excel_structure'?
PS D:\CMS\CMS> 
