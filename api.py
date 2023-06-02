import codecs
import json
import os
import re
import threading
import time
import traceback
import urllib

import flask
import redis
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
        # 可以获取到的视频网站的地址
        self.type_list = ['v.qq.com',  # 腾讯视频
                          'weixin.qq.com',  # 微信公众号
                          'zhihu',  # 知乎
                          'weibo', 't.cn',  # 微博
                          'ixigua.com',  # 西瓜视频(需要cookie)
                          'toutiao.com',  # 今日头条
                          'haokan',  # 好看视频
                          'pipix.com',  # 皮皮虾
                          'kuaishou', 'chenzhongtech.com',  # 快手
                          'bilibili', 'b23.tv',  # bilibili(需要cookie)
                          'weishi',  # 腾讯微视
                          'acfun',  # acfun
                          'ifeng',  # 凤凰网
                          'cctvnews',  # 央视新闻
                          'sina',  # 新浪网
                          'xspshare.baidu.com', 'quanmin.baidu.com',  # 度小视（全民视频）
                          'sohu',  # 搜狐视频
                          'huoshan',  # 抖音火山版
                          'xiaochuankeji',  # 最右
                          'qtt',  # 趣头条
                          'pearvideo',  # 梨视频
                          'cctv',  # 央视网
                          'douyin',  # 抖音
                          'youtu',  # YouTube
                          'tiktok',  # TikTok
                          'instagram',  # instagram
                          'vimeo',  # vimeo
                          '163.com',  # 网易视频
                          'www.56.com',  # 56视频
                          'ku6',  # 酷6网
                          'eyepetizer',  # 开眼视频
                          'mtime',  # 时光网
                          '.news.cn',  # 新华网
                          'v1.cn',  # 第一视频
                          'v.tom',  # tom宽频站
                          'ouou',  # 偶偶网
                          'yun.ce',  # 中国经济网
                          'art.china',  # 艺术中国
                          'yicai.com',  # 第一财经
                          'jiemian.com',  # 界面新闻
                          'huxiu.com',  # 虎嗅
                          'skypixel.com',  # 天空之城
                          'mbd.baidu.com', 'mbdlite.baidu.com',  # 百度视频
                          'dailymotion.com',  # DailyMotion
                          'xinpianchang.com',  # 新片场
                          'docuchina.cn',  # 中国纪录片网
                          '360kuai.com',  # 360快资讯   (墨鱼丸)
                          'ntv.cn',  # 农视网
                          'twitter.com',  # 推特
                          'facebook.com', 'fb.watch',  # facebook
                          'xiaohongshu.com', 'xhslink.com',  # 小红书
                          'dongchedi.com',  # 懂车帝
                          'xuexi.cn',  # 学习强国
                          'taobao.com', 'tmall.com',  # 淘宝，天猫
                          'kankanews.com',  # 看看新闻
                          'm.baidu.com',  # 其他平台接在百度的视频
                          'mandaoo.com',  # 漫岛
                          'yangkeduo.com',  # 拼多多
                          'jd.com',         # 京东
                          ]
        # 调用的方法，和上面列表里一一对应
        self.project_list = [video_list.wx_new.wx_video,
                             video_list.wx_new.wx_video,
                             video_list.zhihu.zhihu_video,
                             video_list.weibo.wb_video,
                             video_list.weibo.wb_video,
                             video_list.ixigua.ixigua_video,
                             video_list.toutiao.toutiao_video,
                             video_list.haokan.haokan_video,
                             video_list.pipix.pipix_video,
                             video_list.kuaishou.kuaishou_video,
                             video_list.kuaishou.kuaishou_video,
                             video_list.bilibili.bilibili_video,
                             video_list.bilibili.bilibili_video,
                             video_list.weishi.weishi_video,
                             video_list.acfun.acfun_video,
                             video_list.ifeng.ifeng_video,
                             video_list.cctvnews.cctvnews_video,
                             video_list.sina.sina_video,
                             video_list.quanmin.quanmin_video,
                             video_list.quanmin.quanmin_video,
                             video_list.souhu.souhu_video,
                             video_list.huoshan.huoshan_video,
                             video_list.izuiyou.izuiyou_video,
                             video_list.qtt.qtt_video,
                             video_list.pear.pear_video,
                             video_list.cctv.cctv_video,
                             video_list.douyin.douyin_video,
                             video_list.youtube.youtube_video,
                             video_list.tiktok.tiktok_video,
                             video_list.instagram.instagram_video,
                             video_list.vimeo.vimeo_video,
                             video_list.v_163.v_163_video,
                             video_list.souhu.souhu_video,
                             video_list.ku6.ku6_video,
                             video_list.eyepetizer.eyepetizer_video,
                             video_list.mtime.mtime_video,
                             video_list.xinhua.xinhua_video,
                             video_list.v1.v1_video,
                             video_list.tom.tom_video,
                             video_list.ouou.ouou_video,
                             video_list.yun_ce.yun_ce_video,
                             video_list.art_china.art_china_video,
                             video_list.yicai.yicai_video,
                             video_list.jiemian.jiemian_video,
                             video_list.huxiu.huxiu_video,
                             video_list.skypixel.skypixel_video,
                             video_list.baidu.baidu_video,
                             video_list.baidu.baidu_video,
                             video_list.dailymotion.dailymotion_video,
                             video_list.xinpianchang.xinpianchang_video,
                             video_list.docuchina.docuchina_video,
                             video_list.i360kuai.i360kuai_video,
                             video_list.ntv.ntv_video,
                             video_list.twitter.twitter_video,
                             video_list.facebook.facebook_video,
                             video_list.facebook.facebook_video,
                             video_list.xhs.xhs_video,
                             video_list.xhs.xhs_video,
                             video_list.dongchedi.dongchedi_video,
                             video_list.xuexi.xuexi_video,
                             video_list.taobao.taobao_video,
                             video_list.taobao.taobao_video,
                             video_list.kankan.kankan_news_video,
                             video_list.m_baidu.m_baidu_video,
                             video_list.mandaoo.mandaoo_video,
                             video_list.pdd.pdd_video,
                             video_list.jd.jd_video,
                             ]
        self.url = url
        self.ret_single = ret_single
        self.home = home
        return

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

        for t in range(len(self.type_list)):
            if self.type_list[t] in self.url:
                self.data['code'] = 200
                try:
                    if self.home:
                        self.data['info'] = self.project_list[t](self.url, self.ret_single, self.home).start()
                    else:
                        self.data['info'] = self.project_list[t](self.url, self.ret_single).start()
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


class into_redis:
    def __init__(self):

        self.r = redis.Redis(host=CONFIG['redis']['host'],
                             port=CONFIG['redis']['port'],
                             password=CONFIG['redis']['password'],
                             db=CONFIG['redis']['db']
                             )

    def post_task(self, task_data):
        self.r.lpush(CONFIG['redis']['key_name'], json.dumps(task_data))

    def get_data(self, site):
        list_name = f"{CONFIG['redis']['key_name']}_{site}"
        # print(list_name)
        if self.r.exists(list_name):
            end_data = json.loads(self.r.brpop(list_name, timeout=1)[1])

            t = time.localtime()
            tyear = t.tm_year
            tmon = t.tm_mon
            today = t.tm_mday

            # 每隔1秒访问一次接口，如果返回code=200就拿到数据解析
            # 写入日志
            if not os.path.exists(f'{ROOTPATH}/logs'):
                try:
                    os.mkdir(f'{ROOTPATH}/logs')
                except:
                    pass
            if not os.path.exists(f'{ROOTPATH}/logs/{tyear}'):
                try:
                    os.mkdir(f'{ROOTPATH}/logs/{tyear}')
                except:
                    pass
            # 每个月分一个文件夹储存
            if not os.path.exists(f'{ROOTPATH}/logs/{tyear}/{tmon}'):
                try:
                    os.mkdir(f'{ROOTPATH}/logs/{tyear}/{tmon}')
                except:
                    pass

            up_data = end_data['up_data']
            task_site = end_data['task_site']
            data = end_data['data']
            up_data_tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # req = requests.post(url=CONFIG['api']['list'][task_site]['up'], json=up_data).text

            with open(f'{ROOTPATH}/logs/{tyear}/{tmon}/main_{today}.log', 'a',
                      encoding='utf-8') as f:
                f.write('任务线程：\t' + threading.current_thread().getName() + '\n')
                # f.write(f'任务时间：\t{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n')
                # f.write(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]这是被获取的任务\n')
                f.write(f'任务信息：[{data["time"]}]\t' + json.dumps(data) + '\n')
                f.write(f'任务结果：[{up_data_tm}]\t' + json.dumps(up_data) + '\n')
                f.write(f'上报结果：[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]\t' + '被获取成功' + '\n\n\n')

            return up_data
        else:
            no_data = {
                "data": [
                    {
                        "api": "Down_uploadRes",
                        "data": {
                            "res": [

                            ],
                            "taskId": "",
                            "code": 3005,
                            "message": "暂时没有结果"
                        }
                    }
                ]
            }
            return no_data


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


@app.route(CONFIG['api']['post_task'], methods=["post"])
def post_task():
    try:
        data = flask.request.json
        # print(data)
        site = data['site']
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for _data in data['urls']:
            task_id = _data['task_id']
            url = _data['url']
            task_data = {
                'site': site,
                'task_id': task_id,
                'url': url,
                'time': tm
            }

            into_redis().post_task(task_data)
        return 'ok'
    except:
        return 'error'


@app.route(CONFIG['api']['get_data'], methods=["get"])
def get_data():
    try:
        site = flask.request.args.get("site")
        # print(site)
        return into_redis().get_data(site)

    except:
        # print(traceback.format_exc())
        return '未传入site参数'


class main:
    def main(self):
        app.run(host='0.0.0.0', port=CONFIG['api']['port'])


if __name__ == "__main__":
    main().main()
