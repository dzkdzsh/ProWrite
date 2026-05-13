# 批量打开Sci-Hub论文链接
# 每篇论文之间间隔3秒，避免浏览器一次性打开太多标签页

$papers = @(
    @{DOI="10.1016/j.jallcom.2012.01.108"; Ref="ref3"; Title="Room-temperature MBE deposition Bi2Te3 Sb2Te3"},
    @{DOI="10.1007/s12274-021-3613-7"; Ref="ref4"; Title="Moire-pattern Sb2Te3-graphene"},
    @{DOI="10.3390/nano13131973"; Ref="ref5"; Title="Self-powered Sb2Te3-MoS2 photodetector"},
    @{DOI="10.1016/j.jssc.2024.124785"; Ref="ref6"; Title="Weak interlayer 1T-MoTe2-Sb2Te3"},
    @{DOI="10.1016/j.ijheatmasstransfer.2024.126479"; Ref="ref7"; Title="Sb2Te3-Te van der Waals"},
    @{DOI="10.1016/j.jallcom.2024.177313"; Ref="ref8"; Title="Anomalous thermoelectric AgSbTe2-Sb2Te3"},
    @{DOI="10.1016/j.vacuum.2018.12.017"; Ref="ref9"; Title="Improved Sb2Te3-Cr bilayers"},
    @{DOI="10.1016/j.spmi.2018.05.035"; Ref="ref10"; Title="GeTe-Sb2Te3 superlattices"},
    @{DOI="10.1126/sciadv.aao1669"; Ref="ref11"; Title="Tailoring tricolor magnetic topological insulator"}
)

$sciHubBase = "https://sci-hub.jp/"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "正在打开Sci-Hub论文PDF..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($paper in $papers) {
    $url = "$sciHubBase$($paper.DOI)"
    Write-Host "打开 [$($paper.Ref)]: $($paper.Title)" -ForegroundColor Yellow
    Start-Process $url
    Start-Sleep -Seconds 3
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "全部9篇论文已打开！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "请在每个PDF标签页中：" -ForegroundColor Cyan
Write-Host "  1. 点击打印图标（或Ctrl+P）" -ForegroundColor White
Write-Host "  2. 选择'另存为PDF'或'Microsoft Print to PDF'" -ForegroundColor White
Write-Host "  3. 保存到: D:\course\proWrite\papers\" -ForegroundColor White
Write-Host "  4. 使用对应的文件名保存" -ForegroundColor White
Write-Host ""
Write-Host "文件名对应表：" -ForegroundColor Yellow
Write-Host "  ref3  -> Room-temperature MBE deposition Bi2Te3 Sb2Te3.pdf" -ForegroundColor White
Write-Host "  ref4  -> Moire-pattern Sb2Te3-graphene.pdf" -ForegroundColor White
Write-Host "  ref5  -> Self-powered Sb2Te3-MoS2 photodetector.pdf" -ForegroundColor White
Write-Host "  ref6  -> Weak interlayer 1T-MoTe2-Sb2Te3.pdf" -ForegroundColor White
Write-Host "  ref7  -> Sb2Te3-Te van der Waals.pdf" -ForegroundColor White
Write-Host "  ref8  -> Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf" -ForegroundColor White
Write-Host "  ref9  -> Improved Sb2Te3-Cr bilayers.pdf" -ForegroundColor White
Write-Host "  ref10 -> GeTe-Sb2Te3 superlattices.pdf" -ForegroundColor White
Write-Host "  ref11 -> Tailoring tricolor magnetic topological insulator.pdf" -ForegroundColor White
