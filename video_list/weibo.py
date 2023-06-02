import json
import re
import urllib.parse

import requests


class wb_video:
    def __init__(self, url, ret_single=True):
        self.num = 0
        self.ret_single = ret_single
        # 用json格式保存数据
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'cookie': 'SINAGLOBAL=6590219507376.854.1678172290144; UOR=,,downni.zhipianbang.vip; ALF=1680923473; SCF=ArAXaZja6pmZMTB7pMmxhrmEfBKr6AP4tdKOTEUvtxtYaXErwKraWgKs_NdZcQDhrUOb71mLZ2NJd2hYnu1UYEg.; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWe5zpffd0kaq1d49T.uVeP; UPSTREAM-V-WEIBO-COM=b09171a17b2b5a470c42e2f713edace0; _s_tentry=-; Apache=1188700438728.3562.1680752978979; ULV=1680752979071:6:1:1:1188700438728.3562.1680752978979:1678673768959; XSRF-TOKEN=FLaIMtzHGKfJ9Tnsq0UahkuA; WBPSESS=g2Va6ZLXRYSCdsm5QPfA3MmbMq4fFBW0fYf_69ahZVqtYhNTQn4lBgsZJgr815rg5EQF8Rd-vmgFlJtRzNNlk8Ro4GiHdvFbHL7GwjRwEC-FvpInv1pz8kTFBaOQKAivnNiUJ_v36N1bwf3dHVr4ZwS9ZpVsXk8J6dfwD_-xDbY=; SUB=_2AkMTcsyhf8NxqwFRmP4cy2_jbI9wyw_EieKlLj16JRMxHRl-yj9kqmMptRB6OPLiTq4qLdVZJnai7wcpILThZwwwzWRb',

        }
        url = urllib.parse.unquote(url)

        if 't.cn' in url:
            self.url = re.sub('/tv/tv', '/tv',
                              re.findall('var url = "(.*?)";', requests.get(url=url, headers=self.headers).text)[0])
        elif 'm.weibo' in url and 'object_id' in url:
            object_id = re.findall('(\d+:\d+)', url)[0]
            self.url = f'https://weibo.com/tv/show/{object_id}'
        else:
            self.url = url
        # print(self.url)
        # exit()
        self.have_top = False

    def start(self):
        # 通过链接判断链接的类型

        if 'detail' in self.url or '?wm' in self.url or '&wm' in self.url or 'status' in self.url:
            try:
                self.video_type2()
            except:
                self.video_type2_()
        elif '?from' in self.url or '?mid' in self.url or 'show' in self.url:
            self.video_type3()
        else:
            self.video_type1()
        return self.data

    def video_type1(self):
        # print(1)
        # 第一种类型，引用视频发布的微博
        # print('here')
        s_url = 'https://weibo.com/ajax/statuses/show?'
        id = self.url.split('/')[-1].split('?')[0]
        # print(self.url)
        data_url = s_url + 'id=' + id
        data_url = data_url.strip()
        # print(data_url)
        data = requests.get(url=data_url).json()
        # print(json.dumps(data))
        _desc = data['page_info']['media_info']['kol_title']
        # print(json.dumps(data))
        if data['page_info']['media_info']['playback_list']:
            for data in data['page_info']['media_info']['playback_list']:
                # print(json.dumps(data))
                if data['play_info']['mime'] != "video/mp4":
                    _type = 'm3u8'
                else:
                    _type = 'video'

                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': '',
                    'type': _type,
                })
                self.data[self.num]['url'] = data['play_info']['url']
                try:
                    self.data[self.num]['file_size'] = data['play_info']["size"]
                except:
                    pass
                self.data[self.num]['width'] = data['play_info']['width']
                self.data[self.num]['height'] = data['play_info']['height']
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True
                if self.ret_single:
                    break
                self.num += 1
        else:
            if self.ret_single:
                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': '',
                    'type': 'video',
                })
                _data = data['page_info']['media_info']['video_details'][-1]
                url_key = _data['label']
                self.data[self.num]['url'] = data['page_info']['media_info'][url_key]
                self.data[self.num]['file_size'] = _data['size']
                self.data[self.num]['width'] = re.findall("template=(\d*)x\d*", self.data[self.num]['url'])[0]
                self.data[self.num]['height'] = re.findall("template=\d*x(\d*)", self.data[self.num]['url'])[0]
            else:
                for _data in data['page_info']['media_info']['video_details']:
                    self.data.append({
                        'desc': _desc,
                        'url': '',
                        'file_size': '',
                        'width': '',
                        'height': '',
                        'img': '',
                        'type': 'video',
                    })

                    url_key = _data['label']
                    self.data[self.num]['url'] = data['page_info']['media_info'][url_key]
                    self.data[self.num]['file_size'] = _data['size']
                    self.data[self.num]['width'] = re.findall("template=(\d*)x\d*", self.data[self.num]['url'])[0]
                    self.data[self.num]['height'] = re.findall("template=\d*x(\d*)", self.data[self.num]['url'])[0]
                    self.num += 1
                    if not self.have_top:
                        self.data[self.num]['top_quality'] = True
                        self.have_top = True
        return

    def video_type2(self):
        # 第二种   超话（？好像是） 里面的视频，直接从这里只能得到最高720p的视频，所以找到它的原地址用第三种方法获取视频
        s_url = 'https://weibo.com/tv/show/'
        e_url = '?from=old_pc_videoshow'
        fid = \
            requests.get(url=self.url, headers=self.headers).text.split(
                '<a  href=\\"https://video.weibo.com/show?fid=')[
                1].split('\\')[0]
        self.url = s_url + fid + e_url
        # print(self.url)
        self.video_type3()
        return

    def video_type2_(self):
        # 在上面的方法不能解析时用这个方式解析
        _id = self.url.split('?')[0].split('/')[-1]
        # print(_id)
        # _id = re.findall('weibo.com/\d+/(\d+)', self.url)[0]            # 获取视频id
        api_url = f'https://weibo.com/ajax/statuses/show?id={_id}'      # 获取接口地址
        res = requests.get(url=api_url, headers=self.headers).json()
        if 'media_info' in res['page_info']:
            data_list = res['page_info']['media_info']['playback_list']
            _desc = res['page_info']['media_info']['next_title']

        elif 'slide_cover' in res['page_info']:
            data_list = res['page_info']['slide_cover']['playback_list']
            _desc = res['page_info']['page_desc']

        # print(json.dumps(res))
        for data in data_list:
            # print(data)
            if data['meta']['type'] != 1:
                continue
            _url = data['play_info']['url']
            _width = data['play_info']['width']
            _height = data['play_info']['height']
            if 'size' in data['play_info']:
                _size = data['play_info']['size']
            else:
                _size = ''
            try:
                url_head = requests.get(url=_url, stream=True).headers
                # print(url_head)
                # print(url_head['Content-Type'])
                if 'mp4' in url_head['Content-Type']:
                    _type = 'video'
                else:
                    _type = 'm3u8'
            except:
                _type = 'video'

            self.data.append({
                'desc': _desc,
                'url': _url,
                'file_size': _size,
                'width': _width,
                'height': _height,
                'img': '',
                'type': _type,
            })

            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break

        # print(json.dumps(data_list))

    def video_type3(self):
        # 第三种  最初始的地址，从这里拿到的数据有些少，没有不同清晰度下的大小，高宽，只能获取到清晰度的名称和地址
        definition = ['超清 4K60', '超清 4K', '超清 2K60', '超清 2K', '高清 1080P60', '高清 1080P', '高清 720P',
                      '标清 480P', '流畅 360P']
        s_url = 'https://weibo.com/tv/api/component?page=/tv/show/'
        if '?from' in self.url:
            fid = self.url.split('?from')[0].split('/')[-1]
        elif '?mid' in self.url:
            fid = self.url.split('?mid')[0].split('/')[-1]
        elif 'fid' in self.url:
            fid = re.findall('fid=([a-zA-Z0-9]+:[a-zA-Z0-9]+)', self.url)[0]
        else:
            fid = re.findall('([a-zA-Z0-9]+:[a-zA-Z0-9]+)', self.url)[0]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'referer': 'https://weibo.com/tv/show/',
            # 'cookie': 'SUB=_2A25OiRNuDeRhGeBM61YV9CfPwjmIHXVt_wOmrDV8PUNbmtAfLUTTkW9NRQTqgKENTXbsZX9qeGkdEgLOH7OiCM8r'
            # 访问请求里要带一个cookie里的值，但是这个值是什么都行只要有而且不为空
            'cookie': 'SUB=1'
        }
        # print(fid)
        data = {
            'data': '{"Component_Play_Playinfo":{"oid":"' + fid + '"}}'
        }

        url = s_url + fid

        rel = requests.post(url=url, headers=headers, data=data).text

        # print(rel)
        _desc = json.loads(rel)['data']['Component_Play_Playinfo']['title']
        for x in definition:
            if x in json.loads(rel)['data']['Component_Play_Playinfo']['urls']:
                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': '',
                    'type': 'video',
                })
                self.data[self.num]['url'] = 'http:' + json.loads(rel)['data']['Component_Play_Playinfo']['urls'][x]
                try:
                    self.data[self.num]['width'] = re.findall('template=(\d*)x\d*', self.data[self.num]['url'])[0]
                    self.data[self.num]['height'] = re.findall('template=\d*x(\d*)', self.data[self.num]['url'])[0]
                except:
                    pass
                if 'm3u8' in self.data[self.num]['url']:
                    self.data[self.num]['type'] = 'm3u8'
                    # start = 'http://live.video.weibocdn.com/'
                    # m3u8_data = requests.get(url=self.data[self.num]['url'], headers=self.headers).text
                    # m3u8_data = re.sub('#EXTM3U', '', m3u8_data)
                    # m3u8_data = re.sub('#EXT-X-VERSION:\d+', '', m3u8_data)
                    # m3u8_data = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data)
                    # m3u8_data = re.sub('#EXT-X-PLAYLIST-TYPE:VOD', '', m3u8_data)
                    # m3u8_data = re.sub('#EXTINF:\d+.\d+,', '', m3u8_data)
                    # m3u8_data = re.sub('#EXT-X-ENDLIST', '', m3u8_data)
                    # m3u8_data = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data).split()
                    # url_data = {
                    #     'start': start,
                    #     'end': m3u8_data
                    # }
                    # self.data[self.num]['url'] = url_data
                if not self.have_top:
                    self.data[self.num]['top_quality'] = True
                    self.have_top = True
                if self.ret_single:
                    break
                self.num += 1

        return


if __name__ == '__main__':
    url = 'https://video.weibo.com/show?fid=1034:4895448641765443'
    ret_single = False
    print(json.dumps(wb_video(url=url, ret_single=ret_single).start()))
