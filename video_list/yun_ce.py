import requests
import re
import json
from lxml import etree


class yun_ce_video:
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
        if "/cen/" in self.url:
            self.data[0]['url'] = rel.xpath('//*[@class="mdysp"]/video/@src')[0]
            self.data[0]['desc'] = rel.xpath('//*[@class="article"]/h3/text()')[0]
            if not self.data[0]['url']:
                self.data[0]['url'] = rel.xpath('//*[@controls="controls"]/@src')[0]
        else:
            try:
                self.data[0]['desc'] = rel.xpath('//*/article/h2/text()')[0]
            except:
                self.data[0]['desc'] = rel.xpath('/html/body/div[3]/div[1]/h3/text()')[0]
            # print(self.data[0]['desc'])
            try:
                self.data[0]['url'] = rel.xpath('//*[@controls="controls"]/@src')[0]
            except:
                try:
                    self.data[0]['url'] = rel.xpath('//*[@class="content"]/@src')[0]
                except:
                    self.data[0]['url'] = rel.xpath('//*/video/@src')[0]
        try:
            self.data[0]['quality_str'] = re.findall('(\d*?p)\.mp4', self.data[0]['url'])[0]
        except:
            pass

    def start(self):
        self.get_data(self.url)

        return self.data


if __name__ == "__main__":
    # url = "http://district.ce.cn/zg/202209/30/t20220930_38138450.shtml"
    url = "http://yun.ce.cn/gj/202302/15/t20230215_38394149.shtml"
    print(json.dumps(yun_ce_video(url).start()))