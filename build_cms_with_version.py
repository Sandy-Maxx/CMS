#!/usr/bin/env python3
"""
Build script for CMS application with version stamping.
This script updates the version file with current timestamp and builds the executable.
"""
import os
import sys
import subprocess
import shutil
from datetime import datetime


def update_version_file():
    """Update the version file with current build timestamp"""
    print("Updating version information...")
    
    version_content = f'''"""
Version information for CMS Application
Generated at build time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

# Version information
__version__ = "1.0.0"
__build_timestamp__ = "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
__build_date__ = "{datetime.now().strftime("%Y%m%d")}"

# Combined version string for display
VERSION_STRING = f"{{__version__}}.{{__build_date__}}"
FULL_VERSION_INFO = f"CMS v{{__version__}} (Build: {{__build_timestamp__}})"

def get_version():
    """Return the version string"""
    return VERSION_STRING

def get_full_version():
    """Return the full version info with timestamp"""
    return FULL_VERSION_INFO

def get_build_info():
    """Return build information"""
    return {{
        'version': __version__,
        'build_timestamp': __build_timestamp__,
        'build_date': __build_date__,
        'version_string': VERSION_STRING
    }}
'''
    
    with open('__version__.py', 'w') as f:
        f.write(version_content)
    
    print(f"Version updated: v1.0.0 (Build: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")


def clean_build_directories():
    """Clean existing build and dist directories"""
    print("Cleaning build directories...")
    
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"Removed {dir_name} directory")
            except Exception as e:
                print(f"Warning: Could not remove {dir_name}: {e}")


def clean_temp_files():
    """Clean temporary files that could cause build issues"""
    print("Cleaning temporary files...")
    
    temp_patterns = [
        "features/estimates/exported/~$*.xlsx",
        "Templates/Letters/~$*.*",
        "Templates/Letters/LETTERS/~$*.*",
        "Templates/Letters/LETTERS/~WRL*.tmp"
    ]
    
    for pattern in temp_patterns:
        try:
            # Use PowerShell to remove files matching patterns
            cmd = f'powershell -Command "Remove-Item \\"{pattern}\\" -Force -ErrorAction SilentlyContinue"'
            subprocess.run(cmd, shell=True, capture_output=True)
        except Exception:
            pass  # Ignore errors for temp file cleanup


def run_pyinstaller():
    """Run PyInstaller to build the executable"""
    print("Running PyInstaller...")
    
    # Use the portable spec file
    spec_file = 'cms_portable.spec'
    if not os.path.exists(spec_file):
        spec_file = 'cms_simple.spec'
    
    cmd = [sys.executable, '-m', 'PyInstaller', spec_file, '--noconfirm']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("PyInstaller build completed successfully!")
            return True
        else:
            print("PyInstaller build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Error running PyInstaller: {e}")
        return False


def verify_build():
    """Verify that the build was successful"""
    exe_path = os.path.join('dist', 'CMS_Portable', 'CMS.exe')
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        print(f"\\nBuild successful!")
        print(f"Executable: {exe_path}")
        print(f"Size: {size:,} bytes ({size/1024/1024:.1f} MB)")
        
        # Get directory size
        dist_path = os.path.join('dist', 'CMS_Portable')
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(dist_path):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
                file_count += 1
        
        print(f"Total application size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
        print(f"Total files: {file_count}")
        
        return True
    else:
        print("\\nBuild failed - executable not found!")
        return False


def main():
    """Main build process"""
    print("=" * 60)
    print("CMS Application Build with Version Stamping")
    print("=" * 60)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Step 1: Update version information
        update_version_file()
        
        # Step 2: Clean temporary files
        clean_temp_files()
        
        # Step 3: Clean build directories
        clean_build_directories()
        
        # Step 4: Run PyInstaller
        if not run_pyinstaller():
            print("\\nBuild process failed!")
            return 1
        
        # Step 5: Verify build
        if not verify_build():
            print("\\nBuild verification failed!")
            return 1
        
        print("\\n" + "=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("The portable CMS application is ready in dist/CMS_Portable/")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\\nBuild process failed with error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
