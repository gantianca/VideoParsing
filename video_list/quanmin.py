import json
import re

import requests


class quanmin_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.url = url
        self.have_top = False

    def get_json(self, url):
        # 从源码里获取json数据
        _html = requests.get(url=url, headers=self.headers).text
        _json = re.findall('window._page_data = (.*?);', _html)[0]
        # print(_json)
        _json = json.loads(_json)
        return _json

    def get_data(self, _json):
        # 把数据写入
        _desc = _json['meta']['title']
        _img = _json['meta']['image']
        if self.ret_single:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            url_data = _json['meta']['videoInfo']['clarityUrl'][-1]
            self.data[0]['url'] = url_data['url']
            self.data[0]['file_size'] = 1024 * 1024 * url_data['videoSize']
            self.data[0]['width'] = re.findall('(\d*)$', url_data['vodVideoHW'])[0]
            self.data[0]['height'] = re.findall('(\d*)', url_data['vodVideoHW'])[0]
        else:
            for url_data in _json['meta']['videoInfo']['clarityUrl'][::-1]:
                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': _img,
                    'type': 'video',
                })
                self.data[self.num]['url'] = url_data['url']
                self.data[self.num]['file_size'] = 1024 * 1024 * url_data['videoSize']
                self.data[self.num]['width'] = re.findall('(\d*)$', url_data['vodVideoHW'])[0]
                self.data[self.num]['height'] = re.findall('(\d*)', url_data['vodVideoHW'])[0]
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True
                self.num += 1

        return

    def start(self):
        _json = self.get_json(url=self.url)
        self.get_data(_json)
        return self.data


if __name__ == '__main__':
    url = 'https://quanmin.baidu.com/v/4165500769015057810?source=share-1024102t-0&tab=share&pd=1024102t&autoplay=1'
    ret_single = False
    print(json.dumps(quanmin_video(url=url, ret_single=ret_single).start()))
