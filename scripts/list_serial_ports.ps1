$ErrorActionPreference = "Stop"

Write-Host "Serial port names:"
[System.IO.Ports.SerialPort]::GetPortNames() | ForEach-Object {
    Write-Host "  $_"
}

Write-Host ""
Write-Host "Serial device details:"
Get-CimInstance Win32_SerialPort |
    Select-Object DeviceID, Name, Description, Manufacturer |
    Format-Table -AutoSize
