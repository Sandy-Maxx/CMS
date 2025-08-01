#!/usr/bin/env python3
"""
Build script for creating optimized CMS executable
This script ensures all dependencies are properly handled and creates a lightweight executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'PyInstaller',
        'PyPDF2', 
        'PyMuPDF',
        'pandas',
        'python-dateutil',
        'tkcalendar', 
        'requests',
        'python-docx',
        'openpyxl',
        'xlsxwriter'
    ]
    
    print("Checking required packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PyMuPDF':
                import fitz
            elif package == 'python-docx':
                import docx
            elif package == 'python-dateutil':
                import dateutil
            elif package == 'PyInstaller':
                import PyInstaller
            elif package == 'PyPDF2':
                import PyPDF2
            else:
                __import__(package.lower().replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - MISSING")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    print("All required packages are installed!\n")
    return True

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    print("Build directories cleaned!\n")

def verify_files():
    """Verify all essential files exist"""
    essential_files = [
        'main.py',
        'cms_database.db',
        'config.py',
        'cms_optimized.spec',
        'hook-babel.py'
    ]
    
    essential_dirs = [
        'database',
        'features', 
        'utils',
        'assets',
        'Templates'
    ]
    
    print("Verifying essential files...")
    for file in essential_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            return False
    
    print("\nVerifying essential directories...")
    for dir_name in essential_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ - MISSING")
            return False
    
    print("All essential files verified!\n")
    return True

def build_executable():
    """Build the optimized executable"""
    print("Building optimized executable...")
    print("This may take several minutes...\n")
    
    try:
        # Use the optimized spec file
        cmd = [
            sys.executable, '-m', 'PyInstaller', 
            '--clean',  # Clean build
            '--noconfirm',  # Don't ask for confirmation
            'cms_optimized.spec'
        ]
        
        print("Running PyInstaller command:")
        print(" ".join(cmd))
        print()
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Build completed successfully!")
            
            # Check if executable was created
            exe_path = os.path.join('dist', 'CMS_Optimized', 'CMS_Optimized.exe')
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
                print(f"✓ Executable created: {exe_path}")
                print(f"✓ File size: {file_size:.1f} MB")
                
                # Get folder size
                folder_path = os.path.join('dist', 'CMS_Optimized')
                folder_size = get_folder_size(folder_path) / (1024 * 1024)  # Size in MB
                print(f"✓ Total folder size: {folder_size:.1f} MB")
                
                return True
            else:
                print("✗ Executable not found in expected location")
                return False
        else:
            print("✗ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def get_folder_size(folder_path):
    """Calculate total size of a folder"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def create_portable_version():
    """Create a portable version with batch file"""
    dist_path = os.path.join('dist', 'CMS_Optimized')
    if not os.path.exists(dist_path):
        return False
    
    # Create run.bat for easy execution
    bat_content = '''@echo off
echo Starting CMS Application...
CMS_Optimized.exe
if errorlevel 1 (
    echo.
    echo Application encountered an error.
    echo Press any key to close...
    pause >nul
)
'''
    
    with open(os.path.join(dist_path, 'run.bat'), 'w') as f:
        f.write(bat_content)
    
    # Create README
    readme_content = '''CMS Application - Portable Version

SYSTEM REQUIREMENTS:
- Windows 7/10/11 (64-bit)
- No additional software required
- Minimum 4GB RAM recommended

INSTALLATION:
1. Extract all files to a folder
2. Double-click 'run.bat' or 'CMS_Optimized.exe'
3. The application will start automatically

TROUBLESHOOTING:
- If the app doesn't start, try running as Administrator
- Ensure Windows Defender/Antivirus is not blocking the file
- Check Windows Event Viewer for detailed error messages

For support, contact your system administrator.
'''
    
    with open(os.path.join(dist_path, 'README.txt'), 'w') as f:
        f.write(readme_content)
    
    print("✓ Portable version created with run.bat and README.txt")
    return True

def main():
    """Main build process"""
    print("=" * 60)
    print("CMS OPTIMIZED BUILD SCRIPT")
    print("=" * 60)
    print()
    
    # Check current directory
    if not os.path.exists('main.py'):
        print("✗ Please run this script from the CMS root directory")
        return False
    
    # Step 1: Check requirements
    if not check_requirements():
        return False
    
    # Step 2: Verify files
    if not verify_files():
        return False
    
    # Step 3: Clean build directories
    clean_build_dirs()
    
    # Step 4: Build executable
    if not build_executable():
        return False
    
    # Step 5: Create portable version
    create_portable_version()
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Your optimized executable is ready at:")
    print("dist/CMS_Optimized/CMS_Optimized.exe")
    print()
    print("You can copy the entire 'CMS_Optimized' folder to any Windows PC")
    print("and run the application without installing Python or dependencies.")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nBuild failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("Build process completed successfully!")
        input("Press Enter to exit...")
