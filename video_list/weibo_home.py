import json
import re
import traceback

import requests


class weibo_home:
    def __init__(self, url):
        self.data = []
        self.url = url
        pass

    def get_data(self, uid, cursor):
        api_url = f"https://weibo.com/ajax/profile/getWaterFallContent?uid={uid}&cursor={cursor}"
        headers = {
            'Cookie': 'SUB=_2AkMTcsyhf8NxqwFRmP4cy2_jbI9wyw_EieKlLj16JRMxHRl-yj9kqmMptRB6OPLiTq4qLdVZJnai7wcpILThZwwwzWRb',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
        }

        data = requests.get(url=api_url, headers=headers).json()
        try:
            self.into_data(data)
        except:
            # print(traceback.format_exc())
            pass

        new_cursor = data['data']['next_cursor']
        # print(new_cursor)
        if str(new_cursor) != '-1':
            self.get_data(uid, new_cursor)

    def into_data(self, data):
        video_list = data['data']['list']
        for video_data in video_list:
            if 'page_info' in video_data:
                pass
            else:
                continue
            _desc = video_data['page_info']['media_info']['kol_title']
            url_data = video_data['page_info']['media_info']['playback_list'][0]
            _url = url_data['play_info']['url']
            _width = url_data['play_info']['width']
            _height = url_data['play_info']['height']

            if 'size' in url_data['play_info']:
                _size = url_data['play_info']['size']
            else:
                _size = ''

            try:
                url_head = requests.get(url=_url, stream=True).headers
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
                'type': 'video',
            })

    def main(self):
        uid = re.findall('u/(\d+)', self.url)[0]
        # print(uid)
        self.get_data(uid, cursor=0)

        return self.data


if __name__ == '__main__':
    url = 'https://weibo.com/u/1713031610?tabtype=newVideo'
    print(json.dumps(weibo_home(url).main()))
