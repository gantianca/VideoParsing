import requests
import re
import json
from lxml import etree


class art_china_video:
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
        res = requests.get(url=url, headers=self.headers)
        self._html = res.text
        self.rel = etree.HTML(res.content)

    def get_type(self, url):
        # 获取链接的类型
        if "txt" in url:
            self.get_data1()
        elif "scheme" in url:
            self.get_data2()
        elif "salon" in url:
            self.get_data3()

    # 数据都在源码里，通过xpath定位数据
    def get_data1(self):
        try:
            self.data[0]['url'] = self.rel.xpath('//*[@id="videofile"]/@src')[0]
        except:
            try:
                self.data[0]['url'] = self.rel.xpath('//*[@class="vdoAddr none"]/text()')[0]
            except:
                self.data[0]['url'] = self.rel.xpath('//*[@class="vdoAddr"]/text()')[0]
        self.data[0]['desc'] = self.rel.xpath('//*[@class="content"]/h1/text()')[0].strip()
        try:
            self.data[0]['img'] = re.findall('<picsmall>(.*?)</picsmall>',self._html)[0]
        except:
            pass

    def get_data2(self):

        self.data[0]['url'] = self.rel.xpath('//*[@class="video"]/text()')[0].strip()
        self.data[0]['desc'] = self.rel.xpath('//*[@class="main"]/h1/text()')[0].strip()
        self.data[0]['img'] = re.findall("url\((.*)\)", self.rel.xpath('//*[@class="vdBg"]/@style')[0])[0]

    def get_data3(self):
        self.data[0]['url'] = self.rel.xpath('//*[@id="videofile"]/@src')[0]
        self.data[0]['desc'] = self.rel.xpath('//*[@class="banner"]/h1/text()')[0].strip()

    def start(self):
        self.get_type(self.url)

        return self.data


if __name__ == "__main__":
    url = "http://art.china.cn/txt/2019-05/17/content_40754898.shtml"
    print(json.dumps(art_china_video(url).start()))