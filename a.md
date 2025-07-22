PS D:\CMS\CMS> python main.py
Firm documents table columns after ALTER: ['id', 'work_id', 'firm_name', 'pg_no', 'pg_amount', 'bank_name', 'bank_address', 'firm_address', 'indemnity_bond_details', 'other_docs_details', 'submission_date', 'pg_submitted', 'indemnity_bond_submitted']
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__     
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\vitiation\QuantityVariationDialog.py", line 86, in _load_firms
    firms = db_manager.get_all_firm_names() 
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   
AttributeError: module 'database.db_manager' has no attribute 'get_all_firm_names'. Did you mean: 'get_all_unique_firm_names'?      
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__     
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\vitiation\QuantityVariationDialog.py", line 86, in _load_firms
    firms = db_manager.get_all_firm_names() 
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   
AttributeError: module 'database.db_manager' has no attribute 'get_all_firm_names'. Did you mean: 'get_all_unique_firm_names'?      
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__     
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\vitiation\QuantityVariationDialog.py", line 86, in _load_firms
    firms = db_manager.get_all_firm_names() 
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   
AttributeError: module 'database.db_manager' has no attribute 'get_all_firm_names'. Did you mean: 'get_all_unique_firm_names'?      
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__     
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\vitiation\QuantityVariationDialog.py", line 86, in _load_firms
    firms = db_manager.get_all_firm_names() 
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   
AttributeError: module 'database.db_manager' has no attribute 'get_all_firm_names'. Did you mean: 'get_all_unique_firm_names'?      
