import requests
import re
import json


class jd_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.data = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url

    def get_data(self):
        res = requests.get(url=self.url, headers=self.headers)
        _html = res.text
        vid = re.findall('"mainVideoId":\s*"(\d+)"', _html)[0]
        api_url = 'https://api.m.jd.com/ware/image/getPlayUrl?appid=m_core&functionId=image_getPalyUrl&body={"externalLoginType":1,"callback":"videoUrlCB","type":"1","vid":"' + vid + '","sceneval":"2"}'
        self.headers['referer'] = 'https://item.m.jd.com/'
        data = requests.get(url=api_url, headers=self.headers).json()
        # print(json.dumps(data))
        _desc = re.findall('<title>(.*?)</title>', _html)[0]
        _img = data['result']['imageUrls'][0]
        _size = data['result']['videoSize']
        _url = data['result']['data'][-1]['main_url']

        self.data.append({
            'desc': _desc,
            'url': _url,
            'file_size': _size,
            'width': '',
            'height': '',
            'img': _img,
            'type': 'video',
        })

        return

    def start(self):
        self.get_data()

        return self.data


if __name__ == "__main__":
    url = "https://item.jd.com/100035486759.html"
    ret_single = False
    print(json.dumps(jd_video(url=url, ret_single=ret_single).start()))
