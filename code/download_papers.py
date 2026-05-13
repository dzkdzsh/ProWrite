import requests
import os
import time
from urllib.parse import quote

# 配置
DOWNLOAD_DIR = r"D:\course\proWrite\papers"
SCIHUB_BASE = "https://sci-hub.jp/"

# 论文列表 (DOI, 文件名)
# ref3-ref11需要下载
papers = [
    {
        "doi": "10.1016/j.jallcom.2012.01.108",
        "filename": "Room-temperature MBE deposition thermoelectric properties and advanced structural characterization of binary Bi2Te3 and Sb2Te3 thin films.pdf",
        "ref": "ref3",
        "title": "Room-temperature MBE deposition, thermoelectric properties, and advanced structural characterization of binary Bi2Te3 and Sb2Te3 thin films"
    },
    {
        "doi": "10.1007/s12274-021-3613-7",
        "filename": "Moire-pattern-modulated electronic structures in Sb2Te3-graphene heterostructure.pdf",
        "ref": "ref4",
        "title": "Moiré-pattern-modulated electronic structures in Sb2Te3/graphene heterostructure"
    },
    {
        "doi": "10.3390/nano13131973",
        "filename": "Self-powered Sb2Te3-MoS2 heterojunction broadband photodetector on flexible substrate.pdf",
        "ref": "ref5",
        "title": "Self-powered Sb2Te3/MoS2 heterojunction broadband photodetector on flexible substrate"
    },
    {
        "doi": "10.1016/j.jssc.2024.124785",
        "filename": "Weak interlayer interactions and nearly temperature independent electrical transport in p-type 1T-MoTe2-Sb2Te3 superlattice-like films.pdf",
        "ref": "ref6",
        "title": "Weak interlayer interactions and nearly temperature independent electrical transport in p-type 1T'-MoTe2/Sb2Te3 superlattice-like films"
    },
    {
        "doi": "10.1016/j.ijheatmasstransfer.2024.126479",
        "filename": "Theoretical insights into Sb2Te3-Te van der Waals heterostructures.pdf",
        "ref": "ref7",
        "title": "Theoretical insights into Sb2Te3/Te van der Waals heterostructures for achieving very high figure of merit and conversion efficiency"
    },
    {
        "doi": "10.1016/j.jallcom.2024.177313",
        "filename": "Anomalous thermoelectric nature in disordered AgSbTe2-Sb2Te3 hetero-phase alloys.pdf",
        "ref": "ref8",
        "title": "Anomalous thermoelectric nature in disordered AgSbTe2-Sb2Te3 hetero-phase alloys for room temperature applications"
    },
    {
        "doi": "10.1016/j.vacuum.2018.12.017",
        "filename": "Improved thermoelectric performances of nanocrystalline Sb2Te3-Cr bilayers.pdf",
        "ref": "ref9",
        "title": "Improved thermoelectric performances of nanocrystalline Sb2Te3/Cr bilayers by reducing thermal conductivity in the grain boundaries and heterostructure interface"
    },
    {
        "doi": "10.1016/j.spmi.2018.05.035",
        "filename": "Structural electronic and optical properties of GeTe-Sb2Te3 superlattices.pdf",
        "ref": "ref10",
        "title": "Structural, electronic and optical properties of GeTe/Sb2Te3 superlattices: a first-principles study"
    },
    {
        "doi": "10.1126/sciadv.aao1669",
        "filename": "Tailoring tricolor structure of magnetic topological insulator for robust axion insulator.pdf",
        "ref": "ref11",
        "title": "Tailoring tricolor structure of magnetic topological insulator for robust axion insulator"
    }
]

def download_paper(doi, filename, ref, title):
    """下载单篇论文"""
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    # 检查是否已存在
    if os.path.exists(filepath):
        print(f"✓ [{ref}] 文件已存在，跳过: {filename}")
        return True
    
    print(f"\n{'='*60}")
    print(f"正在下载 [{ref}]: {title}")
    print(f"DOI: {doi}")
    
    try:
        # 访问Sci-Hub
        url = f"{SCIHUB_BASE}{doi}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # 检查返回的是PDF还是HTML页面
            content_type = response.headers.get('Content-Type', '')
            
            if 'pdf' in content_type.lower():
                # 直接是PDF
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✓ [{ref}] 下载成功: {filename}")
                return True
            else:
                print(f"✗ [{ref}] 无法直接下载，需要手动保存")
                print(f"  请在浏览器中打开: {url}")
                return False
        else:
            print(f"✗ [{ref}] 下载失败，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"✗ [{ref}] 请求超时")
        return False
    except Exception as e:
        print(f"✗ [{ref}] 错误: {str(e)}")
        return False

def main():
    print("="*60)
    print("Sci-Hub 论文下载程序")
    print("="*60)
    print(f"下载目录: {DOWNLOAD_DIR}\n")
    
    # 确保下载目录存在
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for paper in papers:
        result = download_paper(
            paper["doi"],
            paper["filename"],
            paper["ref"],
            paper["title"]
        )
        
        if result:
            success_count += 1
        else:
            fail_count += 1
        
        # 避免请求过快
        time.sleep(2)
    
    # 统计结果
    print("\n" + "="*60)
    print("下载完成统计")
    print("="*60)
    print(f"成功: {success_count}")
    print(f"失败/需手动下载: {fail_count}")
    
    # 列出目录中的所有PDF
    print(f"\n{DOWNLOAD_DIR} 中的PDF文件:")
    pdf_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.pdf')]
    for i, f in enumerate(pdf_files, 1):
        print(f"  {i}. {f}")

if __name__ == "__main__":
    main()
