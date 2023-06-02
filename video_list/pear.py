import json
import re

import requests


class pear_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Cookie': 'PEAR_UUID=1'
            # 需要一个cookie但是只要有值就行
        }
        self.url = requests.get(url=url, headers=self.headers).url
        self.have_top = False

    def get_id(self):
        # 从url中获取id
        id = re.findall('video_(\d*)', self.url)[0]
        return id

    def get_json(self, id):
        # 通过id拼出保存了json数据的url
        url = f'http://app.pearvideo.com/clt/jsp/v4/content.jsp?contId={id}'
        # print(url)
        _json = json.loads(requests.get(url=url, headers=self.headers).text)

        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 写入数据
        _desc = _json['content']['name']
        _img = _json['content']['pic']
        for _data in _json['content']['videos']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[self.num]['url'] = _data['url']
            self.data[self.num]['file_size'] = _data['fileSize']
            self.data[self.num]['quality_str'] = _data['tag']
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            else:
                self.num += 1
        return

    def start(self):
        id = self.get_id()
        _json = self.get_json(id)
        self.get_data(_json)

        # print(_json)
        return self.data


if __name__ == "__main__":
    url = 'https://www.pearvideo.com/video_1301581?st=7'
    ret_single = False
    print(json.dumps(pear_video(url=url, ret_single=ret_single).start()))
