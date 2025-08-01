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

# Add only English locale data for tkcalendar
try:
    import tkcalendar
    tk_cal_path = os.path.dirname(tkcalendar.__file__)
    data_files.append((tk_cal_path, 'tkcalendar'))
except:
    pass

# Add minimal babel data (English only)
try:
    import babel
    babel_path = os.path.dirname(babel.__file__)
    # Only include core babel files, not all locales
    data_files.append((os.path.join(babel_path, 'core.py'), 'babel/'))
    data_files.append((os.path.join(babel_path, 'dates.py'), 'babel/'))
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
        # Heavy unused packages
        'matplotlib',
        'scipy', 
        'numpy.random.mtrand',  # Heavy numpy submodules
        'numpy.fft',
        'numpy.linalg.lapack_lite',
        'jupyter',
        'IPython',
        'notebook',
        
        # Unused GUI frameworks
        'PyQt4', 'PyQt5', 'PyQt6',
        'PySide', 'PySide2', 'PySide6', 
        'wx', 'wxPython',
        'gi', 'gtk',
        
        # Development tools
        'pytest', 'unittest', 'nose', 'coverage',
        'setuptools', 'pip', 'wheel',
        'distutils',
        
        # Documentation
        'sphinx', 'docutils', 'jinja2',
        
        # Web frameworks (if not used)
        'flask', 'django', 'tornado',
        'fastapi', 'uvicorn',
        
        # Heavy standard library modules not needed
        'multiprocessing.pool',
        'concurrent.futures',
        'asyncio',
        'email',
        'http.server',
        'urllib3.poolmanager',
        'xml.etree.cElementTree',
        
        # Unused babel locales (keep only en)
        'babel.localedata.af',
        'babel.localedata.ar', 
        'babel.localedata.de',
        'babel.localedata.es',
        'babel.localedata.fr',
        'babel.localedata.hi',
        'babel.localedata.ja',
        'babel.localedata.ko',
        'babel.localedata.ru',
        'babel.localedata.zh',
        # Add more locale excludes as needed
        
        # Testing modules
        'test',
        '_pytest',
        'py.test',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate datas
seen = set()
unique_datas = []
for dest, source, kind in a.datas:
    if dest not in seen:
        seen.add(dest)
        unique_datas.append((dest, source, kind))
a.datas = unique_datas

# Remove duplicate binaries  
seen_bin = set()
unique_binaries = []
for name, path, kind in a.binaries:
    if name not in seen_bin:
        seen_bin.add(name)
        unique_binaries.append((name, path, kind))
a.binaries = unique_binaries

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CMS_Optimized',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip debug symbols
    upx=True,    # Enable UPX compression
    console=False,  # GUI application
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
    strip=True,  # Strip debug info
    upx=True,    # Compress all files
    upx_exclude=[
        # Don't compress these (can cause issues)
        'vcruntime140.dll',
        'python38.dll',
        'python39.dll', 
        'python310.dll',
        'python311.dll',
        'python312.dll',
    ],
    name='CMS_Optimized'
)
