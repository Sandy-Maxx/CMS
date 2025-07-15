PS D:\CMS\CMS> python main.py
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\schedule_items_tab.py", line 92, in _add_sub_item
    if dialog.item_name_entry.get(): # Check if an item was actually added/saved
       ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 3258, in get
    return self.tk.call(self._w, 'get')
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^
_tkinter.TclError: invalid command name ".!toplevel.!notebook.!scheduleitemstab.!quantityvariationdialog4.!frame.!entry"
