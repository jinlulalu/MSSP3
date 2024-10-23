import requests
from bs4 import BeautifulSoup
import re
import json

def liveContent(article_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }

    response = requests.get(article_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"無法訪問該頁面，狀態碼: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    script_tag = soup.find("script", text=lambda t: t and "__NUXT__" in t)
    if not script_tag:
        raise Exception("找不到包含 __NUXT__ 的 script")
    
    script_content = script_tag.string
    
    broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', script_content)
    if not broadcast_id_match:
        raise Exception("找不到 broadcastId")
    broadcast_id = broadcast_id_match.group(1)

    api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
    api_response = requests.get(api_url, headers=headers)
    
    if api_response.status_code != 200:
        raise Exception(f"無法訪問 API，狀態碼: {api_response.status_code}")
    
    api_data = json.loads(api_response.text)

    # 檢查 api_data 是否包含 hlsUrls
    if 'hlsUrls' not in api_data or 'abr' not in api_data['hlsUrls']:
        raise Exception("無法找到 HLS URL")

    hls_url = api_data['hlsUrls']['abr']
    return hls_url