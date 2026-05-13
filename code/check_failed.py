import requests
import re
import os

DOWNLOAD_DIR = r"D:\course\proWrite\papers"

papers = [
    {"doi": "10.1007/s12274-021-3613-7", "name": "ref4"},
    {"doi": "10.3390/nano13131973", "name": "ref5"},
    {"doi": "10.1016/j.jssc.2024.124785", "name": "ref6"},
    {"doi": "10.1016/j.ijheatmasstransfer.2024.126479", "name": "ref7"},
    {"doi": "10.1016/j.jallcom.2024.177313", "name": "ref8"},
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

session = requests.Session()
session.verify = False

for paper in papers:
    print(f"\n{'='*60}")
    print(f"检查: {paper['name']} - {paper['doi']}")
    
    url = f"https://sci-hub.jp/{paper['doi']}"
    resp = session.get(url, headers=headers, timeout=30)
    html = resp.text
    
    # 保存HTML以便分析
    html_file = os.path.join(DOWNLOAD_DIR, f"{paper['name']}_page.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML长度: {len(html)}")
    
    # 查找所有可能的PDF链接
    patterns = [
        (r'<meta[^>]+name="citation_pdf_url"[^>]+content=["\']([^"\']+)["\']', "citation_pdf_url"),
        (r'<object[^>]+data\s*=\s*["\']([^"\']+\.pdf[^"\']*)["\']', "object.data"),
        (r'<iframe[^>]+src\s*=\s*["\']([^"\']+\.pdf[^"\']*)["\']', "iframe.src"),
        (r'href\s*=\s*["\'](/storage/[^"\']+\.pdf[^"\']*)["\']', "a.href"),
        (r'url\s*\(\s*["\']?([^"\')\s]+\.pdf[^"\')\s]*)["\']?\s*\)', "url()"),
        (r'"pdfUrl"\s*:\s*["\']([^"\']+)["\']', "pdfUrl"),
        (r'var\s+pdfUrl\s*=\s*["\']([^"\']+)["\']', "var pdfUrl"),
    ]
    
    found = False
    for pattern, name in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            pdf_path = match.group(1)
            if pdf_path.startswith('/'):
                pdf_url = f"https://sci-hub.jp{pdf_path}"
            else:
                pdf_url = pdf_path
            print(f"  找到 [{name}]: {pdf_url[:100]}")
            found = True
    
    if not found:
        # 查找所有包含/storage/的链接
        storage_links = re.findall(r'["\'](/storage/[^"\']+)["\']', html)
        if storage_links:
            print(f"  找到 {len(storage_links)} 个/storage/链接:")
            for link in storage_links[:5]:
                print(f"    {link[:80]}")
        else:
            print("  ✗ 未找到任何PDF链接")
            # 查看页面内容关键词
            if 'captcha' in html.lower():
                print("  ⚠ 检测到验证码!")
            if 'block' in html.lower():
                print("  ⚠ 可能被封锁")
