@echo off
echo ========================================
echo Zeta Proposer - Release Update Script
echo ========================================

echo.
echo 1. Building new executable...
call venv\Scripts\activate
pyinstaller zeta_proposer.spec

echo.
echo 2. Updating release folder...
copy dist\Zeta_Proposer.exe release\ /Y

echo.
echo 3. Updating configuration files...
copy section_descriptions.json release\ /Y
copy logging_config.json release\ /Y

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