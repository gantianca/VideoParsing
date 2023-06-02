import random
import urllib.parse

import requests
import re
import json

import video_list.ixigua
import video_list.douyin_home
# import path


class douyin_video:
    def __init__(self, url, ret_single=True, home=False):
        self.home = home
        self.ret_single = ret_single
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]
        # cookie = ""
        # ROOTPATH = path.path().start()
        # with open(f'{ROOTPATH}/cookies/douyin_cookie.txt', 'r') as f:
        #     a = json.loads(f.read())
        # for _data in a['cookie']:
        #     # cookie += f"{_data['name']}={_data['value']};"
        #     if _data['name'] == 's_v_web_id':
        #         s_v_web_id = _data['value']
        #         break
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'referer': 'https://cn.bing.com/',

        }
        # print(self.headers)
        if 'modal_id=' in url:
            _id = re.findall('modal_id=(\d+)', url)[0]
            self.url = f'https://www.douyin.com/video/{_id}'
        else:
            self.url = requests.get(url=url, headers=self.headers, stream=True).url
            self.url = requests.get(url=self.url, headers=self.headers, stream=True).url

        # print(self.url)

    def get_ac_nonce(self):
        # 获取ac_nonce 参数
        key_list = '1234567890abcde'
        _ac_data = ''
        for _ in range(21):
            _ac_data += key_list[random.randint(0, len(key_list)-1)]

        return _ac_data

    def get_ttwid(self):
        # 获取 ttwid 参数
        url = "https://ttwid.bytedance.com/ttwid/union/register/"
        _json = {"region": "cn", "aid": 1768, "needFid": False, "service": "www.ixigua.com",
               "migrate_info": {"ticket": "", "source": "node"}, "cbUrlProtocol": "https", "union": True}
        tt = requests.post(url=url, json=_json).headers['Set-Cookie']
        tt_data = re.findall('ttwid=(.*?);', tt)[0]
        return tt_data

    def get_type(self):
        # 判断视频的类型
        url = self.url
        if 'video' in url:
            self.data[0]['type'] = "video"
            _id = re.findall('video/(\d*)', self.url)[0]
            self.url = f"https://www.douyin.com/video/{_id}"
        elif 'note' in url:
            self.data[0]['type'] = "images"

    def get_json(self):
        # 从源码里获取到数据
        _html = requests.get(url=self.url, headers=self.headers).text
        # print(_html)
        _json = json.loads(urllib.parse.unquote(re.findall('">(.*?)</script>', _html)[0]))
        # print(json.dumps(_json))
        return _json

    def get_video_data(self, _json):
        # 写入视频数据
        num = list(_json.keys())[1]
        if 'aweme' in _json[num]:
            self.data[0]['desc'] = _json[num]['aweme']['detail']['desc']
            self.data[0]['url'] = f"http:{_json[num]['aweme']['detail']['video']['playAddr'][0]['src']}"
            self.data[0]['width'] = _json[num]['aweme']['detail']['video']['width']
            self.data[0]['height'] = _json[num]['aweme']['detail']['video']['height']
            self.data[0]['img'] = _json[num]['aweme']['detail']['video']['coverUrlList'][0]
        else:
            self.data[0]['desc'] = _json[num]['post']['data'][0]['desc']
            self.data[0]['url'] = f"http:{_json[num]['post']['data'][0]['video']['playAddr'][0]['src']}"
            self.data[0]['width'] = _json[num]['post']['data'][0]['video']['width']
            self.data[0]['height'] = _json[num]['post']['data'][0]['video']['height']
            self.data[0]['img'] = _json[num]['post']['data'][0]['video']['coverUrlList'][0]

    def get_note_data(self, _json):
        # 写入图片数据
        num = list(_json.keys())[1]
        self.data[0]['desc'] = _json[num]['aweme']['detail']['desc']
        self.data[0]['img'] = _json[num]['aweme']['detail']['video']['coverUrlList'][0]
        img_list = _json[num]['aweme']['detail']['images']
        url_list = []
        for img in img_list:
            url_list.append(img['urlList'][-1])
        self.data[0]['url'] = url_list

    def start(self):
        if self.home:
            if 'user' in self.url:
                return video_list.douyin_home.douyin_home(url=self.url).main()
            else:
                raise
        else:
            if 'user' in self.url:
                raise
            else:
                pass
        # print(self.url)
        if 'ixigua.com' in self.url:
            _id = re.findall('video/(\d+)', self.url)[0]
            t_url = f'https://www.ixigua.com/{_id}'
            return video_list.ixigua.ixigua_video(url=t_url, ret_single=self.ret_single).start()

        self.get_type()
        _json = self.get_json()
        # print(json.dumps(_json))

        if self.data[0]['type'] == "video":
            self.get_video_data(_json)
        elif self.data[0]['type'] == "images":
            self.get_note_data(_json)

        return self.data


if __name__ == "__main__":
    url = 'https://www.douyin.com/user/MS4wLjABAAAAa_K5cMgCWyHyBi-6-oRnaYinPFaBJhGv48Z9ZKwbYfU'
    # url = 'https://www.douyin.com/note/7037827546599263488'
    ret_single = False
    home = True
    print(json.dumps(douyin_video(url=url, ret_single=ret_single, home=home).start()))
