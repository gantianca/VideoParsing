import re

import requests
import json
from lxml import etree

class v_163_video:
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
        if 'm.163.com' in url:
            self.url = re.sub('m\.163\.com', 'www.163.com', url)
        else:
            self.url = url

    def get_data(self, url):
        # 数据都在源码的标签里，用xpath定位获取
        _data = requests.get(url=url, headers=self.headers).text
        sel = etree.HTML(_data)
        self.data[0]['url'] = sel.xpath('//*[@id="video_dom"]/@src')[0]
        self.data[0]['desc'] = sel.xpath('//*[@class="title_wrap"]/h1/text()')[0]
        self.data[0]['img'] = sel.xpath('//*[@class="hidden"]/img/@src')[0]
        return

    def start(self):
        self.get_data(self.url)

        return self.data


if __name__ == "__main__":
    url = "https://www.163.com/v/video/VD2D82MEQ.html"
    print(json.dumps(v_163_video(url).start()))