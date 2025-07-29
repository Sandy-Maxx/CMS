PS D:\CMS\CMS>  python main.py
Firm documents table columns after ALTER: ['id', 'work_id', 'firm_name', 'pg_no', 'pg_amount', 'bank_name', 'bank_address', 'firm_address', 'indemnity_bond_details', 'other_docs_details', 'submission_date', 'pg_submitted', 'indemnity_bond_submitted', 'pg_type', 'pg_submitted_on', 'pg_vetted_on', 'indemnity_submitted_on', 'indemnity_vetted_on', 'ib_vetted_on']        
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 454, in edit_work
    self._show_work_editor_view(work_id=work_id)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 151, in _show_work_editor_view
    self.current_work_editor = WorkDetailsEditor(self.work_editor_container_frame, self, work_id, self.root)
                               ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\work_management\work_editor.py", line 73, in __init__ 
    self.firm_documents_tab = FirmDocumentsTab(self.notebook, self.work_id_var, self.main_window_instance)
                              ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\firm_documents\firm_documents_tab.py", line 21, in __init__
    self._create_widgets()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "D:\CMS\CMS\features\firm_documents\firm_documents_tab.py", line 167, in _create_widgets
    self._toggle_pg_fields()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "D:\CMS\CMS\features\firm_documents\firm_documents_tab.py", line 425, in _toggle_pg_fields
    self.pg_no_entry.config(state=state) 
    ^^^^^^^^^^^^^^^^
AttributeError: 'FirmDocumentsTab' object has no attribute 'pg_no_entry'
