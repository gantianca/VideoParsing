import json
import re

import requests


class cctv_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.url = url
        self.have_top = False

    def get_guid(self, url):
        # 从源码里获取视频的guid
        _html = requests.get(url=url, headers=self.headers).text
        if 'var guid = "' in _html:
            guid = re.findall('var guid = "(.*?)";', _html)[0]
        else:
            guid = re.findall('videoCenterId: "(.*?)",', _html)[0]
        return guid

    def get_json(self, guid):
        # 通过guid获取链接，再获取json数据
        url = f'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={guid}'
        _json = requests.get(url).text
        # print(_json)
        _json = json.loads(_json)
        return _json

    def get_data(self, _json):
        # 写入数据
        num_list = [5, 3, 2, '']
        quality_list = ['1080p', '720p', '360p', '270p']
        _desc = _json['title']
        for num in num_list:
            if f'chapters{num}' in _json['video']:
                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': '',
                    'type': 'video',
                })
                if len(_json['video'][f'chapters{num}']) > 1:
                    url_list = []
                    for _data in _json['video'][f'chapters{num}']:
                        url_list.append(_data['url'])
                    self.data[self.num]['url'] = url_list
                    self.data[self.num]['type'] = "block_video"
                else:
                    self.data[self.num]['url'] = _json['video'][f'chapters{num}'][0]['url']
                self.data[self.num]['img'] = _json['video'][f'chapters{num}'][0]['image']
                self.data[self.num]['quality_str'] = quality_list[num_list.index(num)]
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True
                if self.ret_single:
                    break
                else:
                    self.num += 1
        return

    def start(self):
        guid = self.get_guid(self.url)
        _json = self.get_json(guid)
        self.get_data(_json)
        return self.data


if __name__ == '__main__':
    url = 'http://jishi.cctv.com/2018/07/13/VIDESn7XdHTMwsugBpJL4AK4180713.shtml'
    ret_single = False
    print(json.dumps(cctv_video(url=url, ret_single=ret_single).start()))
