import json
import re
import time

import requests
import yaml

import path


class twitter_video:
    def __init__(self, url, ret_single=True):
        self.data = [{
            'desc': '',
            'url': '',
            'file_size': '',
            'width': '',
            'height': '',
            'img': '',
            'type': 'video',
        }]
        cookie = ""
        ROOTPATH = path.path().start()
        with open(f'{ROOTPATH}/cookies/twitter_cookie.txt', 'r') as f:
            a = json.loads(f.read())
        for _data in a['cookie']:
            cookie += f"{_data['name']}={_data['value']};"
            if _data['name'] == "ct0":
                _ct0 = _data['value']

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-csrf-token': _ct0,
            'cookie': cookie,
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            # 理论上来说，可以不需要cookie，但是需要这个token参数，然而这个token参数过期更快，而且找不到生成token参数的方法
        }
        # self.proxies = {
        #     "http": "127.0.0.1:7890",
        #     "https": "127.0.0.1:7890"
        # }
        # 获取代理
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
        self.url = requests.get(url=url, headers=self.headers, proxies=self.proxies).url

    def get_json(self, url):
        # 获取视频id 合成访问api的参数 访问api获取数据
        id = re.findall('status/(\d*)', url)[0]
        api_url_data = f'variables=%7B%22focalTweetId%22%3A%22{id}%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Afalse%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22vibe_api_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_appeal_label_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_text_conversations_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
        api_url = f'https://api.twitter.com/graphql/VaihYjIIeVg4gfvwMgQsUA/TweetDetail?{api_url_data}'
        _json = requests.get(url=api_url, headers=self.headers, proxies=self.proxies).json()

        # print(json.dumps(_json))
        return _json

    def get_data(self, _json):
        # 写入数据

        self.data[0]['desc'] = \
            _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content'][
                'itemContent']['tweet_results']['result']['legacy']['full_text']

        # 判断链接类型，是视频还是图片
        if "card" in \
                _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content'][
                    'itemContent']['tweet_results']['result']:
            if 'image_value' in \
                    _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0][
                        'content'][
                        'itemContent']['tweet_results']['result']['card']['legacy']['binding_values'][0]['value']:
                self.data[0]['type'] = "image"
                self.data[0]['url'] = \
                    _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0][
                        'content'][
                        'itemContent']['tweet_results']['result']['card']['legacy']['binding_values'][0]['value'][
                        'image_value']['url']
                self.data[0]['width'] = \
                    _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0][
                        'content'][
                        'itemContent']['tweet_results']['result']['card']['legacy']['binding_values'][0]['value'][
                        'image_value']['width']
                self.data[0]['height'] = \
                    _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0][
                        'content'][
                        'itemContent']['tweet_results']['result']['card']['legacy']['binding_values'][0]['value'][
                        'image_value']['height']

            else:
                video_data = \
                    _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0][
                        'content'][
                        'itemContent']['tweet_results']['result']['card']['legacy']['binding_values'][0]['value'][
                        'string_value']
                video_data = json.loads(video_data)
                _type = video_data['type']
                _key = video_data['component_objects']['media_1']['data']['id']

                if _type == "video_website":
                    self.data[0]['type'] = "video"
                    self.data[0]['img'] = video_data['media_entities'][_key]['media_url_https']
                    url_list = video_data['media_entities'][_key]['video_info']['variants']
                    self.get_video_data(url_list)

                else:
                    self.data[0]['type'] = "image"
                    self.data[0]['url'] = video_data['media_entities'][_key]['media_url_https']

        elif 'video_info' in \
                _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content'][
                    'itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0]:
            self.data[0]['type'] = 'video'
            self.data[0]['img'] = \
                _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content'][
                    'itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0][
                    'media_url_https']
            url_list = \
                _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content'][
                    'itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0]['video_info'][
                    'variants']
            self.get_video_data(url_list)

        else:
            self.data[0]['type'] = 'image'
            self.data[0]['url'] = \
                _json['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content'][
                    'itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0][
                    'media_url_https']

        return

    def get_video_data(self, url_list):
        bitrate = 0
        for data in url_list:
            if data['content_type'] == "video/mp4":
                if data['bitrate'] > bitrate:
                    bitrate = data['bitrate']
                    _url = data['url']
        self.data[0]['url'] = _url
        self.data[0]['width'] = re.findall('/(\d*)x\d*/', _url)[0]
        self.data[0]['height'] = re.findall('/\d*x(\d*)/', _url)[0]

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
        _json = self.get_json(self.url)
        self.get_data(_json)
        return self.data


if __name__ == "__main__":
    url = "https://twitter.com/FightHaven/status/1637861558381592577?s=20"
    print(json.dumps(twitter_video(url).start()))
