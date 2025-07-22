# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('D:/CMS/CMS/assets', 'assets'),
    ('D:/CMS/CMS/database', 'database'),
    ('D:/CMS/CMS/features', 'features'),
    ('D:/CMS/CMS/prompts', 'prompts'),
    ('D:/CMS/CMS/template_data', 'template_data'),
    ('D:/CMS/CMS/utils', 'utils'),
    ('D:/CMS/CMS/cms_database.db', '.'),
    ('D:/CMS/CMS/config.py', '.'),
    ('D:/CMS/CMS/cms_db_checker.py', '.'),
    ('D:/CMS/CMS/create_dirs.py', '.'),
    ('D:/CMS/CMS/create_dummy_pdf.py', '.'),
    ('D:/CMS/CMS/create_dummy_template.py', '.'),
    ('D:/CMS/CMS/create_variation_dir.py', '.'),
    ('D:/CMS/CMS/create_vitiation_dir.py', '.'),
    ('D:/CMS/CMS/populate_db.py', '.'),
    ('D:/CMS/CMS/requirements.txt', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=['D:/CMS/CMS'],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='cms',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_info_entries=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
