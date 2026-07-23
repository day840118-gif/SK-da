@echo off
setlocal
cd /d "%~dp0"
title SK - ដំឡើង និងបើកកម្មវិធីស្វ័យប្រវត្តិ

echo ================================================
echo   SK - ការដំឡើងស្វ័យប្រវត្តិ (One-Click Install)
echo ================================================
echo.

REM ---------- ១. ពិនិត្យមើលថាតើ Python បានដំឡើងឬនៅ ----------
where python >nul 2>nul
if errorlevel 1 (
    echo [!] រកមិនឃើញ Python នៅលើកុំព្យូទ័រនេះទេ។
    echo.
    echo សូមទាញយក ^ដំឡើង Python ជាមុនសិន ^(ឥតគិតថ្លៃ^)៖
    echo   https://www.python.org/downloads/
    echo.
    echo ^*^*^* សំខាន់ណាស់ ^*^*^*៖ ពេលដំឡើង សូមធីកប្រអប់
    echo   "Add python.exe to PATH" នៅទំព័រដំបូងផង!
    echo.
    echo កម្មវិធីនឹងបើក webpage ទាញយកជូនអ្នកឥឡូវនេះ...
    start https://www.python.org/downloads/
    echo.
    echo ដំឡើង Python រួចហើយ សូម Double-click ឯកសារនេះម្តងទៀត។
    pause
    exit /b 1
)
echo [OK] រកឃើញ Python ហើយ។
echo.

REM ---------- ២. ដំឡើង library ចាំបាច់ ----------
echo [1/3] កំពុងដំឡើង library ចាំបាច់ (yt-dlp)...
python -m pip install --upgrade pip >nul 2>nul
python -m pip install -r app\requirements.txt
if errorlevel 1 (
    echo.
    echo [!] ការដំឡើង library បរាជ័យ។
    echo សូម screenshot សារខាងលើនេះ ហើយផ្ញើមកសួរជំនួយ។
    pause
    exit /b 1
)
echo.

REM ---------- ៣. បង្កើត + ធ្វើ Activation ដោយស្វ័យប្រវត្តិ (លើកដំបូង) ----------
echo [2/3] កំពុងពិនិត្យ Activation...
python -c "import sys; sys.path.insert(0,'app'); import license; sys.exit(0 if license.is_activated() else 1)" >nul 2>nul
if errorlevel 1 (
    echo កំពុងបង្កើត Activation Key ស្វ័យប្រវត្តិ សម្រាប់ការប្រើលើកដំបូង...
    python -c "import sys; sys.path.insert(0,'app'); import license; k=license.generate_key(); ok=license.activate(k); print('Activation Key របស់អ្នក:', k)"
    echo [OK] បានធ្វើ Activation រួចរាល់ស្វ័យប្រវត្តិ។ ^(មិនចាំបាច់វាយបញ្ចូល key ដោយដៃទេ^)
) else (
    echo [OK] កម្មវិធីត្រូវបាន Activate រួចហើយ។
)
echo.

REM ---------- ៤. បើកកម្មវិធី ----------
echo [3/3] កំពុងបើកកម្មវិធី SK...
echo.
cd app
python sk.py

pause
