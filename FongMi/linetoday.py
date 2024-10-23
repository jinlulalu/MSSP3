import requests
import re

def processLiveContent(text):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }

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
    results = []

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

    # 將處理結果寫入結果列表並獲取 HLS URL
    for group in live.get_groups():
        # 寫入群組名稱
        results.append(f"{group.name},#genre#")  # 將群組名稱添加到結果列表
        for channel in group.channels:
            for url in channel.urls:
                # 獲取 HLS URL 的邏輯
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # 檢查請求是否成功

                # 使用正則表達式直接提取 broadcastId
                broadcast_id_match = re.search(r'broadcastId:\s*"(\w+)"', response.text)
                if not broadcast_id_match:
                    continue  # 若找不到 broadcastId，跳過
                broadcast_id = broadcast_id_match.group(1)

                # 呼叫 API 獲取 HLS URL
                api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
                api_response = requests.get(api_url, headers=headers)
                api_data = api_response.json()

                # 獲取 HLS URL 並添加到結果
                hls_url = api_data['hlsUrls']['abr']
                results.append(f"{channel.name},{hls_url}")  # 將替換結果添加到列表中

    return "\n".join(results)  # 返回結果列表，使用換行符連接

# 從指定的 URL 讀取 text
text_url = 'https://raw.githubusercontent.com/jinlulalu/MSSP3/main/FongMi/linetoday.txt'
response = requests.get(text_url)
response.raise_for_status()  # 檢查請求是否成功
text = response.text  # 獲取文本內容

# 呼叫處理函數並獲取結果
processed_content = processLiveContent(text)
print(processed_content)
