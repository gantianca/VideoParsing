import json
import os
import re
import time
from urllib.parse import quote

import requests

import path

ROOTPATH = path.path().start()


# ROOTPATH = ''
# print(ROOTPATH)


class tx_video:

    def __init__(self, url, ret_single=True):

        # 定义一些后面会用的上的值
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        self.buid = 'vinfoad'
        self.int_time = int(time.time())

        self.guid = '5c4a8fc9f9b01471'
        self.num = 0
        self.video_data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]
        # self.vid_list = []
        self.vid = ''
        self.vinfo_list = None
        self.url = requests.get(url=url, headers=self.headers).url

    # def parse_cookie(self):
    #     if self.cookie:
    #         for i in self.cookie.split(";"):
    #             kv = i.split("=")
    #             self.cookie_dict[kv[0].strip()] = kv[1]

    def get_cKey(self, platform, version, vid, guid, tm):
        # 通过js获取cKey
        # path = os.getcwd()
        # print(path)
        file = ROOTPATH + '/js/getck.js'
        # ctx = execjs.compile(open(file).read())
        # params = ctx.call("getckey", platform, version, vid, '', guid,
        #                   tm, ROOTPATH)
        command1 = 'node {6} {0} {1} {2} {3} {4} {5}'.format(platform, version, vid, guid, tm, ROOTPATH, file)
        with os.popen(command1) as nodejs:
            params = nodejs.read().replace('\n', '')
        return params

    def get_vinfoparams(self):
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
        # logintoken = quote(
        #     str({"main_login": self.cookie_dict['main_login'], "openid": self.cookie_dict['_video_qq_openid'],
        #          "appid": self.cookie_dict['appid'],
        #          "access_token": self.cookie_dict['access_token'],
        #          "vuserid": self.cookie_dict['vuserid'],
        #          "vusession": self.cookie_dict['_video_qq_vusession']}))
        logintoken = ''
        defn = "shd"
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
        vid = self.vid
        guid = self.guid
        cKey = self.get_cKey(platform, appVer, vid, guid, tm)
        # 最后拼接    PS：这个拼接好像对顺序有要求
        result = f"charge={charge}&otype={otype}&defnpayver={defnpayver}&spau={spau}&spaudio={spaudio}&spwm={spwm}&sphls={sphls}&host={host}&refer={refer}&ehost={ehost}&sphttps={sphttps}&encryptVer={encryptVer}&cKey={cKey}&clip={clip}&guid={guid}&flowid={flowid}&platform={platform}&sdtfrom={sdtfrom}&appVer={appVer}&unid={unid}&auth_from={auth_from}&auth_ext={auth_ext}&vid={vid}&defn={defn}&fhdswitch={fhdswitch}&dtype={dtype}&spsrt={spsrt}&tm={tm}&lang_code={lang_code}&logintoken={logintoken}&spvvpay={spvvpay}&spadseg={spadseg}&spsfrhdr={spsfrhdr}&spvideo={spvideo}&spm3u8tag={spm3u8tag}&spmasterm3u8={spmasterm3u8}&drm={drm}"
        # result = 'charge=0&otype=ojson&defnpayver=0&spau=1&spaudio=0&spwm=1&sphls=2&host=v.qq.com&refer=https%3A%2F%2Fmp.weixin.qq.com%2F&ehost=https%3A%2F%2Fv.qq.com%2Ftxp%2Fiframe%2Fplayer.html&sphttps=1&encryptVer=8.1&cKey=AAD71C792E9FD909E1F5DC6BE9BB4EE228D5A15B591AD5C213844818B6ADA55C1BF3B46D2805061566B55F25DB8E225165C4FB98693B6121B43389A5AFB15F6A15B56A713A7316D69E3FEE1BCE139C328C347E4481F237387822AA2FCC0172E14239FEEF027C5BA31E90C62C76F9BFD9B5A06747532A0474424C9CE181E5D6CF69035C3FC24C77F7E65C9A91A3861FFE610CC82E9E2B9E7A2201AF8927794967D232CBDA177E5CCD8D9F436B97060E29FD0A86A84444BA5282C4E23BDE73175A4E5FA1926AE93FAF44BB3B85C8BA372E3C25C591576B38F2AE35E543E39E2C9A91CAA3ED983FC8C0EBEED8F69E81A08A&clip=4&guid=5c4a8fc9f9b01471&flowid=ef72763e1db0c15f3d4c239e796ac443&platform=70201&sdtfrom=v1104&appVer=3.5.57&unid=&auth_from=&auth_ext=&vid=v0393r9a1re&defn=&fhdswitch=0&dtype=3&spsrt=2&tm=1669864460&lang_code=0&logintoken=%7B%22access_token%22%3A%2263_SqILg3wZCVw99d3WFjepvaa7q2azP5J1Fwm1Uqa7RsXfP-1nrgkUf66CH2rKlh73CVH0apwJRfL9SkJHQ2UbYA%22%2C%22appid%22%3A%22wxa75efa648b60994b%22%2C%22vusession%22%3A%22rtfNc5XtV5oKGED0AlACUg.N%22%2C%22openid%22%3A%22oXw7q0AyFPQTpSwCjeAwP81xlI_4%22%2C%22vuserid%22%3A%221371140120%22%2C%22video_guid%22%3A%225c4a8fc9f9b01471%22%2C%22main_login%22%3A%22wx%22%7D&spvvpay=1&spadseg=3&spsfrhdr=0&spvideo=0&spm3u8tag=67&spmasterm3u8=3&drm=8'
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
        vid = self.vid
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
        _html = requests.get(url=self.url, headers=self.headers).text
        try:
            self.vid = _html.split('"currentVid":"')[1].split('","')[0]
        except:
            self.vid = re.findall("var vid = '(.*?)';", _html)[0]
        return

    def start(self):
        # 开始的函数
        self.get_vid()  # 先获取到vid

        # for self.num in range(len(self.vid_list)):  # 根据vid的数量每有一个vid执行一次后面的函数
        ad_params = self.get_adparams()
        vinfoparams = self.get_vinfoparams()
        buid = self.buid

        # 拼接成最后的参数
        params = {"buid": buid,
                  "adparam": ad_params,
                  "vinfoparam": vinfoparams}
        # print(json.dumps(params))
        # 传入参数获取请求
        res = requests.post("https://vd6.l.qq.com/proxyhttp", headers=self.headers, json=params)
        # print(res.text)

        # self.video_data.append({})
        self.url_type(vinfo_list=res.json()['vinfo'])
        return self.video_data

    def url_type(self, vinfo_list):
        # 判断视频的类型
        self._url = json.loads(vinfo_list)['vl']['vi'][0]['ul']['ui'][-2]['url']
        ti = json.loads(vinfo_list)['vl']['vi'][0]['ti']
        topic = f"http://puui.qpic.cn/vpic_cover/{self.vid}/{self.vid}_hz.jpg"
        vh = json.loads(vinfo_list)['vl']['vi'][0]['vh']
        vw = json.loads(vinfo_list)['vl']['vi'][0]['vw']
        time = json.loads(vinfo_list)['preview']
        size = json.loads(vinfo_list)['vl']['vi'][0]['fs']

        self.video_data[self.num]['desc'] = ti

        if 'm3u8' in json.loads(vinfo_list)['vl']['vi'][0]['ul']:
            self.url_m3u8(vinfo_list)
        else:
            self.url_mp4(vinfo_list)
        self.video_data[self.num]['file_size'] = size
        self.video_data[self.num]['width'] = vw
        self.video_data[self.num]['height'] = vh
        self.video_data[self.num]['img'] = topic

        # self.video_data[self.num]['time'] = str(time) + 's'
        # print(self.url)
        # 判断视频类型

        # print(vinfo_list)

        return

    def url_m3u8(self, vinfo_list):
        # 对于m3u8类型视频的处理
        # print(vinfo_list)
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
        self.video_data[self.num]['url'] = {}
        self.video_data[self.num]['url']['start'] = self._url
        self.video_data[self.num]['url']['end'] = m3u8_data
        self.video_data[self.num]['type'] = "m3u8"
        return
    def url_mp4(self, vinfo_list):
        # 对mp4格式视频的处理
        self.video_data[self.num]['url'] = f"{json.loads(vinfo_list)['vl']['vi'][0]['ul']['ui'][-2]['url']}{json.loads(vinfo_list)['vl']['vi'][0]['fn']}?vkey={json.loads(vinfo_list)['vl']['vi'][0]['fvkey']}"
        self.video_data[self.num]['type'] = "video"

if __name__ == '__main__':
    url = 'https://m.v.qq.com/x/m/play?vid=t0174kvg507&cid=&url_from=share&second_share=0&share_from=wxf'
    print(tx_video(url).start())
