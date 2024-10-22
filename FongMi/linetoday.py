import requests
from bs4 import BeautifulSoup
import json

def liveContent(article_url):
    result = {"name": "LINE Today 直播", "url": "", "type": 1}  # type=1 表示 HLS URL

    try:
        # 取得文章ID
        article_id = article_url.split('/')[-1]

        # 構建API請求的URL
        api_url = f'https://today.line.me/tw/v2/article/{article_id}'

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
        hls_api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
        api_response = requests.get(hls_api_url)
        api_response.raise_for_status()  # 確保請求成功

        # 確認 response 內容
        if api_response.text:
            data = api_response.json()
            hls_url = data["hlsUrls"]["abr"]
            result["url"] = hls_url  # 將 HLS URL 填入結果

        else:
            raise Exception("API 回應的內容為空")

    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
        result["url"] = ""
    except Exception as e:
        print(f"處理過程中出現錯誤: {e}")
        result["url"] = ""

    # 返回 FongMi TV 所需的 JSON 格式
    return json.dumps([result], ensure_ascii=False)
