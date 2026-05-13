import requests
import re

url = "https://sci-hub.se/10.1016/j.vacuum.2018.12.017"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

resp = requests.get(url, headers=headers, timeout=20)
html = resp.text

# 保存HTML到本地查看结构
with open("d:/course/proWrite/scihub_page.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Status: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('Content-Type', '')}")
print(f"HTML length: {len(html)}")

# 查找所有可能的URL
print("\n=== 查找PDF相关链接 ===")
patterns = [
    r'src=["\']([^"\']+)["\']',
    r'href=["\']([^"\']+)["\']',
    r'location\.href[^"\']*=["\']([^"\']+)["\']',
    r'url\(["\']?([^"\')\s]+)["\']?',
]

for pat in patterns:
    matches = re.findall(pat, html, re.IGNORECASE)
    if matches:
        print(f"\nPattern: {pat[:30]}...")
        for m in matches[:10]:
            print(f"  {m}")
