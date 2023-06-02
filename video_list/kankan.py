import requests
import re
import json


class kankan_news_video:
    def __init__(self, url, ret_single=True):
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

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url

    def get_data(self):
        _html = requests.get(url=self.url, headers=self.headers).text

        video_data = re.findall('window\.__NUXT__=(.*?);</script>', _html)[0]
        _desc = re.findall('<title>(.*?)</title>', _html)[0]
        _url = re.sub('\\\\u002F', '/', re.findall('play_url:"(.*?)"', video_data)[0])
        # _img = re.sub('\\\\u002F', '/', video_data.split('","')[-1].split('"')[0])

        self.data[0]['desc'] = _desc
        self.data[0]['url'] = _url
        # self.data[0]['img'] = _img
        return

    def start(self):
        self.get_data()

        return self.data


if __name__ == "__main__":
    url = "https://www.kankanews.com/detail/LMwVGgj402z"
    ret_single = False
    print(json.dumps(kankan_news_video(url=url, ret_single=ret_single).start()))
