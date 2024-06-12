import re
from pathlib import Path

from ixigua import utils
from .base import IXiGuaBase


class IXiGuaDown(IXiGuaBase):

    def __init__(self,
                 url: str,
                 outdir='download',
                 rank_prefix=False,
                 index_prefix=None,
                 playlist=False,
                 playlist_start=0,
                 playlist_end=None,
                 playlist_limit=30,
                 ):
        super().__init__(url)

        self.outdir = Path(outdir)
        self.rank_prefix = rank_prefix
        self.index_prefix = index_prefix
        self.playlist = playlist
        self.playlist_start = playlist_start
        self.playlist_end = playlist_end
        self.playlist_limit = playlist_limit

    def get_video_url_new(self):
        """
        anyVideo.gidInformation.packerData.video.videoResource.normal.video_list

        待解决：获取的main_url, 使用base64解码后为乱码，而不是真实的URL
        """

    def get_video_list(self):
        video_list = []
        if self.is_series and self.playlist:
            # 获取合集视频列表
            items = utils.get_series_list(
                pseries_id=self.pseries['id'],
                start=self.playlist_start,
                end=self.playlist_end or self.pseries['seriesInfo']['item_num'],
                limit=self.playlist_limit
            )
            for item in items:
                video_id = item['video_id']
                video_list.append({
                    'item_id': item['item_id'],
                    'vid': video_id,
                    'title': item['title'],
                    'rank': item['rank'],
                })
        else:
            # 获取单视频信息
            video_list.append({
                'item_id': self.video['item_id'],
                'vid': self.video['vid'],
                'title': self.video['title'],
                'rank': self.video['rank'],
            })

        return video_list

    def download(self, dryrun=False, prefix_pattern=None, definition='720p'):
        if not self.ssr_hydrated_data:
            return

        video_list = self.get_video_list()

        start_index = 1
        if self.index_prefix and isinstance(self.index_prefix, int):
            start_index = self.index_prefix

        outfile_list = []
        for n, item in enumerate(video_list, start_index):
            if prefix_pattern:
                xigua = IXiGuaDown(url=item['item_id'])
                if not xigua.ssr_hydrated_data:
                    item['prefix'] = '000. '
                else:
                    video_abstract = xigua.video.get('video_abstract')
                    result = re.findall(prefix_pattern, video_abstract)
                    item['prefix'] = '{}. '.format(result[0]) if result else '111. '
            else:
                item['prefix'] = ''
                if self.index_prefix:
                    item['prefix'] = f'{n}. '
                if self.rank_prefix:
                    item['prefix'] = '{rank}. '.format(**item)

            if dryrun:
                video_url_list = utils.get_video_url_list(video_id=item['vid'])
                item['definitions'] = ', '.join(video_url_list.keys())
                utils.print_item(item)
            else:
                outfile = self.outdir / '{prefix}{title}.mp4'.format(**item)
                utils.download_video(vid=item['vid'], outfile=outfile, definition=definition)
                outfile_list.append(outfile)

        return outfile_list
