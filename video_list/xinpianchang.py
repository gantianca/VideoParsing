import json
import re

import requests


class xinpianchang_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url
        self.have_top = False

    def start(self):
        # 获取源码，从源码中获取参数
        _html = requests.get(url=self.url, headers=self.headers).text
        vid = re.findall('"video_library_id":"(.*?)"', _html)[0]
        # appKey是固定值，不知是否会变化
        appKey = "61a2f329348b3bf77"
        api_url = f"https://mod-api.xinpianchang.com/mod/api/v2/media/{vid}?appKey={appKey}"

        _json = requests.get(url=api_url, headers=self.headers).json()
        # print(json.dumps(_json))
        # 写入数据
        _desc = _json['data']['title']
        _img = _json['data']['cover']

        for _data in _json['data']['resource']['progressive']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[self.num]['file_size'] = _data['filesize']
            self.data[self.num]['url'] = _data['url']
            self.data[self.num]['width'] = _data['width']
            self.data[self.num]['height'] = _data['height']
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            else:
                self.num += 1
        return self.data


if __name__ == "__main__":
    url = "https://www.xinpianchang.com/a12378317?from=IndexPick&part=%E5%8F%A4%E9%A3%8E&index=2"
    ret_single = False
    print(json.dumps(xinpianchang_video(url=url, ret_single=ret_single).start()))
