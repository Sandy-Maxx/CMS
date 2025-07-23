PS D:\CMS\CMS> python main.py
Firm documents table columns after ALTER: ['id', 'work_id', 'firm_name', 'pg_no', 'pg_amount', 'bank_name', 'bank_address', 'firm_address', 'indemnity_bond_details', 'other_docs_details', 'submission_date', 'pg_submitted', 'indemnity_bond_submitted']
Traceback (most recent call last):
  File "D:\CMS\CMS\features\work_management\main_window.py", line 252, in _export_estimate_report
    run_export(work_id, selected_firm)
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\estimates\export_runner.py", line 15, in run_export
    data = load_data(work_id, firm_name)
  File "D:\CMS\CMS\features\estimates\data_loader.py", line 33, in load_data
    firm_rate = db_manager.get_firm_rate_for_item(item['item_id'], firm_name)
  File "D:\CMS\CMS\database\db_manager.py", line 260, in get_firm_rate_for_item
    cursor.execute(
    ~~~~~~~~~~~~~~^
        "SELECT id, schedule_item_id, firm_name, unit_rate, labour_rate, date_recorded FROM firm_rates WHERE schedule_item_id = ? AND firm_name = ?",
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        (schedule_item_id, firm_name)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
sqlite3.OperationalError: no such column: labour_rate