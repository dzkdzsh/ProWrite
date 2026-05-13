import requests
import re
import os
from urllib.parse import urljoin

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
}

session = requests.Session()
session.verify = False  # Sci-Hub可能有SSL问题

def extract_pdf_url(html):
    """从Sci-Hub HTML中提取PDF直接链接"""
    # 方法1: 从object标签的data属性
    match = re.search(r'<object[^>]+data\s*=\s*["\']([^"\']+)["\']', html)
    if match:
        return match.group(1)
    
    # 方法2: 从citation_pdf_url meta标签
    match = re.search(r'<meta[^>]+name="citation_pdf_url"[^>]+content=["\']([^"\']+)["\']', html)
    if match:
        return match.group(1)
    
    # 方法3: 从download链接
    match = re.search(r'<a\s+href\s*=\s*["\'](/storage/[^"\']+\.pdf)["\']', html)
    if match:
        return match.group(1)
    
    return None

def download_paper(doi, filename):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"✓ [{doi}] 已存在: {filename}")
        return True
    
    print(f"\n正在下载: {doi}")
    
    # 第一步: 获取Sci-Hub页面
    url = f"https://sci-hub.jp/{doi}"
    resp = session.get(url, headers=headers, timeout=30)
    
    if resp.status_code != 200:
        print(f"  ✗ 页面请求失败: {resp.status_code}")
        return False
    
    # 第二步: 提取PDF直接链接
    pdf_path = extract_pdf_url(resp.text)
    
    if not pdf_path:
        print(f"  ✗ 未找到PDF链接")
        return False
    
    # 构建完整的PDF URL
    if pdf_path.startswith('/'):
        pdf_url = f"https://sci-hub.jp{pdf_path}"
    else:
        pdf_url = pdf_path
    
    print(f"  PDF URL: {pdf_url}")
    
    # 第三步: 直接下载PDF
    pdf_resp = session.get(pdf_url, headers=headers, timeout=60)
    
    if pdf_resp.status_code == 200:
        # 验证是否为PDF
        if pdf_resp.content[:5] == b'%PDF-':
            with open(filepath, 'wb') as f:
                f.write(pdf_resp.content)
            
            size = os.path.getsize(filepath) / 1024
            print(f"  ✓ 下载成功: {size:.1f} KB")
            return True
        else:
            print(f"  ✗ 下载的内容不是PDF")
            return False
    else:
        print(f"  ✗ PDF下载失败: {pdf_resp.status_code}")
        return False

success = 0
for paper in papers:
    if download_paper(paper['doi'], paper['filename']):
        success += 1

print(f"\n{'='*60}")
print(f"下载完成! 成功: {success}/{len(papers)}")
print(f"\n{DOWNLOAD_DIR} 中的PDF文件:")

for f in sorted(os.listdir(DOWNLOAD_DIR)):
    if f.endswith('.pdf'):
        path = os.path.join(DOWNLOAD_DIR, f)
        size = os.path.getsize(path) / 1024
        print(f"  {f} ({size:.1f} KB)")
