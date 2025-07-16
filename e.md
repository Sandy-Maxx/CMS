PS D:\CMS\CMS> python main.py
Traceback (most recent call last):
  File "D:\CMS\CMS\main.py", line 3, in <module>
    from features.work_management.main_window import MainWindow
  File "D:\CMS\CMS\features\work_management\main_window.py", line 11, in <module>
    from features.comparison.comparison_exporter import ComparisonExporter
  File "D:\CMS\CMS\features\comparison\comparison_exporter.py", line 47
    percentage_format = workbook.add_format({'num_format': '0.00%'}
                                           ^      
SyntaxError: '(' was never closed
PS D:\CMS\CMS> 