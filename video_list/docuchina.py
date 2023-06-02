import json
import re

import requests


class docuchina_video:
    def __init__(self, url, ret_single=True):
        self.data = self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url

    def get_json(self, url):
        # 从源码里获取pid，访问api获取json数据
        pid = re.findall('var guid.*"(.*?)"', requests.get(url=url, headers=self.headers).text)[0]
        api_url = f"https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={pid}"
        _json = requests.get(url=api_url, headers=self.headers).json()

        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 写入数据， 视频是mp4格式但是被分割成2分钟的片段
        self.data[0]['desc'] = _json['title']
        v_num = _json['video']['validChapterNum']
        while True:
            if f'chapters{v_num}' in _json['video']:
                self.data[0]['img'] = _json['video'][f'chapters{v_num}'][0]['image']
                break
            v_num -= 1
        url_list = []
        for url in _json['video'][f'chapters{v_num}']:
            url_list.append(url['url'])
        self.data[0]['url'] = url_list
        self.data[0]['type'] = 'block_video'

        return

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)

        return self.data


if __name__ == "__main__":
    url = "https://tv.cctv.com/2023/02/22/VIDEGpubjEeD0RB7mCm5s4Mt230222.shtml?spm=C52507945305.P1Tyk9aHorGZ.0.0"
    print(json.dumps(docuchina_video(url).start()))
