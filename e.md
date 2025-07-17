PS D:\CMS\CMS> python main.py
Error in export_vitiation_data_to_excel: name 'firm_summary_data' is not defined
Traceback (most recent call last):
  File "D:\CMS\CMS\features\vitiation\vitiation_data_exporter.py", line 114, in export_vitiation_data_to_excel
    total_costs_before.append((firm_summary_data[firm_name]['total_cost_before_gst'], firm_name))
                               ^^^^^^^^^^^^^^^^^
NameError: name 'firm_summary_data' is not defined
PS D:\CMS\CMS> 