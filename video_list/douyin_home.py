import json
import os
import re
import time
import urllib.parse
import path
import requests


class douyin_home:
    def __init__(self, url):
        self.url = url
        self.data = []
        pass

    def get_XBogus(self, url, user_agent):
        # 生成XBogus参数
        _path = f'{path.path().start()}/js/X-Bogus.js'
        query = urllib.parse.urlparse(url).query

        command1 = 'node {0} "{1}" "{2}"'.format(_path, query, user_agent)
        with os.popen(command1) as nodejs:
            xbogus = nodejs.read().replace('\n', '')

        return xbogus

    def get_data(self, _id, max_cursor):
        api = f'https://www.douyin.com/aweme/v1/web/aweme/post/?aid=6383&sec_user_id={_id}&max_cursor={max_cursor}&count=40&publish_video_strategy_type=2'  # 构造获取数据的链接
        headers = {
            'Referer': f'https://www.douyin.com/user/{_id}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42'
        }

        xbogus = self.get_XBogus(api, headers['User-Agent'])

        new_api = api + f'&X-Bogus={xbogus}'

        # print(new_api)

        for _ in range(10):
            try:
                data = requests.get(url=new_api, headers=headers).json()
                break
            except:
                time.sleep(1)
                xbogus = self.get_XBogus(api, headers['User-Agent'])

                new_api = api + f'&X-Bogus={xbogus}'
        try:
            self.into_data(data)
        except:
            pass
        new_max_cursor = data['max_cursor']  # 获取下一个访问的链接需要的参数
        has_more = data['has_more']  # 判断是否有下一页的值
        # print(new_max_cursor)
        # print(has_more)
        print(len(self.data))
        if int(has_more) == 1 and len(self.data) <= 1000:
            time.sleep(1)
            self.get_data(_id, new_max_cursor)

    def into_data(self, data):
        # 解析数据
        for video_data in data['aweme_list']:
            try:
                _desc = video_data['desc']
                _img = video_data['video']['cover']['url_list'][-1]
                for _data in video_data['video']['bit_rate']:
                    _url = _data['play_addr']['url_list'][0]
                    _size = _data['play_addr']['data_size']
                    _height = _data['play_addr']['height']
                    _width = _data['play_addr']['width']
                    self.data.append({
                        'desc': _desc,
                        'url': _url,
                        'file_size': _size,
                        'width': _width,
                        'height': _height,
                        'img': _img,
                        'type': 'video',
                    })
                    break
            except:
                continue

    def main(self):
        if '?' in self.url:
            _id = re.findall('user/(.*?)\?', self.url)[0]
        else:
            _id = re.findall('user/(.*?)$', self.url)[0]
        # print(_id)
        self.get_data(_id=_id, max_cursor=0)

        # print(len(self.data))
        return self.data


if __name__ == '__main__':
    # _id = 'MS4wLjABAAAASuSQvniHZ6QNuhl01srEFcasVKn2jFEmVSkTQ3cUrs8'
    # max_cursor = 0
    # douyin_home().get_data(_id, max_cursor)
    url = 'https://www.douyin.com/user/MS4wLjABAAAAG32NmKFR-vWIbVId3Kyrq-z7JoWsNMB9UNv9vkEY7ks'
    print(json.dumps(douyin_home(url).main()))
