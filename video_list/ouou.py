import requests
import re
import json
from lxml import etree


class ouou_video:
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
        self.url = url.replace('https', 'http')

    def get_data(self, url):
        # 数据都在源码里，通过xpath定位数据
        _html = requests.get(url=url, headers=self.headers).text
        rel = etree.HTML(_html)
        self.data[0]['img'] = rel.xpath('//*[@id="my-player"]/@poster')[0]
        self.data[0]['url'] = "http://www.ouou.com" + rel.xpath('//*[@id="my-player"]/source/@src')[0]
        self.data[0]['desc'] = rel.xpath('//*[@class="text-uppercase"]/text()')[0]

    def start(self):
        self.get_data(self.url)

        return self.data


if __name__ == "__main__":
    url = "http://www.ouou.com/article/index/id/3812/cid/12"
    print(json.dumps(ouou_video(url).start()))