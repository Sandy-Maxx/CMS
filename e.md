PS D:\CMS\CMS>  python main.py
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\schedule_items_tab.py", line 92, in <lambda>
    self.header_context_menu.entryconfigure(0, command=lambda: self._delete_variation(column_name))
                                                              
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\work_management\schedule_items_tab.py", line 95, in _delete_variation
    self.variation_manager.delete_variation(variation_name)   
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^   
  File "D:\CMS\CMS\features\work_management\variation_manager.py", line 35, in delete_variation
    confirm = utils_helpers.show_confirm_dialog(self.schedule_items_tab.parent_app.window, f"Are you sure you want to delete the variation '{variation_name}'?")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'utils.helpers' has no attribute 'show_confirm_dialog'
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\tkinter\__init__.py", line 2068, in __call__
    return self.func(*args)
           ~~~~~~~~~^^^^^^^
  File "D:\CMS\CMS\features\work_management\schedule_items_tab.py", line 92, in <lambda>
    self.header_context_menu.entryconfigure(0, command=lambda: self._delete_variation(column_name))
                                                              
 ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\work_management\schedule_items_tab.py", line 95, in _delete_variation
    self.variation_manager.delete_variation(variation_name)   
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^   
  File "D:\CMS\CMS\features\work_management\variation_manager.py", line 35, in delete_variation
    confirm = utils_helpers.show_confirm_dialog(self.schedule_items_tab.parent_app.window, f"Are you sure you want to delete the variation '{variation_name}'?")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'utils.helpers' has no attribute 'show_confirm_dialog'
