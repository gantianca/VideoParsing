import codecs
import json
import os
import re
import time
import traceback
import urllib

import flask
import urlextract
import yaml
import path

import video_list.acfun
import video_list.bilibili
import video_list.cctv
import video_list.cctvnews
import video_list.douyin
import video_list.haokan
import video_list.huoshan
import video_list.ifeng
import video_list.ixigua
import video_list.izuiyou
import video_list.kuaishou
import video_list.pear
import video_list.pipix
import video_list.qtt
import video_list.quanmin
import video_list.sina
import video_list.souhu
import video_list.toutiao
import video_list.tx
import video_list.weibo
import video_list.weishi
import video_list.wx
import video_list.zhihu
import video_list.youtube
import video_list.tiktok
import video_list.instagram
import video_list.vimeo
import video_list.v_163
import video_list.ku6
import video_list.eyepetizer
import video_list.mtime
import video_list.xinhua
import video_list.v1
import video_list.tom
import video_list.ouou
import video_list.yun_ce
import video_list.art_china
import video_list.yicai
import video_list.jiemian
import video_list.huxiu
import video_list.skypixel
import video_list.baidu
import video_list.dailymotion
import video_list.wx_new
import video_list.xinpianchang
import video_list.docuchina
import video_list.i360kuai
import video_list.ntv
import video_list.twitter
import video_list.facebook
import video_list.xhs
import video_list.dongchedi
import video_list.xuexi
import video_list.taobao
import video_list.kankan
import video_list.m_baidu
import video_list.mandaoo
import video_list.pdd
import video_list.jd

ROOTPATH = path.path().start()
with open(f'{ROOTPATH}/video_data_list.yaml', 'r', encoding='utf-8') as f:
    video_data = f.read()
video_list_data = yaml.load(video_data, Loader=yaml.FullLoader)['video_list']

with open(f'{ROOTPATH}/config.yaml', 'r', encoding='utf-8') as f:
    config = f.read()
CONFIG = yaml.load(config, Loader=yaml.FullLoader)


class start:
    def __init__(self, url, ret_single=True, home=False):
        t = time.localtime()
        self.tyear = t.tm_year
        self.tmon = t.tm_mon
        self.today = t.tm_mday
        if not os.path.exists(f'{ROOTPATH}/logs'):
            os.mkdir(f'{ROOTPATH}/logs')
        if not os.path.exists(f'{ROOTPATH}/logs/{self.tyear}'):
            os.mkdir(f'{ROOTPATH}/logs/{self.tyear}')
        # 每个月分一个文件夹储存
        if not os.path.exists(f'{ROOTPATH}/logs/{self.tyear}/{self.tmon}'):
            os.mkdir(f'{ROOTPATH}/logs/{self.tyear}/{self.tmon}')

        self.data = {}
        self.url = url
        self.ret_single = ret_single
        self.home = home

    def main(self):
        # cli -> arg -> url -> 判断网站 -》 解析 -》 返回json
        # {status：200 / 999 ，info：{“解析的内容”}，message：“失败原因”}

        extractor = urlextract.URLExtract()
        try:
            try:
                self.url = re.findall('(https?://[^\s]+)', self.url)[0]
            except:
                self.url = extractor.find_urls(self.url)[0]
        except:
            self.data['code'] = 1010
            self.data['message'] = '未发现有效视频，请更换有效下载链接！'
            return json.dumps(self.data)

        for t in video_list_data:
            url_list = video_list_data[t]['url']
            for url in url_list:
                if url in self.url:
                    self.data['code'] = 200
                    try:
                        if self.home:
                            self.data['info'] = eval(
                                f"video_list.{video_list_data[t]['name']}.{video_list_data[t]['name']}_video(self.url, self.ret_single, self.home).start()")
                        else:
                            self.data['info'] = eval(
                                f"video_list.{video_list_data[t]['name']}.{video_list_data[t]['name']}_video(self.url, self.ret_single).start()")
                    # except KeyError:
                    #     self.data['info'] = self.project_list[t](self.url).start()
                    except:
                        if 'bilibili' in self.url or 'b23.tv' in self.url:
                            self.data['code'] = 999
                            self.data['message'] = '版权原因无法下载'
                            return self.data
                        # 在调用方法出现错误之后记录进日志，并且输出code=999
                        info = traceback.format_exc()
                        self.data['code'] = 999
                        self.data['message'] = '链接无效'
                        with codecs.open(f'{ROOTPATH}/logs/{self.tyear}/{self.tmon}/解析_{self.today}.log', 'a',
                                         encoding='utf-8') as f:
                            f.write(f'解析时间：\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n')
                            f.write(f'链接地址为：\t{self.url}\n')
                            f.write(f'错误原因：\t{info}\n')
                    try:
                        if not self.data['info']:
                            self.data['code'] = 999
                            self.data['message'] = '链接无效'
                    except:
                        self.data['code'] = 999
                        self.data['message'] = '链接无效'
                    return json.dumps(self.data)
        self.data['code'] = 1010
        self.data['message'] = '未发现有效视频，请更换有效下载链接！'
        return self.data


app = flask.Flask(__name__)


# 访问地址为 https://127.0.0.1:5000/getdata
# post 请求中携带json中url参数
@app.route(CONFIG['api']['analysis'], methods=["post"])
def analysis():
    url = urllib.parse.unquote(flask.request.json['url'])
    if 'ret_single' in flask.request.json:
        ret_single = flask.request.json['ret_single']
    else:
        ret_single = True
    if 'home' in flask.request.json:
        home = flask.request.json['home']
    else:
        home = False

    data = start(url=url, ret_single=ret_single, home=home).main()
    return data


class main:
    def main(self):
        app.run(host='0.0.0.0', port=CONFIG['api']['port'])


if __name__ == "__main__":
    main().main()
