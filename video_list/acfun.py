import json
import re

import requests


class acfun_video:
    def __init__(self, url, ret_single=True):
        self.num = 0
        self.ret_single = ret_single
        self.url_data = {}
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.url = url
        self.have_top = False

    def get_json(self, url):
        # 从源码里获取到json数据
        _html = requests.get(url=url, headers=self.headers).text
        _json = re.findall('window.videoInfo = (.*);', _html)[0]
        # print(_json)
        _json = json.loads(_json)
        return _json

    def get_data(self, _json):
        # 写入数据
        _desc = _json['title']
        _img = _json['coverUrl']

        # 获取到包含m3u8地址的文件和对应清晰度的数据
        url_data = json.loads(_json['currentVideoInfo']['ksPlayJson'])
        # print(json.dumps(url_data))

        for _data in url_data['adaptationSet'][0]['representation']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })

            self.data[self.num]['file_size'] = _json['currentVideoInfo']['transcodeInfos'][self.num]['sizeInBytes']
            self.data[self.num]['width'] = _data['width']
            self.data[self.num]['height'] = _data['height']
            # self.url_data['start'] = 'https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/'
            # self.url_data['start'] = re.findall('(.*/)', _data['url'])[0]
            #
            # m3u8_data_url = _data['url']
            # # print(m3u8_data_url)
            # m3u8_data = requests.get(url=m3u8_data_url).text
            # m3u8_data = re.sub('#EXTM3U', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-VERSION:\d+', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-PLAYLIST-TYPE:VOD', '', m3u8_data)
            # m3u8_data = re.sub('#EXTINF:\d+.\d+,', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-ENDLIST', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data).split()
            # self.url_data['end'] = m3u8_data
            # self.data[self.num]['url'] = self.url_data
            self.data[self.num]['url'] = _data['url']
            self.data[self.num]['type'] = 'm3u8'
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            self.num += 1
        return

    def start(self):
        _json = self.get_json(url=self.url)
        self.get_data(_json)
        return self.data


if __name__ == '__main__':
    # url = 'https://www.acfun.cn/v/ac40703140'
    url = "https://www.acfun.cn/v/ac41278541"
    ret_single = False
    print(json.dumps(acfun_video(url=url, ret_single=ret_single).start()))
