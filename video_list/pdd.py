import requests
import re
import json


class pdd_video:
    def __init__(self, url, ret_single=True):
        self.ret_single = ret_single
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]

        self.headers = {
            'User-Agent': 'android Mozilla/5.0 (Linux; Android 5.1.1; GM1900 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36  phh_android_version/5.76.0 phh_android_build/5e2cc2590060d518a64d6d1ce7507021a96b0143 phh_android_channel/hw pversion/0',
        }
        self.url = url

    def get_json(self, url):
        feed_id = re.findall('feed_id=(\d+)', url)[0]
        api_url = 'https://api.pinduoduo.com/api/peacevideo/live/supplement'
        data = {
            "extra": "{\"use_lego_container\":\"1\",\"ext\":\"{\\\"tab_style\\\":1,\\\"feed_scene_id\\\":369}\",\"page_from\":\"909\",\"lego_business_type\":\"1002\",\"list_id\":\"0fa9617111\",\"scene_id\":\"41\",\"hub_type\":\"hub\\\/zb_scene_tab\\\/weak\",\"location_required\":\"0\",\"use_hub\":\"1\",\"direction\":0}",
            "biz_type": 1, "is_32_process": "1", "page_from": "909",
            "link_url": "moore_video.html?ext=%7B%22page_from%22%3A%22909%22%2C%22feed_scene_id%22%3A369%7D&use_lego_container=1&feed_source_type=1&play_url=http%3A%2F%2Fvideo4-2.pddugc.com%2Ftower-video-b%2F73e472a6b846ea2336ed1a6ea218bb2ab3494fdf.v11.f30.mp4%3Fk%3D01e309a8fb43b000bdda077ad9233b59%26t%3D1685784714&lego_business_type=1002&biz_type=1&h=1280&scene_id=41&if_soft_h265=false&if_h265=false&host_list=%5B%7B%22host%22%3A%22video4-5.pddpic.com%22%2C%22vendor%22%3Anull%7D%2C%7B%22host%22%3A%22video4-4.pddpic.com%22%2C%22vendor%22%3Anull%7D%2C%7B%22host%22%3A%22video4-1.pddpic.com%22%2C%22vendor%22%3Anull%7D%2C%7B%22host%22%3A%22video4-1.pddugc.com%22%2C%22vendor%22%3Anull%7D%2C%7B%22host%22%3A%22video4-2.pddugc.com%22%2C%22vendor%22%3Anull%7D%5D&use_hub=1&page_from=909&subtitle_coordinate=%5B0.5%2C0.5%2C0.5%2C0.5%5D&sps=AWQAMv_hAB5nZAAyrHIEQLQKGwFqAgICgAAAAwCAAAAeB4wYwjABAAdo6EOEyyLA&w=720&goods_style=1&head_ids=5254991957377312447&hub_type=hub%2Fzb_scene_tab%2Fweak&location_required=0&idx=0&page_sn=92010&open_gps=1",
            "scene_type": 3, "feed_id": feed_id, "lego_tem_list": [
                {"tem_key": "moore-lego-leo.group_label", "tem_code": "0a651dde21ed83f2cc943fb5178ad561"}],
            "scene_id": "41"}

        _json = requests.post(url=api_url, json=data, headers=self.headers).json()
        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        self.data[0]['desc'] = _json['result']['hyman_interact']['share']['title']
        self.data[0]['img'] = _json['result']['hyman_interact']['share']['thumbnail_url']
        self.data[0]['url'] = _json['result']['apodis_instep_entry']['resource_url']
        return

    def get_store_data(self):
        goods_id = re.findall('goods_id=(\d+)', self.url)[0]
        api_url = f'https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}'
        self.headers['cookie'] = 'PDDAccessToken=SYUDXWYVIHOK2ADCQM32R3EXYHGI2P2FJKCASAKSGOOPBBH37SXQ1237421;'
        _html = requests.get(url=api_url, headers=self.headers).text

        _json = re.findall('window\.rawData=(.*?)</script>', _html)[0]

    def start(self):
        if 'feed_id' in self.url:
            _json = self.get_json(self.url)
            self.get_data(_json)
        if 'goods.html' in self.url:
            # 商品页面，访问要cookie，放弃
            # self.get_store_data()
            raise
        return self.data


if __name__ == "__main__":
    url = "https://mobile.yangkeduo.com/goods.html?goods_id=375153874510&_oak_gallery=https%3A%2F%2Fimg.pddpic.com%2Fmms-material-img%2F2022-12-24%2Fe8663425-293a-4662-b412-46f9389639ae.jpeg&page_from=35&thumb_url=https%3A%2F%2Fimg.pddpic.com%2Fmms-material-img%2F2022-12-24%2Fe8663425-293a-4662-b412-46f9389639ae.jpeg%3FimageMogr2%2Fthumbnail%2F400x%257CimageView2%2F2%2Fw%2F400%2Fq%2F80%2Fformat%2Fwebp&refer_page_name=index&refer_page_id=10002_1685671109920_aoxo8ipfl6&refer_page_sn=10002&_x_share_id=edf80581e93543fd95a0e35390c0e319&uin=CB3VCRH7YBGBSDTAQFV4R23ISQ_GEXDA"
    ret_single = False
    print(json.dumps(pdd_video(url=url, ret_single=ret_single).start()))
