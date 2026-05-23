$ErrorActionPreference = "Stop"

$sdkBin = "D:\MyProject\Bohack2\.sdk_extract\windows\Windows_CameraSDK-2.1.1_MediaSDK-3.1.3\CameraSDK\CameraSDK-20250812_192505-2.1.1-win64\bin"
$sdkTest = Join-Path $sdkBin "CameraSDKTest.exe"

function Show-MatchingBlocks {
    param(
        [string] $Text,
        [string] $Pattern
    )

    $blocks = [regex]::Split($Text, "(?m)(?=^\s*(?:Instance ID:|Published Name:))")
    $matches = @($blocks | Where-Object { $_ -match $Pattern })
    if ($matches.Count -eq 0) {
        Write-Host "  (no matching entries)"
        return
    }

    foreach ($match in $matches) {
        Write-Host $match.Trim()
        Write-Host ""
    }
}

function Show-MatchingDeviceLines {
    param(
        [string] $Text,
        [string] $Pattern
    )

    $lines = $Text -split "`r?`n"
    $current = New-Object System.Collections.Generic.List[string]
    $matchedBlocks = New-Object System.Collections.Generic.List[string]

    foreach ($line in $lines) {
        if ($line -match "^\s*(Instance ID:|Published Name:)") {
            if ($current.Count -gt 0 -and (($current -join "`n") -match $Pattern)) {
                $item = $current.ToArray() -join "`n"
                [void] $matchedBlocks.Add($item)
            }
            $current.Clear()
        }
        if ($line.Trim().Length -gt 0) {
            $current.Add($line)
        }
    }

    if ($current.Count -gt 0 -and (($current -join "`n") -match $Pattern)) {
        $item = $current.ToArray() -join "`n"
        [void] $matchedBlocks.Add($item)
    }

    if ($matchedBlocks.Count -eq 0) {
        Write-Host "  (no matching entries)"
        return
    }

    foreach ($matchedBlock in $matchedBlocks) {
        Write-Host $matchedBlock
        Write-Host ""
    }
}

Write-Host "OmniEye X4 USB diagnosis"
Write-Host "Expected X4 mode: Android phone control"
Write-Host ""

Write-Host "Connected devices that look camera-related:"
$connectedDevices = pnputil /enum-devices /connected | Out-String
Show-MatchingDeviceLines $connectedDevices "Insta360|X4|Android|ADB|MTP|Portable|ExpressL|USBX_storage|VID_070A|libusb|WinUSB"

Write-Host ""
Write-Host "Installed driver packages that look relevant:"
$drivers = pnputil /enum-drivers | Out-String
Show-MatchingBlocks $drivers "libusb|WinUSB|Android|Google|Insta360|Zadig"

Write-Host ""
if (Test-Path $sdkTest) {
    Write-Host "Running official CameraSDKTest.exe..."
    Push-Location $sdkBin
    try {
        cmd /c "echo 0|CameraSDKTest.exe"
    } finally {
        Pop-Location
    }
} else {
    Write-Host "CameraSDKTest.exe not found at $sdkTest"
}
