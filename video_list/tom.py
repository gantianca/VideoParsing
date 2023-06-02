import requests
import re
import json
from lxml import etree


class tom_video:
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

    def get_data(self, url):
        # 在源码中通过xpath定位数据
        _html = requests.get(url=url, headers=self.headers).content
        rel = etree.HTML(_html)
        self.data[0]['url'] = rel.xpath('//*[@preload="none"]/@src')[0]
        self.data[0]['img'] = rel.xpath('//*[@name="Imageurl"]/@content')[0]
        self.data[0]['desc'] = rel.xpath('//*[@id="video_name"]/text()')[0]
        return

    def start(self):
        self.get_data(self.url)

        return self.data


if __name__ == "__main__":
    url = "https://v.tom.com/202109/3830235474.html"
    print(json.dumps(tom_video(url).start()))