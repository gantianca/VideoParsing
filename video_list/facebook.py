import json
import re
import time
from urllib import parse

import requests
import yaml

import path


class facebook_video:
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
        cookie = ""
        ROOTPATH = path.path().start()
        with open(f'{ROOTPATH}/cookies/facebook_cookie.txt', 'r') as f:
            a = json.loads(f.read())
        for _data in a['cookie']:
            cookie += f"{_data['name']}={_data['value']};"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cookie': cookie,

            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "viewport-width": "2560",
        }
        # 代理地址
        # self.proxies = {
        #     "http": "127.0.0.1:7890",
        #     "https": "127.0.0.1:7890"
        # }
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
        # print(self.proxies)

        self.url = parse.unquote(requests.get(url=url, headers=self.headers, proxies=self.proxies).url)
        if "next" in self.url:
            self.url = re.findall('next=(.*)$', self.url)[0]
        self.url = parse.unquote(requests.get(url=self.url, headers=self.headers, proxies=self.proxies).url)
        if "next" in self.url:
            self.url = re.findall('next=(.*)$', self.url)[0]
        # print(self.url)

    def get_json(self, url):
        # 从源码中获取json数据，顺便获取标题
        _html = requests.get(url=url, headers=self.headers, proxies=self.proxies).text
        # print(_html)
        if 'groups' in self.url:
            self.data[0]['desc'] = re.findall('<title>([\s\S]*?)</title>', _html)[0]
        else:
            try:
                self.data[0]['desc'] = re.findall(
                    'CometVideoHomeHeroUnit_story\$defer\$CometVideoHomeHeroUnitSidePane_story.*?"title":\{"delight_ranges":\[],"image_ranges":\[],"inline_style_ranges":\[],"aggregated_ranges":\[],"ranges":\[],"color_ranges":\[],"text":"(.*?)"},"info"',
                    _html)[0].encode('utf-8').decode('unicode_escape')
            except:
                try:
                    self.get_desc(_html)
                except:
                    self.data[0]['desc'] = re.findall('<title>([\s\S]*?)</title>', _html)[0]
        if not self.data[0]['desc']:
            try:
                self.get_desc(_html)
            except:
                self.data[0]['desc'] = re.findall('<title>([\s\S]*?)</title>', _html)[0]
        if not self.data[0]['desc']:
            self.data[0]['desc'] = re.findall('<title>([\s\S]*?)</title>', _html)[0]

        # self.data[0]['desc'] = re.findall('<title>([\s\S]*?)</title>', _html)[0].strip(' ')
        # _json = re.findall(
        #     '\{"define":\[\["VideoPlayerShakaPerformanceLoggerConfig".*?(\{"__bbox".*?}})]],\["RequireDeferredReference".*?]]]}\)',
        #     _html)[0]
        try:
            _json = re.findall('(\{"require".*?VideoPlayerShakaPerformanceLoggerConfig.*?})</script>', _html)[0]
        except:
            _json = re.findall('(\{"define".*?VideoPlayerShakaPerformanceLoggerConfig.*?})\);</script>', _html)[0]
        # print(_json)
        # _json = json.loads(_json)['require'][0][-1][0]['__bbox']['require'][5][-1][-1]
        _json = json.loads(re.findall('",(\{"__bbox".*?})]],', _json)[0])
        # print(json.dumps(_json))
        return _json

    def get_desc(self, _html):
        # 获取标题
        try:
            self.data[0]['desc'] = re.findall('"message":\{"text":"(.*?)","delight_ranges"', _html)[0].encode(
                'utf-8').decode(
                'unicode_escape')
        except:
            try:
                self.data[0]['desc'] = \
                    re.findall(',"text":"(.*?)"}],"__module_operation_CometTahoeVideoContextSectionBody_video"', _html)[
                        0].encode('utf-8').decode('unicode_escape')
            except:
                try:
                    self.data[0]['desc'] = re.findall('\{"ranges":\[],"text":"(.*?)","delight_ranges"', _html)[
                        0].encode(
                        'utf-8').decode('unicode_escape')
                except:
                    self.data[0]['desc'] = re.findall('"color_ranges":\[],"text":"(.*?)"},"info"', _html)[0].encode(
                        'utf-8').decode('unicode_escape')

    def get_data(self, _json):
        # 写入数据
        if "video" in _json['__bbox']['result']['data']:
            if "story" in _json['__bbox']['result']['data']['video']:
                video_data = _json['__bbox']['result']['data']['video']['story']['attachments'][0]['media']
            else:
                video_data = _json['__bbox']['result']['data']['video']
        else:
            video_data = \
                _json['__bbox']['result']['data']['node']['comet_sections']['content']['story']['attached_story'][
                    'attachments'][0]['styles']['attachment']['media']
        try:
            self.data[0]['img'] = video_data['preferred_thumbnail']['image']['uri']
        except:
            pass
        self.data[0]['url'] = video_data['playable_url_quality_hd']
        if self.data[0]['url'] is None:
            self.data[0]['url'] = video_data['playable_url']
        # self.data[0]['width'] = video_data['width']
        # self.data[0]['height'] = video_data['height']

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
        _json = self.get_json(self.url)
        self.get_data(_json)
        return self.data


if __name__ == "__main__":
    url = "https://fb.watch/iInbMAf4Hm/"
    print(json.dumps(facebook_video(url).start()))
