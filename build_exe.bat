@echo off
REM ============================================================
REM  build_exe.bat — Build SK.exe (Windows only)
REM  ត្រូវរត់ script នេះនៅលើម៉ាស៊ីន Windows ដែលបានដំឡើង Python រួច
REM ============================================================

cd /d "%~dp0..\app"

echo [1/3] កំពុងដំឡើង dependencies...
pip install -r requirements.txt

echo [2/3] កំពុង build .exe ជាមួយ PyInstaller...
pyinstaller --noconfirm --onefile --windowed ^
  --name "SK" ^
  --icon "..\chrome_extension\icons\app_icon.ico" ^
  sk.py

echo [3/3] ចម្លងឯកសារបន្ថែម (license.py, server.py already bundled by PyInstaller)...
echo.
echo ✅ ស្រេចហើយ! ឯកសារ .exe នៅក្នុងថត: app\dist\SK.exe
echo   ជំហានបន្ទាប់៖ បើក installer\SKSetup.iss ជាមួយ Inno Setup Compiler
echo   ដើម្បីបង្កើត Setup Installer ពិតប្រាកដ។
pause
