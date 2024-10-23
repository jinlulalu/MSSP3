import requests
from bs4 import BeautifulSoup
import re

def fetch_live_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }

    # 發送請求並解析網頁內容
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 檢查請求是否成功

    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找 broadcastId
    script_tag = soup.find("script", text=lambda t: t and "__NUXT__" in t)
    broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', script_tag.string)
    if not broadcast_id_match:
        return None  # 若找不到 broadcastId，返回 None
    broadcast_id = broadcast_id_match.group(1)

    # 使用 broadcastId 獲取 HLS URL
    api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
    api_response = requests.get(api_url, headers=headers)
    api_data = api_response.json()

    hls_url = api_data['hlsUrls']['abr']

    return hls_url  # 返回 HLS URL

def process_text(text):
    class Group:
        def __init__(self, name):
            self.name = name
            self.channels = []

        @staticmethod
        def create(name):
            return Group(name)

        def find(self, channel):
            for ch in self.channels:
                if ch.name == channel.name:
                    return ch
            self.channels.append(channel)
            return channel

    class Channel:
        def __init__(self, name):
            self.name = name
            self.urls = []

        @staticmethod
        def create(name):
            return Channel(name)

        def add_urls(self, urls):
            self.urls.extend(urls)

    class Live:
        def __init__(self):
            self.groups = []

        def get_groups(self):
            return self.groups

        def is_pass(self):
            return True

    class Setting:
        @staticmethod
        def create():
            return Setting()

        def find(self, line):
            return False

        def check(self, line):
            pass

        def clear(self):
            pass

        def copy(self, channel):
            pass

    live = Live()
    setting = Setting.create()
    results = ["職棒,#genre#"]  # 預設內容

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue  # 跳過空行

        split = line.split(",")
        index = line.find(",") + 1

        if setting.find(line):
            setting.check(line)

        if "#genre#" in line:
            setting.clear()
            live.get_groups().append(Group.create(split[0]))

        if len(split) > 1 and not live.get_groups():
            live.get_groups().append(Group.create("Default Group"))

        if len(split) > 1 and "://" in split[1]:
            group = live.get_groups()[-1]
            channel = group.find(Channel.create(split[0]))
            channel.add_urls(line[index:].split("#"))
            setting.copy(channel)

    # 將處理結果傳遞給 fetch_live_content 並寫入結果列表
    for group in live.get_groups():
        for channel in group.channels:
            for url in channel.urls:
                hls_url = fetch_live_content(url)
                if hls_url:
                    results.append(f"{channel.name}, {hls_url}")  # 將替換結果添加到列表中

    return results  # 返回結果列表

# 示例 text
text = '''TVBS新聞台,https://today.line.me/tw/v2/article/jggMBa
生活新聞台,https://today.line.me/tw/v2/article/Lvpg70'''

# 呼叫處理函數並獲取結果
output_results = process_text(text)

# 可以根據需要進行印出
#for result in output_results:
#    print(result)