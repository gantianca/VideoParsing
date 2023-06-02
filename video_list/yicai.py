import requests
import re
import json
from lxml import etree


class yicai_video:
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
        self.url = url.replace('https', 'http')

    def get_data(self, url):
        # 数据都在源码里，通过xpath定位数据
        _html = requests.get(url=url, headers=self.headers).content
        rel = etree.HTML(_html)
        # self.data[0]['url'] = re.findall("playerbox','(.*)'", rel.xpath('//*[@class="playbtn"]/@onclick')[0])[0]
        self.data[0]['url'] = rel.xpath('//*[@class="prism-player"]/@data-videosrc')[0]

        if "m3u8" in self.data[0]['url']:
            self.data[0]['type'] = "m3u8"
            url_list = requests.get(url=self.data[0]['url'], headers=self.headers).text
            m3u8_data = re.sub('#EXTM3U', '', url_list)
            m3u8_data = re.sub('#EXT-X-VERSION:\d+', '', m3u8_data)
            m3u8_data = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data)
            m3u8_data = re.sub('#EXT-X-PLAYLIST-TYPE:VOD', '', m3u8_data)
            m3u8_data = re.sub('#EXTINF:\d+.\d+,', '', m3u8_data)
            m3u8_data = re.sub('#EXT-X-ENDLIST', '', m3u8_data)
            m3u8_data = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data).replace("..", "").split()
            # print(m3u8_data)

            self.data[0]['url'] = {
                "start": "https://ycalvod.yicai.com/record/live",
                "end": m3u8_data
            }
        self.data[0]['desc'] = rel.xpath('//*[@class="title f-pr"]/h1/text()')[0]
        self.data[0]['img'] = rel.xpath('//*[@class="m-poster"]/@src')[0]

    def start(self):
        self.get_data(self.url)

        return self.data


if __name__ == "__main__":
    url = "https://www.yicai.com/video/101663444.html"
    print(json.dumps(yicai_video(url).start()))