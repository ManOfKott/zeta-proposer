@echo off
echo ========================================
echo Zeta Proposer - Release Update Script
echo ========================================

echo.
echo 0. Cleaning up old ZIP files...
for %%f in (Zeta_Proposer_v*.zip) do (
    echo   - Deleting %%f
    del "%%f"
)
if not exist "Zeta_Proposer_v*.zip" (
    echo No old ZIP files found.
) else (
    echo Old ZIP files deleted.
)

echo.
echo 1. Building new executable...
call venv\Scripts\activate
pyinstaller zeta_proposer.spec

echo.
echo 2. Updating release folder...
copy dist\Zeta_Proposer.exe release\ /Y

echo.
echo 2.1. Ensuring output directories exist...
if not exist "release\output" mkdir "release\output"
if not exist "release\output\docx" mkdir "release\output\docx"
if not exist "release\output\json" mkdir "release\output\json"
if not exist "release\output\logs" mkdir "release\output\logs"
echo Output directories created/verified:
echo   - release\output\docx
echo   - release\output\json
echo   - release\output\logs

echo.
echo 3. Updating configuration files...
copy section_descriptions.json release\ /Y
copy logging_config.json release\ /Y
REM Note: config.json is NOT copied as it's automatically created on first run

echo.
echo 4. Creating new ZIP archive...
powershell Compress-Archive -Path release\* -DestinationPath Zeta_Proposer_v1.1.zip -Force

echo.
echo ========================================
echo Release update completed!
echo New files:
echo - release\Zeta_Proposer.exe (updated)
echo - Zeta_Proposer_v1.1.zip (new version)
echo ========================================
pause 