import json
import re
from urllib.parse import unquote

import requests

import video_list.wx


class wx_video:
    def __init__(self, url, ret_single=True):
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        # print(url)
        self.url = url
        self.url = re.sub('&item_show_type=.*?&', '&', self.url)
        # print(self.url)
        self.sum = 0
        self.ret_single = ret_single
        self.have_top = False

    def get_data(self):
        # 获取源码
        _html = requests.get(url=self.url, headers=self.headers).text

        # 从源码中获取视频的mpvid列表以及图片地址列表
        vid_list = re.findall('data-mpvid="(.*?)"', _html)
        if not vid_list:
            vid_list = re.findall(
                "window\.cgiData\.vid = xml \? getXmlValue\('video_page_info\.video_id\.DATA'\) : '(.*?)'", _html)
        cover_list = re.findall('data-cover="(.*?)"', _html)
        # print(cover_list)
        # print(vid_list)

        # 从视频的地址中获取需要的参数
        if len(vid_list) > 1:
            # 对多视频的处理
            try:
                og_url = re.findall('meta property="og:url" content="(.*?)"', _html)[0]
                token = re.findall('window.wxtoken = "(.*?)"', _html)[0]
                if og_url:
                    biz = re.findall('__biz=(.*?)&', og_url)[0]
                    mid = re.findall('mid=(.*?)&', og_url)[0]
                    idx = re.findall('idx=(.*?)&', og_url)[0]

                else:
                    biz = re.findall('var biz = "" \|\| "(.*?)"', _html)[0]
                    mid = re.findall('var mid = "" \|\| "(.*?)"', _html)[0]
                    idx = re.findall('var idx = "" \|\| "(.*?)"', _html)[0]

                # 通过获取到的参数和视频vid循环获取视频数据并写入
                if self.ret_single:
                    for num in range(len(vid_list)):
                        data_url = f"https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&__biz={biz}&mid={mid}&idx={idx}&vid={vid_list[num]}&wxtoken={token}&x5=0&f=json"
                        self.data.append({
                            'desc': '',
                            'url': '',
                            'file_size': '',
                            'width': '',
                            'height': '',
                            'img': '',
                            'type': 'video',
                        })

                        data_json = requests.get(url=data_url, headers=self.headers).json()
                        # print(json.dumps(data_json))
                        self.data[num]['desc'] = data_json['title']
                        self.data[num]['url'] = data_json['url_info'][0]['url']
                        self.data[num]['file_size'] = data_json['url_info'][0]['filesize']
                        self.data[num]['width'] = data_json['url_info'][0]['width']
                        self.data[num]['height'] = data_json['url_info'][0]['height']
                        self.data[num]['img'] = unquote(cover_list[num])
                else:
                    _num = 0
                    for num in range(len(vid_list)):
                        data_url = f"https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&__biz={biz}&mid={mid}&idx={idx}&vid={vid_list[num]}&wxtoken={token}&x5=0&f=json"
                        # print(data_url)
                        data_json = requests.get(url=data_url, headers=self.headers).json()
                        # print(json.dumps(data_json))
                        _desc = data_json['title']
                        _img = unquote(cover_list[num])
                        # print(len(data_json['url_info']))
                        for _data in data_json['url_info'][:len(data_json['url_info']) // 2]:
                            self.data.append({
                                'desc': _desc,
                                'url': '',
                                'file_size': '',
                                'width': '',
                                'height': '',
                                'img': _img,
                                'type': 'video',
                            })
                            self.data[_num]['url'] = _data['url']
                            self.data[_num]['file_size'] = _data['filesize']
                            self.data[_num]['width'] = _data['width']
                            self.data[_num]['height'] = _data['height']
                            if not self.have_top:
                                self.data[_num]['top_quality'] = True
                                self.have_top = True
                            _num += 1
            except:
                self.data.clear()
                num = 0
                data_list = re.findall("var videoPageInfos = ([\s\S]*?]);", _html)[0]
                data_list = re.findall("(\{\s*video_id[\s\S]*?width[\s\S]*?)},\s*]", data_list)
                for data_json in data_list:
                    # print(data_json)
                    # _desc = data_json['title']
                    _desc = re.findall('og:title" content="(.*?)"', _html)[0]
                    _img = unquote(cover_list[num])
                    url_list = re.findall("\s+?url: '(.*?)'", data_json)
                    file_size_list = re.findall("filesize: '(.*?)'", data_json)
                    width_list = re.findall("width: '(.*?)'", data_json)
                    height_list = re.findall("height: '(.*?)'", data_json)

                    for x in range(len(url_list)):
                        if not url_list[x]:
                            continue
                        else:
                            self.data.append({
                                'desc': _desc,
                                'url': '',
                                'file_size': '',
                                'width': '',
                                'height': '',
                                'img': _img,
                                'type': 'video',
                            })

                            self.data[self.sum]['url'] = url_list[x].replace('\\x26amp', '&')
                            self.data[self.sum]['url'] = re.sub('&;', '&', self.data[self.sum]['url'])
                            self.data[self.sum]['file_size'] = file_size_list[x]
                            self.data[self.sum]['width'] = width_list[x]
                            self.data[self.sum]['height'] = height_list[x]
                            if not self.have_top:
                                self.data[self.sum]['top_quality'] = True
                                self.have_top = True
                            self.sum += 1
                            if self.ret_single:
                                break

                    num += 1


        elif len(vid_list) == 1:
            # 对单视频的处理
            try:
                data_json = re.findall("var videoPageInfos = ([\s\S]*?]);", _html)[0]
            except:
                data_json = re.findall("window.__mpVideoTransInfo = ([\s\S]*?]);", _html)[0]
            # print(data_json)
            if data_json:
                try:
                    _img = unquote(cover_list[0])
                except:
                    _img = re.findall(" window.__mpVideoCoverUrl = '(.*?)'", _html)[0]
                _desc = re.findall('og:title" content="(.*?)"', _html)[0]
                # print(data_json)
                quality_list = re.findall("video_quality_wording: '(.*?)'", data_json)
                url_list = re.findall("\s+?url: '(.*?)'", data_json)
                file_size_list = re.findall("filesize: '(.*?)'", data_json)
                width_list = re.findall("width: '(.*?)'", data_json)
                height_list = re.findall("height: '(.*?)'", data_json)

                # quality_size = {'超清': 0, '流畅': 1}

                # for x in range(len(quality_list)):
                #     if quality_list[x] not in quality_size:
                #         quality_size[quality_list[x]] = x
                #     else:
                #         if int(file_size_list[x]) > int(file_size_list[quality_size[quality_list[x]]]):
                #             quality_size[quality_list[x]] = x

                # print(quality_size)

                h264_list = range(len(url_list) // 2, len(url_list))
                for x in url_list[len(url_list) // 2: len(url_list)]:
                    if 'f101' in x:
                        h264_list = range(len(url_list) // 2)
                        break
                # print(h264_list)
                # print(quality_size)
                for x in h264_list:
                    if not url_list[x]:
                        continue
                    else:
                        self.data.append({
                            'desc': _desc,
                            'url': '',
                            'file_size': '',
                            'width': '',
                            'height': '',
                            'img': _img,
                            'type': 'video',
                        })

                        self.data[self.sum]['url'] = url_list[x].replace('\\x26amp', '&')
                        self.data[self.sum]['url'] = re.sub('&;', '&', self.data[self.sum]['url'])
                        self.data[self.sum]['file_size'] = file_size_list[x]
                        self.data[self.sum]['width'] = width_list[x]
                        self.data[self.sum]['height'] = height_list[x]
                        if not self.have_top:
                            self.data[self.sum]['top_quality'] = True
                            self.have_top = True
                        if self.ret_single:
                            break
                        self.sum += 1

        n_data = video_list.wx.wx_video(self.url, ret_single=self.ret_single).start()
        if n_data:
            for x in n_data:
                self.data.append(x)
        # print(n_data)
        # print(self.data)

    def start(self):
        self.get_data()
        # print(self.data)
        url = self.data[0]['url']

        return self.data


if __name__ == "__main__":
    # url = "https://mp.weixin.qq.com/s/985wc3VEU2bfJZTY1lgo8g"
    url = "https://mp.weixin.qq.com/s/OmUVXTsYmWyIGpA1gDjJSA"
    ret_single = False
    print(json.dumps(wx_video(url=url, ret_single=ret_single).start()))
