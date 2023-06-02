import json
import re

import requests


class sina_video:
    def __init__(self, url, ret_single=True):
        self.num = 0
        self.ret_single = ret_single
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.url = url
        self.have_top = False

    def get_id(self, url):
        # 从源码里获取id
        _html = requests.get(url=url, headers=self.headers).text
        try:
            id = re.findall('video_id:(.*?),', _html)[self.num]
        except:
            try:
                id = re.findall('video_id=(\d*)', _html)[self.num]
            except:
                id = re.findall('"videoId":\D*(\d*)', _html)[self.num]
        # print(id)
        return id

    def get_json(self, id):
        # 通过id访问保存了json数据的网页，获取json数据
        url = f'https://api.ivideo.sina.com.cn/public/video/play?video_id={id}&appver=V&appname=sinaplayer_pc&applt=web&tags=sinaplayer_pc'
        # print(url)
        _json = requests.get(url, headers=self.headers).text
        # print(_json)
        _json = json.loads(_json)
        return _json

    def get_data(self, _json):
        # 保存数据
        _desc = _json['data']['title']
        _img = _json['data']['transcode_image']
        for _data in _json['data']['videos']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[self.num]['url'] = _data['dispatch_result']['url']
            self.data[self.num]['width'] = _data['width']
            self.data[self.num]['height'] = _data['height']
            self.data[self.num]['file_size'] = _data['size']
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            else:
                self.num += 1
        return

    def start(self):
        id = self.get_id(self.url)
        _json = self.get_json(id)
        self.get_data(_json)
        return self.data


if __name__ == '__main__':
    url = 'https://k.sina.cn/article_2686474383_ma020588f0570153q7.html?from=food'
    ret_single = False
    print(json.dumps(sina_video(url=url, ret_single=ret_single).start()))
