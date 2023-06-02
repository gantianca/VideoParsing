import json
import random
import re
import time

import requests
import yaml

import path


class tiktok_video:
    def __init__(self, url, ret_single=True):
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        # 代理地址
        # self.proxies = {
        #     "http": "127.0.0.1:7890",
        #     "https": "127.0.0.1:7890"
        # }
        ROOTPATH = path.path().start()
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
        self.url = url
        # print(self.url)
        # print(self.proxies)

    def get_id(self, url):
        # 获取视频的 item_id
        try:
            id = re.findall("video/(\d*)", url)[0]
        except:
            url = requests.get(url=url, headers=self.headers, proxies=self.proxies).url
            try:
                id = re.findall("video/(\d*)", url)[0]
            except:
                id = re.findall("item_id=(\d*)", url)[0]
        # print(id)
        return id

    def get_json(self, id):
        # 通过视频的item_id和生成的参数 访问api获取josn数据
        openudid = ''.join(random.sample('0123456789abcdef', 16))
        uuid = ''.join(random.sample('01234567890123456', 16))
        ts = int(time.time())
        url = f'https://api-h2.tiktokv.com/aweme/v1/feed/?aweme_id={id}&version_name=26.1.3&version_code=2613&build_number=26.1.3&manifest_version_code=2613&update_version_code=2613&{openudid}=6273a5108e49dfcb&uuid={uuid}&_rticket=1667123410000&ts={ts}&device_brand=Google&device_type=Pixel%204&device_platform=android&resolution=1080*1920&dpi=420&os_version=10&os_api=29&carrier_region=US&sys_region=US%C2%AEion=US&app_name=trill&app_language=en&language=en&timezone_name=America/New_York&timezone_offset=-14400&channel=googleplay&ac=wifi&mcc_mnc=310260&is_my_cn=0&aid=1180&ssmix=a&as=a1qwert123&cp=cbfhckdckkde1'
        _json = requests.get(url=url, headers=self.headers, proxies=self.proxies).json()
        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 写入数据
        video_data = _json['aweme_list'][0]
        self.data[0]['desc'] = video_data['desc']
        self.data[0]['url'] = video_data['video']['play_addr']['url_list'][0]
        self.data[0]['width'] = video_data['video']['play_addr']['width']
        self.data[0]['height'] = video_data['video']['play_addr']['height']
        self.data[0]['file_size'] = video_data['video']['play_addr']['data_size']
        self.data[0]['img'] = video_data['video']['cover']['url_list'][-1]
        return

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
        self.get_data(_json)
        return self.data


if __name__ == '__main__':
    url = 'https://www.tiktok.com/t/ZTRWd9KQM/'
    print(json.dumps(tiktok_video(url).start()))
