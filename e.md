PS D:\CMS\CMS> python main.py
Traceback (most recent call last):
  File "D:\CMS\CMS\main.py", line 14, in <module>
    main()
    ~~~~^^
  File "D:\CMS\CMS\main.py", line 10, in main
    app = MainWindow(root)
  File "D:\CMS\CMS\features\work_management\main_window.py", line 22, in __init__
    self._create_widgets()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "D:\CMS\CMS\features\work_management\main_window.py", line 34, in _create_widgets
    self.pdf_tool_tab = PdfToolTab(self.notebook, self)
                        ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "D:\CMS\CMS\features\pdf_tools\pdf_tool_tab.py", line 23, in __init__
    self._create_widgets()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "D:\CMS\CMS\features\pdf_tools\pdf_tool_tab.py", line 38, in _create_widgets
    self.tab_control.bind("<Motion>", self._show_tab_tooltip)
                                      ^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'PdfToolTab' object has no attribute '_show_tab_tooltip'