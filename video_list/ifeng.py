import json
import re

import requests


class ifeng_video:
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
        # 从源码里提取到json数据
        _html = requests.get(url=url, headers=self.headers).text
        _json = re.findall('var allData = (.*);', _html)[0]
        # print(self.url)
        # print(_json)
        _json = json.loads(_json)
        return _json

    def get_data(self, _json):
        # 写入数据,判断一下是分享的地址还是直接的地址，这是两种不同的网页
        if 'ishare' in self.url:
            self.data[0]['url'] = _json['videoInfo']['mobileUrl']
            self.data[0]['desc'] = _json['videoInfo']['desc']
            self.data[0]['img'] = _json['videoInfo']['bigPosterUrl']
        elif 'news' in self.url:
            self.data[0]['url'] = _json['docData']['contentData']['contentList'][0]['data']['playUrl']
            self.data[0]['desc'] = _json['docData']['contentData']['contentList'][0]['data']['title']
            self.data[0]['img'] = _json['docData']['contentData']['contentList'][0]['data']['bigPosterUrl']
            self.data[0]['file_size'] = eval(
                _json['docData']['contentData']['contentList'][0]['data']['fileSize']) * 1024
        else:
            self.data[0]['url'] = _json['docData']['videoPlayUrl']
            self.data[0]['desc'] = _json['docData']['title']
            self.data[0]['img'] = _json['docData']['posterUrl']
        return

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)
        return self.data


if __name__ == '__main__':
    url = 'https://news.ifeng.com/c/8M5VmS0fVPC'
    ret_single = False
    print(json.dumps(ifeng_video(url=url, ret_single=ret_single).start()))
