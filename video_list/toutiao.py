import json
import re

import requests

import video_list.ixigua


class toutiao_video:
    def __init__(self, url, ret_single=True):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'cookie': 'ttwid=1%7CoFg0M0UemvHQL9jX24gMN4L0yaWXSOfj-p6OsLxSpq0%7C1680751526%7Cc0ea06c75027551cb5886cf76ea649a255898c259438d18de005001ba82ce608',
        }
        url = requests.get(url=url, headers=headers).url
        if 'video' in url:
            self.true_id = re.findall('video/(\d*)',url)[0]
        elif 'article' in url:
            self.true_id = re.findall('article/(\d*)',url)[0]
        _html = requests.get(url=url, headers=headers).text
        # print(_html)
        try:
            self.id = re.findall('pseriesId%22%3A%22(\d+)%22%2C%22', _html)[0]
        except:
            self.id = self.true_id
        self.ret_single = ret_single

    def start(self):
        _url = f'https://www.ixigua.com/{self.id}'
        # print(_url)
        return video_list.ixigua.ixigua_video(url=_url, ret_single=self.ret_single, _id=self.true_id).start()


if __name__ == '__main__':
    url = 'https://m.toutiao.com/video/7233370165369733690/?app=news_article&timestamp=1684174895&share_uid=MS4wLjABAAAApdsd9ZKrNopbrVnZ950nGdufCxxK570JXoqa3Bw9lUg&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=04162bb4-09d4-4692-9b0f-40253fbcec29'
    # while True:
    print(json.dumps(toutiao_video(url).start()))
