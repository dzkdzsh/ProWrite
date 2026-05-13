import requests
import re
import os
import time
from urllib.parse import urljoin, unquote

DOWNLOAD_DIR = r"D:\course\proWrite\papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

papers = [
    {"doi": "10.1016/j.jallcom.2012.01.108", "filename": "Room-temperature MBE deposition Bi2Te3 Sb2Te3.pdf"},
    {"doi": "10.1007/s12274-021-3613-7", "filename": "Moire-pattern Sb2Te3-graphene.pdf"},
    {"doi": "10.3390/nano13131973", "filename": "Self-powered Sb2Te3-MoS2 photodetector.pdf"},
    {"doi": "10.1016/j.jssc.2024.124785", "filename": "Weak interlayer 1T-MoTe2-Sb2Te3.pdf"},
    {"doi": "10.1016/j.ijheatmasstransfer.2024.126479", "filename": "Sb2Te3-Te van der Waals.pdf"},
    {"doi": "10.1016/j.jallcom.2024.177313", "filename": "Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf"},
    {"doi": "10.1016/j.vacuum.2018.12.017", "filename": "Improved Sb2Te3-Cr bilayers.pdf"},
    {"doi": "10.1016/j.spmi.2018.05.035", "filename": "GeTe-Sb2Te3 superlattices.pdf"},
    {"doi": "10.1126/sciadv.aao1669", "filename": "Tailoring tricolor magnetic topological insulator.pdf"},
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def download_paper(doi, filename):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"✓ 已存在: {filename}")
        return True
    
    mirrors = [
        "https://sci-hub.se/",
        "https://sci-hub.st/",
        "https://sci-hub.ru/",
    ]
    
    for mirror in mirrors:
        try:
            print(f"尝试 {mirror}{doi}")
            session = requests.Session()
            
            # 第一步: 获取Sci-Hub页面
            resp = session.get(f"{mirror}{doi}", headers=headers, timeout=20, allow_redirects=True)
            
            if resp.status_code != 200:
                print(f"  状态码: {resp.status_code}")
                continue
            
            html = resp.text
            
            # 尝试从HTML中提取PDF链接
            # Sci-Hub通常在iframe或onclick中嵌入PDF URL
            patterns = [
                r'<iframe[^>]+src=["\']([^"\']+)["\']',
                r'id="pdf"[^>]+src=["\']([^"\']+)["\']',
                r'location\.href\s*=\s*["\']([^"\']+)["\']',
                r'ajax\.post\(["\']([^"\']+)["\']',
                r'downloadFile\(["\']([^"\']+)["\']',
                r'window\.open\(["\']([^"\']+)["\']',
            ]
            
            pdf_url = None
            for pattern in patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    pdf_url = match.group(1)
                    if not pdf_url.startswith('http'):
                        pdf_url = urljoin(mirror, pdf_url)
                    break
            
            if not pdf_url:
                # 尝试查找所有链接
                links = re.findall(r'href=["\']([^"\']+)["\']', html)
                for link in links:
                    if '.pdf' in link.lower() or 'pdf' in link.lower():
                        pdf_url = urljoin(mirror, link)
                        break
            
            if pdf_url:
                print(f"  找到PDF链接: {pdf_url[:80]}...")
                
                # 下载PDF
                resp2 = session.get(pdf_url, headers=headers, timeout=30)
                
                if resp2.status_code == 200:
                    content = resp2.content
                    if content[:5] == b'%PDF-':
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        size = os.path.getsize(filepath) / 1024
                        print(f"✓ 下载成功: {size:.1f} KB")
                        return True
                    else:
                        print(f"  内容不是PDF")
                else:
                    print(f"  PDF请求失败: {resp2.status_code}")
            else:
                print(f"  未找到PDF链接")
                
        except Exception as e:
            print(f"  错误: {str(e)[:80]}")
            continue
    
    return False

success = 0
for i, paper in enumerate(papers):
    print(f"\n[{i+1}/{len(papers)}] 下载: {paper['filename']}")
    if download_paper(paper['doi'], paper['filename']):
        success += 1
    time.sleep(3)

print(f"\n{'='*50}")
print(f"完成! 成功: {success}/{len(papers)}")
print(f"\n{DOWNLOAD_DIR} 中的文件:")
for f in sorted(os.listdir(DOWNLOAD_DIR)):
    if f.endswith('.pdf'):
        size = os.path.getsize(os.path.join(DOWNLOAD_DIR, f)) / 1024
        print(f"  {f} ({size:.1f} KB)")
