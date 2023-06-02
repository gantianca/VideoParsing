import requests
import re
import json


class i360kuai_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url

    def get_json(self, url):
        # 从源码中获取数据
        _html = requests.get(url=url, headers=self.headers).text
        _json = re.findall('window.__INITIAL_DATA__ = (.*?);', _html)[0]

        # print(_json)
        return json.loads(_json)

    def get_data(self, _json):
        # 写入数据
        self.data[0]['desc'] = _json['result']['Detail']['title']
        self.data[0]['img'] = _json['result']['Detail']['video_data'][0]['cover_picture']
        self.data[0]['url'] = _json['result']['Detail']['video_data'][0]['play_url']

        return

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)

        return self.data


if __name__ == "__main__":
    url = "https://www.360kuai.com/968393d1f053a7ed3?nsid=ffc890ccd590bc183dc4796efae20c90&refer_scene=&scene=130&sign=look&tj_url=968393d1f053a7ed3&uid=ffe7ae097a614962a1cad90e930eab10"
    ret_single = False
    print(json.dumps(i360kuai_video(url=url, ret_single=ret_single).start()))