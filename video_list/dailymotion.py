import json
import re
import time

import requests
import yaml

import path


class dailymotion_video:
    def __init__(self, url, ret_single=True):
        self.data = [{
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

        ROOTPATH = path.path().start()
        try:
            with open(f'{ROOTPATH}/config.yaml', "r", encoding='utf-8') as f:
                text = f.read()
                # print(text)
                text = yaml.load(text, Loader=yaml.FullLoader)['porxy']
                if text:
                    data = text
                    if 'http' in data and 'https' in data:
                        self.proxies = data
                    else:
                        self.proxies = ''
                else:
                    self.proxies = ''
        except:
            self.proxies = ''

        # self.proxies = {'http': 'http://192.168.124.84:7890', 'https': 'http://192.168.124.84:7890'}

    def get_id(self, url):
        # 获取视频id
        try:
            id = re.findall('/video/(.*)\??', url)[0]
        except:
            pass

        return id

    def get_json(self, id):
        # 通过id访问api获取json数据
        img_list = ["1080", "720", "480", "360", "240", "180", "120", "60"]
        api_url = f"https://www.dailymotion.com/player/metadata/video/{id}"
        # print(api_url)
        _json = requests.get(url=api_url, headers=self.headers, proxies=self.proxies).json()
        # print(json.dumps(_json))
        self.data[0]['desc'] = _json['title']
        for x in img_list:
            if x in _json['posters']:
                self.data[0]['img'] = _json['posters'][x]
                break

        # 视频的真实地址藏在这个链接的文本中
        data_url = _json['qualities']['auto'][0]['url']
        data = requests.get(url=data_url, headers=self.headers, proxies=self.proxies).text
        # print(data)
        self.data[0]['url'] = re.findall('PROGRESSIVE-URI="(.*?)"',data)[-1]
        self.data[0]['width'] = re.findall('RESOLUTION=(\d*)x\d*', data)[-1]
        self.data[0]['height'] = re.findall('RESOLUTION=\d*x(\d*)', data)[-1]
        # print(data)
        # print(json.dumps(_json))
        return

    def start(self):
        try:
            return self._start()
        except requests.exceptions.ProxyError:
            # print("解析出错")
            time.sleep(3)
            try:
                # print("第一次重试")
                return self._start()
            except requests.exceptions.ProxyError:
                # print("解析出错")
                time.sleep(10)
                try:
                    # print("第二次重试")
                    return self._start()
                except requests.exceptions.ProxyError:
                    # print("解析出错")
                    time.sleep(30)
                    # print("第三次重试")
                    return self._start()

    def _start(self):
        id = self.get_id(self.url)
        self.get_json(id)
        return self.data


if __name__ == "__main__":
    url = "https://www.dailymotion.com/video/x8go6j7"
    print(json.dumps(dailymotion_video(url).start()))
