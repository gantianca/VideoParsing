import json
import re

import requests


class izuiyou_video:
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
        self.pid = ''

    def get_pid(self):
        # 从url里获取pid
        self.pid = re.findall('pid=(\d*)', self.url)[0]
        return self.pid

    def get_json(self, pid):
        # 通过传pid参数获取到post请求里的json数据
        json = {
            'pid': eval(pid)
        }
        url = 'https://share.izuiyou.com/planck/share/post/detail'
        _json = requests.post(url=url, headers=self.headers, json=json).text

        # print(_json)
        return _json

    def get_data(self, _json):
        # 写入数据
        _json = json.loads(_json)
        video_data = json.loads(re.findall('{"\d*":(.*)}', json.dumps(_json['data']['post']['videos']))[0])
        self.data[0]['desc'] = _json['data']['post']['content']
        self.data[0]['url'] = video_data['url']

        self.data[0]['img'] = re.findall('"urls": \["(.*?)"]}', json.dumps(_json['data']['post']['imgs'][0]))[-2]
        return

    def start(self):
        pid = self.get_pid()
        _json = self.get_json(pid)
        self.get_data(_json)

        # print(_json)
        return self.data


if __name__ == '__main__':
    url = 'https://share.izuiyou.com/detail/247459980?from=zuiyoupc'
    print(json.dumps(izuiyou_video(url).start()))
