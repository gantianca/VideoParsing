import json
import re

import requests


class eyepetizer_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-thefair-ua': 'EYEPETIZER_UNIAPP_H5/100000 (android;android;OS_VERSION_UNKNOWN;zh-Hans-CN;h5;1.0.0;cn-bj;SOURCE_UNKNOWN;0c4cace6d3eebb8dabe7347f2e11afd9;2560*1440;NETWORK_UNKNOWN) native/1.0',
            'x-thefair-appid': 'xfpa44crf2p70lk8',
            'x-thefair-auth': 'oFuzDjDxTgttPjbT3lnS1CYFbyb7m3Aqx+6FCcnEq0L8g8ueQ/tW8rR7ufo2PM/Rcf283aGn+CLomgnquuVg4McSpPecPKCyW2cOhrxZanIklwkmAl6I4qbU1tpRQkytL07saLkU/uNAoVUrwk+YiOq9C6MYJXImsvgm68CKqBokZbB7S/Mjjp1jdkyZycs3cMczUjtM3AKgQfjv4mtgRFXHrY5x0BwdocPYMqY8gZIFpn8picpJDFhAHnobQmyU',
            'x-thefair-cid': '0c4cace6d3eebb8dabe7347f2e11afd9',
            'x-thefair-forward-host': 'https://api.eyepetizer.net',
            'cookie': 'PHPSESSID=1',
            # 这里需要的参数都不能少，cookie里需要一个参数，值随意

        }
        self.url = url
        self.have_top = False

    def get_id(self, url):
        # 获取视频id
        if "video_id" in url:
            id = re.findall("video_id=(\d*)", url)[0]
        elif "resource_id" in url:
            id = re.findall("resource_id=(\d*)", url)[0]
        return id

    def get_json(self, id):
        # 通过id发送请求获取json数据
        url = "https://proxy.eyepetizer.net/v1/content/item/get_item_detail_v2"
        _data = {
            'resource_type': 'pgc_video',
            'resource_id': eval(id),
        }
        _json = requests.post(url=url, headers=self.headers, data=_data).text
        # print(_json)
        return json.loads(_json)

    def get_data(self, _json):
        # 写入数据
        _desc = _json['result']['video']['title']
        _img = _json['result']['video']['cover']['url']
        if _json['result']['video']['play_info']:
            if self.ret_single:
                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': _img,
                    'type': 'video',
                })
                self.data[0]['url'] = _json['result']['video']['play_info'][-1]['url']
                self.data[0]['width'] = _json['result']['video']['play_info'][-1]['width']
                self.data[0]['height'] = _json['result']['video']['play_info'][-1]['height']
                self.data[0]['file_size'] = _json['result']['video']['play_info'][-1]['url_list'][-1]['size']
            else:
                for _data in _json['result']['video']['play_info'][::-1]:
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
                    self.data[self.num]['width'] = _data['width']
                    self.data[self.num]['height'] = _data['height']
                    self.data[self.num]['file_size'] = _data['url_list'][-1]['size']
                    if not self.have_top:
                        self.data[self.num]['top_quality'] = True
                        self.have_top = True
                    self.num += 1


        else:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[0]['url'] = _json['result']['video']['play_url']
            self.data[0]['width'] = _json['result']['video']['width']
            self.data[0]['height'] = _json['result']['video']['height']
        return

    def start(self):
        id = self.get_id(self.url)
        _json = self.get_json(id)
        self.get_data(_json)

        return self.data


if __name__ == "__main__":
    url = "https://m.eyepetizer.net/u1/video-detail?video_id=158655&udid=4dee173bb363451d949a7530e84f1c18&vc=7052000&vn=7.5.200&size=1080X2264&first_channel=testflight&last_channel=testflight&system_version_code=30&deviceModel=LM-V510N"
    ret_single = False
    print(json.dumps(eyepetizer_video(url=url, ret_single=ret_single).start()))
