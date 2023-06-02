import requests
import re
import json


class m_baidu_video:
    def __init__(self, url, ret_single=True):

        self.data = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.url = url

    def get_data(self):
        _html = requests.get(url=self.url, headers=self.headers)
        _html.encoding = 'utf-8'
        _html = _html.text
        _data = json.loads(re.findall('(\{"data":\{"summaryList":\[].*?})</script>', _html)[0])['data'][
            'mcpInvokeInfoData']
        _desc = _data['title']
        _img = _data['posterImage']
        _url = _data['videoUrl']
        _width = _data['videoWidth']
        _height = _data['videoHeight']

        self.data.append({
            'desc': _desc,
            'url': _url,
            'file_size': '',
            'width': _width,
            'height': _height,
            'img': _img,
            'type': 'video',
        })

    def start(self):
        self.get_data()

        return self.data


if __name__ == "__main__":
    url = "https://m.baidu.com/video/page?pd=video_page&nid=589869654124437213&sign=&word=%E6%88%91%E5%9C%A8%E9%BB%91%E8%89%B2%E5%8D%9A%E7%89%A9%E9%A6%86%E4%BD%93%E9%AA%8C%E7%B2%BE%E7%A5%9E%E7%97%85%E4%BA%BA%E7%9A%84%E7%9C%9F%E5%AE%9E%E7%94%9F%E6%B4%BB%EF%BC%9A%E7%94%9F%E8%80%8C%E4%B8%BA%E4%BA%BA%EF%BC%8C%E4%B8%8D%E5%BF%85%E6%8A%B1%E6%AD%89%EF%BC%8C%E4%BD%A0%E5%80%BC%E5%BE%97%E8%A2%AB%E8%BF%99%E4%B8%AA%E4%B8%96%E7%95%8C%E6%B7%B1%E7%88%B1%EF%BC%81&oword=%E6%88%91%E5%9C%A8%E9%BB%91%E8%89%B2%E5%8D%9A%E7%89%A9%E9%A6%86%E4%BD%93%E9%AA%8C%E7%B2%BE%E7%A5%9E%E7%97%85%E4%BA%BA%E7%9A%84%E7%9C%9F%E5%AE%9E%E7%94%9F%E6%B4%BB%EF%BC%9A%E7%94%9F%E8%80%8C%E4%B8%BA%E4%BA%BA%EF%BC%8C%E4%B8%8D%E5%BF%85%E6%8A%B1%E6%AD%89%EF%BC%8C%E4%BD%A0%E5%80%BC%E5%BE%97%E8%A2%AB%E8%BF%99%E4%B8%AA%E4%B8%96%E7%95%8C%E6%B7%B1%E7%88%B1%EF%BC%81&atn=index&ext=%7B%22jsy%22%3A1%7D&top=%7B%22sfhs%22%3A1%2C%22_hold%22%3A2%7D&_t=1684136835786"
    ret_single = False
    print(json.dumps(m_baidu_video(url=url, ret_single=ret_single).start()))
