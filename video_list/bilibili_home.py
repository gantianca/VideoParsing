import json
import os
import re
import time
import path
import queue
import threading

import requests


class bilibili_home:
    def __init__(self, url):
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
            "cookie": "SESSDATA=c0469110%2C1699345325%2Cfab11%2A51;sid="
            # "cookie": cookie
            # 需要一个cookie参数 从网页上看有效期半年
        }
        self.url = url
        self.task_list = queue.Queue()
        self.data_list = queue.Queue()

    def get_w_rid(self, api_data):
        # 获取w_rid，要调用js
        _path = f'{path.path().start()}/js/bilibili.js'
        command1 = 'node {0} "{1}"'.format(_path, api_data + "ce6d4422ece814c69d256fa9617e4acc")

        with os.popen(command1) as nodejs:
            w_rid = nodejs.read().replace('\n', '')

        return w_rid

    def get_page_data(self, mid, pn):
        # 解析每一页的数据
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51'
        }
        wts = int(time.time())
        api_data = f'keyword=&mid={mid}&order=pubdate&order_avoided=true&platform=web&pn={pn}&ps=30&tid=0&web_location=1550101&wts={wts}'
        w_rid = self.get_w_rid(api_data)
        api_url = f'https://api.bilibili.com/x/space/wbi/arc/search?{api_data}&w_rid={w_rid}'  # 接口地址
        data = requests.get(url=api_url, headers=headers).json()
        video_list = data['data']['list']['vlist']

        for video_data in video_list:
            # 任务列表
            self.task_list.put(video_data)

        print(self.task_list.qsize())
        count = data['data']['page']['count']

        if pn * 30 < count and self.task_list.qsize() < 1000:
            pn += 1
            self.get_page_data(mid, pn)

    def do_jiexi(self):
        while True:
            try:
                data = self.task_list.get(timeout=1)
                self.jiexi(data)
            except:
                break

    def jiexi(self, video_data):
        _img = video_data['pic']
        _desc = video_data['title']
        # aid = video_data['aid']
        bvid = video_data['bvid']
        cid = self.get_cid(bvid)
        _json = self.get_json(bvid, cid, qn=80)
        _url = f"{_json['data']['durl'][0]['url']}&referer=https://www.bilibili.com/"
        _url = re.sub("https://upos-sz-mirrorali\.bilivideo", "https://cn-sxxa-ct-03-02.bilivideo", _url)
        _size = _json['data']['durl'][0]['size']
        self.data_list.put({
            'desc': _desc,
            'url': _url,
            'file_size': _size,
            'width': '',
            'height': '',
            'img': _img,
            'type': 'video',
        })

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
        # print(json.dumps(_json))
        return _json

    def get_cid(self, bvid):
        # 获取cid
        data = requests.get(url=f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}').json()
        cid = data['data']['pages'][0]['cid']
        # print(cid)
        return cid

    def main(self):
        mid = re.findall('space\.bilibili\.com/(\d+)', self.url)[0]

        self.get_page_data(mid, pn=1)
        th_list = []
        for _ in range(10):
            th_list.append(threading.Thread(target=self.do_jiexi))
        for a in th_list:
            a.start()
        for b in th_list:
            b.join()

        while True:
            try:
                data = self.data_list.get(timeout=1)
                self.data.append(data)
            except:
                break
        return self.data


if __name__ == '__main__':
    url = "https://space.bilibili.com/14444480/video"
    print(json.dumps(bilibili_home(url).main()))
