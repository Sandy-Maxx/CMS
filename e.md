PS D:\CMS\CMS> python main.py
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 237, in add_work
    WorkDetailsEditor(self.root, None, self.load_works)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\work_management\work_editor.py", line 77, in __init__
    self.window.protocol("WM_DELETE_WINDOW", self.on_close)
                                             ^^^^^^^^^^^^^
AttributeError: 'WorkDetailsEditor' object has no attribute 'on_close'
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__   
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 237, in add_work    
    WorkDetailsEditor(self.root, None, self.load_works)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\work_management\work_editor.py", line 77, in __init__     
    self.window.protocol("WM_DELETE_WINDOW", self.on_close)
                                           
  ^^^^^^^^^^^^^
AttributeError: 'WorkDetailsEditor' object has no attribute 'on_close'
