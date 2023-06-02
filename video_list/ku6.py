import requests
import re
import json


class ku6_video:
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

    def get_html(self, url):
        # 获取源码
        _html = requests.get(url=url, headers=self.headers).text
        # print(_html)

        return _html

    def get_data(self, _html):
        # 数据都在源码里，直接用正则获取
        self.data[0]['url'] = re.findall('type: "video/mp4", src: "(.*)"}', _html)[0]
        self.data[0]['img'] = re.findall('"poster": "(.*)"', _html)[0]
        self.data[0]['desc'] = re.findall('document.title = "(.*)";', _html)[0]
        return

    def start(self):
        _html = self.get_html(self.url)
        self.get_data(_html)

        return self.data


if __name__ == "__main__":
    url = "https://www.ku6.com/video/detail?id=2G7ot9jrlEWBjoCRBa85IEBbRSk."
    print(json.dumps(ku6_video(url).start()))