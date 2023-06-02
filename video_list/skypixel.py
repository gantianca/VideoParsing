import json
import re

import requests


class skypixel_video:
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
        # 通过链接里的id访问api获取json数据
        id = re.findall('/videos/(.*)\??', url)[0]
        api_url = f"https://www.skypixel.com/api/v2/videos/{id}"
        _json = requests.get(url=api_url, headers=self.headers).json()

        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 写入数据
        quality_list = ['large', 'medium', 'small']
        _desc = _json['data']['item']['title']
        _img = _json['data']['item']['image']['large']

        for _quality in quality_list:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[self.num]['url'] = _json['data']['item']['cdn_url'][_quality]
            self.data[self.num]['quality_str'] = re.sub('sd', '480', re.findall('/(sd|\d*?)\.mp4', self.data[self.num]['url'])[0] + 'p')
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            else:
                self.num += 1
        return

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)

        return self.data


if __name__ == "__main__":
    url = "https://www.skypixel.com/videos/0a415ec5-84a9-49b4-a474-01765ff14f11?utm_source=copied&utm_medium=PCWeb&utm_campaign=share&sp=0"
    ret_single = False
    print(json.dumps(skypixel_video(url=url, ret_single=ret_single).start()))
