import json
import re
import time

import yaml
import yt_dlp

import path


class youtube_video:
    def __init__(self, url, ret_single=True):
        self.have_top = False
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        url = url.strip()
        if '&list' in url or '?list' in url:
            self.url = re.findall('(.*?)[&?]list', url)[0]
        else:
            self.url = url

        ROOTPATH = path.path().start()
        try:
            with open(f'{ROOTPATH}/config.yaml', "r", encoding='utf-8') as f:
                text = f.read()
                # print(text)
                text = yaml.load(text, Loader=yaml.FullLoader)['porxy']
                if text:
                    data = text
                    if 'http' in data and 'https' in data:
                        self.proxies = data['http']
                    else:
                        self.proxies = ''
                else:
                    self.proxies = ''
        except:
            self.proxies = ''

        # self.url = requests.get(url=url, headers=self.headers, proxies={
        #     "http": "127.0.0.1:7890",
        #     "https": "127.0.0.1:7890"
        # }).url
        # print(a)
        # print(self.proxies)
        # self.proxies = "http://127.0.0.1:10001"

    def yt_dlp(self):
        # 调用yt-dlp这个库来获取视频信息
        ydl = yt_dlp.YoutubeDL({'cachedir': False, 'quiet': True, 'proxy': self.proxies})
        result = ydl.extract_info(self.url, download=False)
        # print(json.dumps(result))
        return result

    def get_data(self, _json):
        # 写入数据
        quality_list = {
            '571': '8k',
            '313': '4k',
            '401': '4k',
            '271': '1440p',
            '400': '1440p',
            '248': '1080p',
            '137': '1080p',
            '399': '1080p',
        }
        over_list = []
        _desc = _json['title']
        _img = _json['thumbnail']

        for data in _json['formats']:
            if data['format_id'] == '22':
                self.into_data(_desc, _img, data)
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True
                if self.ret_single:
                    return
                else:
                    self.num += 1
            if data['format_id'] == '251':
                audio_url = data['url']
        for data in _json['formats']:
            if data['format_id'] == '18':
                self.into_data(_desc, _img, data)
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True
                if self.ret_single:
                    return
                else:
                    self.num += 1
            if data['format_id'] == '251':
                audio_url = data['url']
        for data in _json['formats']:
            if data['format_id'] in quality_list:
                if quality_list[data['format_id']] not in over_list:
                    self.into_data(_desc, _img, data)
                    video_url = self.data[self.num]['url']
                    _url = {
                        'video': video_url,
                        'sound': audio_url
                    }
                    self.data[self.num]['url'] = _url
                    over_list.append(quality_list[data['format_id']])
                    self.data[self.num]['type'] = 'split'
                    self.num += 1
        return

    def into_data(self, _desc, _img, data):
        self.data.append({
            'desc': _desc,
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': _img,
            'type': 'video',
        })
        self.data[self.num]['url'] = data['url']
        self.data[self.num]['file_size'] = data['filesize']
        self.data[self.num]['width'] = data['width']
        self.data[self.num]['height'] = data['height']

    def start(self):
        try:
            return self._start()
        except yt_dlp.utils.DownloadError:
            # print("解析出错")
            time.sleep(3)
            try:
                # print("第一次重试")
                return self._start()
            except yt_dlp.utils.DownloadError:
                # print("解析出错")
                time.sleep(10)
                try:
                    # print("第二次重试")
                    return self._start()
                except yt_dlp.utils.DownloadError:
                    # print("解析出错")
                    time.sleep(30)
                    # print("第三次重试")
                    return self._start()

    def _start(self):
        _json = self.yt_dlp()
        self.get_data(_json)
        return self.data


if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=4vZoPlBWq7g&list=PL20CSEl4nCwCnn8uAfUTz3aa3u8yZ6i1z&index=4"
    # url = 'https://youtube.com/shorts/qKI-VCGshnY?feature=share'
    url = "https://www.youtube.com/watch?v=lPG2ZFpEWBs"
    # url = 'https://www.instagram.com/reel/CpAgIYEpJSd/'
    ret_single = False
    print(json.dumps(youtube_video(url=url, ret_single=ret_single).start()))
