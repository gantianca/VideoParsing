import requests
import re
import json
from lxml import etree


class jiemian_video:
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
        _html = requests.get(url=url, headers=self.headers).content
        rel = etree.HTML(_html)
        self.data[0]['url'] = rel.xpath('//*[@class="video-main"]/video/@src')[0]
        self.data[0]['img'] = "https:" + rel.xpath('//*[@class="video-main"]/video/@poster')[0]
        self.data[0]['desc'] = rel.xpath('//*[@class="article-header"]/h1/text()')[0]

    def start(self):
        self.get_data(self.url)

        return self.data


if __name__ == "__main__":
    url = "https://www.jiemian.com/video/AGQCOAhuB2ABO1Vl.html"
    print(json.dumps(jiemian_video(url).start()))