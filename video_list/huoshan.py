import json
import re

import requests


class huoshan_video:
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

    def get_item_id(self):
        # 从url中获取item_id
        item_id = re.findall('item_id=(\d*)', self.url)[0]
        return item_id

    def get_json(self, id):
        # 通过id拼接地址访问api获取json数据
        url = f'http://hotsoon.snssdk.com/hotsoon/item/video/_get/?item_id={id}'
        _json = requests.get(url=url, headers=self.headers).text

        # print(_json)
        return _json

    def get_data(self, _json):
        # 写入数据
        _json = json.loads(_json)
        self.data[0]['url'] = _json['data']['video']['url_list'][0]
        self.data[0]['desc'] = _json['data']['title']
        self.data[0]['img'] = _json['data']['video']['cover']['url_list'][0]
        # self.data[0]['width'] = _json['data']['video']['width']
        # self.data[0]['height'] = _json['data']['video']['height']
        return

    def start(self):
        # 有时运行会出现不知道原因的错误，重新运行就不会报错，设置报错重新运行一次
        try:
            id = self.get_item_id()
            _json = self.get_json(id)
            self.get_data(_json)
        except:
            id = self.get_item_id()
            _json = self.get_json(id)
            self.get_data(_json)

        # print(_json)
        return self.data


if __name__ == '__main__':
    url = 'https://share.huoshan.com/hotsoon/s/w8edqOVx3A8/'
    ret_single = False
    print(json.dumps(huoshan_video(url=url, ret_single=ret_single).start()))
