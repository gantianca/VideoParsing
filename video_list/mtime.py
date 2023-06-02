import requests
import re
import json
from lxml import etree


class mtime_video:
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
        self.url = requests.get(url=url, headers=self.headers).url
        # print(self.url)

    # 判断链接类型
    def get_type(self, url):
        # 第一种类型，从网页打开视频
        if "mid" in url:
            id = re.findall("trailer/(\d*)/", url)[0]
            self.get_data1(id)

        # app分享的链接
        elif "type" in url:
            _type = int(re.findall("type=(\d*)", url)[0])

            # 视频链接
            if _type == 5:
                id = re.findall("articlesId=(\d*)", url)[0]
                self.get_data3(id)

            # 文章链接
            elif _type == 4:
                id = re.findall("articlesId=(\d*)", url)[0]
                self.url = f"http://content.mtime.com/article/{id}"
                self.get_data2()
        # 从网页打开的文章
        elif "article" in url:
            self.get_data2()

    def get_data1(self, mid):
        # 从网页打的开视频
        url = f"https://front-gateway.mtime.com/video/play_url?video_id={mid}&source=1&scheme=https"
        _json = requests.get(url=url, headers=self.headers).json()
        _html = requests.get(url=self.url, headers=self.headers).text.encode('raw_unicode_escape').decode()
        sel = etree.HTML(_html)
        self.data[0]['desc'] = sel.xpath('/html/head/title/text()')[0]
        self.data[0]['desc'] = re.sub('_Mtime时光网', '', self.data[0]['desc'])
        self.data[0]['url'] = _json['data'][0]['url']
        self.data[0]['quality_str'] = _json['data'][0]['name']
        self.data[0]['quality_str'] = re.findall('.*?(\d*p)', self.data[0]['quality_str'])[0]
        return

    def get_data2(self):
        # 从网页打开的文章，app分享的文章也可以转到这里
        _html = requests.get(self.url, headers=self.headers).text.encode('raw_unicode_escape').decode()
        # print(_html.encode('raw_unicode_escape').decode())
        sel = etree.HTML(_html)
        self.data[0]['url'] = sel.xpath('//*[@controls="controls"]/@src')[0]
        self.data[0]['img'] = sel.xpath('//*[@controls="controls"]/@poster')[0]
        self.data[0]['desc'] = sel.xpath('//*[@name="keywords"]/@content')[0]
        # print(a)

    def get_data3(self, id):
        # app分享的视频
        url = f"https://m.mtime.cn/api/community/content.api?type=5&contentId={id}"
        _json = requests.get(url=url, headers=self.headers).json()
        self.data[0]['desc'] = _json['data']['title']
        self.data[0]['img'] = _json['data']['video']['posterUrl']
        self.data[0]['url'] = _json['data']['video']['videoResolutions'][0]['url']
        self.data[0]['file_size'] = _json['data']['video']['videoResolutions'][0]['fileSize']

    def start(self):
        self.get_type(self.url)

        return self.data


if __name__ == "__main__":
    url = "http://content.mtime.com/trailer/79181/?mid=268304"
    print(json.dumps(mtime_video(url).start()))
