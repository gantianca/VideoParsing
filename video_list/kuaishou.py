import json
import random
import re
import time

import requests
import video_list.kuaishou_home

class kuaishou_video:

    def __init__(self, url, ret_single=True, home=False):
        self.home = home
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]

        # 生成did参数
        did_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
        self.did = 'web_'
        for x in range(32):
            self.did += str(random.choice(did_arr))
        self.did = self.did.lower()

        # 生成didv参数
        self.didv = str(int(time.time())) + '000'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Cookie': f'clientid=3; did={self.did}; didv={self.didv}; clientid=3',

        }
        # print(json.dumps(self.headers))
        self.url = requests.get(url=url, headers=self.headers, stream=True).url
        # print(self.url)
        # 生成referer
        # if 'shareToken=' not in self.url:
        #     if '?' not in self.url:
        #         self.headers['Referer'] = self.url + '?shareToken=X-11111111111111'
        #     else:
        #         self.headers['Referer'] = self.url + '&shareToken=X-11111111111111'
        # else:
        #     self.headers['Referer'] = self.url
        self.headers['Referer'] = 'https://www.kuaishou.com?shareToken=X-11111111111111'
        # self.headers['Referer'] = 'https://www.kuaishou.com/short-video/3xvj2sbcjfp9xya?shareToken=X-11111111111111'
        # print(self.headers)
        # 获取一个id 用来在后面的json里定位

    def get_type(self, _json):
        # 判断视频的类型，（short-video类型的视频会重定向成photo的网站）
        # print(type(_json))
        # _json = json.loads(_json)
        # print(json.dumps(_json))
        self.data[0]['desc'] = _json['photo']['caption']
        if 'atlas' in _json:
            self.data[0]['type'] = 'images'
            try:
                self.get_photo_data(_json)
            except:
                try:
                    self.get_video_data(_json)
                except:
                    self.get_image_data(_json)
        else:
            self.data[0]['type'] = 'video'
            try:
                self.get_video_data(_json)
            except:
                try:
                    self.get_photo_data(_json)
                except:
                    self.get_image_data(_json)

    def get_photo_data(self, _json):
        # 写入图片数据
        # _json = json.loads(_json)

        self.data[0]['img'] = _json['photo']['webpCoverUrls'][0]['url']
        url_list = []
        url_head = _json['atlas']['cdn'][0]
        img_list = _json['atlas']['list']
        for img in img_list:
            url_list.append(f"https://{url_head}{img}")
        self.data[0]['url'] = str(url_list)

    def get_image_data(self, _json):
        self.data[0]['type'] = 'image'
        self.data[0]['url'] = _json['photo']['webpCoverUrls'][0]['url']
        self.data[0]['height'] = _json['photo']['height']
        self.data[0]['width'] = _json['photo']['width']

    def start(self):
        if self.home:
            return video_list.kuaishou_home.kuaishou_home(self.url).main()
        else:
            self.get_id()
            _json = self.get_josn()
            self.get_type(_json)

        return self.data

    def get_video_data(self, _json):
        # 写入视频数据
        # print(_json)
        # _json = json.loads(_json)

        self.data[0]['img'] = _json['photo']['coverUrls'][0]['url']
        self.data[0]['url'] = _json['photo']['mainMvUrls'][0]['url']
        self.data[0]['width'] = _json['photo']['width']
        self.data[0]['height'] = _json['photo']['height']
        return

    def get_josn(self):
        # 通过访问api获取json数据
        _json = {
            "photoId": self.id,

        }
        # print(self.id)
        # print(self.headers)
        url = "https://v.m.chenzhongtech.com/rest/wd/photo/info?kpn=KUAISHOU&captchaToken="
        data = requests.post(url=url, headers=self.headers, json=_json).text
        # if json.loads(data)['result'] != 1:
        #     self.headers['Cookie'] = self.cookie
        #     print(1)
        #     exit()
        # data = requests.post(url=url, headers=self.headers, json=_json).text
        # print(data)
        # print(data)

        return json.loads(data)

    def get_id(self):
        if 'video' in self.url:
            try:
                self.id = re.findall('video/(.*?)\?', self.url)[0]
            except:
                self.id = re.findall('video/(.*?)$', self.url)[0]
        elif 'photo' in self.url:
            self.url = requests.get(url=self.url, headers=self.headers).url
            self.id = re.findall('photo/(.*?)\?', self.url)[0]
        # print(self.id)


if __name__ == "__main__":
    url = 'https://www.kuaishou.com/short-video/3xf747wbnisk3e2'
    # url = "https://v.kuaishou.com/PPzsjV"
    # url = "https://www.kuaishou.com/short-video/3xkagse6bz97tma?fid=124316183&cc=share_copylink&followRefer=151&shareMethod=TOKEN&docId=9&kpn=NEBULA&subBiz=BROWSE_SLIDE_PHOTO&photoId=3xkagse6bz97tma&shareId=17468585439696&shareToken=X-9zH9Zlypb9z8dk&shareResourceType=PHOTO_OTHER&userId=3xu8zzpekz8w6hk&shareType=1&et=1_a%2F2002184874397155538_sl3909bl%24s&shareMode=APP&originShareId=17468585439696&appType=21&shareObjectId=5192931951275487254&shareUrlOpened=0&timestamp=1684185256224&utm_source=app_share&utm_medium=app_share&utm_campaign=app_share&location=app_share"
    # url = 'https://v.kuaishou.com/JNzmg1'
    ret_single = False
    print(json.dumps(kuaishou_video(url=url, ret_single=ret_single).start()))
