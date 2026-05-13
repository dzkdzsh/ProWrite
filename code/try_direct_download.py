import requests
import os
from urllib.parse import urljoin

DOWNLOAD_DIR = r"D:\course\proWrite\papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 直接从官方/开放来源下载
papers = [
    {
        "name": "ref5",
        "filename": "Self-powered Sb2Te3-MoS2 photodetector.pdf",
        "url": "https://www.mdpi.com/2079-4991/13/13/1973/pdf?version=1688029587"
    },
    {
        "name": "ref4",
        "filename": "Moire-pattern Sb2Te3-graphene.pdf",
        "url": "https://link.springer.com/content/pdf/10.1007/s12274-021-3613-7.pdf"
    },
    {
        "name": "ref7",
        "filename": "Sb2Te3-Te van der Waals.pdf",
        "url": "https://www.sciencedirect.com/science/article/pii/S0017931024008326/pdfft"
    },
    {
        "name": "ref6",
        "filename": "Weak interlayer 1T-MoTe2-Sb2Te3.pdf",
        "url": "https://www.sciencedirect.com/science/article/pii/S0022459624002134/pdfft"
    },
    {
        "name": "ref8",
        "filename": "Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf",
        "url": "https://www.sciencedirect.com/science/article/pii/S0925838824003531/pdfft"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

session = requests.Session()
session.verify = False

for paper in papers:
    filepath = os.path.join(DOWNLOAD_DIR, paper['filename'])
    
    if os.path.exists(filepath):
        print(f"✓ 已存在: {paper['filename']}")
        continue
    
    print(f"\n尝试下载 {paper['name']}: {paper['url']}")
    
    try:
        resp = session.get(paper['url'], headers=headers, timeout=30)
        
        if resp.status_code == 200:
            if resp.content[:5] == b'%PDF-':
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                size = os.path.getsize(filepath) / 1024
                print(f"  ✓ 下载成功: {size:.1f} KB")
            else:
                print(f"  ✗ 响应不是PDF (前20字节: {resp.content[:20]})")
        else:
            print(f"  ✗ HTTP状态码: {resp.status_code}")
    except Exception as e:
        print(f"  ✗ 错误: {str(e)[:80]}")

print(f"\n{'='*60}")
print(f"下载完成!")
print(f"\n{DOWNLOAD_DIR} 中的PDF文件:")
for f in sorted(os.listdir(DOWNLOAD_DIR)):
    if f.endswith('.pdf'):
        path = os.path.join(DOWNLOAD_DIR, f)
        size = os.path.getsize(path) / 1024
        print(f"  {f} ({size:.1f} KB)")
