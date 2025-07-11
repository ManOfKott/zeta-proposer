# Zeta Proposer - Release Update Script (PowerShell)
param(
    [string]$Version = "1.1",
    [switch]$SkipBuild = $false
)

Write-Host "========================================" -ForegroundColor Green
Write-Host "Zeta Proposer - Release Update Script" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`n0. Cleaning up old ZIP files..." -ForegroundColor Yellow
$oldZips = Get-ChildItem -Path "." -Filter "Zeta_Proposer_v*.zip"
if ($oldZips) {
    Write-Host "Found $($oldZips.Count) old ZIP file(s):" -ForegroundColor Cyan
    foreach ($zip in $oldZips) {
        Write-Host "  - $($zip.Name)" -ForegroundColor White
        Remove-Item $zip.FullName -Force
    }
    Write-Host "Old ZIP files deleted." -ForegroundColor Green
}
else {
    Write-Host "No old ZIP files found." -ForegroundColor Cyan
}

if (-not $SkipBuild) {
    Write-Host "`n1. Building new executable..." -ForegroundColor Yellow
    & venv\Scripts\Activate.ps1
    pyinstaller zeta_proposer.spec
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Build failed! Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n2. Updating release folder..." -ForegroundColor Yellow
Copy-Item "dist\Zeta_Proposer.exe" "release\" -Force

Write-Host "`n2.1. Ensuring output directories exist..." -ForegroundColor Yellow
# Create output directory structure
New-Item -Path "release\output" -ItemType Directory -Force | Out-Null
New-Item -Path "release\output\docx" -ItemType Directory -Force | Out-Null
New-Item -Path "release\output\json" -ItemType Directory -Force | Out-Null
New-Item -Path "release\output\logs" -ItemType Directory -Force | Out-Null
Write-Host "Output directories created/verified:" -ForegroundColor Cyan
Write-Host "  - release\output\docx" -ForegroundColor White
Write-Host "  - release\output\json" -ForegroundColor White
Write-Host "  - release\output\logs" -ForegroundColor White

Write-Host "`n2.2. Copying templates folder..." -ForegroundColor Yellow
if (Test-Path "templates") {
    Copy-Item "templates" "release\" -Recurse -Force
    Write-Host "Templates folder copied to release." -ForegroundColor Green
}
else {
    Write-Host "Warning: templates folder not found!" -ForegroundColor Yellow
}

Write-Host "`n3. Updating configuration files..." -ForegroundColor Yellow
Copy-Item "section_descriptions.json" "release\" -Force
Copy-Item "logging_config.json" "release\" -Force
# Note: config.json is NOT copied as it's automatically created on first run

Write-Host "`n4. Creating new ZIP archive..." -ForegroundColor Yellow
$zipName = "Zeta_Proposer_v$Version.zip"
Compress-Archive -Path "release\*" -DestinationPath $zipName -Force

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Release update completed!" -ForegroundColor Green
Write-Host "New files:" -ForegroundColor White
Write-Host "- release\Zeta_Proposer.exe (updated)" -ForegroundColor White
Write-Host "- release\templates\ (copied)" -ForegroundColor White
Write-Host "- $zipName (new version)" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Green

# Show file sizes
$exeSize = (Get-Item "release\Zeta_Proposer.exe").Length / 1MB
$zipSize = (Get-Item $zipName).Length / 1MB
Write-Host "`nFile sizes:" -ForegroundColor Cyan
Write-Host "- EXE: $([math]::Round($exeSize, 1)) MB" -ForegroundColor White
Write-Host "- ZIP: $([math]::Round($zipSize, 1)) MB" -ForegroundColor White 