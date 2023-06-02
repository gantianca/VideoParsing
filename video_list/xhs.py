import requests
import re
import json

import path


class xhs_video:
    def __init__(self, url, ret_single=True):
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'images',
        }]
        # 读取cookie
        self.ROOTPATH = path.path().start()
        with open(f'{self.ROOTPATH}/cookies/xhs_cookie.txt', 'r') as f:
            a = json.loads(f.read())
        for _data in a['cookie']:
            if _data['name'] == 'web_session':
                web_session = _data['value']
            elif _data['name'] == 'webId':
                webId = _data['value']

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
            'cookie': f'webId={webId};web_session={web_session}',

        }
        # print(self.headers)
        self.url = requests.get(url=url, headers=self.headers).url

    def get_json(self, url):
        # 从源码里获取json数据

        _html = requests.get(url=url, headers=self.headers).text
        # print(_html)
        with open(f'{self.ROOTPATH}/logs/xhs.log', 'a', encoding='utf-8') as f:
            f.write(f"请求的headers：\n{self.headers}\n")
            f.write(f"请求到的html数据：\n{_html}\n")
        _data = re.findall('window\.__INITIAL_STATE__=(.*?)</script>', _html)[0]
        _data = re.sub('undefined', 'null', _data)
        # print(_data)
        _json = json.loads(_data)
        return _json

    def get_data(self, _json):
        # 处理数据
        _type = _json['note']['note']['type']
        _desc = _json['note']['note']['title']
        # print(json.dumps(_json))
        # 判断类型
        if _type == "video":

            self.data[0]['type'] = "video"
            self.data[0][
                'img'] = f"https://ci.xiaohongshu.com/{_json['note']['note']['imageList'][0]['traceId']}?imageView2/webp"
            self.data[0][
                'url'] = f"http://sns-video-bd.xhscdn.com/{_json['note']['note']['video']['consumer']['originVideoKey']}"
            # self.data[0]['width'] = _json['note']['note']['video']['media']['stream']['h264'][0]['width']
            # self.data[0]['height'] = _json['note']['note']['video']['media']['stream']['h264'][0]['height']
            # self.data[0]['file_size'] = _json['note']['note']['video']['media']['stream']['h264'][0]['size']
            header = requests.get(url=self.data[0]['url'], stream=True).headers
            self.data[0]['file_size'] = header['Content-Length']
            # print(header)
        else:

            self.data[0]['type'] = "images"
            url_list = []
            data_list = _json['note']['note']['imageList']
            # if len(data_list) > 1:
            #     self.data[0]['type'] = "images"
            # else:
            #     self.data[0]['type'] = "image"
            for _data in data_list:
                url = f"https://ci.xiaohongshu.com/{_data['traceId']}?imageView2/webp"
                url_list.append(url)
            self.data[0]['url'] = url_list

        self.data[0]['desc'] = _desc
        return

    def start(self):
        _json = self.get_json(self.url)
        self.get_data(_json)

        return self.data


if __name__ == "__main__":
    url = "http://xhslink.com/CaFdmq"
    # url = 'https://www.xiaohongshu.com/explore/63e8bf22000000000703b6c2'
    ret_single = False
    print(json.dumps(xhs_video(url=url, ret_single=ret_single).start()))
