import json
import re

import requests


class souhu_video:
    def __init__(self, url, ret_single=True):
        self.have_top = False
        self.type = 0
        self.num = 0
        self.ret_single = ret_single
        self.data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            # 'cookie': 'gidinf=x099980109ee14d0f5a52ac7500083c983a014e00eec; SUV=220305124316PVZZ; _ga=GA1.1.647074031.1654079836; __gpi=UID=00000617f36ee17c:T=1654079836:RT=1654079836:S=ALNI_MZMzuqoMYQvjVrsILlSJHUPUmp1-A; __gads=ID=ab6829217ebc4ab9-22dd4e46a1d3003b:T=1654079836:S=ALNI_MZJOyhdKHQbqrFafyy9_CeI9R4_IA; cto_bundle=nDc9B19Wb0RlMSUyQmxjM25XNVR6TWFtc0k0dWwxUFFBekhkUDN5aDBRVkxTeFNmRkQzcEU1NWRZckhOeEJBZTM5V1lKMVV3Q3phaWt5ZlAwWEpOTWFRdnVmZzVSN0FNN05FRmxzQW1wRWZjQlJuc0dlTmZMUnk5cHlxY1QlMkZWUlJKVkpFQkc; _ga_DFBWYFE6Q0=GS1.1.1654079836.1.1.1654081111.60; newpuid=16714169852289559256; IPLOC=CN3100; ip_ctcode=1312; fuid=16714169969625351393; cityIpLocation=182.84.235.138; __bid_n=185511ad75f29785534207; FEID=v10-64810cc4dc09edf31e90506a438784d6149c74fa; __xaf_fpstarttimer__=1672102991835; __xaf_ths__={"data":{"0":1,"1":43200,"2":60},"id":"0906dbbe-791c-44aa-8d81-cec70bd587ad"}; __xaf_thstime__=1672102991986; FPTOKEN=aoHLCr4MJeYY3Rnq6c9bQzS7ZFdu4nH2/ZZnLbdu2dKE7RfGyTu9LXn6fJLGy4GHmhTGi58NbGvdkQcNIDNy9yMVrop0jWn/y1L1lLYJ0nvuolavVGAhKreIzQEa7UuKScpydc77CLKg2vaDpP06cJh4hiFLRaEaEIqz2GMuJac52t4SjhhX89y51/fdYQ9JpZH+bJfg3jafhnb2Apx85iKV2BsOdgipeHyp62BEG/mOuxo7Z9ksxbeccf0Poi0MYq0IK9/cDlmfqNPzk8IW/F5ppNiW0sLIjJvza74nuNFdNdTUtAawpbOXGIbjkzpX6c7wrnVHGuIZPHqmuE+8XUHjRSQnpMUMCp/5BL8KclM9hhxQlHpvBM4nsJoXwcMBVIpwibfpfCw8i2xUDfb+cg==|QJ74whrKLO65MBWPvSv9ROruKGP4rx6R3IB76JYTqhE=|10|94d9736ec70996d68467aadf9198af66; __xaf_fptokentimer__=1672102992012; beans_dmp=%7B%2210191%22%3A1671416986%2C%22admaster%22%3A1671416986%2C%22shunfei%22%3A1671416986%2C%22reachmax%22%3A1671416986%2C%22lingji%22%3A1671416986%2C%22yoyi%22%3A1671416986%2C%22ipinyou%22%3A1671416986%2C%22ipinyou_admaster%22%3A1671416986%2C%22miaozhen%22%3A1672102994%2C%22diantong%22%3A1671416986%2C%22huayang%22%3A1671416986%2C%22precisionS%22%3A1671416986%2C%22qunyi%22%3A1671416986%7D; beans_dmp_done=1; Hm_lvt_082a80ccf2db99dbd7b5006fe0744b57=1672103009; pgc_wakeup20221227=1; reqtype=pc; landingrefer=https%3A%2F%2Fcn.bing.com%2F; sokey=%5B%7B%22key%22%3A%224k%22%7D%5D; reall=exited; jv=c98be2314f62454b4c347f016d0dffec-il0I68uy1672132406719; ppinf=2|1672132407|1673342007|bG9naW5pZDowOnx1c2VyaWQ6Mjg6MTYwNzY2NTk1MzY1MzcwMjY1NkBzb2h1LmNvbXxzZXJ2aWNldXNlOjMwOjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMHxjcnQ6MTA6MjAyMi0xMi0yN3xlbXQ6MTowfGFwcGlkOjY6MTA3NDA1fHRydXN0OjE6MXxwYXJ0bmVyaWQ6MTowfHJlbGF0aW9uOjA6fHV1aWQ6MTY6c2U0MTJkZGU1OGMxMGZlN3x1aWQ6MTY6c2U0MTJkZGU1OGMxMGZlN3x1bmlxbmFtZTowOnw; pprdig=4oMLEaJX2Q7BH6zj9bP-0QdQOapwP4JtrmrKsKsnJ9RRcolwVNu1gLdMgGNoNJHced_vR4J2rRyI1kZkNyN3WuZruXBEt_DMIPNese1iIUBjkvMleCXoO2uXOR9InGC0O67IFC1b_USMU-OM2Cud-o0E2wC3yZnttNUsfdE3nUA; ppmdig=16721324070000008be2c507b49a09be208ce0e5be2f328b; user_isOpenedVip=0; beans_freq=1; iwt_uuid=692942fe-4780-4abe-a494-6757743002f7; t=1672132421485; JSESSIONID=8AA50D0DC076E8B749C51F011FD5E632'
        }
        self.url = url

    def get_id(self):
        # 从源码中获取id
        _html = requests.get(url=self.url, headers=self.headers).text
        try:
            id = re.findall("var vid = '(\d*)'", _html)[0]
        except:
            try:
                id = re.findall("vid: \"(\d*)\"", _html)[0]
            except:
                try:
                    id = re.findall('"videoId":(\d*)', _html)[0]
                except:
                    try:
                        id = re.findall('var vid="(\d*)";', _html)[0]
                        self.type = 1
                    except:
                        id = re.findall('"id":(\d*),', _html)[0]
                        self.type = 2
        # print(id)

        return id

    def get_json_1(self, id):
        ver_list = [11, 21, 1]
        url_data_list = []
        # 通过id拼出保存了json数据的url
        for ver in ver_list:
            if self.type == 0:
                url = f'https://my.tv.sohu.com/play/videonew.do?vid={id}&ver={ver}'
            elif self.type == 1:
                url = f'https://hot.vrs.sohu.com/vrs_flash.action?vid={id}&ver={ver}'
            _json = requests.get(url=url, headers=self.headers).text
            # print(_json)
            _json = json.loads(_json)
            url_data = _json['data']['su'][0]
            if url_data in url_data_list:
                continue
            else:
                url_data_list.append(url_data)
            self.get_data(_json)
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            else:
                self.num += 1

        return

    def get_json_2(self, id):
        url = f"https://vxml.56.com/json/v2/{id}"
        _json = requests.get(url=url, headers=self.headers).text
        # print(_json)
        _json = json.loads(_json)
        _img = _json['info']['bimg']
        _desc = _json['info']['Subject']
        for _data in _json['info']['rfiles']:
            self.data.append({
                'desc': _desc,
                'url': '',
                'file_size': '',
                'width': '',
                'height': '',
                'img': _img,
                'type': 'video',
            })
            self.data[self.num]['file_size'] = _data['filesize']
            url_data = re.findall('file=(.*?)&', _data['url'])[0]
            _url = f"https://data.vod.itc.cn/ip?new={url_data}"
            data = requests.get(url=_url, headers=self.headers).text
            self.data[self.num]['url'] = json.loads(data)['servers'][0]['url']
            _type = _data['type']
            if _type == "vga":
                self.data[self.num]['quality_str'] = '480p'
            elif _type == "wvga":
                self.data[self.num]['quality_str'] = '720p'
            if not self.have_top:
                self.data[self.num]['top_quality'] = True
                self.have_top = True
            if self.ret_single:
                break
            else:
                self.num += 1

    def get_data(self, _json):
        _desc = _json['data']['tvName']
        _img = _json['data']['coverImg']
        self.data.append({
            'desc': _desc,
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': _img,
            'type': 'video',
        })
        if self.type == 0:
            _id = _json['id'].split('_')[1]
            if _id == '1':
                self.data[self.num]['quality_str'] = '480p'
            elif _id == '21':
                self.data[self.num]['quality_str'] = '720p'
            elif _id == '31':
                self.data[self.num]['quality_str'] = '1080p'

        # 视频播放地址被单独保存了
        if self.type == 1:
            self.data[self.num]['width'] = _json['data']['width']
            self.data[self.num]['height'] = _json['data']['height']
        self.data[self.num]['file_size'] = _json['data']['totalBytes']
        if len(_json['data']['su']) == 1:
            url_data = _json['data']['su'][0]
            if 'http' in url_data:
                self.data[self.num]['url'] = url_data
            else:
                url = f'https://data.vod.itc.cn/ip?new={url_data}'
                # print(url)
                data = requests.get(url=url, headers=self.headers).text
                # print(data)
                self.data[self.num]['url'] = json.loads(data)['servers'][0]['url']
        else:
            url_list = []
            for url_data in _json['data']['su']:
                if 'http' in url_data:
                    self.data[self.num]['url'] = url_data
                else:
                    url = f'https://data.vod.itc.cn/ip?new={url_data}'
                    # print(url)
                    data = requests.get(url=url, headers=self.headers).text
                    # print(data)
                    url_list.append(json.loads(data)['servers'][0]['url'])
            self.data[self.num]['url'] = url_list
            if self.type == 1:
                self.data[self.num]['type'] = 'block_video'

        return

    def start(self):
        id = self.get_id()
        if self.type == 2:
            self.get_json_2(id)
        else:
            self.get_json_1(id)

        return self.data


if __name__ == '__main__':
    url = 'https://tv.sohu.com/v/dXMvMjk5NjI0NDI0LzQyMzk3NjgzNi5zaHRtbA==.html'
    # url = 'https://www.56.com/u60/v_MTYyNjY4OTI5.html'
    ret_single = False
    print(json.dumps(souhu_video(url=url, ret_single=ret_single).start()))
