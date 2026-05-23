param(
    [int] $DurationSeconds = 45,
    [int] $IntervalMs = 500
)

$ErrorActionPreference = "Stop"

function Get-MatchingDeviceBlocks {
    param([string] $Pattern)

    $text = pnputil /enum-devices /connected | Out-String
    $lines = $text -split "`r?`n"
    $current = New-Object System.Collections.Generic.List[string]
    $matchedBlocks = New-Object System.Collections.Generic.List[string]

    foreach ($line in $lines) {
        if ($line -match "^\s*Instance ID:") {
            if ($current.Count -gt 0 -and (($current -join "`n") -match $Pattern)) {
                [void] $matchedBlocks.Add(($current.ToArray() -join "`n"))
            }
            $current.Clear()
        }
        if ($line.Trim().Length -gt 0) {
            $current.Add($line)
        }
    }

    if ($current.Count -gt 0 -and (($current -join "`n") -match $Pattern)) {
        [void] $matchedBlocks.Add(($current.ToArray() -join "`n"))
    }

    if ($matchedBlocks.Count -eq 0) {
        return "(no X4-like USB device visible)"
    }

    return ($matchedBlocks -join "`n---`n")
}

$pattern = "Insta360|X4|Android|ADB|MTP|Portable|ExpressL|USBX_storage|USBSTOR|VID_070A|PID_4026|libusb|WinUSB"
$end = (Get-Date).AddSeconds($DurationSeconds)
$last = $null

Write-Host "Watching X4 USB enumeration for $DurationSeconds seconds."
Write-Host "Now trigger Android phone control on the X4."
Write-Host ""

while ((Get-Date) -lt $end) {
    $snapshot = Get-MatchingDeviceBlocks $pattern
    if ($snapshot -ne $last) {
        Write-Host "[$((Get-Date).ToString('HH:mm:ss.fff'))] USB state changed:"
        Write-Host $snapshot
        Write-Host ""
        $last = $snapshot
    }
    Start-Sleep -Milliseconds $IntervalMs
}
