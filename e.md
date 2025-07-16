PS D:\CMS\CMS> python main.py
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 160, in edit_work
    WorkDetailsEditor(self.root, work_id, self.load_works)    
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "D:\CMS\CMS\features\work_management\work_editor.py", line 40, in __init__
    self.work_details_tab = WorkDetailsTab(
                            ~~~~~~~~~~~~~~^
        self.notebook, self, self.work_id_var, self.is_new_work_var, self.status_label,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.notebook, self.schedule_items_tab, self.populate_reference_firm_combobox
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
TypeError: WorkDetailsTab.__init__() missing 1 required positional argument: 'populate_reference_firm_combobox_callback'    
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 160, in edit_work
    WorkDetailsEditor(self.root, work_id, self.load_works)    
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
  File "D:\CMS\CMS\features\work_management\work_editor.py", line 40, in __init__
    self.work_details_tab = WorkDetailsTab(
                            ~~~~~~~~~~~~~~^
        self.notebook, self, self.work_id_var, self.is_new_work_var, self.status_label,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.notebook, self.schedule_items_tab, self.populate_reference_firm_combobox
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
TypeError: WorkDetailsTab.__init__() missing 1 required positional argument: 'populate_reference_firm_combobox_callback'    
PS D:\CMS\CMS> 