import json
import os
import re
import time
from urllib.parse import quote

import requests
import yaml

import path

ROOTPATH = path.path().start()


class wx_video:

    def __init__(self, url, ret_single=True):
        # 定义一些后面会用的上的值
        self.have_top = False
        self.ret_single = ret_single
        self._url = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',

        }
        self.buid = 'vinfoad'
        # self.url = url
        self.int_time = int(time.time())
        self.guid = '5c4a8fc9f9b01471'
        self.num = 0
        self.id_num = 0
        self.video_data = []
        self.vid_list = []
        self.vinfo_list = None
        self.url = requests.get(url=url, headers=self.headers).url

        # b = requests.get(
        #     url='http://v2.api.juliangip.com/dynamic/getips?num=4&pt=1&result_type=text&split=1&trade_no=1331475403546777&sign=6d96f450fca1b2a342820f253caf94ca').text
        # b_data = b.split()
        # self.proxy = {
        #     "http": b_data[0]
        # }
        try:
            with open(f'{ROOTPATH}/config.yaml', "r", encoding='utf-8') as f:
                text = f.read()
                # print(text)
                text = yaml.load(text, Loader=yaml.FullLoader)['porxy']
                if text:
                    data = text
                    if 'http' in data and 'https' in data:
                        self.proxies = data
                    else:
                        self.proxies = ''
                else:
                    self.proxies = ''
        except:
            self.proxies = ''

    def get_cKey(self, platform, version, vid, guid, tm):
        # 通过js获取cKey
        file = ROOTPATH + '/js/getck.js'
        command1 = 'node {6} {0} {1} {2} {3} {4} {5}'.format(platform, version, vid, guid, tm, ROOTPATH, file)
        with os.popen(command1) as nodejs:
            params = nodejs.read().replace('\n', '')
        return params

    def get_vinfoparams(self, fn):
        # 构建要获取的响应需要的参数
        # 固定的值
        spsrt = "2"
        charge = "0"
        # defaultfmt = "auto"
        otype = "ojson"
        # 随机数 + platform
        flowid = "3d0258391e691c265ee61be872b683a5"
        platform = "70201"
        sdtfrom = "v1104"
        defnpayver = "0"
        appVer = "3.5.57"
        host = "v.qq.com"
        sphttps = "1"
        spwm = "1"
        logintoken = ''
        defn = fn
        fhdswitch = "0"
        show1080p = "false"
        # isHLS = "1"
        dtype = "3"
        sphls = "2"
        # spgzip = "1"
        # dlver = "2"
        drm = "8"
        # hdcp = "1"
        spau = "1"
        spaudio = "0"
        # defsrc = "1"
        encryptVer = "8.1"
        # fp2p = "1"
        spadseg = "3"
        spmasterm3u8 = '3'
        spm3u8tag = '67'
        spvideo = '0'
        spsfrhdr = '0'
        spvvpay = '1'
        lang_code = '0'
        auth_ext = ''
        auth_from = ''
        unid = ''
        clip = '4'
        # 动态的值
        ehost = quote(self.url)
        refer = quote(self.url)
        tm = self.int_time
        vid = self.vid_list[self.id_num]
        guid = self.guid
        cKey = self.get_cKey(platform, appVer, vid, guid, tm)
        # 最后拼接    PS：这个拼接好像对顺序有要求
        result = f"charge={charge}&otype={otype}&defnpayver={defnpayver}&spau={spau}&spaudio={spaudio}&spwm={spwm}&sphls={sphls}&host={host}&refer={refer}&ehost={ehost}&sphttps={sphttps}&encryptVer={encryptVer}&cKey={cKey}&clip={clip}&guid={guid}&flowid={flowid}&platform={platform}&sdtfrom={sdtfrom}&appVer={appVer}&unid={unid}&auth_from={auth_from}&auth_ext={auth_ext}&vid={vid}&defn={defn}&fhdswitch={fhdswitch}&dtype={dtype}&spsrt={spsrt}&tm={tm}&lang_code={lang_code}&logintoken={logintoken}&spvvpay={spvvpay}&spadseg={spadseg}&spsfrhdr={spsfrhdr}&spvideo={spvideo}&spm3u8tag={spm3u8tag}&spmasterm3u8={spmasterm3u8}&drm={drm}"
        # print(result)
        return result

    def get_adparams(self):
        # 构建要获取的响应需要的参数
        # 静态的值
        pf = "in"
        ad_type = quote("LD|KB|PVL")
        pf_ex = "pc"
        refer = quote("https://v.qq.com/")
        ty = "web"
        plugin = "1.14.2"
        v = "1.13.0"
        pt = "0"
        flowid = ""
        vptag = ""
        pu = ""
        chid = "0"
        adaptor = "1"
        dtype = "1"
        live = "0"
        resp_type = "json"
        # req_type = 1
        # from = "0"
        appversion = "3.2.3"
        # uid = self.cookie_dict['vuserid']
        uid = ''
        # tkn = self.cookie_dict['_video_qq_vusession']
        tkn = ''
        lt = ""
        platform = ""
        # opid = self.cookie_dict['_video_qq_openid']
        opid = ''
        # atkn = self.cookie_dict['access_token']
        atkn = ''
        # appid = self.cookie_dict['_video_qq_appid']
        appid = ''
        tpid = ''
        # 动态的值
        guid = self.guid
        vid = self.vid_list[self.id_num]
        url = quote(self.url)
        try:
            coverid = re.search("cover/(.*?).html", self.url).group(1)
        except:
            coverid = ''
        # 拼接参数的值
        result = f"pf={pf}&ad_type={ad_type}&pf_ex={pf_ex}&url={url}&refer={refer}&ty={ty}&plugin={plugin}&v={v}&coverid={coverid}&vid={vid}&pt={pt}&flowid={flowid}&vptag={vptag}&pu={pu}&chid={chid}&adaptor={adaptor}&dtype={dtype}&live={live}&resp_type={resp_type}&guid={guid}&from=0&appversion={appversion}&" \
                 f"uid={uid}&tkn={tkn}&lt={lt}&platform={platform}&opid={opid}&atkn={atkn}&appid={appid}&tpid={tpid}"
        # print(result)
        return result

    def get_vid(self):
        # 从源码里获取vid的列表
        mima = '+'
        vid_list = []
        # vid=''
        _vid1 = self.url.split('/')[-1].split('.')[0]
        if len(_vid1) == 11:
            vid_list.append(_vid1)
        else:
            _html = requests.get(url=self.url, headers=self.headers).text
            rel = _html.split('vid=')
            # print(rel[2])
            for num in range(len(rel)):
                x = rel[num].split('"')[0].split('&')[0]
                # print(x)
                if len(x) == 11:
                    if mima in x:
                        pass
                    else:
                        vid_list.append(x)
        try:
            # print(_html)
            _vid = re.findall("vid: xml \? getXmlValue\('video_page_info.video_id.DATA'\) : '(.*?)',", _html)[0]
            if len(_vid) == 11:
                vid_list.append(_vid)
        except:
            pass
        # print(vid_list)
        self.vid_list = vid_list
        # print(vid_list)
        return

    def start(self):
        # 有时候微信公众号的视频一次获取失败，下一次就能成功，不知道为什么，所以这里直接让他获取失败之后再重新运行一次
        try:
            # 开始的函数
            self.get_vid()  # 先获取到vid
            # print(self.vid_list[self.num])

            for self.id_num in range(len(self.vid_list)):  # 根据vid的数量每有一个vid执行一次后面的函数
                ad_params = self.get_adparams()
                vinfoparams = self.get_vinfoparams(fn="fhd")
                buid = self.buid

                self.video_data.append({
                    'desc': '',
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': '',
                    'type': 'video',
                })

                # 拼接成最后的参数
                params = {"buid": buid,
                          "adparam": ad_params,
                          "vinfoparam": vinfoparams}
                # print(json.dumps(params))
                # 传入参数获取请求
                res = requests.post("http://vd6.l.qq.com/proxyhttp", headers=self.headers, json=params, proxies=self.proxies)
                vinfo_list = res.json()['vinfo']
                # 调用判断视频类型的函数
                if not self.have_top:
                    self.video_data[self.num]['top_quality'] = True
                    self.have_top = True
                self.url_type(vinfo_list=vinfo_list)

                if not self.ret_single:
                    fn_list = []
                    if len(json.loads(vinfo_list)['fl']['fi']) > 1:
                        for fn in json.loads(vinfo_list)['fl']['fi'][:-1]:
                            fn_list.append(fn['name'])
                    # print(fn_list)
                    for fn in fn_list:
                        vinfoparams = self.get_vinfoparams(fn=fn)
                        self.video_data.append({
                            'desc': '',
                            'url': '',
                            'file_size': '',
                            'width': '',
                            'height': '',
                            'img': '',
                            'type': 'video',
                        })

                        # 拼接成最后的参数
                        params = {"buid": buid,
                                  "adparam": ad_params,
                                  "vinfoparam": vinfoparams}
                        # print(json.dumps(params))
                        # 传入参数获取请求
                        res = requests.post("http://vd6.l.qq.com/proxyhttp", headers=self.headers, json=params, proxies=self.proxies)
                        vinfo_list = res.json()['vinfo']
                        # 调用判断视频类型的函数
                        self.url_type(vinfo_list=vinfo_list)

            return self.video_data
        except:
            # 开始的函数
            self.get_vid()  # 先获取到vid
            # print(self.vid_list[self.num])

            for self.id_num in range(len(self.vid_list)):  # 根据vid的数量每有一个vid执行一次后面的函数
                ad_params = self.get_adparams()
                vinfoparams = self.get_vinfoparams(fn="fhd")
                buid = self.buid

                self.video_data.append({
                    'desc': '',
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': '',
                    'type': 'video',
                })

                # 拼接成最后的参数
                params = {"buid": buid,
                          "adparam": ad_params,
                          "vinfoparam": vinfoparams}
                # print(json.dumps(params))
                # 传入参数获取请求
                res = requests.post("http://vd6.l.qq.com/proxyhttp", headers=self.headers, json=params, proxies=self.proxies)
                vinfo_list = res.json()['vinfo']
                # 调用判断视频类型的函数
                if not self.have_top:
                    self.video_data[self.num]['top_quality'] = True
                    self.have_top = True
                self.url_type(vinfo_list=vinfo_list)

                if not self.ret_single:
                    fn_list = []
                    if len(json.loads(vinfo_list)['fl']['fi']) > 1:
                        for fn in json.loads(vinfo_list)['fl']['fi'][:-1]:
                            fn_list.append(fn['name'])
                    # print(fn_list)
                    for fn in fn_list:
                        vinfoparams = self.get_vinfoparams(fn=fn)
                        self.video_data.append({
                            'desc': '',
                            'url': '',
                            'file_size': '',
                            'width': '',
                            'height': '',
                            'img': '',
                            'type': 'video',
                        })

                        # 拼接成最后的参数
                        params = {"buid": buid,
                                  "adparam": ad_params,
                                  "vinfoparam": vinfoparams}
                        # print(json.dumps(params))
                        # 传入参数获取请求
                        res = requests.post("http://vd6.l.qq.com/proxyhttp", headers=self.headers, json=params, proxies=self.proxies)
                        vinfo_list = res.json()['vinfo']
                        # 调用判断视频类型的函数
                        self.url_type(vinfo_list=vinfo_list)

            return self.video_data

    def url_type(self, vinfo_list):
        # 判断视频的类型
        # 获取视频的基础信息
        # print(vinfo_list)

        if '该视频不合规，暂无法观看哦' in vinfo_list:
            return
        else:
            self._url = json.loads(vinfo_list)['vl']['vi'][0]['ul']['ui'][-2]['url']
        # print(self.url)
        # print(vinfo_list)
        ti = json.loads(vinfo_list)['vl']['vi'][0]['ti']
        topic = f"http://puui.qpic.cn/vpic_cover/{self.vid_list[self.id_num]}/{self.vid_list[self.id_num]}_hz.jpg"
        vh = json.loads(vinfo_list)['vl']['vi'][0]['vh']
        vw = json.loads(vinfo_list)['vl']['vi'][0]['vw']
        time = json.loads(vinfo_list)['preview']
        size = json.loads(vinfo_list)['vl']['vi'][0]['fs']

        self.video_data[self.num]['desc'] = ti
        if 'm3u8' in self._url:
            self.video_data[self.num]['type'] = "m3u8"
            self.video_data[self.num]['url'] = {}
            self.url_m3u8(vinfo_list)
        else:
            self.video_data[self.num]['type'] = "video"
            self.url_mp4(vinfo_list)

        self.video_data[self.num]['file_size'] = size
        self.video_data[self.num]['width'] = vw
        self.video_data[self.num]['height'] = vh
        # self.video_data[self.num]['time'] = str(time) + 's'
        self.video_data[self.num]['img'] = topic
        # print(self.url)
        # 判断视频类型

        self.num += 1
        return

    def url_m3u8(self, vinfo_list):
        # 对于m3u8类型视频的处理
        m3u8_data = json.loads(vinfo_list)['vl']['vi'][0]['ul']['m3u8']
        # 获取链接的尾部以及处理
        m3u8_data = re.sub('#EXTM3U', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-VERSION:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-PLAYLIST-TYPE:VOD', '', m3u8_data)
        m3u8_data = re.sub('#EXTINF:\d+.\d+,', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-ENDLIST', '', m3u8_data)
        m3u8_data = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data).split()
        # print(m3u8_data)
        self.video_data[self.num]['url']['start'] = self._url
        self.video_data[self.num]['url']['end'] = m3u8_data
        return

    def url_mp4(self, vinfo_list):
        # 对于mp4类型视频的处理
        self._url = json.loads(vinfo_list)['vl']['vi'][0]['ul']['ui'][-1]['url']
        fn = json.loads(vinfo_list)['vl']['vi'][0]['fn']
        vkey = json.loads(vinfo_list)['vl']['vi'][0]['fvkey']
        url = f"{self._url}{fn}?vkey={vkey}"
        self.video_data[self.num]['url'] = url
        return


if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/s/qXC8dmEmMys5C2yrta1ykA'
    ret_single = False
    print(json.dumps(wx_video(url=url, ret_single=ret_single).start()))

    # with open(f"{ROOTPATH}/wx_proxy.txt", "r") as f:
    #     proxy_list = f.read().split()
    # for proxy in proxy_list:
    #     print(json.dumps(wx_video(url, proxy).start()))
