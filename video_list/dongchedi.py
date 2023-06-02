import json
import re

import requests

import video_list.ixigua


class dongchedi_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'cookie': 'ttwid=1%7CoFg0M0UemvHQL9jX24gMN4L0yaWXSOfj-p6OsLxSpq0%7C1680751526%7Cc0ea06c75027551cb5886cf76ea649a255898c259438d18de005001ba82ce608',
        }
        # 获取id
        url = requests.get(url=url, headers=headers).url
        self.id = re.findall('video/(\d+)', url)[0]

    def start(self):
        # 把id拼接成西瓜的链接，去西瓜解析
        _url = f'https://www.ixigua.com/{self.id}'
        # print(_url)
        return video_list.ixigua.ixigua_video(url=_url, ret_single=self.ret_single).start()


if __name__ == '__main__':
    url = 'https://www.dongchedi.com/video/7217333362640290339'
    # while True:
    print(json.dumps(dongchedi_video(url).start()))
