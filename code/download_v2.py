import requests
import re
import os
import time

DOWNLOAD_DIR = r"D:\course\proWrite\papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

papers = [
    {"doi": "10.1016/j.jallcom.2012.01.108", "filename": "Room-temperature MBE deposition Bi2Te3 Sb2Te3 thin films.pdf", "ref": "ref3"},
    {"doi": "10.1007/s12274-021-3613-7", "filename": "Moire-pattern Sb2Te3-graphene heterostructure.pdf", "ref": "ref4"},
    {"doi": "10.3390/nano13131973", "filename": "Self-powered Sb2Te3-MoS2 heterojunction photodetector.pdf", "ref": "ref5"},
    {"doi": "10.1016/j.jssc.2024.124785", "filename": "Weak interlayer interactions 1T-MoTe2-Sb2Te3.pdf", "ref": "ref6"},
    {"doi": "10.1016/j.ijheatmasstransfer.2024.126479", "filename": "Theoretical insights Sb2Te3-Te van der Waals.pdf", "ref": "ref7"},
    {"doi": "10.1016/j.jallcom.2024.177313", "filename": "Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf", "ref": "ref8"},
    {"doi": "10.1016/j.vacuum.2018.12.017", "filename": "Improved thermoelectric Sb2Te3-Cr bilayers.pdf", "ref": "ref9"},
    {"doi": "10.1016/j.spmi.2018.05.035", "filename": "Structural electronic optical GeTe-Sb2Te3 superlattices.pdf", "ref": "ref10"},
    {"doi": "10.1126/sciadv.aao1669", "filename": "Tailoring tricolor magnetic topological insulator axion.pdf", "ref": "ref11"},
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

success_count = 0
for paper in papers:
    filepath = os.path.join(DOWNLOAD_DIR, paper['filename'])
    if os.path.exists(filepath):
        print(f"✓ {paper['ref']} 已存在")
        success_count += 1
        continue
    
    print(f"\n尝试下载 {paper['ref']}...")
    
    # 尝试不同镜像
    for mirror in ["https://sci-hub.se/", "https://sci-hub.st/", "https://sci-hub.ru/"]:
        try:
            url = f"{mirror}{paper['doi']}"
            print(f"  使用: {mirror}")
            
            session = requests.Session()
            resp = session.get(url, headers=headers, timeout=15, allow_redirects=True)
            
            if resp.status_code == 200:
                # 检查是否是PDF
                if resp.content[:5] == b'%PDF-':
                    with open(filepath, 'wb') as f:
                        f.write(resp.content)
                    print(f"  ✓ 成功! {os.path.getsize(filepath)/1024:.1f} KB")
                    success_count += 1
                    break
                else:
                    # 提取PDF链接
                    html = resp.text
                    # 查找onclick或location中的URL
                    patterns = [
                        r"location\.href='([^']+)'",
                        r"location\.href=\"([^\"]+)\"",
                        r"<iframe[^>]+src='([^']+)'",
                        r"ajax\.post\('([^']+)'",
                    ]
                    for pat in patterns:
                        match = re.search(pat, html)
                        if match:
                            pdf_link = match.group(1)
                            if not pdf_link.startswith('http'):
                                # 尝试构造完整URL
                                from urllib.parse import urljoin
                                pdf_link = urljoin(mirror, pdf_link)
                            print(f"  找到链接: {pdf_link[:80]}...")
                            
                            # 尝试下载PDF
                            resp2 = session.get(pdf_link, headers=headers, timeout=15)
                            if resp2.status_code == 200 and resp2.content[:5] == b'%PDF-':
                                with open(filepath, 'wb') as f:
                                    f.write(resp2.content)
                                print(f"  ✓ 成功! {os.path.getsize(filepath)/1024:.1f} KB")
                                success_count += 1
                                break
                    else:
                        # 尝试直接查找任何URL
                        if 'captcha' in html.lower():
                            print(f"  ✗ 需要验证码")
                            break
            else:
                print(f"  ✗ 状态码: {resp.status_code}")
                
        except Exception as e:
            print(f"  ✗ 错误: {str(e)[:60]}")
            continue
    
    time.sleep(2)

print(f"\n{'='*50}")
print(f"下载完成! 成功: {success_count}/{len(papers)}")
