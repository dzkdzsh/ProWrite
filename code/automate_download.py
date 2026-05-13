from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

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

print("正在启动Edge浏览器...")

options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Edge(options=options)

try:
    for i, paper in enumerate(papers):
        filepath = os.path.join(DOWNLOAD_DIR, paper['filename'])
        
        if os.path.exists(filepath):
            print(f"[{i+1}/{len(papers)}] 已存在: {paper['filename']}")
            continue
        
        print(f"\n[{i+1}/{len(papers)}] 下载: {paper['doi']}")
        
        url = f"https://sci-hub.jp/{paper['doi']}"
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 尝试查找PDF元素
        try:
            # 检查是否有PDF iframe
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            iframe_src = iframe.get_attribute("src")
            print(f"  找到iframe: {iframe_src[:80]}")
            
            # 如果iframe有src，直接下载
            if iframe_src and 'pdf' in iframe_src.lower():
                driver.execute_script(f"window.open('{iframe_src}');")
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)
                
        except:
            pass
        
        # 尝试在页面中查找canvas（PDF渲染）
        try:
            canvases = driver.find_elements(By.TAG_NAME, "canvas")
            if canvases:
                print(f"  找到 {len(canvases)} 个canvas元素")
                # 使用JavaScript导出PDF
                driver.execute_script("""
                    var pdfData = document.querySelector('canvas').toDataURL('image/png');
                    return pdfData;
                """)
        except:
            pass
        
        print(f"  页面标题: {driver.title}")
        
        # 尝试获取当前页面的完整HTML，查找PDF链接
        page_source = driver.page_source
        
        # 查找所有链接
        import re
        links = re.findall(r'href=["\']([^"\']+)["\']', page_source)
        pdf_links = [l for l in links if '.pdf' in l.lower() or 'pdf' in l.lower()]
        
        if pdf_links:
            print(f"  找到PDF链接: {pdf_links[0][:80]}")
        
        time.sleep(2)
    
    print("\n下载完成!")
    
finally:
    driver.quit()
