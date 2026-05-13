import requests
import os

DOWNLOAD_DIR = r"D:\course\proWrite\papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

url = "https://sci-hub.jp/10.1016/j.vacuum.2018.12.017"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

print("尝试连接Sci-Hub...")

# 禁用SSL验证
session = requests.Session()
session.verify = False

try:
    resp = session.get(url, headers=headers, timeout=30)
    print(f"状态码: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
    print(f"响应长度: {len(resp.content)} bytes")
    
    # 检查前几个字节
    print(f"前20字节: {resp.content[:20]}")
    
    # 如果是PDF
    if resp.content[:5] == b'%PDF-':
        filepath = os.path.join(DOWNLOAD_DIR, "test.pdf")
        with open(filepath, 'wb') as f:
            f.write(resp.content)
        print(f"PDF已保存: {filepath}")
    else:
        # 保存HTML查看结构
        filepath = os.path.join(DOWNLOAD_DIR, "test.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(resp.text)
        print(f"HTML已保存: {filepath}")
        
        # 查找iframe
        import re
        iframes = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', resp.text)
        if iframes:
            print(f"\n找到iframe: {iframes[0]}")
            
            # 尝试下载iframe内容
            iframe_url = iframes[0]
            if not iframe_url.startswith('http'):
                iframe_url = "https://sci-hub.jp" + iframe_url
            print(f"iframe完整URL: {iframe_url}")
            
            resp2 = session.get(iframe_url, headers=headers, timeout=30)
            print(f"iframe状态码: {resp2.status_code}")
            print(f"iframe Content-Type: {resp2.headers.get('Content-Type', 'N/A')}")
            
            if resp2.content[:5] == b'%PDF-':
                filepath = os.path.join(DOWNLOAD_DIR, "test.pdf")
                with open(filepath, 'wb') as f:
                    f.write(resp2.content)
                print(f"PDF已保存!")
                
except Exception as e:
    print(f"错误: {e}")
