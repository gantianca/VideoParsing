import json
import re
import random

import requests


class kuaishou_home:
    def __init__(self, url):
        self.data = []
        self.url = url

    def get_did(self):
        # 生成did参数，但是用不上，要他识别过的did才行
        did_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
        did = 'web_'
        for x in range(32):
            did += str(random.choice(did_arr))
        did = did.lower()
        return did

    def get_data(self, userid, pcursor):
        headers = {
            'Referer': 'https://www.kuaishou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
            'Cookie': f"kpf=PC_WEB; clientid=3; did=web_3bb25b85aa1a12adaa45e967e1b57213; kpn=KUAISHOU_VISION"
        }

        api = 'https://www.kuaishou.com/graphql'    # 接口地址
        json_data = {"operationName": "visionProfilePhotoList",     # 接口参数
                     "variables": {"userId": userid, "pcursor": pcursor, "page": "profile"},
                     "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}

        data = requests.post(url=api, json=json_data, headers=headers).json()
        try:
            self.into_data(data)
        except:
            pass

        new_pcursor = data['data']['visionProfilePhotoList']['pcursor']
        # print(new_pcursor)
        # print(json.dumps(data))
        print(len(self.data))
        # 判断是否还有视频
        if new_pcursor is None:
            raise
        if new_pcursor != 'no_more' and len(self.data) <= 1000:
            self.get_data(userid, new_pcursor)

    def into_data(self, data):
        # 解析数据
        for video_data in data['data']['visionProfilePhotoList']['feeds']:
            try:
                if video_data['type'] == 1:
                    try:
                        _desc = video_data['photo']['caption']
                    except:
                        _desc = ''
                    try:
                        _img = video_data['photo']['coverUrl']
                    except:
                        _img = ''

                    url_data = video_data['photo']['videoResource']['h264']['adaptationSet'][0]

                    # print(url_data)
                    _url = url_data['representation'][0]['url']
                    try:
                        _width = url_data['representation'][0]['width']
                    except:
                        _width = ''
                    try:
                        _height = url_data['representation'][0]['height']
                    except:
                        _height = ''
                    try:
                        _size = url_data['representation'][0]['fileSize']
                    except:
                        _size = ''
                    self.data.append({
                        'desc': _desc,
                        'url': _url,
                        'file_size': _size,
                        'width': _width,
                        'height': _height,
                        'img': _img,
                        'type': 'video',
                    })
            except:
                continue

    def main(self):

        # userid = '3xtd6ysfipm3mri'
        if '?' in self.url:
            userid = re.findall('profile/(.*?)\?', self.url)[0]
        else:
            userid = re.findall('profile/(.*?)$', self.url)[0]
        pcursor = ''
        # print(userid)
        self.get_data(userid, pcursor)

        return self.data


if __name__ == '__main__':
    # userid = '3x9bwu3ukuxq3ii'
    # pcursor = ''
    # kuaishou_home().get_data(userid, pcursor)
    # url = 'https://www.kuaishou.com/profile/3xtd6ysfipm3mri'
    url = 'https://www.kuaishou.com/profile/3xnxk8cvvde9drm'
    print(json.dumps(kuaishou_home(url).main()))
