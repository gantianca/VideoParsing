import base64

import requests
import re
import json


class mandaoo_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.data = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68',
        }
        self.url = url

    def get_data(self):
        # 获取视频的数据
        page = int(re.findall('/((\d+-)*?\d+)\.html', self.url)[0][0].split('-')[-1]) + 1
        # print(page)

        _html = requests.get(url=self.url, headers=self.headers)
        _html.encoding = 'utf-8'
        _html = _html.text
        _desc = re.findall('<title>(.*?) - 漫岛动漫</title>', _html)[0]

        b64_data = re.findall('VideoInfoList=base64decode\("(.*?)"\)', _html)[0]

        # 获取视频的vid和类型
        vid, _type, x = re.findall(f'第{page}集\\$(.*?)\\$(.*?)([$#]|$)', base64.b64decode(b64_data).decode())[0]

        # 解析不同类型的数据
        if _type == 'mp4':
            url = self.get_mp4(vid)
            video_type = 'video'
        elif _type == 'm3u8':
            url = vid
            video_type = 'm3u8'

        self.data.append({
            'desc': _desc,
            'url': url,
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': video_type,
        })

    def get_mp4(self, vid):
        # mp4类型视频的地址的获取
        api_url = f"https://www.mandaoo.com/templets/player/player_php/aixixi.php?vid={vid}"
        api_headers = {
            'referer': 'https://www.mandaoo.com/templets/player/mp4.html'
        }

        _data = requests.get(url=api_url, headers=api_headers).text
        # print(_data)

        video_data = re.findall('video: ({[\s\S]*?}),\s*}\);', _data)[0]

        url = re.findall("url: '(.*?)'", video_data)[0]

        # print(url)
        return url

    def get_m3u8(self, vid):
        # m3u8类型视频的获取
        url_1 = vid
        print(url_1)
        data_1 = requests.get(url=url_1, headers=self.headers).text
        data_1 = self.m3u8_jiexi(data_1)[0]
        url_2 = re.sub('index\.m3u8', data_1, url_1)
        # print(url_2)
        data_2 = requests.get(url=url_2, headers=self.headers).text
        data_2 = self.m3u8_jiexi(data_2)

        url = {
            'start': re.sub('index\.m3u8', '', url_2),
            'end': data_2
        }

        # print(url)
        return url

    def m3u8_jiexi(self, m3u8_data):
        # 对m3u8类型数据解析的函数
        m3u8_data = re.sub('#EXTM3U', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-VERSION:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-PLAYLIST-TYPE:VOD', '', m3u8_data)
        m3u8_data = re.sub('#EXTINF:\d+.\d+,', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-ENDLIST', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-X-VERSION:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-X-VCODEC:\d+\.\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-X-ACODEC:\d+\.\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-X-FORMAT:HLS-TS', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-FILESTARTTIME:\d+\.\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-VIDEO-WIDTH:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-VIDEO-HEIGHT:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-MGTV-File-SIZE:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-STREAM-INF:PROGRAM-ID=\d+,BANDWIDTH=\d+,RESOLUTION=\d+x\d+', '', m3u8_data)

        m3u8_data = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data).split()

        return m3u8_data

    def start(self):
        self.get_data()

        return self.data


if __name__ == "__main__":
    # _url = "https://www.mandaoo.com/man_v/13881-0-2.html"
    _url = "https://www.mandaoo.com/man_v/12272-0-2.html"
    ret_single = False
    print(json.dumps(mandaoo_video(url=_url, ret_single=ret_single).start()))
