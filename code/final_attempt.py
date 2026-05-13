import requests
import os

DOWNLOAD_DIR = r"D:\course\proWrite\papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 这些论文被Sci-Hub封锁了，需要验证码
# 尝试从其他来源下载

papers = [
    {
        "name": "ref5",
        "filename": "Self-powered Sb2Te3-MoS2 photodetector.pdf",
        "urls": [
            "https://www.mdpi.com/2079-4991/13/13/1973/pdf",
            "https://pubmed.ncbi.nlm.nih.gov/37446483/",  # PMC免费
        ]
    },
    {
        "name": "ref4",
        "filename": "Moire-pattern Sb2Te3-graphene.pdf",
        "urls": [
            "https://link.springer.com/content/pdf/10.1007/s12274-021-3613-7.pdf",
        ]
    },
    {
        "name": "ref6",
        "filename": "Weak interlayer 1T-MoTe2-Sb2Te3.pdf",
        "urls": [
            "https://www.sciencedirect.com/science/article/pii/S0022459624002134/pdfft",
        ]
    },
    {
        "name": "ref7",
        "filename": "Sb2Te3-Te van der Waals.pdf",
        "urls": [
            "https://www.sciencedirect.com/science/article/pii/S0017931024008326/pdfft",
        ]
    },
    {
        "name": "ref8",
        "filename": "Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf",
        "urls": [
            "https://www.sciencedirect.com/science/article/pii/S0925838824003531/pdfft",
        ]
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# 使用系统代理设置（你的浏览器使用的代理）
session = requests.Session()
session.trust_env = True  # 使用环境变量中的代理设置

for paper in papers:
    filepath = os.path.join(DOWNLOAD_DIR, paper['filename'])
    
    if os.path.exists(filepath):
        print(f"✓ 已存在: {paper['filename']}")
        continue
    
    print(f"\n尝试下载 {paper['name']}...")
    
    for url in paper['urls']:
        try:
            print(f"  URL: {url}")
            resp = session.get(url, headers=headers, timeout=30, allow_redirects=True)
            
            print(f"  状态码: {resp.status_code}")
            print(f"  Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
            
            if resp.status_code == 200:
                if resp.content[:5] == b'%PDF-':
                    with open(filepath, 'wb') as f:
                        f.write(resp.content)
                    size = os.path.getsize(filepath) / 1024
                    print(f"  ✓ 下载成功: {size:.1f} KB")
                    break
                else:
                    print(f"  ✗ 不是PDF")
            else:
                print(f"  ✗ 状态码不正确")
        except Exception as e:
            print(f"  ✗ 错误: {str(e)[:60]}")

print(f"\n{'='*60}")
print(f"下载完成!")
print(f"\n{DOWNLOAD_DIR} 中的PDF文件:")
count = 0
for f in sorted(os.listdir(DOWNLOAD_DIR)):
    if f.endswith('.pdf'):
        path = os.path.join(DOWNLOAD_DIR, f)
        size = os.path.getsize(path) / 1024
        print(f"  {f} ({size:.1f} KB)")
        count += 1
print(f"\n总计: {count} 篇PDF")
