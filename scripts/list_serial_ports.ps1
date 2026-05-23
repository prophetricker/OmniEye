$ErrorActionPreference = "Stop"

Write-Host "Available serial port names:"
[System.IO.Ports.SerialPort]::GetPortNames() | Sort-Object | ForEach-Object {
    Write-Host "  $_"
}

Write-Host ""
Write-Host "Windows port devices:"
Get-PnpDevice -Class Ports -ErrorAction SilentlyContinue |
    Select-Object Status,FriendlyName,InstanceId |
    Format-Table -AutoSize
