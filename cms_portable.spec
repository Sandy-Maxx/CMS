# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Get the current directory
current_dir = os.path.dirname(os.path.abspath('main.py'))

# Collect all hidden imports needed for the application
hidden_imports = [
    # Tkinter and GUI related
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    
    # Date picker dependencies
    'tkcalendar',
    'tkcalendar.calendar_',
    'tkcalendar.dateentry',
    'babel',
    'babel.dates',
    'babel.numbers',
    'babel.core',
    
    # PDF and document processing
    'PyPDF2',
    'fitz',  # PyMuPDF
    'docx',
    'python_docx',
    
    # Excel and data processing
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'openpyxl.utils',
    'pandas',
    'numpy',
    'xlsxwriter',
    
    # Date and time handling
    'dateutil',
    'dateutil.parser',
    'dateutil.relativedelta',
    'datetime',
    
    # Database
    'sqlite3',
    
    # HTTP requests
    'requests',
    'urllib3',
    
    # System and file operations
    'pathlib',
    'shutil',
    'tempfile',
    'json',
    'csv',
    're',
    'os',
    'sys',
    'subprocess',
    
    # All application modules
    'database',
    'database.db_manager',
    'database.db_manager_oop',
    'database.managers',
    'features',
    'features.AutodocGen',
    'features.about_tab',
    'features.calculation',
    'features.comparison',
    'features.estimates',
    'features.excel_export',
    'features.firm_documents',
    'features.pdf_tools',
    'features.price_variation',
    'features.template_engine',
    'features.variation',
    'features.vitiation',
    'features.work_management',
    'utils',
]

# Collect all submodules from main packages
for pkg in ['database', 'features', 'utils']:
    hidden_imports.extend(collect_submodules(pkg))

# Data files to include
data_files = [
    # Assets and icons
    ('assets', 'assets'),
    
    # Database file
    ('cms_database.db', '.'),
    
    # Configuration
    ('config.py', '.'),
    
    # Version information
    ('__version__.py', '.'),
    
    # Templates directory
    ('Templates', 'Templates'),
    
    # Template data
    ('template_data', 'template_data'),
    
    # Prompts
    ('prompts', 'prompts'),
    
    # Documentation
    ('docs', 'docs'),
    
    # All Python packages as data
    ('database', 'database'),
    ('features', 'features'),
    ('utils', 'utils'),
    
    # Support scripts
    ('cms_db_checker.py', '.'),
    ('create_dirs.py', '.'),
    ('create_dummy_pdf.py', '.'),
    ('create_dummy_template.py', '.'),
    ('create_variation_dir.py', '.'),
    ('create_vitiation_dir.py', '.'),
    ('populate_db.py', '.'),
    ('requirements.txt', '.'),
]

# Add tkcalendar data files
try:
    tk_cal_data = collect_data_files('tkcalendar')
    data_files.extend(tk_cal_data)
except:
    pass

# Add babel data files for date localization
try:
    babel_data = collect_data_files('babel')
    data_files.extend(babel_data)
except:
    pass

a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=data_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude development and testing modules
        'test_*',
        'pytest',
        'unittest',
        'nose',
        
        # Exclude unused GUI frameworks
        'PyQt4',
        'PyQt5',
        'PyQt6',
        'PySide',
        'PySide2',
        'PySide6',
        'wx',
        
        # Exclude unused packages to reduce size
        'matplotlib',
        'scipy',
        'jupyter',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Filter out duplicate data files
seen = set()
filtered_datas = []
for dest, source, kind in a.datas:
    if dest not in seen:
        seen.add(dest)
        filtered_datas.append((dest, source, kind))
a.datas = filtered_datas

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CMS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/logo.jpg' if os.path.exists('assets/icons/logo.jpg') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CMS_Portable'
)
