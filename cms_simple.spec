# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Define all data files to include
datas = [
    ('assets', 'assets'),
    ('cms_database.db', '.'),
    ('config.py', '.'),
    ('__version__.py', '.'),
    ('template_data', 'template_data'),
    ('prompts', 'prompts'),
    ('docs', 'docs'),
    ('cms_db_checker.py', '.'),
    ('create_dirs.py', '.'),
    ('create_dummy_pdf.py', '.'),
    ('create_dummy_template.py', '.'),
    ('create_variation_dir.py', '.'),
    ('create_vitiation_dir.py', '.'),
    ('populate_db.py', '.'),
    ('requirements.txt', '.'),
]

# Add important hidden imports
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkcalendar',
    'babel.numbers',
    'babel.dates',
    'PyPDF2',
    'fitz',
    'docx',
    'openpyxl',
    'pandas',
    'dateutil',
    'sqlite3',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/logo.jpg',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CMS_Portable',
)
