import requests
from bs4 import BeautifulSoup
import json
import re

def fetch_live_content(live, text):
    live_content = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }

    for group in text['groups']:
        group_name = group['name']
        group_data = {
            "name": group_name,
            "channels": []
        }

        for channel in group['channels']:
            article_url = channel['urls'][0]  # 使用第一個 URL
            article_name = channel['name']

            # 發送請求並解析網頁內容
            try:
                response = requests.get(article_url, headers=headers)
                response.raise_for_status()  # 檢查是否成功
            except requests.RequestException as e:
                print(f"Error fetching {article_url}: {e}")
                continue  # 跳過該 channel

            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找 broadcastId
            script_tag = soup.find("script", text=lambda t: t and "__NUXT__" in t)
            if script_tag is None:
                print(f"No script tag with __NUXT__ found for {article_name}")
                continue  # 跳過該 channel

            broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', script_tag.string)
            if broadcast_id_match is None:
                print(f"No broadcastId found for {article_name}")
                continue  # 跳過該 channel
            broadcast_id = broadcast_id_match.group(1)

            # 使用 broadcastId 獲取 HLS URL
            api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
            try:
                api_response = requests.get(api_url, headers=headers)
                api_response.raise_for_status()  # 檢查是否成功
            except requests.RequestException as e:
                print(f"Error fetching API data for broadcastId {broadcast_id}: {e}")
                continue  # 跳過該 channel

            api_data = api_response.json()

            # 確認 'hlsUrls' 和 'abr' 是否存在
            if 'hlsUrls' not in api_data or 'abr' not in api_data['hlsUrls']:
                print(f"HLS URL not found for {article_name}")
                continue  # 跳過該 channel

            hls_url = api_data['hlsUrls']['abr']

            # 添加頻道的名稱和 HLS URL 到當前 group 的 channels 列表中
            group_data['channels'].append({
                "name": article_name,
                "urls": [hls_url]
            })

        # 添加完整的 group 到 live_content
        live_content.append(group_data)

    return live_content