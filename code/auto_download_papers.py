import requests
import os
import time
import re

# 配置
DOWNLOAD_DIR = r"D:\course\proWrite\papers"

# 论文列表
papers = [
    {
        "doi": "10.1016/j.jallcom.2012.01.108",
        "filename": "Room-temperature MBE deposition thermoelectric properties Bi2Te3 Sb2Te3 thin films.pdf",
        "ref": "ref3"
    },
    {
        "doi": "10.1007/s12274-021-3613-7",
        "filename": "Moire-pattern-modulated electronic structures Sb2Te3-graphene heterostructure.pdf",
        "ref": "ref4"
    },
    {
        "doi": "10.3390/nano13131973",
        "filename": "Self-powered Sb2Te3-MoS2 heterojunction broadband photodetector.pdf",
        "ref": "ref5"
    },
    {
        "doi": "10.1016/j.jssc.2024.124785",
        "filename": "Weak interlayer interactions 1T-MoTe2-Sb2Te3 superlattice-like films.pdf",
        "ref": "ref6"
    },
    {
        "doi": "10.1016/j.ijheatmasstransfer.2024.126479",
        "filename": "Theoretical insights Sb2Te3-Te van der Waals heterostructures.pdf",
        "ref": "ref7"
    },
    {
        "doi": "10.1016/j.jallcom.2024.177313",
        "filename": "Anomalous thermoelectric nature disordered AgSbTe2-Sb2Te3 hetero-phase alloys.pdf",
        "ref": "ref8"
    },
    {
        "doi": "10.1016/j.vacuum.2018.12.017",
        "filename": "Improved thermoelectric performances nanocrystalline Sb2Te3-Cr bilayers.pdf",
        "ref": "ref9"
    },
    {
        "doi": "10.1016/j.spmi.2018.05.035",
        "filename": "Structural electronic optical properties GeTe-Sb2Te3 superlattices.pdf",
        "ref": "ref10"
    },
    {
        "doi": "10.1126/sciadv.aao1669",
        "filename": "Tailoring tricolor structure magnetic topological insulator axion insulator.pdf",
        "ref": "ref11"
    }
]

def download_from_scihub(doi, filename, ref):
    """从Sci-Hub下载论文"""
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"✓ [{ref}] 已存在，跳过")
        return True
    
    # 尝试多个Sci-Hub镜像
    mirrors = [
        "https://sci-hub.jp/",
        "https://sci-hub.se/",
        "https://sci-hub.ru/",
        "https://sci-hub.st/"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    for mirror in mirrors:
        try:
            print(f"  尝试镜像: {mirror}")
            url = f"{mirror}{doi}"
            
            # 第一步：获取页面
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=20, allow_redirects=True)
            
            if response.status_code == 200:
                # 检查是否是PDF
                content_type = response.headers.get('Content-Type', '')
                
                if 'application/pdf' in content_type or response.content[:4] == b'%PDF':
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    file_size = os.path.getsize(filepath)
                    print(f"✓ [{ref}] 下载成功: {file_size/1024:.1f} KB")
                    return True
                else:
                    # 尝试从HTML中提取PDF链接
                    html_content = response.text
                    
                    # 查找iframe或embed标签中的PDF链接
                    pdf_patterns = [
                        r'<iframe[^>]+src=["\']([^"\']+\.pdf[^"\']*)["\']',
                        r'<embed[^>]+src=["\']([^"\']+\.pdf[^"\']*)["\']',
                        r'location\.href\s*=\s*["\']([^"\']+\.pdf[^"\']*)["\']',
                    ]
                    
                    for pattern in pdf_patterns:
                        match = re.search(pattern, html_content)
                        if match:
                            pdf_url = match.group(1)
                            if not pdf_url.startswith('http'):
                                pdf_url = mirror.rstrip('/') + pdf_url
                            
                            print(f"  找到PDF链接: {pdf_url}")
                            pdf_response = session.get(pdf_url, headers=headers, timeout=20)
                            
                            if pdf_response.status_code == 200:
                                with open(filepath, 'wb') as f:
                                    f.write(pdf_response.content)
                                file_size = os.path.getsize(filepath)
                                print(f"✓ [{ref}] 下载成功: {file_size/1024:.1f} KB")
                                return True
                    
                    print(f"  ✗ 页面不是PDF，无法提取下载链接")
                    return False
            else:
                print(f"  ✗ 状态码: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"  ✗ 超时")
            continue
        except Exception as e:
            print(f"  ✗ 错误: {str(e)[:50]}")
            continue
    
    return False

def main():
    print("="*70)
    print("Sci-Hub 论文自动下载工具")
    print("="*70)
    print(f"下载目录: {DOWNLOAD_DIR}\n")
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    success = 0
    failed = 0
    
    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] 下载 {paper['ref']}...")
        
        result = download_from_scihub(
            paper['doi'],
            paper['filename'],
            paper['ref']
        )
        
        if result:
            success += 1
        else:
            failed += 1
        
        # 请求间隔
        if i < len(papers):
            time.sleep(3)
    
    # 统计
    print("\n" + "="*70)
    print("下载完成！")
    print("="*70)
    print(f"成功: {success}")
    print(f"失败/跳过: {failed}")
    
    # 列出所有PDF
    print(f"\n{DOWNLOAD_DIR} 中的PDF文件:")
    pdfs = sorted([f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.pdf')])
    for i, pdf in enumerate(pdfs, 1):
        size = os.path.getsize(os.path.join(DOWNLOAD_DIR, pdf))
        print(f"  {i}. {pdf} ({size/1024:.1f} KB)")

if __name__ == "__main__":
    main()
