import requests
import re

def processArticle(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }

    # 發送請求到指定的文章 URL
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 檢查請求是否成功
    content = response.text  # 獲取文章的 HTML 內容

    # 使用正則表達式提取 broadcastId
    broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', content)
    if not broadcast_id_match:
        return "無法找到 broadcastId"

    broadcast_id = broadcast_id_match.group(1)

    # 呼叫 API 獲取 HLS URL
    api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
    api_response = requests.get(api_url, headers=headers)
    api_response.raise_for_status()  # 檢查 API 請求是否成功
    api_data = api_response.json()

    # 獲取 HLS URL
    hls_url = api_data.get('hlsUrls', {}).get('abr')
    if hls_url:
        return f"測試,{hls_url}"
    else:
        return "無法找到 HLS URL"

# 呼叫函數來處理指定的文章 URL
article_url = 'https://today.line.me/tw/v2/article/jggMBa'
result = processArticle(article_url)
print(result)
