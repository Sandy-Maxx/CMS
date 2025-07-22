Traceback (most recent call last):
  File "main.py", line 16, in <module>
  File "main.py", line 12, in main
  File "features\work_management\main_window.py", line 25, in __init__
    self._create_widgets()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "features\work_management\main_window.py", line 49, in _create_widgets
    self.about_tab = AboutTab(self.notebook)
                     ~~~~~~~~^^^^^^^^^^^^^^^
  File "features\about_tab\about_tab.py", line 8, in __init__
    self.create_widgets()
    ~~~~~~~~~~~~~~~~~~~^^
  File "features\about_tab\about_tab.py", line 45, in create_widgets
    self._add_faqs_section()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "features\about_tab\about_tab.py", line 244, in _add_faqs_section
    self._create_collapsible_section(self.accordion_frame, "Frequently Asked Questions (FAQ)", faq_content_frame)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "features\about_tab\about_tab.py", line 64, in _create_collapsible_section
    content_builder_func(content_frame)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
TypeError: 'Frame' object is not callable
