import requests
import json
from bs4 import BeautifulSoup

def liveContent(article_url):
    # 取得文章ID
    article_id = article_url.split('/')[-1]

    # 構建API請求的URL
    api_url = f'https://today.line.me/tw/v2/article/{article_id}'
    
    try:
        # 發送GET請求
        response = requests.get(api_url)
        response.raise_for_status()  # 確保請求成功

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find("script", string=lambda text: text and "__NUXT__" in text)

        if script is None:
            raise Exception("找不到 script")

        script_data = script.string
        # 提取 broadcastId
        id_start = script_data.index("broadcastId:") + len("broadcastId:") + 1
        id_end = script_data.index("\"", id_start)
        broadcast_id = script_data[id_start:id_end]

        # 獲取 HLS URL
        api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
        api_response = requests.get(api_url)
        api_response.raise_for_status()  # 確保請求成功
        data = api_response.json()

        # 獲取 HLS URL
        hls_url = data["hlsUrls"]["abr"]
        return hls_url

    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
    except Exception as e:
        print(f"處理過程中出現錯誤: {e}")

    return None  # 若有錯誤，返回 None
