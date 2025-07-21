    ~~~~~~~~~~~~~~~~^^^
KeyboardInterrupt
PS D:\CMS\CMS> Dated: 21-07-2025C^C
PS D:\CMS\CMS> python main.py
Traceback (most recent call last):
  File "D:\CMS\CMS\main.py", line 4, in <module>
    from features.work_management.main_window import MainWindow
  File "D:\CMS\CMS\features\work_management\main_window.py", line 15, in <module>
    from features.template_engine.template_engine_tab import TemplateEngineTab
  File "D:\CMS\CMS\features\template_engine\template_engine_tab.py", line 5, in <module>
    from features.template_engine.template_processor import TemplateProcessor
  File "D:\CMS\CMS\features\template_engine\template_processor.py", line 4, in <module>
    from .work_data_provider import WorkDataProvider
  File "D:\CMS\CMS\features\template_engine\work_data_provider.py", line 79
    f"{i+1}. {doc['firm_name']} {pg_status} {doc['pg_no'] or 'N/A'}, Dated: {doc['submission_date'] or 'N/A'}, Amount: Rs. {formatted_pg_amount}, Bank details: {doc['bank_name'] or 'N/A'}, Address: {doc['bank_address'] or 'N/A'.}\n"
                                                                                                                 
                                                                                                                 
 ^
SyntaxError: f-string: expecting '=', or '!', or ':', or '}'
PS D:\CMS\CMS> 