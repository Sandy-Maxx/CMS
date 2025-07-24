PS D:\CMS\CMS>  python main.py
Firm documents table columns after ALTER: ['id', 'work_id', 'firm_name', 'pg_no', 'pg_amount', 'bank_name', 'bank_address', 'firm_address', 'indemnity_bond_details', 'other_docs_details', 'submission_date', 'pg_submitted', 'indemnity_bond_submitted']
Traceback (most recent call last):
  File "D:\CMS\CMS\main.py", line 16, in <module>
    main()
    ~~~~^^
  File "D:\CMS\CMS\main.py", line 12, in main
    app = MainWindow(root)
  File "D:\CMS\CMS\features\work_management\main_window.py", line 28, in __init__
    self._create_widgets()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 118, in _create_widgets
    self.backup_button = ttk.Button(button_frame, image=self.backup_icon, compound=tk.LEFT, command=self._backup_database, style='Success.TButton')
                                                                                                    ^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'MainWindow' object has no attribute '_backup_database'
PS D:\CMS\CMS> 