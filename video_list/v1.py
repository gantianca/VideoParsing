import requests
import re
import json
from lxml import etree


class v1_video:
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

    def get_id(self, url):
        # 获取id
        if "id=" in url:
            id = re.findall("id=(\d*)", url)[0]
        else:
            id = re.findall("video/(\d*)", url)[0]
        # print(id)
        return id

    def get_data(self, id):
        # 通过id获取网页地址，通过xpath定位数据
        url = f"https://www.v1.cn/video/{id}.html"
        _html = requests.get(url=url, headers=self.headers).text
        # print(_html)
        rel = etree.HTML(_html)
        self.data[0]['url'] = rel.xpath('//*[@property="og:videosrc"]/@content')[0]
        self.data[0]['img'] = rel.xpath('//*[@property="og:image"]/@content')[0]
        self.data[0]['desc'] = rel.xpath('//*[@property="og:title"]/@content')[0]

    def start(self):
        id = self.get_id(self.url)
        self.get_data(id)

        return self.data


if __name__ == "__main__":
    url = "https://www.v1.cn/video/1629417403619299329.html"
    print(json.dumps(v1_video(url).start()))
