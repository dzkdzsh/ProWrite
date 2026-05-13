# 批量打开Sci-Hub论文链接的脚本
# 每篇论文之间间隔几秒，避免浏览器一次性打开太多标签页

$papers = @(
    @{DOI="10.1016/j.jallcom.2012.01.108"; Ref="ref3"; Title="Room-temperature MBE deposition Bi2Te3 Sb2Te3 thin films"},
    @{DOI="10.1007/s12274-021-3613-7"; Ref="ref4"; Title="Moire-pattern-modulated electronic structures Sb2Te3-graphene"},
    @{DOI="10.3390/nano13131973"; Ref="ref5"; Title="Self-powered Sb2Te3-MoS2 heterojunction photodetector"},
    @{DOI="10.1016/j.jssc.2024.124785"; Ref="ref6"; Title="Weak interlayer interactions 1T-MoTe2-Sb2Te3 superlattice"},
    @{DOI="10.1016/j.ijheatmasstransfer.2024.126479"; Ref="ref7"; Title="Theoretical insights Sb2Te3-Te van der Waals heterostructures"},
    @{DOI="10.1016/j.jallcom.2024.177313"; Ref="ref8"; Title="Anomalous thermoelectric AgSbTe2-Sb2Te3 hetero-phase alloys"},
    @{DOI="10.1016/j.vacuum.2018.12.017"; Ref="ref9"; Title="Improved thermoelectric Sb2Te3-Cr bilayers"},
    @{DOI="10.1016/j.spmi.2018.05.035"; Ref="ref10"; Title="Structural electronic optical GeTe-Sb2Te3 superlattices"},
    @{DOI="10.1126/sciadv.aao1669"; Ref="ref11"; Title="Tailoring tricolor magnetic topological insulator axion"}
)

$sciHubBase = "https://sci-hub.jp/"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "正在打开Sci-Hub论文链接..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($paper in $papers) {
    $url = "$sciHubBase$($paper.DOI)"
    Write-Host "打开 [$($paper.Ref)]: $($paper.Title)" -ForegroundColor Yellow
    Write-Host "  URL: $url" -ForegroundColor Gray
    Start-Process $url
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "所有9篇论文链接已在浏览器中打开！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "请在每个标签页中：" -ForegroundColor Yellow
Write-Host "1. 等待PDF加载完成" -ForegroundColor White
Write-Host "2. 右键点击PDF，选择'另存为'" -ForegroundColor White
Write-Host "3. 保存到: D:\course\proWrite\papers\" -ForegroundColor White
Write-Host "4. 使用对应的文件名保存" -ForegroundColor White
