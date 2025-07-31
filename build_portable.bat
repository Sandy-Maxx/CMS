@echo off
echo Building Portable CMS Application...
echo.

:: Clean up temporary files that could cause issues
echo Cleaning temporary files...
del /q /f "features\estimates\exported\~$*.xlsx" 2>nul
del /q /f "Templates\Letters\~$*.*" 2>nul
del /q /f "Templates\Letters\LETTERS\~$*.*" 2>nul
del /q /f "Templates\Letters\LETTERS\~WRL*.tmp" 2>nul

:: Remove existing build/dist directories
echo Removing old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Build the application
echo Building application with PyInstaller...
python -m PyInstaller cms_simple.spec --noconfirm

:: Check if build was successful
if exist "dist\CMS_Portable\CMS.exe" (
    echo.
    echo ===============================================
    echo Build completed successfully!
    echo.
    echo Portable application is available at:
    echo %CD%\dist\CMS_Portable\
    echo.
    echo Main executable: CMS.exe
    echo Application size: 
    dir "dist\CMS_Portable" /s /-c | find "File(s)"
    echo.
    echo The application is now ready to run on any Windows PC
    echo without requiring Python or additional installations.
    echo ===============================================
    echo.
    
    :: Test the executable
    echo Testing executable...
    cd dist\CMS_Portable
    timeout /t 3 /nobreak >nul
    start CMS.exe
    cd ..\..
    
) else (
    echo.
    echo ===============================================
    echo Build FAILED!
    echo Check the console output above for errors.
    echo ===============================================
    echo.
)

pause
