# -*- coding: utf-8 -*-
import base64
import json
import re

import requests


# import path


class ixigua_video:

    def __init__(self, url, ret_single=True, _id=''):
        self.true_id = _id
        self.ret_single = ret_single
        self.type_list = ['video_6', 'video_5', 'video_4', 'video_3', 'video_2', 'video_1']
        # 视频清晰度从高到低排列的列表
        self.data = []
        # cookie = ""
        # ROOTPATH = path.path().start()
        # with open(f'{ROOTPATH}/cookies/ixigua_cookie.txt', 'r') as f:
        #     a = json.loads(f.read())
        # for _data in a['cookie']:
        #     if _data['name'] == 'ttwid':
        #         ttwid = _data['value']
        #         break
        # self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            # 'cookie': 'ttwid=1%7CRSrl_nl3_HyAt9eRtSCKvcuiI8w8w7YQOQn5TqgRE4A%7C1670401547%7Cafcb91a470a13b0177292356d749fd9c1b00019e76032d7caea87307864f7f6f',
            # 'cookie': 'ttwid=1',
            # 'referer': 'https://www.ixigua.com',
            # 'cookie': '__ac_nonce=06391950c007b3ef5ccd5; ttwid=1%7CRSrl_nl3_HyAt9eRtSCKvcuiI8w8w7YQOQn5TqgRE4A%7C1670485285%7Cb1336b28cdcef1cba69bdfe15b8718f68173475e53645e7bdc61b4abd9d49305'
            'cookie': f'__ac_nonce=0;ttwid={self.get_ttwid()}'
            # 这个cookie里要两个值，一个值只要有不为空就行，另一个值必须从真实的cookie里获取，从网页上看这个值一年过期
        }
        self.url = requests.get(url=url, headers=self.headers).url
        self.num = 0
        # print(self.url)
        self.have_top = False

    def get_ttwid(self):
        # 获取 ttwid 参数
        url = "https://ttwid.bytedance.com/ttwid/union/register/"
        _json = {"region": "cn", "aid": 1768, "needFid": False, "service": "www.ixigua.com",
                 "migrate_info": {"ticket": "", "source": "node"}, "cbUrlProtocol": "https", "union": True}
        tt = requests.post(url=url, json=_json).headers['Set-Cookie']
        tt_data = re.findall('ttwid=(.*?);', tt)[0]

        # print(tt_data)
        return tt_data

    def test(self):
        # 直接从源码中获取数据
        _html = requests.get(url=self.url, headers=self.headers)
        _html.encoding = 'utf-8'
        _html = _html.text
        try:
            video_data = \
                json.loads(re.sub('undefined', 'null', re.findall('window\._SSR_HYDRATED_DATA=(.*?)</script>', _html)[0]))[
                    'anyVideo']['gidInformation']['packerData']['video']
            _desc = video_data['title']
            _img = video_data['poster_url']
        except:
            video_data = \
                json.loads(
                    re.sub('undefined', 'null', re.findall('window\._SSR_HYDRATED_DATA=(.*?)</script>', _html)[0]))[
                    'anyVideo']['gidInformation']['packerData']
            _desc = video_data['albumInfo']['title']
            _img = video_data['albumInfo']['coverList'][0]['url']
            # video_data = video_data['videoResource']
            # print(json.dumps(video_data))

        for url_type in self.type_list:
            if url_type in video_data['videoResource']['normal']['video_list']:
                url_data = video_data['videoResource']['normal']['video_list'][url_type]
                # print(url_data)
                _width = url_data['vwidth']
                _height = url_data['vheight']
                _size = url_data['size']

                url_1 = url_data['main_url']
                url_1 = self.url_data(url_1)
                url_2 = url_data['backup_url_1']
                url_2 = self.url_data(url_2)
                # print(url_1)
                # print(url_2)
                # 这里会获取到两个地址，解密后一个可以打开，一个不可以，获取那个可以的
                if '//v3' in url_1:
                    _url = url_1
                else:
                    _url = url_2
                self.data.append({
                    'desc': _desc,
                    'url': _url,
                    'file_size': _size,
                    'width': _width,
                    'height': _height,
                    'img': _img,
                    'type': 'video',
                })
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True

                if self.ret_single:
                    break
                else:
                    self.num += 1

    def url_data(self, url):
        if 'https:' in url:
            url = re.sub('\\\\u002F', '/', url)
        else:
            url = re.findall("b'(.*?)'", str(base64.b64decode(url)))[0].replace('.\\xd3M\\x85', '?')

        return url

    def start(self):
        self.test()
        for x in self.data:
            if not x['url']:
                self.data.remove(x)
        return self.data


if __name__ == '__main__':
    __url = 'https://www.ixigua.com/7163072294313689604?id=7188129257455878668'
    # __url = 'https://v.douyin.com/DKey4F4/'
    ret_single = False
    print(json.dumps(ixigua_video(url=__url, ret_single=ret_single).start()))
