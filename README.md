# CMS Project Overview

This document provides a comprehensive overview of the CMS (Contract Management System) project, detailing its directory structure, features, and the purpose of its main components.

## Project Structure

```
D:/CMS/CMS/
├───a.md
├───cms_database.db
├───cms_db_checker.py
├───cms.spec
├───config.py
├───create_dirs.py
├───create_dummy_pdf.py
├───create_dummy_template.py
├───create_variation_dir.py
├───create_vitiation_dir.py
├───get_pymupdf_version.py
├───image.png
├───main.py
├───main.spec
├───populate_db.py
├───Project_Beta_Variation_Report_20250721_014648.xlsx
├───Project_Gamma1_Firm_A-Gamma_Report_20250721_080351.xlsx
├───Project_Gamma1_Price_Variation_Report_20250721_075937.xlsx
├───Project_Gamma1_Variation_Report_20250721_075831.xlsx
├───Project_Gamma1_Vitiation_Report_20250721_075906.xlsx
├───README.md
├───requirements.txt
├───t.txt
├───test_calculation_tab.py
├───test_comparison_report.py
├───test_pdf_tools.py
├───test_price_variation_report.py
├───test_template_engine.py
├───test_variation_report.py
├───test_vitiation_report.py
├───test_work_flow.py
├───work_1_export.xlsx
├───__pycache__/
│   └───config.cpython-313.pyc
├───.git/...
├───assets/
│   └───icons/
│       ├───add.png
│       ├───arrange.png
│       ├───browse.png
│       ├───calendar.png
│       ├───cancel.png
│       ├───compare.png
│       ├───delete.png
│       ├───down.png
│       ├───edit.png
│       ├───export.png
│       ├───extract.png
│       ├───folder.png
│       ├───logo.jpg
│       ├───merge.png
│       ├───report.png
│       ├───rotate.png
│       ├───rupee.png
│       ├───save.png
│       ├───selection.png
│       ├───up-arrow.png
│       ├───up.png
│       ├───variation.png
│       └───dark-mode.png
├───database/
│   ├───__init__.py
│   ├───db_manager_oop.py
│   ├───db_manager.py
│   └───__pycache__/
│       ├───__init__.cpython-313.pyc
│       ├───db_manager_oop.cpython-313.pyc
│       └───db_manager.cpython-313.pyc
├───exported/
│   └───Description_for_Project_Alpha_estimate_20250724_201638.xlsx
├───features/
│   ├───__init__.py
│   ├───__pycache__/
│   │   └───__init__.cpython-313.pyc
│   ├───about_tab/
│   │   ├───about_tab.py
│   │   └───__pycache__/
│   ├───AutodocGen/
│   │   ├───__init__.py
│   │   ├───autodoc_manager.py
│   │   ├───constants.py
│   │   ├───data_fetcher.py
│   │   ├───document_generator.py
│   │   ├───firm_selector_dialog.py
│   │   ├───pg_details_formatter.py
│   │   ├───placeholder_parser.py
│   │   └───__pycache__/
│   ├───calculation/
│   │   ├───__init__.py
│   │   ├───calculation_logic.py
│   │   ├───calculation_tab.py
│   │   └───__pycache__/
│   ├───comparison/
│   │   ├───comparison_data_manager.py
│   │   ├───comparison_excel_structure.py
│   │   ├───comparison_exporter.py
│   │   └───__pycache__/
│   ├───estimates/
│   │   ├───__init__.py
│   │   ├───constants.py
│   │   ├───data_loader.py
│   │   ├───export_runner.py
│   │   ├───formatter.py
│   │   ├───utils.py
│   │   ├───workbook_builder.py
│   │   ├───writer.py
│   │   └───__pycache__/
│   ├───excel_export/
│   │   ├───excel_exporter.py
│   │   └───__pycache__/
│   ├───firm_documents/
│   │   ├───__init__.py
│   │   ├───firm_documents_manager.py
│   │   ├───firm_documents_tab.py
│   │   └───__pycache__/
│   ├───pdf_tools/
│   │   ├───__init__.py
│   │   ├───compression_dial_widget.py
│   │   ├───pdf_manager.py
│   │   ├───pdf_tool_tab.py
│   │   └───__pycache__/
│   ├───price_variation/
│   │   ├───__init__.py
│   │   ├───price_variation_data_manager.py
│   │   ├───price_variation_excel_structure.py
│   │   ├───price_variation_exporter.py
│   │   └───__pycache__/
│   ├───template_engine/
│   │   ├───__init__.py
│   │   ├───data_manager.py
│   │   ├───date_picker_widget.py
│   │   ├───special_placeholder_handler.py
│   │   ├───template_engine_tab.py
│   │   ├───template_processor.py
│   │   ├───work_data_provider.py
│   │   └───__pycache__/
│   ├───variation/
│   │   ├───__init__.py
│   │   ├───variation_data_exporter.py
│   │   ├───variation_excel_structure.py
│   │   ├───Variation_report.py
│   │   └───__pycache__/
│   ├───vitiation/
│   │   ├───__init__.py
│   │   ├───QuantityVariationDialog.py
│   │   ├───vitiation_data_exporter.py
│   │   ├───vitiation_excel_structure.py
│   │   ├───Vitiation_report.py
│   │   └───__pycache__/
│   └───work_management/
│       ├───__init__.py
│       ├───individual_firm_rates_tab.py
│       ├───main_window.py
│       ├───schedule_items_tab.py
│       ├───variation_manager.py
│       ├───work_details_tab.py
│       ├───work_editor.py
│       ├───work_search_bar.py
│       ├───__pycache__/
│       ├───dialogs/
│       ├───firm_registration/
│       ├───single_firm_export/
│       └───work_details_extension/
├───prompts/
│   ├───comparision.json
│   ├───drafting.md
│   ├───icon.md
│   ├───TEMPLATE_ENGINE.md
│   ├───variation.md
│   └───vitiation.md
├───template_data/
│   ├───template - Copy.docx.json
│   └───Under 5 Lacs on Quotation M&P.docx.json
├───Templates/
│   └───Letters/
│       ├───Generated_New Microsoft Word Document.docx
│       └───New Microsoft Word Document.docx
├───utils/
│   ├───__init__.py
│   ├───date_picker.py
│   ├───helpers.py
│   ├───styles.py
│   └───__pycache__/
│       ├───__init__.cpython-313.pyc
│       ├───date_picker.cpython-313.pyc
│       ├───helpers.cpython-313.pyc
│       └───styles.cpython-313.pyc
└───venv/
    ├───.gitignore
    ├───pyvenv.cfg
    ├───Include/
    ├───Lib/
    │   └───site-packages/
    └───Scripts/
        ├───activate
        ├───activate.bat
        ├───activate.fish
        ├───Activate.ps1
        ├───deactivate.bat
        ├───f2py.exe
        ├───num2words
        ├───...
        └───...
```

## Component Descriptions

### Root Directory (`D:/CMS/CMS/`)
*   `a.md`: A markdown file, possibly for notes or temporary content.
*   `cms_database.db`: The SQLite database file for the CMS application.
*   `cms_db_checker.py`: A script likely used to check or verify the integrity of the CMS database.
*   `cms.spec`: PyInstaller spec file for building the application.
*   `config.py`: Configuration settings for the application, such as database connection details or other global parameters.
*   `create_dirs.py`: A script to create necessary directories for the project.
*   `create_dummy_pdf.py`: Script to create dummy PDF files for testing PDF tools.
*   `create_dummy_template.py`: Script to create dummy template files for testing the template engine.
*   `create_variation_dir.py`: A script specifically for creating directories related to variations.
*   `create_vitiation_dir.py`: A script specifically for creating directories related to vitiations.
*   `get_pymupdf_version.py`: A utility script to get the PyMuPDF version.
*   `image.png`: An image file, likely used for testing or as a placeholder.
*   `main.py`: The main entry point of the application, initializing the database and the main window.
*   `main.spec`: PyInstaller spec file for the main executable.
*   `populate_db.py`: A script used to populate the database with initial or sample data.
*   `Project_Beta_Variation_Report_20250721_014648.xlsx`: Example exported Excel file for Variation Report.
*   `Project_Gamma1_Firm_A-Gamma_Report_20250721_080351.xlsx`: Example exported Excel file for Firm Report.
*   `Project_Gamma1_Price_Variation_Report_20250721_075937.xlsx`: Example exported Excel file for Price Variation Report.
*   `Project_Gamma1_Variation_Report_20250721_075831.xlsx`: Example exported Excel file for Variation Report.
*   `Project_Gamma1_Vitiation_Report_20250721_075906.xlsx`: Example exported Excel file for Vitiation Report.
*   `README.md`: This file, providing an overview of the project.
*   `requirements.txt`: Lists the Python dependencies required for the project.
*   `t.txt`: A text file, likely for temporary content or testing.
*   `test_calculation_tab.py`: Unit tests for the calculation tab.
*   `test_comparison_report.py`: Unit tests for the comparison report feature.
*   `test_pdf_tools.py`: Unit tests for the PDF tools.
*   `test_price_variation_report.py`: Unit tests for the price variation report.
*   `test_template_engine.py`: Unit tests for the template engine.
*   `test_variation_report.py`: Unit tests for the variation report.
*   `test_vitiation_report.py`: Unit tests for the vitiation report.
*   `test_work_flow.py`: Unit tests for the overall work flow.
*   `work_1_export.xlsx`: An example Excel export file, likely generated by the `excel_export` feature.
*   `__pycache__/`: Directory for Python bytecode cache files.
*   `.git/`: Git repository metadata.

### `assets/`
This directory contains static assets used by the application.
*   `icons/`: Stores various icon image files used in the user interface.
    *   `add.png`: Icon for adding new items.
    *   `arrange.png`: Icon for arranging elements.
    *   `browse.png`: Icon for browsing files.

    *   `calendar.png`: Icon related to calendar or date selection.
    *   `cancel.png`: Icon for canceling operations.
    *   `compare.png`: Icon for comparison features.
    *   `delete.png`: Icon for deleting items.
    *   `down.png`: Icon for down arrow/movement.
    *   `edit.png`: Icon for editing items.
    *   `export.png`: Icon for exporting data.
    *   `extract.png`: Icon for extracting data.
    *   `folder.png`: Icon for folder or directory representation.
    *   `logo.jpg`: Application logo.
    *   `merge.png`: Icon for merging operations.
    *   `report.png`: Icon for generating reports.
    *   `rotate.png`: Icon for rotating elements.
    *   `rupee.png`: Icon representing the Indian Rupee currency.
    *   `save.png`: Icon for saving data.
    *   `selection.png`: Icon for selection-related actions.
    *   `up-arrow.png`: Icon for up arrow/movement.
    *   `up.png`: Another icon for up arrow/movement.
    *   `variation.png`: Icon related to variation features.
    *   `dark-mode.png`: Icon for the dark mode toggle button.

### `database/`
Manages database interactions.
*   `__init__.py`: Initializes the Python package.
*   `db_manager_oop.py`: Object-oriented database manager (possibly an alternative or newer implementation).

*   `db_manager.py`: Contains functions and classes for managing SQLite database operations (e.g., creating tables, adding/updating/deleting works, schedule items, firm rates, template data, variations, and firm details). Includes functions for database backup and restore.
*   `__pycache__/`: Python bytecode cache.

### `exported/`
Contains exported reports and documents.
*   `Description_for_Project_Alpha_estimate_20250724_201638.xlsx`: Example exported Excel estimate report.

### `features/`
Contains distinct feature modules of the application.
*   `__init__.py`: Initializes the Python package.
*   `__pycache__/`: Python bytecode cache.
*   `about_tab/`: Module for the "About" section of the application.
    *   `about_tab.py`: Implements the UI and content for the about tab.
    *   `__pycache__/`: Python bytecode cache.
*   `AutodocGen/`: Module for automated document generation.
    *   `__init__.py`: Initializes the Python package.
    *   `autodoc_manager.py`: Manages the overall process of generating documents.
    *   `constants.py`: Defines constants used in document generation.
    *   `data_fetcher.py`: Handles fetching data required for document generation.
    *   `document_generator.py`: Contains the logic for generating various types of documents (e.g., letters, office notes).
    *   `firm_selector_dialog.py`: Dialog for selecting firms during document generation.
    *   `pg_details_formatter.py`: Formats PG (Performance Guarantee) details for documents.
    *   `placeholder_parser.py`: Parses placeholders within document templates.
    *   `__pycache__/`: Python bytecode cache.
*   `calculation/`: Module for various calculations within the application.
    *   `__init__.py`: Initializes the Python package.
    *   `calculation_logic.py`: Contains the core calculation algorithms.
    *   `calculation_tab.py`: Implements the UI and logic for the calculation tab, including date difference calculations (days, months, years) with options to include/exclude start and end dates.
    *   `__pycache__/`: Python bytecode cache.
*   `comparison/`: Module for comparing data between different works or firms.
    *   `comparison_data_manager.py`: Manages data for comparison operations.
    *   `comparison_excel_structure.py`: Defines the Excel structure for comparison reports.
    *   `comparison_exporter.py`: Handles exporting comparison data to Excel.
    *   `__pycache__/`: Python bytecode cache.
*   `estimates/`: Module for generating estimate reports.
    *   `__init__.py`: Initializes the Python package.
    *   `constants.py`: Defines constants for estimate generation.
    *   `data_loader.py`: Loads data relevant to estimates.
    *   `export_runner.py`: Orchestrates the estimate export process.
    *   `formatter.py`: Formats data for estimate reports.
    *   `utils.py`: Utility functions for estimates.
    *   `workbook_builder.py`: Builds the Excel workbook structure for estimates.
    *   `writer.py`: Writes data to the Excel workbook for estimates.
    *   `__pycache__/`: Python bytecode cache.
*   `excel_export/`: Module responsible for exporting general work data to Excel files.
    *   `excel_exporter.py`: Implements the logic for exporting work data to Excel.
    *   `__pycache__/`: Python bytecode cache.
*   `firm_documents/`: Module for managing firm-related documents and their details.
    *   `__init__.py`: Initializes the Python package.
    *   `firm_documents_manager.py`: Manages database operations for firm documents.
    *   `firm_documents_tab.py`: Implements the UI and logic for the firm documents tab.
    *   `__pycache__/`: Python bytecode cache.
*   `pdf_tools/`: Module providing various PDF manipulation tools.
    *   `__init__.py`: Initializes the Python package.
    *   `compression_dial_widget.py`: UI widget for PDF compression settings.
    *   `pdf_manager.py`: Manages PDF operations like compression, merging, and extraction.
    *   `pdf_tool_tab.py`: Implements the UI and logic for the PDF tools tab.
    *   `__pycache__/`: Python bytecode cache.
*   `price_variation/`: Module for generating price variation reports.
    *   `__init__.py`: Initializes the Python package.
    *   `price_variation_data_manager.py`: Manages data for price variation reports.
    *   `price_variation_excel_structure.py`: Defines the Excel structure for price variation reports.
    *   `price_variation_exporter.py`: Handles exporting price variation data to Excel.
    *   `__pycache__/`: Python bytecode cache.
*   `template_engine/`: Module for processing and managing document templates.
    *   `__init__.py`: Initializes the Python package.
    *   `data_manager.py`: Manages data used by the template engine, including saving and loading template data with historical input tracking for suggestions.
    *   `date_picker_widget.py`: Implements a date picker UI widget.
    *   `special_placeholder_handler.py`: Handles special placeholders within templates.
    *   `template_engine_tab.py`: Manages the UI and logic for the template engine tab, including input suggestions and loading generated documents.
    *   `template_processor.py`: Processes templates, replacing placeholders with actual data.
    *   `work_data_provider.py`: Provides work-related data to the template engine.
    *   `__pycache__/`: Python bytecode cache.
*   `variation/`: Module for managing variations in work items and generating reports.
    *   `__init__.py`: Initializes the Python package.
    *   `variation_data_exporter.py`: Handles data export for variation reports.
    *   `variation_excel_structure.py`: Defines the Excel structure for variation reports.
    *   `Variation_report.py`: Generates reports related to variations.
    *   `__pycache__/`: Python bytecode cache.
*   `vitiation/`: Module for managing vitiations (defects/deviations) in work items and generating reports.
    *   `__init__.py`: Initializes the Python package.
    *   `QuantityVariationDialog.py`: Implements a dialog for handling quantity variations, often related to vitiations.
    *   `vitiation_data_exporter.py`: Handles data export for vitiation reports.
    *   `vitiation_excel_structure.py`: Defines the Excel structure for vitiation reports.
    *   `Vitiation_report.py`: Generates reports related to vitiations.
    *   `__pycache__/`: Python bytecode cache.
*   `work_management/`: Core module for managing work-related functionalities.
    *   `__init__.py`: Initializes the Python package.
    *   `individual_firm_rates_tab.py`: Manages the UI and logic for individual firm rates.
    *   `main_window.py`: Defines the main application window and its layout, integrating various feature tabs. Includes a dark mode toggle button.
    *   `schedule_items_tab.py`: Manages the UI and logic for schedule items.
    *   `variation_manager.py`: Manages the creation, editing, and deletion of variations within work items.
    *   `work_details_tab.py`: Manages the UI and logic for displaying and editing work details.
    *   `work_editor.py`: Provides functionality for editing work-related data.
    *   `work_search_bar.py`: Implements the search bar functionality for work items.
    *   `__pycache__/`: Python bytecode cache.
    *   `dialogs/`: Contains general dialog box implementations for work management.
        *   `__init__.py`: Initializes the Python package.
    *   `firm_registration/`: Module for registering and managing firm details.
        *   `firm_details_dialog.py`: Dialog for adding/editing firm details.
        *   `firm_manager.py`: Manages firm-related database operations.
        *   `firm_registration_tab.py`: Implements the UI and logic for the firm registration tab.
    *   `single_firm_export/`: Module for exporting data related to single firms.
        *   `__init__.py`: Initializes the Python package.
        *   `single_firm_data_manager.py`: Manages data for single firm exports.
        *   `single_firm_excel_structure.py`: Defines the Excel structure for single firm exports.
        *   `single_firm_exporter.py`: Handles exporting single firm data to Excel.
    *   `work_details_extension/`: Module for extending work details functionalities.
        *   `__init__.py`: Initializes the Python package.
        *   `work_details_extension_tab.py`: Manages the UI and logic for extended work details.

### `prompts/`
Contains JSON and markdown files used as prompts or templates.
*   `comparision.json`: JSON file likely containing data or configuration for comparison prompts.
*   `drafting.md`: Markdown file for drafting related content.
*   `icon.md`: A markdown file, likely containing instructions or descriptions related to icons, or possibly a prompt for icon generation/usage.
*   `TEMPLATE_ENGINE.md`: Markdown file providing context or instructions for the template engine.
*   `variation.md`: Markdown file for variation related content.
*   `vitiation.md`: Markdown file for vitiation related content.

### `template_data/`
Stores data related to document templates.
*   `template - Copy.docx.json`: JSON data for a copied document template.
*   `Under 5 Lacs on Quotation M&P.docx.json`: JSON data for a specific document template.

### `Templates/`
Stores actual document templates.
*   `Letters/`: Directory for letter templates.
    *   `Generated_New Microsoft Word Document.docx`: An example of a generated Word document.
    *   `New Microsoft Word Document.docx`: A template Word document.

### `utils/`
Contains utility functions and helper modules.
*   `__init__.py`: Initializes the Python package.
*   `date_picker.py`: Implements a date picker utility.
*   `helpers.py`: General utility functions that can be used across different parts of the application, including UI helpers and data formatting. Now includes in-app toast messages with emojis.
*   `styles.py`: Defines styling and theming parameters for the application's UI, including light and dark modes.
*   `__pycache__/`: Python bytecode cache.

### `venv/`
This directory contains the Python virtual environment for the project. It includes:
*   `.gitignore`: Specifies intentionally untracked files to ignore by Git.
*   `pyvenv.cfg`: Configuration file for the virtual environment.
*   `Include/`: Directory for C header files.
*   `Lib/`: Directory for Python libraries and packages.
    *   `site-packages/`: Contains third-party Python packages installed in the virtual environment.
*   `Scripts/`: Contains executable scripts for the virtual environment (e.g., `activate`, `python.exe`, `pip.exe`).

## Dependencies
The project relies on the following Python packages, as specified in `requirements.txt`:

*   `PyPDF2==3.0.1`
*   `PyMuPDF==1.24.5`
*   `python-docx`
*   `openpyxl`
*   `pandas`
*   `tkcalendar`
*   `num2words`
*   `sv_ttk`
*   `lxml`
*   `Pillow`
*   `pytz`
*   `tzdata`
*   `python-dateutil`

## Building the Executable
The application can be packaged into a standalone executable using PyInstaller.

**Prerequisites:**
*   Ensure you have PyInstaller installed: `pip install pyinstaller`

**Steps:**
1.  **Clean previous builds (optional but recommended):**
    ```bash
    rmdir /s /q build dist && del /q *.spec
    ```
    (Note: If these directories/files don't exist, the commands will show an error, which is normal.)

2.  **Build the executable:**
    ```bash
    python -m PyInstaller --noconfirm --onefile --windowed --add-data "assets;assets" --add-data "cms_database.db;." main.py
    ```
    *   `--noconfirm`: Overwrite existing files without asking.
    *   `--onefile`: Create a single executable file.
    *   `--windowed`: Create a windowed application (no console window).
    *   `--add-data "assets;assets"`: Include the `assets` directory. The first `assets` is the source path, the second is the destination folder inside the executable.
    *   `--add-data "cms_database.db;."`: Include the `cms_database.db` file in the root of the executable's data.
    *   `main.py`: The main script of your application.

3.  **Adding an Icon (Optional):**
    If you wish to add a custom icon to your executable, you need a `.ico` file. If you only have `logo.jpg`, you'll need to convert it to `logo.ico` using an online converter or an image editing tool. Once you have `logo.ico`, you can include it in the build command:
    ```bash
    python -m PyInstaller --noconfirm --onefile --windowed --add-data "assets;assets" --add-data "cms_database.db;." --icon="path/to/your/logo.ico" main.py
    ```
    Replace `"path/to/your/logo.ico"` with the actual path to your icon file.

**Output:**
The generated executable will be located in the `dist` directory (e.g., `dist/main.exe`).

## Usage
To run the application after building the executable, simply navigate to the `dist` directory and execute `main.exe`.

