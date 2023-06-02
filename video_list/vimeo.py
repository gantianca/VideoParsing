import json
import re
import time

import requests
import yaml

import path


class vimeo_video:
    def __init__(self, url, ret_single=True):
        self.have_top = False
        self.ret_single = ret_single
        self.num = 0
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        # 代理地址
        # self.proxies = {
        #     "http": "127.0.0.1:10001",
        #     "https": "127.0.0.1:10001"
        # }
        ROOTPATH = path.path().start()
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
        self.url = url

    def get_id(self, url):
        # 获取视频id
        if "staffpicks" in url:
            id = re.findall('staffpicks/(\d*)', url)[0]
        else:
            try:
                id = re.findall("vimeo\.com/(\d*)", url)[0]
            except:
                id = re.findall("/(\d*)$", url)[0]

        # print(id)
        return id

    def get_json(self, id):
        # 通过id获取json数据
        url = f'https://player.vimeo.com/video/{id}/config'
        _json = requests.get(url=url, headers=self.headers, proxies=self.proxies).json()
        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 写入数据
        # 获取最高清晰度
        num_list = []
        _desc = _json['video']['title']
        _img = _json['video']['thumbs']['base']

        if _json['request']['files']['progressive']:
            if self.ret_single:
                self.data.append({
                    'desc': _desc,
                    'url': '',
                    'file_size': '',
                    'width': '',
                    'height': '',
                    'img': _img,
                    'type': 'video',
                })
                for x in _json['request']['files']['progressive']:
                    num_list.append(int(x["profile"]))
                url_data = _json['request']['files']['progressive'][num_list.index(max(num_list))]
                self.data[self.num]['url'] = url_data['url']
                self.data[self.num]['width'] = url_data['width']
                self.data[self.num]['height'] = url_data['height']
            else:
                for x in _json['request']['files']['progressive']:
                    self.data.append({
                        'desc': _desc,
                        'url': '',
                        'file_size': '',
                        'width': '',
                        'height': '',
                        'img': _img,
                        'type': 'video',
                    })
                    self.data[self.num]['url'] = x['url']
                    self.data[self.num]['width'] = x['width']
                    self.data[self.num]['height'] = x['height']
                    if not self.have_top:
                        self.data[self.num]['top_quality'] = True
                        self.have_top = True
                    self.num += 1

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
            self.data[self.num]['type'] = "split"
            self.get_split_data(_json)

        return

    def get_split_data(self, _json):
        # 要解析前，把json改成mpd查看
        # 对于部分音视频被分离的视频处理
        # 分别获取到包含了最高清晰度视频和最高质量音频的url
        data_url = _json['request']['files']['dash']['cdns']['akfire_interconnect_quic']['url']
        # print(data_url)
        video_id = re.findall('/video/(.*?)/audio/', data_url)[0].split(',')[-2]
        video_data_url = data_url.replace(re.findall('/video/(.*?/audio/.*?)/master', data_url)[0], video_id)
        audio_id = re.findall('/audio/(.*?)/master', data_url)[0].split(',')[-1]
        audio_data_url = data_url.replace(re.findall('/video/(.*?/audio/.*?)/master', data_url)[0], audio_id).replace(
            "video", "audio")

        # 解析数据获取到视频和音频的真实地址
        video_data = requests.get(url=video_data_url, headers=self.headers, proxies=self.proxies).text
        audio_data = requests.get(url=audio_data_url, headers=self.headers, proxies=self.proxies).text
        # print(video_data)

        video_url = f"{re.findall('(.*?)/sep/video', data_url)[0]}/parcel/video/{json.loads(video_data)['video'][0]['segments'][0]['url']}".replace(
            'range', 'amp;range')
        audio_url = f"{re.findall('(.*?)/sep/video', data_url)[0]}/parcel/video/{json.loads(audio_data)['audio'][0]['segments'][0]['url']}".replace(
            'range', 'amp;range')

        _url = {
            "video": video_url,
            "sound": audio_url
        }
        self.data[self.num]['url'] = _url

        self.data[self.num]['width'] = json.loads(video_data)['video'][0]['width']
        self.data[self.num]['height'] = json.loads(video_data)['video'][0]['height']

    # def get_m3u8_data(self, _json):
    #     num_list = []
    #     m3u8_data_list = _json['request']['files']['hls']['cdns']['akfire_interconnect_quic']['url']
    #     for x in _json['request']['files']['dash']['streams']:
    #         # print(x)
    #         num_list.append(int(x["quality"].split('p')[0]))
    #     id = _json['request']['files']['dash']['streams'][num_list.index(max(num_list))]['id'].split('-')[0]
    #     m3u8_data = f"{re.findall('(.*/video/)', m3u8_data_list)[0]}{id}/playlist.m3u8?query_string_ranges=1"
    #     # print(m3u8_data)
    #
    #     m3u8_data_video = requests.get(url=m3u8_data, headers=self.headers, proxies=self.proxies).text
    #     m3u8_data_video = re.sub('#EXTINF:\d+.\d+', '', m3u8_data_video)
    #     m3u8_data_video = re.sub('#EXTM3U', '', m3u8_data_video)
    #     m3u8_data_video = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data_video)
    #     m3u8_data_video = re.sub('#EXT-X-PLAYLIST-TYPE:VOD', '', m3u8_data_video)
    #     m3u8_data_video = re.sub('#EXT-X-VERSION:\d+', '', m3u8_data_video)
    #     m3u8_data_video = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data_video)
    #     m3u8_data_video = re.sub('#EXT-X-ENDLIST', '', m3u8_data_video).split()
    #     video_data = {
    #         'start': f"{re.findall('(.*/video/)', m3u8_data_list)[0]}{id}",
    #         'end': []
    #     }
    #     audio_data = {
    #         'start': video_data['start'].replace('video','audio'),
    #         'end':[]
    #     }
    #     for x in m3u8_data_video:
    #         video_data['end'].append(x)
    #         audio_data['end'].append(x)
    #     url_data = {}
    #     url_data['video'] = video_data
    #     url_data['sound'] = audio_data
    #     self.data[self.num]['url'] = url_data

    def start(self):
        try:
            return self._start()
        except requests.exceptions.ProxyError:
            # print("解析出错")
            time.sleep(3)
            try:
                # print("第一次重试")
                return self._start()
            except requests.exceptions.ProxyError:
                # print("解析出错")
                time.sleep(10)
                try:
                    # print("第二次重试")
                    return self._start()
                except requests.exceptions.ProxyError:
                    # print("解析出错")
                    time.sleep(30)
                    # print("第三次重试")
                    return self._start()

    def _start(self):
        id = self.get_id(self.url)
        _json = self.get_json(id)
        self.get_data(_json)
        return self.data


if __name__ == '__main__':
    url = 'https://vimeo.com/800791883'
    ret_single = False
    print(json.dumps(vimeo_video(url=url, ret_single=ret_single).start()))
