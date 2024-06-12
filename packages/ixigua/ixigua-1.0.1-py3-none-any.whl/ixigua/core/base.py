import re
import json
from typing import Union

from webrequests import WebRequest
from simple_loggers import SimpleLogger

from ixigua import utils
from .cookies import cookies


class IXiGuaBase(object):

    def __init__(self, url: Union[str, int]):
        self.logger = SimpleLogger()
        self.url = utils.wrap_ixigua_url(url)
        self._ssr_hydrated_data = None

    @property
    def ssr_hydrated_data(self):
        """_SSR_HYDRATED_DATA
        """
        if self._ssr_hydrated_data is None:
            response = WebRequest.get_response(self.url, cookies=cookies, allowed_codes=[200, 404])
            if response.status_code == 404:
                # 404页面报错：视频已下架
                self.logger.debug(f'视频已下架：{self.url}')
                return

            pattern = re.compile(r'_SSR_HYDRATED_DATA=(.*?)</script>', re.DOTALL)
            result = pattern.search(response.text).group(1)
            self._ssr_hydrated_data = json.loads(
                result.replace('undefined', 'null'))
        return self._ssr_hydrated_data

    @property
    def packer_data(self):
        """
        packerData
            - pSeries
                - id
                - seriesInfo
                    - title
                    - item_num
            - video
                - vid
                - title
                - videoResource
                    - normal
                        - video_list
        """
        return self.ssr_hydrated_data['anyVideo']['gidInformation']['packerData']

    @property
    def video(self):
        return self.packer_data['video']

    @property
    def pseries(self):
        return self.packer_data.get('pSeries')

    @property
    def is_series(self):
        return self.pseries is not None
