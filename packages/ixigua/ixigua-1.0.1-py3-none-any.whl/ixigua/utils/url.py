import time
import random
from typing import Union
from webrequests import WebRequest



def video_url_base():
    urls = [
        'https://i.snssdk.com',
        'https://vas.snssdk.com',
        'https://vas-lf-x.snssdk.com',
        'https://ib.365yg.com',
    ]
    return random.choice(urls)


def get_video_url_list(video_id: Union[str, int]):
    """
    使用其他接口，根据video_id获取视频列表

    缺点：清晰度最高为720P，无1080P
    """
    # base_url = video_url_base()
    base_url = 'https://i.snssdk.com'

    params = {
        'nobase64': '1',
        't': int(time.time()),
    }

    url = f'{base_url}/video/urls/1/2/3/{video_id}'
    video_list = WebRequest.get_response(url, params=params).json()['data']['video_list']

    data = {}
    for value in video_list.values():
        url = value['main_url']
        definition = value['definition']
        data[definition] = url

    return data

def get_video_url(video_id: Union[str, int], definition='720p'):

    video_urls = get_video_url_list(video_id=video_id)

    video_url = video_urls.get(definition.lower())
    if video_url is None:
        best_definition = sorted(video_urls, key=lambda x: int(x[:-1]))[-1]
        video_url = video_urls[best_definition]

    return video_url

def wrap_ixigua_url(url: Union[str, int]):
    """
    url: 完整的URL或ID

    添加`wid_try=1`，方可获取到渲染后的`_SSR_HYDRATED_DATA`数据
    """
    extra_params = 'wid_try=1'

    if str(url).isdigit():
        return f'https://www.ixigua.com/{url}?{extra_params}'

    if extra_params in url:
        return url

    if '?' in url:
        return url + '&' + extra_params

    return url + '?' + extra_params
