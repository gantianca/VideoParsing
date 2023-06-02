import time

import requests
import re
import json


class xuexi_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url

    def get_json(self, url):
        # 获取视频id然后访问js文件获取json数据
        _id = re.findall('id=(\d+)', url)[0]

        # print(_id)
        api_url = f'https://boot-source.xuexi.cn/data/app/{_id}.js?callback=callback&_st={time.time()}'

        _json = re.findall('callback\(([\s\S]*?)\)$', requests.get(url=api_url, headers=self.headers).text)[0]

        # print(_json)
        return json.loads(_json)

    def get_data(self, _json):
        # 分析获取的json数据
        max_size_pic = 0
        video_data = _json['videos'][0]
        _desc = _json['title']
        for x in video_data['thumbnails']:
            if x['data'][0]['image_size'] > max_size_pic:
                max_size_pic = x['data'][0]['image_size']
                _img = x['data'][0]['url']

        max_size = 0
        if self.ret_single:
            for video_info in video_data['video_storage_info']:
                if video_info['type'] == 2 and video_info['size'] > max_size:
                    max_size = video_info['size']
                    _data = video_info
            self.data.append({
                'desc': _desc,
                'url': _data['normal'],
                'file_size': _data['size'],
                'width': _data['width'],
                'height': _data['height'],
                'img': _img,
                'type': 'video',
            })
        else:
            for video_info in video_data['video_storage_info']:
                if video_info['type'] == 2:
                    _data = video_info
                    self.data.append({
                        'desc': _desc,
                        'url': _data['normal'],
                        'file_size': _data['size'],
                        'width': _data['width'],
                        'height': _data['height'],
                        'img': _img,
                        'type': 'video',
                    })
        return

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)

        return self.data


if __name__ == "__main__":
    url = "https://www.xuexi.cn/lgpage/detail/index.html?id=2488106569188658141&item_id=2488106569188658141"
    ret_single = False
    print(json.dumps(xuexi_video(url=url, ret_single=ret_single).start()))
