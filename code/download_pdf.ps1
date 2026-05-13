$downloadDir = "D:\course\proWrite\papers"
$sciHubBase = "https://sci-hub.jp/"

$papers = @(
    @{DOI="10.1016/j.jallcom.2012.01.108"; File="Room-temperature MBE deposition Bi2Te3 Sb2Te3.pdf"},
    @{DOI="10.1007/s12274-021-3613-7"; File="Moire-pattern Sb2Te3-graphene.pdf"},
    @{DOI="10.3390/nano13131973"; File="Self-powered Sb2Te3-MoS2 photodetector.pdf"},
    @{DOI="10.1016/j.jssc.2024.124785"; File="Weak interlayer 1T-MoTe2-Sb2Te3.pdf"},
    @{DOI="10.1016/j.ijheatmasstransfer.2024.126479"; File="Sb2Te3-Te van der Waals.pdf"},
    @{DOI="10.1016/j.jallcom.2024.177313"; File="Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf"},
    @{DOI="10.1016/j.vacuum.2018.12.017"; File="Improved Sb2Te3-Cr bilayers.pdf"},
    @{DOI="10.1016/j.spmi.2018.05.035"; File="GeTe-Sb2Te3 superlattices.pdf"},
    @{DOI="10.1126/sciadv.aao1669"; File="Tailoring tricolor magnetic topological insulator.pdf"}
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sci-Hub PDF Download Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($paper in $papers) {
    $url = "$sciHubBase$($paper.DOI)"
    $filePath = Join-Path $downloadDir $paper.File
    
    if (Test-Path $filePath) {
        Write-Host "[SKIP] Already exists: $($paper.File)" -ForegroundColor Green
        continue
    }
    
    Write-Host "[DOWNLOAD] $($paper.DOI)" -ForegroundColor Yellow
    Write-Host "  URL: $url" -ForegroundColor Gray
    Write-Host "  Saving to: $($paper.File)" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing -TimeoutSec 30 -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
        # Check if response is PDF
        $contentType = $response.Headers["Content-Type"]
        $contentBytes = $response.Content
        
        if ($contentBytes[0] -eq 0x25 -and $contentBytes[1] -eq 0x50 -and $contentBytes[2] -eq 0x44 -and $contentBytes[3] -eq 0x46) {
            # It's a PDF (%PDF)
            [System.IO.File]::WriteAllBytes($filePath, $contentBytes)
            $fileSize = (Get-Item $filePath).Length / 1024
            Write-Host "[SUCCESS] Downloaded: $fileSize KB" -ForegroundColor Green
        } else {
            Write-Host "[WARN] Not a PDF, content type: $contentType" -ForegroundColor Red
            Write-Host "  Need to open in browser manually" -ForegroundColor Red
        }
    } catch {
        Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 2
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Download Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files in $downloadDir :" -ForegroundColor Yellow
Get-ChildItem $downloadDir -Filter "*.pdf" | Select-Object Name, @{Name="Size(KB)";Expression={[math]::Round($_.Length/1024,1)}} | Format-Table -AutoSize
