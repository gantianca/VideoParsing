import json
import re

import requests
from lxml import etree


class ntv_video:
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

    def get_json_zb(self, url):
        # 第一种类型的视频，直播回放     同过id访问api获取json数据
        id = re.findall("topic_id=(\d*)", url)[0]
        api_url = f"https://backcloud.ntv.cn/cloud-hotlive/?m=Apituwenol&c=tuwenol&a=detail&app_secret=1e235c84bf4c35c9c93a781e771460cc&id={id}"
        _json = requests.get(url=api_url, headers=self.headers).json()

        # print(json.dumps(_json))
        return _json

    def get_data_zb(self, _json):
        # 写入数据
        self.data[0]['desc'] = _json[0]['title']
        self.data[0]['url'] = _json[0]['live_info'][0]['url']
        self.data[0]['img'] = "http://plusimg.ntv.cn/" + _json[0]['indexpic']['filename']
        return

    def get_data_sp(self, url):
        # 第二种类型的视频， 通过xpath定位在源码中获取
        _html = requests.get(url=url, headers=self.headers).text
        sel = etree.HTML(_html)
        self.data[0]['desc'] = sel.xpath('//*[@class="mb10"]/text()')[0]
        self.data[0]['img'] = sel.xpath('//*[@name="indexpic"]/@value')[0]
        self.data[0]['url'] = sel.xpath('//*[@name="m3u8"]/@value')[0].replace(".m3u8", ".mp4")

        return

    def get_data_np(self, url):
        # 第三种类型的视频， 通过获取视频id访问api获取json数据然后写入
        _html = requests.get(url=url, headers=self.headers).text
        rel = etree.HTML(_html)
        id = rel.xpath("//*[@class='publishId']/@value")[0]
        api_url = f"https://mapi.ntv.cn/api/v1/item.php?&id={id}"
        _json = requests.get(url=api_url, headers=self.headers).json()

        # print(json.dumps(_json))
        # 写入数据
        self.data[0]['desc'] = _json['title']
        self.data[0]['img'] = "http://plusimg.ntv.cn/" + _json['index_pic']
        try:
            self.data[0]['url'] = _json['streams'][0]['url']
        except:
            self.data[0]['url'] = "http://plusvod.ntv.cn/" + _json['target_path'] + _json['target_filename']
        self.data[0]['file_size'] = _json['target_size']

    def start(self):
        # 有好几种类型的视频，分别用不同的方式解析
        if "hotlive" in self.url:
            _json = self.get_json_zb(self.url)
            self.get_data_zb(_json)
        elif "/p/" in self.url:
            self.get_data_sp(self.url)
        else:
            self.get_data_np(self.url)
        return self.data


if __name__ == "__main__":
    url = "https://www.ntv.cn/p/folder1589/folder1271/folder543/szpzc/folder815/2023-02-20/915811.html"
    print(json.dumps(ntv_video(url).start()))

# ntv.cn
