import json
import re

import requests


class qtt_video:
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
        self.url = requests.get(url=url, headers=self.headers).url

    def get_id(self):
        # 从url中获取id
        id = re.findall('content_id=(\d*)', self.url)[0]
        return id

    def get_json(self, id):
        # 通过获取到的id拼出json数据的地址
        url = f'http://api.1sapp.com/content/getContent?content_id={id}'
        _json = requests.get(url=url, headers=self.headers).text

        # print(_json)
        return json.loads(_json)

    def get_data(self, _json):
        # 写入数据
        qx_list = ['hd', 'ld', 'hhd', 'hld']
        self.data[0]['desc'] = _json['data'][0]['title']
        self.data[0]['img'] = _json['data'][0]['cover'][0]
        for qx in qx_list:
            if qx in _json['data'][0]['video_info']:
                self.data[0]['url'] = _json['data'][0]['video_info'][qx]['url']
                self.data[0]['file_size'] = _json['data'][0]['video_info'][qx]['intsize']
                break
        return

    def start(self):
        id = self.get_id()
        _json = self.get_json(id)
        self.get_data(_json)

        # print(_json)
        return self.data


if __name__ == '__main__':
    url = 'http://new.3qtt.cn/1DPlj8'
    ret_single = False
    print(json.dumps(qtt_video(url=url, ret_single=ret_single).start()))
