import json
import re

import requests


class haokan_video:
    def __init__(self, url, ret_single=True):
        self.num = 0
        self.ret_single = ret_single
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        self.url = requests.get(url=url, headers=self.headers).url
        self.have_top = False

    def get_html(self):
        # 获取链接的源码，数据都在源码里面
        html = requests.get(url=self.url, headers=self.headers).text
        return html

    def get_data(self, html):
        # 从源码里提取出来需要的数据
        data = re.findall(r'window.__PRELOADED_STATE__ = (.*?); ', html)[0]
        # print(data)
        # 转换一下让py能读取
        data = json.loads(data)
        # 写入数据
        _desc = data['curVideoMeta']['title']
        _img = data['curVideoMeta']['poster']
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
            self.data[0]['url'] = re.findall(r'(.*?)\?v_from_s=', data['curVideoMeta']['clarityUrl'][-1]['url'])[0]
            self.data[0]['file_size'] = data['curVideoMeta']['clarityUrl'][-1]['videoSize'] * 1024 * 1024
            self.data[0]['width'] = re.findall(r'\$\$(.*)', data['curVideoMeta']['clarityUrl'][-1]['vodVideoHW'])[0]
            self.data[0]['height'] = re.findall(r'(.*?)\$\$', data['curVideoMeta']['clarityUrl'][-1]['vodVideoHW'])[0]
        else:
            for _data in data['curVideoMeta']['clarityUrl'][::-1]:
                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': _img,
                    'type': 'video',
                })
                # print(_data)
                try:
                    self.data[self.num]['url'] = re.findall(r'(.*?)v_from_s=', _data['url'])[0]
                except:
                    self.data[self.num]['url'] = _data['url']
                self.data[self.num]['file_size'] = _data['videoSize'] * 1024 * 1024
                self.data[self.num]['width'] = re.findall(r'\$\$(.*)', _data['vodVideoHW'])[0]
                self.data[self.num]['height'] = re.findall(r'(.*?)\$\$', _data['vodVideoHW'])[0]
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True
                self.num += 1

        return

    def start(self):
        html = self.get_html()
        self.get_data(html)
        return self.data


if __name__ == '__main__':
    url = 'https://haokan.baidu.com/v?vid=14718297367390806797&'
    # url = 'https://haokan.baidu.com/v?vid=10849565335142954971'
    ret_single = False
    data = haokan_video(url=url, ret_single=ret_single).start()
    print(json.dumps(data))
