# DSGNRG Creative Loop Agent - PowerShell Setup
Write-Host "🔁 DSGNRG Creative Loop Agent Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --no-warn-script-location

Write-Host ""
Write-Host "Setup complete! Here's how to use your Creative Loop Agent:" -ForegroundColor Green
Write-Host ""
Write-Host "CLI Usage:" -ForegroundColor White
Write-Host "  python loop_cli.py status report" -ForegroundColor Gray
Write-Host "  python loop_cli.py input sketch 30 'Your sketch description'" -ForegroundColor Gray
Write-Host ""
Write-Host "Web Dashboard:" -ForegroundColor White
Write-Host "  python loop_server.py" -ForegroundColor Gray
Write-Host "  Then open http://localhost:5000" -ForegroundColor Gray
Write-Host ""

$response = Read-Host "Would you like to run a status report now? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Host ""
    python loop_cli.py status report
}

Write-Host ""
Write-Host "Your Creative Loop Agent is ready! 🎵🖼️📖" -ForegroundColor Green