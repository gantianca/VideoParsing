import json
import re

import requests


class weishi_video:
    def __init__(self, url, ret_single=True):
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.url = url

    def get_json(self, url):
        # 从源码里获取json数据
        html = requests.get(url=url, headers=self.headers).text
        _json = json.loads(re.findall('window\.Vise\.initState = (.*?); } catch', html)[0])

        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 把数据写入
        self.data[0]['desc'] = _json['feedsList'][0]['feedDesc']
        self.data[0]['url'] = _json['feedsList'][0]['videoSpecUrls']['0']['url']
        self.data[0]['file_size'] = _json['feedsList'][0]['videoSpecUrls']['0']['size']
        self.data[0]['width'] = _json['feedsList'][0]['videoSpecUrls']['0']['width']
        self.data[0]['height'] = _json['feedsList'][0]['videoSpecUrls']['0']['height']
        self.data[0]['img'] = _json['feedsList'][0]['images'][0]['url']

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)
        # print(_json)
        return self.data


if __name__ == "__main__":
    url = 'https://isee.weishi.qq.com/ws/app-pages/share/index.html?wxplay=1&id=6ZfXSTYgz1PlDAnSc&spid=4200340348766563010&qua=v1_and_weishi_8.89.0_588_312026001_d&chid=100081014&pkg=3670&attach=cp_reserves3_1000370011'
    ret_single = False
    print(json.dumps(weishi_video(url=url, ret_single=ret_single).start()))
