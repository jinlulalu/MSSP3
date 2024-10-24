import requests
import re

def fetchLineToday(article_ids):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    
    results = []

    for article_id in article_ids:
        article_url = f"https://today.line.me/tw/v2/article/{article_id}"
        # 發送請求到指定的文章 URL
        response = requests.get(article_url, headers=headers)
        content = response.text  # 獲取文章的 HTML 內容

        # 使用正則表達式提取 broadcastId
        broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', content)
        broadcast_id = broadcast_id_match.group(1)

        # 呼叫 API 獲取 HLS URL
        api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
        api_response = requests.get(api_url, headers=headers)
        api_data = api_response.json()

        # 獲取 HLS URL 和標題
        hls_url = api_data.get('hlsUrls', {}).get('abr')
        hls_title = api_data.get('title')
        results.append(f"{hls_title},{hls_url}")
        
    return "\n".join(results)
 
# 主程式
if __name__ == "__main__":
    article_ids = ["jggMBa", "PNNoG5","9mPG2Rm"]
    text = fetchLineToday(article_ids)
    print(text)