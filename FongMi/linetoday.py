import requests
from bs4 import BeautifulSoup
import re
import json

def liveContent(live):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }

    # 1. 獲取 article_url，您需要從 live 中獲取這個 URL
    article_url = live.url  # 假設 live 物件有一個 url 屬性

    # 2. 解析文章頁面
    response = requests.get(article_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"無法訪問該頁面，狀態碼: {response.status_code}")
    
    # 3. 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 4. 尋找包含 __NUXT__ 的 script 標籤
    script_tag = soup.find("script", text=lambda t: t and "__NUXT__" in t)
    if not script_tag:
        raise Exception("找不到包含 __NUXT__ 的 script")
    
    # 5. 提取 script 中的 JSON 資料
    script_content = script_tag.string
    
    # 6. 使用正則表達式找到 broadcastId
    broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', script_content)
    if not broadcast_id_match:
        raise Exception("找不到 broadcastId")
    broadcast_id = broadcast_id_match.group(1)

    # 7. 構建 API 請求 URL 並獲取直播源
    api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
    api_response = requests.get(api_url, headers=headers)
    
    if api_response.status_code != 200:
        raise Exception(f"無法訪問 API，狀態碼: {api_response.status_code}")
    
    api_data = json.loads(api_response.text)

    # 8. 獲取 HLS URL (直播源)
    hls_url = api_data['hlsUrls']['abr']

    return hls_url  # 返回 HLS URL