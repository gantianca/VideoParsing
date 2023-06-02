import json
import re

import requests


class pipix_video:

    def __init__(self, url, ret_single=True):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        # 打开网页获取网页的url，传进来的url可能和这个不同，所以要获取一下
        self.url = requests.get(url=url, headers=self.headers).url
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]

    def get_cell_id(self):
        # 从url里面获取cell_id参数
        cell_id = re.findall('item/(.*?)[?&]', self.url)
        return cell_id

    def get_aid(self):
        # 从url里面获取aid参数
        aid = re.findall('app_id=(.*?)&', self.url)
        return aid

    def get_appname(self):
        # 从url里面获取app_name参数
        app_name = re.findall('&app=(.*?)[/&]', self.url)
        return app_name

    def get_json(self, cell_id, aid, app_name):
        # 拼接url
        json_url = f'https://is.snssdk.com/bds/cell/detail/?cell_type=1&aid={aid}&app_name={app_name}&cell_id={cell_id}'
        return json_url

    def get_data(self, url):
        # 得到需要的数据
        data = requests.get(url=url).text
        # print(url)
        # print(data)
        return data

    def data_end(self, data):
        # 写入数据
        self.data[0]['desc'] = json.loads(data)['data']['data']['item']['content']
        self.data[0]['url'] = \
            json.loads(data)['data']['data']['item']['video']['video_high']['url_list'][0][
                'url']
        # self.data[0]['time'] = \
        #     json.loads(data)['data']['data']['item']['video']['video_high']['duration']
        self.data[0]['width'] = \
            json.loads(data)['data']['data']['item']['video']['video_high']['width']
        self.data[0]['height'] = \
            json.loads(data)['data']['data']['item']['video']['video_high']['height']
        self.data[0]['img'] = json.loads(data)['data']['data']['item']['video']['cover_image']['download_list'][0][
            'url']

    def start(self):
        cell_id = self.get_cell_id()[0]
        aid = self.get_aid()[0]
        app_name = self.get_appname()[0]
        json_url = self.get_json(cell_id, aid, app_name)
        data = self.get_data(json_url)
        self.data_end(data)
        return self.data


if __name__ == "__main__":
    url = 'https://h5.pipix.com/s/S8TxuCT/'
    ret_single = False
    print(pipix_video(url=url, ret_single=ret_single).start())
