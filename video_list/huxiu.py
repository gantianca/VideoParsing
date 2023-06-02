import json
import re

import requests


class huxiu_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url
        self.have_top = False

    def get_json(self, url):
        # 从源码中截取json数据
        _html = requests.get(url=url, headers=self.headers).text
        _json = re.findall("window.__INITIAL_STATE__=(.*?);\(function", _html)[0]
        # print(_json)
        return json.loads(_json)

    def get_data(self, _json):
        # 写入质量最高的数据
        _desc = _json['articleDetail']['articleDetail']['title']
        _img = _json['articleDetail']['articleDetail']['video_info']['cover']

        _width = _json['articleDetail']['articleDetail']['video_info']['width']
        _height = _json['articleDetail']['articleDetail']['video_info']['height']

        if "fhd_link" in _json['articleDetail']['articleDetail']['video_info']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[self.num]['url'] = _json['articleDetail']['articleDetail']['video_info']['fhd_link']
            self.data[self.num]['file_size'] = eval(
                _json['articleDetail']['articleDetail']['video_info']['fhd_size'].replace("MB", '')) * 1024 * 1024

            if len(self.data) == 1:
                self.data[self.num]['width'] = _width
                self.data[self.num]['height'] = _height
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                return
            else:
                self.num += 1
        if "hd_link" in _json['articleDetail']['articleDetail']['video_info']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
                'quality_str': '720p'
            })
            self.data[self.num]['url'] = _json['articleDetail']['articleDetail']['video_info']['hd_link']
            self.data[self.num]['file_size'] = eval(
                _json['articleDetail']['articleDetail']['video_info']['hd_size'].replace("MB", '')) * 1024 * 1024

            if len(self.data) == 1:
                self.data[self.num]['width'] = _width
                self.data[self.num]['height'] = _height
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                return
            else:
                self.num += 1
        if "sd_link" in _json['articleDetail']['articleDetail']['video_info']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
                'quality_str': '270p'
            })
            self.data[self.num]['url'] = _json['articleDetail']['articleDetail']['video_info']['sd_link']
            self.data[self.num]['file_size'] = eval(
                _json['articleDetail']['articleDetail']['video_info']['sd_size'].replace("MB", '')) * 1024 * 1024

            if len(self.data) == 1:
                self.data[self.num]['width'] = _width
                self.data[self.num]['height'] = _height
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                return
            else:
                self.num += 1
        return

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)

        return self.data


if __name__ == "__main__":
    url = "https://www.huxiu.com/article/805004.html"
    ret_single = False
    print(json.dumps(huxiu_video(url=url, ret_single=ret_single).start()))
