import requests
import re

def liveContent(article_data):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    
    results = []  # 用於存儲所有的結果

    for title, article_url in article_data:
        # 發送請求到指定的文章 URL
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()  # 檢查請求是否成功
        content = response.text  # 獲取文章的 HTML 內容

        # 使用正則表達式提取 broadcastId
        broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', content)
        if not broadcast_id_match:
            results.append(f"錯誤-{title},{article_url}")  # 將錯誤信息添加到結果
            continue

        broadcast_id = broadcast_id_match.group(1)

        # 呼叫 API 獲取 HLS URL
        api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
        api_response = requests.get(api_url, headers=headers)
        api_response.raise_for_status()  # 檢查 API 請求是否成功
        api_data = api_response.json()

        # 獲取 HLS URL
        hls_url = api_data.get('hlsUrls', {}).get('abr')
        if hls_url:
            results.append(f"{title},{hls_url}")  # 將標題和 HLS URL 添加到結果
        else:
            results.append(f"錯誤-{title},{article_url}")  # 將錯誤信息添加到結果

    return results  # 返回所有的結果

# 主程式
if __name__ == "__main__":
    article_data = [
        ("TVBS新聞台", 'https://today.line.me/tw/v2/article/jggMBa'),
        ("民視新聞台", 'https://today.line.me/tw/v2/article/PNNoG5')  # 替換為其他實際的網址
    ]
    
    results = liveContent(article_data)

    # 打印所有獲得的結果
    #for result in results:
    #    print(result)