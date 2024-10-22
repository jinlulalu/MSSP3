import requests
from bs4 import BeautifulSoup

def liveContent(article_url):
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
        api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
        api_response = requests.get(api_url)
        api_response.raise_for_status()  # 確保請求成功

        # 確認 response 內容
        if api_response.text:
            data = api_response.json()
            hls_url = data["hlsUrls"]["abr"]
            return hls_url
        else:
            raise Exception("API 回應的內容為空")

    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
    except Exception as e:
        print(f"處理過程中出現錯誤: {e}")

    # 若有錯誤，返回 None
    return None
