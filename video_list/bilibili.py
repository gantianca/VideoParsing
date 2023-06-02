import json
import re

import requests

import path
import video_list.bilibili_home

class bilibili_video:
    def __init__(self, url, ret_single=True, home=False):
        self.home = home
        self.num = 0
        self.ret_single = ret_single
        self.data = []
        cookie = ""
        ROOTPATH = path.path().start()
        with open(f'{ROOTPATH}/cookies/bilibili_cookie.txt', 'r') as f:
            a = json.loads(f.read())
        for _data in a['cookie']:
            cookie += f"{_data['name']}={_data['value']};"
        self.headers = {
            'referer': 'https://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            # "cookie": "SESSDATA=27abe7d9%2C1687932094%2Ce2129%2Ac2;sid="
            "cookie": cookie
            # 需要一个cookie参数 从网页上看有效期半年
        }
        self.url = requests.get(url=url, headers=self.headers).url
        # print(self.url)
        self.have_top = False

    def get_bvid(self, url):
        # 获取bvid
        if 'BV' not in url:
            avid = re.findall("video/av(\d*)/", url)[0]
            data = requests.get(url=f'https://api.bilibili.com/x/web-interface/view?aid={avid}',
                                headers=self.headers).json()
            bvid = data['data']['bvid']
        else:
            bvid = re.findall("[\w.]*[\w:\-\+\%]", url)[3]
        return bvid

    def get_cid(self, bvid):
        # 通过bvid获取cid
        # 一部分数据也从这里拿
        data = requests.get(url=f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}', headers=self.headers).text
        try:
            cid_num = re.findall("p=(\d*)&", self.url)[0]
            cid = json.loads(data)['data']['pages'][int(cid_num)-1]['cid']
        except:
            cid = json.loads(data)['data']['pages'][0]['cid']
        self.desc = json.loads(data)['data']['title']
        self.img = json.loads(data)['data']['pic']
        return cid

    def get_json(self, bvid, cid, qn):
        # 通过bvid 和 cid 获取到json数据
        url = 'https://api.bilibili.com/x/player/playurl'
        params = {
            "bvid": bvid,
            "cid": cid,
            "qn": qn,
            "otype": "json",
            "fnval": 0,
            "fourk": 1,
            'high_quality': 1,
            "platform": "html5"
        }
        _json = json.loads(requests.get(url=url, headers=self.headers, params=params).text)
        print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 把数据写进json
        self.data[self.num]['url'] = f"{_json['data']['durl'][0]['url']}&referer=https://www.bilibili.com/"
        self.data[self.num]['url'] = re.sub("https://upos-sz-mirrorali\.bilivideo", "https://cn-sxxa-ct-03-02.bilivideo", self.data[self.num]['url'])
        self.data[self.num]['file_size'] = _json['data']['durl'][0]['size']

    def start(self):
        if self.home:
            return video_list.bilibili_home.bilibili_home(self.url).main()
        else:
            quality_list = {
                80: "1080p",
                64: "720p",
                16: "360p",
                6: "240p"
            }
            bvid = self.get_bvid(self.url)
            cid = self.get_cid(bvid)
            _json = self.get_json(bvid=bvid, cid=cid, qn="80")
            _quality = _json['data']['accept_quality']

            for _q in quality_list:
                if _q in _quality:
                    if 80 in _quality and 64 in _quality and _q == 64:
                        continue
                    self.data.append({
                        'desc': self.desc,
                        'url': '',
                        'file_size': '',
                        'width': '',
                        'height': '',
                        'img': self.img,
                        'type': 'video',
                        'quality_str': '',
                    })
                    _json = self.get_json(bvid=bvid, cid=cid, qn=_q)
                    self.get_data(_json)
                    self.data[self.num]['quality_str'] = quality_list[_q]
                    if not self.have_top:
                        self.data[self.num]['top_quality'] = True
                        self.have_top = True
                    if self.ret_single:
                        break
                    else:
                        self.num += 1
            # print(json.dumps(_json))
            return self.data


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/av974094859/?vd_source=0b76e3c53c0889a89cdd48cf892d3375'
    ret_single = False
    print(json.dumps(bilibili_video(url=url, ret_single=ret_single).start()))
