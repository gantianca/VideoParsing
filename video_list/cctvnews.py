import base64
import hashlib
import hmac
import json
import re
import time

import requests


def md5Encryption(str, key=''):  # MD5解密
    # 加解密的函数
    md = hashlib.md5(key.encode(encoding='utf-8'))  # 创建md5对象
    md.update(str.encode(encoding='utf-8'))
    return md.hexdigest()


class cctvnews_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            "x-emas-gw-appkey": "20000009",
            "x-emas-gw-pv": "6.1",
            "x-emas-gw-sign": '',
            "x-emas-gw-t": '',
        }
        self.url = url
        self.have_top = False

    def get_id(self):
        # 获取视频的id
        id = re.findall('item_id=(\d*)', self.url)[0]
        # print(id)
        return id

    def get_sgin(self, id):
        # 通过视频id和当前时间戳加密出sgin参数
        ts = round(time.time() / 1000)  # 时间戳
        f = "articleId=%s" % id  # 固定拼接字符串
        key = 'emasgatewayh5'  # 进行sha256加密用到的key
        keyByte = bytes(key, 'UTF-8')
        # 将f进行md5加密后，在进行固定拼接
        d = "&&&20000009&" + md5Encryption(f) + "&" + str(
            ts) + "&" + "emas.feed.article.server.getArticle" + "&" + "1.0.0" + "&&&&&"
        # 使用key对拼接完的字符串进行加密
        sign = hmac.new(keyByte, d.encode(), hashlib.sha256).hexdigest()

        self.headers['x-emas-gw-sign'] = sign
        self.headers['x-emas-gw-t'] = str(ts)

        return sign

    def get_json(self, id):
        # 获取到json数据     ，这里json数据被base64加密
        url = f'https://emas-api.cctvnews.cctv.com/h5/emas.feed.article.server.getArticle/1.0.0?articleId={id}'
        _json = requests.get(url=url, headers=self.headers).json()
        _json = base64.b64decode(_json['response']).decode('UTF-8')
        # print(_json)
        _json = json.loads(_json)

        return _json

    def get_data(self, _json):
        # 写入数据， url是m3u8格式
        _desc = _json['data']['title']
        _img = _json['data']['videos'][0]['cover']['url']
        for _data in _json['data']['videos'][0]['qualities']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'm3u8',
            })
            self.data[self.num]['file_size'] = _data['size']
            self.data[self.num]['width'] = _data['width']
            self.data[self.num]['height'] = _data['height']

            # 对m3u8格式的链接的尾部进行处理
            # m3u8_url = _data['url']
            # m3u8_data = requests.get(url=m3u8_url).text
            # m3u8_data = re.sub('#EXT-X-ALLOW-CACHE:YES', '', m3u8_data)
            # m3u8_data = re.sub('#EXTM3U', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-VERSION:\d+', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-PLAYLIST-TYPE:VOD', '', m3u8_data)
            # m3u8_data = re.sub('#EXTINF:\d+.\d+,', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-ENDLIST', '', m3u8_data)
            # m3u8_data = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data).split()
            # # print(m3u8_data)
            #
            # url_data = {'start': re.findall('(.*)/', m3u8_url)[0] + '/', 'end': m3u8_data}
            # self.data[self.num]['url'] = url_data
            self.data[self.num]['url'] = _data['url']
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            else:
                self.num += 1

    def start(self):
        id = self.get_id()
        self.get_sgin(id)
        _json = self.get_json(id)
        self.get_data(_json)

        # print(json.dumps(_json))
        return self.data


if __name__ == '__main__':
    url = 'https://content-static.cctvnews.cctv.com/snow-book/video.html?item_id=6452368654912253812&toc_style_id=video_default&share_to=copy_url&track_id=dc53bf24-0722-4f4a-aa2c-0a491ccbb850'
    ret_single = False
    print(json.dumps(cctvnews_video(url=url, ret_single=ret_single).start()))
