import time
import os
import subprocess
import requests
import re

DOWNLOAD_DIR = r"D:\course\proWrite\papers"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

papers = [
    {"doi": "10.1007/s12274-021-3613-7", "filename": "Moire-pattern Sb2Te3-graphene.pdf"},
    {"doi": "10.3390/nano13131973", "filename": "Self-powered Sb2Te3-MoS2 photodetector.pdf"},
    {"doi": "10.1016/j.jssc.2024.124785", "filename": "Weak interlayer 1T-MoTe2-Sb2Te3.pdf"},
    {"doi": "10.1016/j.ijheatmasstransfer.2024.126479", "filename": "Sb2Te3-Te van der Waals.pdf"},
    {"doi": "10.1016/j.jallcom.2024.177313", "filename": "Anomalous thermoelectric AgSbTe2-Sb2Te3.pdf"},
]

# 尝试使用curl通过代理下载
print("正在尝试通过代理下载...\n")

for paper in papers:
    filepath = os.path.join(DOWNLOAD_DIR, paper['filename'])
    
    if os.path.exists(filepath):
        print(f"✓ 已存在: {paper['filename']}")
        continue
    
    print(f"\n尝试: {paper['doi']}")
    
    # 第一步: 获取Sci-Hub页面
    sciHubUrl = f"https://sci-hub.jp/{paper['doi']}"
    
    # 使用curl通过代理获取页面
    curlCmd = [
        'curl', '-k', '-s', '-L',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        sciHubUrl
    ]
    
    try:
        result = subprocess.run(curlCmd, capture_output=True, text=True, timeout=30)
        html = result.stdout
        
        if not html or len(html) < 100:
            print(f"  ✗ 页面获取失败")
            continue
        
        # 提取PDF链接
        match = re.search(r'<object[^>]+data\s*=\s*["\']([^"\']+\.pdf[^"\']*)["\']', html)
        if not match:
            match = re.search(r'<meta[^>]+name="citation_pdf_url"[^>]+content=["\']([^"\']+)["\']', html)
        if not match:
            match = re.search(r'href\s*=\s*["\'](/storage/[^"\']+\.pdf[^"\']*)["\']', html)
        
        if match:
            pdf_path = match.group(1)
            if pdf_path.startswith('/'):
                pdf_url = f"https://sci-hub.jp{pdf_path}"
            else:
                pdf_url = pdf_path
            
            print(f"  找到PDF: {pdf_url[:80]}...")
            
            # 下载PDF
            curlCmd2 = [
                'curl', '-k', '-s', '-L', '-o', filepath,
                '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                pdf_url
            ]
            
            result2 = subprocess.run(curlCmd2, capture_output=True, timeout=30)
            
            if os.path.exists(filepath):
                # 检查是否是PDF
                with open(filepath, 'rb') as f:
                    header = f.read(5)
                if header == b'%PDF-':
                    size = os.path.getsize(filepath) / 1024
                    print(f"  ✓ 下载成功: {size:.1f} KB")
                else:
                    print(f"  ✗ 下载的文件不是PDF")
                    os.remove(filepath)
            else:
                print(f"  ✗ 下载失败")
        else:
            print(f"  ✗ 未找到PDF链接")
            
    except subprocess.TimeoutExpired:
        print(f"  ✗ 请求超时")
    except Exception as e:
        print(f"  ✗ 错误: {str(e)[:80]}")
    
    time.sleep(2)

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
