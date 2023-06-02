import json
import re

import requests


class zhihu_video:

    def __init__(self, url, ret_single=True):
        self.num = 0
        self.ret_single = ret_single
        self.data = []
        # self.url = url
        self.head_url = 'https://lens.zhihu.com/api/v4/videos/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.url = requests.get(url=url, headers=self.headers).url
        self.have_top = False
        return

    def start(self):
        # 获取存储了需要的数据的地址的函数

        rel = requests.get(url=self.url, headers=self.headers)
        # 知乎有两种有视频的页面，一种是发视频的页面，一种是回答别人时引用视频的页面
        # 从源码中获取标题和地址尾部
        if 'zhuanlan' in self.url:
            ids = re.findall('data-lens-id="(\d+)"', rel.text)
            self.ti = re.findall('<title.*?>(.*?) - 知乎</title>', rel.text)[0]
            # print(ids)
            for _id in ids:
                url = self.head_url + _id
                self.get_data(url)
            return self.data
        if 'answer' in self.url:
            self.ti = rel.text.split('VideoAnswerPlayer-state--title">')[1].split('</div>')[0]
            url_end = rel.text.split('"attachmentId":"')[1].split('","')[0]
        elif 'pin' in self.url:
            self.ti = re.findall('{"content":"(.*?)<', rel.text)[0]
            url_end = re.findall('"videoId":"(\d*?)"', rel.text)[0]
        else:
            self.ti = rel.text.split('<title data-rh="true">')[1].split('- 知乎')[0]
            url_end = rel.text.split('{"videoId":"')[1].split('","')[0]
        # 对地址进行拼接
        url = self.head_url + url_end
        # print(url_end)
        self.get_data(url)
        return self.data

    def get_data(self, url):
        # 从地址中获取需要数据的函数
        # print(url)
        rel = requests.get(url=url, headers=self.headers)
        # print(json.dumps(rel.json()))
        topic = rel.json()['cover_url']
        if self.ret_single:
            self.data.append({
                'desc': self.ti,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': topic,
                'type': 'video',
            })
            # 从FHD开始获取最高清的视频地址和数据
            if 'FHD' in rel.json()['playlist']:
                data_url = rel.json()['playlist']['FHD']['play_url']
                height = rel.json()['playlist']['FHD']['height']
                width = rel.json()['playlist']['FHD']['width']
                # duration = rel.json()['playlist']['FHD']['duration']
                size = rel.json()['playlist']['FHD']['size']
            elif 'HD' in rel.text:
                data_url = rel.json()['playlist']['HD']['play_url']
                height = rel.json()['playlist']['HD']['height']
                width = rel.json()['playlist']['HD']['width']
                # duration = rel.json()['playlist']['HD']['duration']
                size = rel.json()['playlist']['HD']['size']
            else:
                data_url = rel.json()['playlist']['SD']['play_url']
                height = rel.json()['playlist']['SD']['height']
                width = rel.json()['playlist']['SD']['width']
                # duration = rel.json()['playlist']['SD']['duration']
                size = rel.json()['playlist']['SD']['size']

            # 把获取到的数据写入
            self.data[0]['url'] = data_url
            self.data[0]['file_size'] = size
            self.data[0]['width'] = width
            self.data[0]['height'] = height
        else:
            for item in rel.json()['playlist'].items():
                self.data.append({
                    'desc': self.ti,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': topic,
                    'type': 'video',
                })
                self.data[self.num]['url'] = item[1]['play_url']
                self.data[self.num]['file_size'] = item[1]['size']
                self.data[self.num]['width'] = item[1]['width']
                self.data[self.num]['height'] = item[1]['height']
                if 'FHD' in rel.json()['playlist']:
                    if not self.have_top:
                        self.data[self.num]['top_quality'] = True
                        self.have_top = True
                if 'HD' in rel.json()['playlist']:
                    if not self.have_top:
                        self.data[self.num]['top_quality'] = True
                        self.have_top = True

                self.num += 1

        return


if __name__ == '__main__':
    url = 'https://www.zhihu.com/pin/1636637379783122944'
    ret_single = False
    print(json.dumps(zhihu_video(url=url, ret_single=ret_single).start()))
