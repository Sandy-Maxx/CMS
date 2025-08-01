# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Get the current directory
current_dir = os.path.dirname(os.path.abspath('main.py'))

# Essential hidden imports - only what's actually needed
hidden_imports = [
    # Core GUI
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    
    # Date picker (essential for your app)
    'tkcalendar',
    'tkcalendar.calendar_',
    'tkcalendar.dateentry',
    
    # Document processing (core features)
    'PyPDF2',
    'fitz',  # PyMuPDF
    'docx',
    'python_docx',
    
    # Excel (essential for your CMS)
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.utils',
    'xlsxwriter',
    
    # Data processing (lightweight approach)
    'pandas',  # Keep but optimize usage
    
    # Date handling (essential)
    'dateutil',
    'dateutil.parser',
    'dateutil.relativedelta',
    'datetime',
    
    # Core system
    'sqlite3',
    'requests',
    'json',
    'csv',
    're',
    'pathlib',
    'shutil',
    'tempfile',
    
    # Your application modules (specific imports only)
    'database.db_manager',
    'database.db_manager_oop', 
    'database.managers',
    'features.AutodocGen.document_generator',
    'features.AutodocGen.enquiry_table_formatter',
    'features.template_engine.work_data_provider',
    'features.about_tab',
    'features.calculation',
    'features.comparison',
    'features.estimates', 
    'features.excel_export',
    'features.firm_documents',
    'features.pdf_tools',
    'features.price_variation',
    'features.variation',
    'features.vitiation',
    'features.work_management',
    'utils.helpers',
]

# Minimal data files - only essentials
data_files = [
    # Core assets
    ('assets/icons', 'assets/icons'),
    
    # Database
    ('cms_database.db', '.'),
    
    # Essential config
    ('config.py', '.'),
    ('__version__.py', '.'),
    
    # Templates (core functionality)
    ('Templates', 'Templates'),
    ('template_data', 'template_data'),
    ('prompts', 'prompts'),
    
    # Core modules as data
    ('database', 'database'),
    ('features', 'features'), 
    ('utils', 'utils'),
    
    # Essential scripts only
    ('requirements.txt', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=data_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # Don't exclude anything for debug
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CMS_Debug',
    debug=True,  # Enable debug mode
    bootloader_ignore_signals=False,
    strip=False,  # Don't strip debug symbols
    upx=False,   # Disable UPX for debugging
    console=True,  # Enable console output
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
    strip=False,  # Don't strip debug info
    upx=False,    # No compression for debugging
    upx_exclude=[],
    name='CMS_Debug'
)
