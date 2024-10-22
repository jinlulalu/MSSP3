import requests
import json
from bs4 import BeautifulSoup

def liveContent(article_url):
    # ���o�峹ID
    article_id = article_url.split('/')[-1]

    # �c��API�ШD��URL
    api_url = f'https://today.line.me/tw/v2/article/{article_id}'
    
    try:
        # �o�eGET�ШD
        response = requests.get(api_url)
        response.raise_for_status()  # �T�O�ШD���\

        # �ѪR HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find("script", string=lambda text: text and "__NUXT__" in text)

        if script is None:
            raise Exception("�䤣�� script")

        script_data = script.string
        # ���� broadcastId
        id_start = script_data.index("broadcastId:") + len("broadcastId:") + 1
        id_end = script_data.index("\"", id_start)
        broadcast_id = script_data[id_start:id_end]

        # ��� HLS URL
        api_url = f"https://today.line.me/webapi/glplive/broadcasts/{broadcast_id}"
        api_response = requests.get(api_url)
        api_response.raise_for_status()  # �T�O�ШD���\
        data = api_response.json()

        # ��� HLS URL
        hls_url = data["hlsUrls"]["abr"]
        return hls_url

    except requests.exceptions.RequestException as e:
        print(f"�ШD���~: {e}")
    except Exception as e:
        print(f"�B�z�L�{���X�{���~: {e}")

    return None  # �Y�����~�A��^ None
