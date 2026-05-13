import requests
import re
import os

DOWNLOAD_DIR = r"D:\course\proWrite\papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

papers = [
    {"doi": "10.1007/s12274-021-3613-7", "filename": "Moire-pattern Sb2Te3-graphene.pdf"},
    {"doi": "10.3390/nano13131973", "filename": "Self-powered Sb2Te3-MoS2 photodetector.pdf"},
    {"doi": "10.1016/j.jssc.2024.124785", "filename": "Weak interlayer 1T-MoTe2-Sb2Te3.pdf"},
    {"doi": "10.1016/j.ijheatmasstransfer.2024.126479", "filename": "Sb2Te3-Te van der Waals.pdf"},
    {"doi": "10.1016/j.jallcom.2024.177313", "filename": "Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf"},
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# 尝试多个Sci-Hub镜像
mirrors = [
    "https://sci-hub.st/",
    "https://sci-hub.ru/",
    "https://sci-hub.se/",
]

def extract_pdf_link(html, mirror_base):
    """提取PDF链接"""
    patterns = [
        r'<meta[^>]+name="citation_pdf_url"[^>]+content=["\']([^"\']+)["\']',
        r'<object[^>]+data\s*=\s*["\']([^"\']+\.pdf[^"\']*)["\']',
        r'href\s*=\s*["\'](/storage/[^"\']+\.pdf[^"\']*)["\']',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            path = match.group(1)
            if path.startswith('/'):
                return mirror_base.rstrip('/') + path
            return path
    return None

session = requests.Session()
session.verify = False

for paper in papers:
    filepath = os.path.join(DOWNLOAD_DIR, paper['filename'])
    
    if os.path.exists(filepath):
        print(f"✓ 已存在: {paper['filename']}")
        continue
    
    print(f"\n{'='*60}")
    print(f"DOI: {paper['doi']}")
    
    downloaded = False
    for mirror in mirrors:
        try:
            print(f"\n  尝试镜像: {mirror}")
            url = f"{mirror}{paper['doi']}"
            
            resp = session.get(url, headers=headers, timeout=30)
            
            if resp.status_code != 200:
                print(f"    状态码: {resp.status_code}")
                continue
            
            html = resp.text
            print(f"    HTML长度: {len(html)}")
            
            # 检查是否被封锁
            if 'block' in html.lower() or 'captcha' in html.lower():
                print(f"    ⚠ 需要验证码或被封锁")
                continue
            
            # 提取PDF链接
            pdf_url = extract_pdf_link(html, mirror)
            
            if pdf_url:
                print(f"    找到PDF: {pdf_url[:100]}")
                
                # 下载PDF
                pdf_resp = session.get(pdf_url, headers=headers, timeout=60)
                
                if pdf_resp.status_code == 200 and pdf_resp.content[:5] == b'%PDF-':
                    with open(filepath, 'wb') as f:
                        f.write(pdf_resp.content)
                    size = os.path.getsize(filepath) / 1024
                    print(f"    ✓ 下载成功: {size:.1f} KB")
                    downloaded = True
                    break
                else:
                    print(f"    ✗ PDF下载失败")
            else:
                print(f"    ✗ 未找到PDF链接")
                
        except Exception as e:
            print(f"    ✗ 错误: {str(e)[:80]}")
            continue
    
    if not downloaded:
        print(f"  ✗ 所有镜像都无法下载")

print(f"\n{'='*60}")
print(f"下载完成!")
print(f"\n{DOWNLOAD_DIR} 中的PDF文件:")
for f in sorted(os.listdir(DOWNLOAD_DIR)):
    if f.endswith('.pdf'):
        path = os.path.join(DOWNLOAD_DIR, f)
        size = os.path.getsize(path) / 1024
        print(f"  {f} ({size:.1f} KB)")
