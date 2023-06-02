import json
import re
import time
import traceback

import requests
import yaml

import path


class instagram_video:
    def __init__(self, url, ret_single=True):
        self.have_top = False
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        cookie = ""
        ROOTPATH = path.path().start()
        with open(f'{ROOTPATH}/cookies/ins_cookie.txt', 'r') as f:
            a = json.loads(f.read())
        for _data in a['cookie']:
            cookie += f"{_data['name']}={_data['value']};"
        self.headers = {
            # 用户代理 不能设置为pc端
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            # cookie需要两个参数，有第一个需要存在可以没有值，第二个必须要正确的值(账号可能会被封，所以cookie可能会失效)
            'cookie': cookie,
        }
        # 代理地址
        # self.proxies = {
        #     "http": "127.0.0.1:10001",
        #     "https": "127.0.0.1:10001"
        # }
        try:
            with open(f'{ROOTPATH}/config.yaml', "r", encoding='utf-8') as f:
                text = f.read()
                # print(text)
                text = yaml.load(text, Loader=yaml.FullLoader)['porxy']
                if text:
                    data = text
                    if 'http' in data and 'https' in data:
                        self.proxies = data
                    else:
                        self.proxies = ''
                else:
                    self.proxies = ''
        except:
            self.proxies = ''

        # print(self.proxies)
        self.url = url.split('/?')[0]
        # print(self.url)
        self.have_top = False

    def get_id(self, url):
        # 从源码中获取id
        _html = requests.get(url=url, headers=self.headers, proxies=self.proxies).text
        # print(_html)
        try:
            id = re.findall(r'media\?id=(\d*)"', _html)[0]
        except:
            id = re.findall('"media_id":"(\d*?)","', _html)[0]
        # print(id)

        return id

    def get_json(self, id):
        # 通过id访问保存的数据的api
        url = f"https://www.instagram.com/api/v1/media/{id}/info/"
        _json = requests.get(url=url, headers=self.headers, proxies=self.proxies).json()
        # print(json.dumps(_json))

        try:
            self._desc = _json['items'][0]['caption']['text'].split('\n')[0]
        except:
            self._desc = ""
        return _json

    def get_type(self, _json):
        # 判断媒体类型
        _type = _json['items'][0]['media_type']
        str_type = 'video'
        if _type == 8:
            str_type = "images"
        elif _type == 1:
            str_type = "image"
        # print(_type)
        return str_type

    def get_video_data(self, _json):
        # 对视频数据写入
        _img = _json['items'][0]['image_versions2']['candidates'][0]['url']
        for _data in _json['items'][0]['video_versions']:
            self.data.append({
                'desc': self._desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[self.num]['url'] = _data['url']
            self.data[self.num]['width'] = _data['width']
            self.data[self.num]['height'] = _data['height']
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                return
            else:
                self.num += 1
        return

    def get_images_data(self, _json):
        # 对图集数据写入
        self.data.append({
            'desc': self._desc,
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'images',
        })
        url_list = []
        image_list = _json['items'][0]['carousel_media']
        for img in image_list:
            url_list.append(img['image_versions2']['candidates'][0]['url'])
        self.data[0]['url'] = url_list
        self.data[0]['desc'] = self._desc

    def get_image_data(self, _json):
        # 对单张图片写入
        self.data.append({
            'desc': self._desc,
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'image',
        })
        self.data[0]['url'] = _json['items'][0]['image_versions2']['candidates'][0]['url']
        self.data[0]['desc'] = self._desc

    def start(self):
        try:
            return self._start()
        except requests.exceptions.ProxyError:
            # print("解析出错")
            time.sleep(3)
            try:
                # print("第一次重试")
                return self._start()
            except requests.exceptions.ProxyError:
                # print("解析出错")
                time.sleep(10)
                try:
                    # print("第二次重试")
                    return self._start()
                except requests.exceptions.ProxyError:
                    # print("解析出错")
                    time.sleep(30)
                    # print("第三次重试")
                    return self._start()

    def _start(self):
        id = self.get_id(self.url)
        _json = self.get_json(id)
        str_type = self.get_type(_json)
        if str_type == "video":
            self.get_video_data(_json)
        elif str_type == "images":
            self.get_images_data(_json)
        elif str_type == "image":
            self.get_image_data(_json)
        return self.data


if __name__ == "__main__":
    # url = 'https://www.instagram.com/reel/Cr05nuFgX_A/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=='
    url = "https://www.instagram.com/p/Cm_apxxvg2G/"
    ret_single = False
    print(json.dumps(instagram_video(url=url, ret_single=ret_single).start()))
