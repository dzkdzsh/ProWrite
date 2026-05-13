# Sci-Hub论文下载脚本
# 该脚本会依次打开Sci-Hub链接，你需要手动保存PDF到指定文件夹

$downloadDir = "D:\course\proWrite\papers"
$sciHubBase = "https://sci-hub.jp/"

# 论文列表：DOI和文件名
# 已下载：ref1, ref2
# 待下载：ref3-ref11

$papers = @(
    @{
        DOI = "10.1016/j.jallcom.2012.01.108"
        FileName = "Room-temperature MBE deposition, thermoelectric properties, and advanced structural characterization of binary Bi2Te3 and Sb2Te3 thin films.pdf"
        Ref = "ref3"
    },
    @{
        DOI = "10.1007/s12274-021-3613-7"
        FileName = "Moiré-pattern-modulated electronic structures in Sb2Te3-graphene heterostructure.pdf"
        Ref = "ref4"
    },
    @{
        DOI = "10.3390/nano13131973"
        FileName = "Self-powered Sb2Te3-MoS2 heterojunction broadband photodetector on flexible substrate.pdf"
        Ref = "ref5"
    },
    @{
        DOI = "10.1016/j.jssc.2024.124785"
        FileName = "Weak interlayer interactions and nearly temperature independent electrical transport in p-type 1T'-MoTe2-Sb2Te3 superlattice-like films.pdf"
        Ref = "ref6"
    },
    @{
        DOI = "10.1016/j.ijheatmasstransfer.2024.126479"
        FileName = "Theoretical insights into Sb2Te3-Te van der Waals heterostructures for achieving very high figure of merit and conversion efficiency.pdf"
        Ref = "ref7"
    },
    @{
        DOI = "10.1016/j.jallcom.2024.177313"
        FileName = "Anomalous thermoelectric nature in disordered AgSbTe2-Sb2Te3 hetero-phase alloys for room temperature applications.pdf"
        Ref = "ref8"
    },
    @{
        DOI = "10.1016/j.vacuum.2018.12.017"
        FileName = "Improved thermoelectric performances of nanocrystalline Sb2Te3-Cr bilayers by reducing thermal conductivity in the grain boundaries and heterostructure interface.pdf"
        Ref = "ref9"
    },
    @{
        DOI = "10.1016/j.spmi.2018.05.035"
        FileName = "Structural, electronic and optical properties of GeTe-Sb2Te3 superlattices - a first-principles study.pdf"
        Ref = "ref10"
    },
    @{
        DOI = "10.1126/sciadv.aao1669"
        FileName = "Tailoring tricolor structure of magnetic topological insulator for robust axion insulator.pdf"
        Ref = "ref11"
    }
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sci-Hub 论文下载助手" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "下载目录: $downloadDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "说明：" -ForegroundColor Green
Write-Host "1. 脚本会依次在默认浏览器中打开Sci-Hub链接" -ForegroundColor White
Write-Host "2. 你的Edge浏览器已登录Sci-Hub，可以直接显示论文PDF" -ForegroundColor White
Write-Host "3. 请在浏览器中右键点击PDF，选择'另存为'保存到下载目录" -ForegroundColor White
Write-Host "4. 保存后，按Enter键继续下一篇论文" -ForegroundColor White
Write-Host "5. 如果无法下载，脚本会自动跳过并继续下一篇" -ForegroundColor White
Write-Host ""

foreach ($paper in $papers) {
    $ref = $paper.Ref
    $doi = $paper.DOI
    $fileName = $paper.FileName
    $sciHubUrl = "$sciHubBase$doi"
    
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    Write-Host "正在处理 [$ref]: $fileName" -ForegroundColor Yellow
    Write-Host "DOI: $doi" -ForegroundColor White
    Write-Host "Sci-Hub链接: $sciHubUrl" -ForegroundColor White
    Write-Host ""
    
    # 检查文件是否已存在
    $filePath = Join-Path $downloadDir $fileName
    if (Test-Path $filePath) {
        Write-Host "文件已存在，跳过: $fileName" -ForegroundColor Green
        continue
    }
    
    # 在浏览器中打开Sci-Hub链接
    Write-Host "正在打开浏览器..." -ForegroundColor Yellow
    Start-Process $sciHubUrl
    
    # 等待用户确认
    $response = Read-Host "论文已加载？已保存请按Enter，跳过请按s"
    
    if ($response -eq "s") {
        Write-Host "已跳过 [$ref]" -ForegroundColor Red
    } else {
        if (Test-Path $filePath) {
            Write-Host "下载成功: $fileName" -ForegroundColor Green
        } else {
            Write-Host "未检测到文件，可能未保存成功" -ForegroundColor Red
        }
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "所有论文处理完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下载目录内容：" -ForegroundColor Yellow
Get-ChildItem $downloadDir -Filter "*.pdf" | Select-Object Name | Format-Table -AutoSize
