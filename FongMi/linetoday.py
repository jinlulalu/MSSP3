import requests
from bs4 import BeautifulSoup
import json

def liveContent(api_url):
    try:
        # 發送 GET 請求以獲取文章數據
        response = requests.get(api_url)
        response.raise_for_status()  # 確保請求成功

        # 解析 HTML 內容
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find("script", string=lambda text: text and "__NUXT__" in text)

        if script is None:
            raise Exception("找不到 script")

        # 提取 broadcastId
        script_data = script.string
        id_start = script_data.index("broadcastId:") + len("broadcastId:") + 1
        id_end = script_data.index("\"", id_start)
        broadcast_id = script_data[id_start:id_end]

        # 獲取 HLS URL
        hls_api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
        api_response = requests.get(hls_api_url)
        api_response.raise_for_status()  # 確保請求成功

        # 確認 API 回應內容
        if api_response.text:
            data = api_response.json()
            hls_url = data["hlsUrls"]["abr"]
            
            # 構建 FongMi TV 所需的結果格式
            result = {
                "name": "LINE Today 直播",
                "url": hls_url,
                "type": 1  # type=1 表示 HLS URL
            }
            return json.dumps([result], ensure_ascii=False)  # 返回 JSON 格式結果
            
        else:
            raise Exception("API 回應的內容為空")

    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
    except Exception as e:
        print(f"處理過程中出現錯誤: {e}")

    # 若有錯誤，返回 None
    return None

