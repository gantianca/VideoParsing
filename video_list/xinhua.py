import requests
import re
import json
from lxml import etree


class xinhua_video:
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
        # 通过xpath在源码中定位数据
        _html = requests.get(url=url, headers=self.headers).text
        # print(_html)
        rel = etree.HTML(_html)
        self.data[0]['desc'] = rel.xpath('//*[@name="description"]/@content')[0].split("-")[0]
        self.data[0]['url'] = rel.xpath('//*[@class="pageVideo"]/@video_src')[0]
        if self.data[0]['url'] == 'undefined':
            _uuid = rel.xpath('//*[@class="pageVideo"]/@uuid')[0]
            _vid = rel.xpath('//*[@class="pageVideo"]/@vid')[0]
            _url = f"https://player.v.news.cn/api/v1/getConfigs?uuid={_uuid}&vid={_vid}"
            _data = requests.get(url=_url, headers=self.headers).json()
            self.data[0]['url'] = _data['result']['videoInfos']['src']
        try:
            self.data[0]['width'] = rel.xpath('//*[@class="pageVideo"]/@video_width')[0]
            self.data[0]['height'] = rel.xpath('//*[@class="pageVideo"]/@video_width')[0]
        except:
            pass
        try:
            self.data[0]['file_size'] = rel.xpath('//*[@class="pageVideo"]/@filesize')[0]
        except:
            pass

    def start(self):
        self.get_data(self.url)

        return self.data


if __name__ == "__main__":
    url = "http://hlj.news.cn/dt/2022-09/29/c_1310664587.htm"
    print(json.dumps(xinhua_video(url).start()))