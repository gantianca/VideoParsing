import json
import re

import requests


class baidu_video:
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
        # 从源码获取视频数据
        _html = requests.get(url=self.url, headers=self.headers).text
        # print(_html)
        _json = re.findall('window.jsonData = (.*);window.__firstPerformance', _html)[0]
        # print(_json)
        _json = json.loads(_json)
        return _json

    def get_data(self, _json):
        # 写入数据
        _desc = _json['curVideoMeta']['title']
        if 'poster' in _json['curVideoMeta']:
            _img = _json['curVideoMeta']['poster']
        else:
            _img = ''
        for _data in _json['curVideoMeta']['clarityUrl'][::-1]:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
                "top_quality": False
            })

            self.data[self.num]['url'] = _data['url']
            self.data[self.num]['width'] = re.findall('\d*\$\$(\d*)', _data['vodVideoHW'])[0]
            self.data[self.num]['height'] = re.findall('(\d*)\$\$\d*', _data['vodVideoHW'])[0]
            self.data[self.num]['file_size'] = float(_data['videoSize']) * 1024 * 1024
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
    url = "https://mbd.baidu.com/newspage/data/videoshare?nid=sv_9466319036408548756&source=feed_share_paycolumn"
    ret_single = False
    print(json.dumps(baidu_video(url=url, ret_single=ret_single).start()))
