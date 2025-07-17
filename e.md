PS D:\CMS\CMS>  python main.py
Traceback (most recent call last):
  File "D:\CMS\CMS\main.py", line 3, in <module>
    from features.work_management.main_window import MainWindow
  File "D:\CMS\CMS\features\work_management\main_window.py", line 10, in <module>
    from features.vitiation.Vitiation_report import VitiationReportDialog
  File "D:\CMS\CMS\features\vitiation\Vitiation_report.py", line 6, in <module>
    from features.vitiation.vitiation_data_exporter import export_vitiation_data_to_excel
  File "D:\CMS\CMS\features\vitiation\vitiation_data_exporter.py", line 133
    return False, f"Error generating report: {str(e)}
                  ^
SyntaxError: unterminated f-string literal (detected at line 133)
