import requests
import re
import json


class taobao_video:
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
            'cookie': 'cna=1'
        }
        self.url = url

    def get_html(self, url):
        # 获取id 然后通过id去另一个淘宝的页面获取源码。这里可以更容易获取到视频数据，甚至不需要登录
        if 'id=' in url:
            _id = re.findall('[&?]id=(\d+)', url)[0]
        else:
            # 处理短链接
            t_url = re.findall("var url = '(.*?)';", requests.get(url=url, headers=self.headers).text)[0]
            t_url = requests.get(url=t_url, headers=self.headers).url
            # print(t_url)
            _id = re.findall('[&?]id=(\d+)', t_url)[0]
        n_url = f'https://world.taobao.com/item/{_id}.htm'
        _html = requests.get(url=n_url, headers=self.headers).text
        return _html

    def get_data(self, _html):
        # 解析html数据
        _desc = re.sub(' - Taobao', '', re.findall('<title>(.*?)</title>', _html)[0])
        url = re.findall('<video[\s\S]*?src="(.*?)"', _html)[0]

        self.data[0]['desc'] = _desc
        self.data[0]['url'] = url
        return

    def start(self):
        _html = self.get_html(self.url)
        self.get_data(_html)

        return self.data


if __name__ == "__main__":
    url = "https://detail.tmall.com/item.htm?ali_refid=a3_430582_1006:1367680078:N:FWhk09A41iS561PkW96CMg==:d82b41a0afcdd3434536108e7b632bf2&ali_trackid=1_d82b41a0afcdd3434536108e7b632bf2&id=639687651409&spm=a230r.1.14.1"
    ret_single = False
    print(json.dumps(taobao_video(url=url, ret_single=ret_single).start()))
