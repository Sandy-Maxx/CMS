PS D:\CMS\CMS> python main.py
Firm documents table columns after ALTER: ['id', 'work_id', 'firm_name', 'pg_no', 'pg_amount', 'bank_name', 'bank_address', 'firm_address', 'indemnity_bond_details', 'other_docs_details', 'submission_date', 'pg_submitted', 'indemnity_bond_submitted']
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\work_details_extension\work_details_extension_tab.py", line 88, in <lambda>
    self.loa_date_entry.bind("<Button-1>", lambda event: DatePicker(self.main_window_instance.root, self.loa_date_entry, self.loa_date_var.get()))
                                                         ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\utils\date_picker.py", line 37, in __init__
    set_theme(parent.current_theme) # Apply styles based on parent's theme
              ^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2546, in __getattr__
    return getattr(self.tk, attr)
AttributeError: '_tkinter.tkapp' object has no attribute 'current_theme'
PS D:\CMS\CMS> 