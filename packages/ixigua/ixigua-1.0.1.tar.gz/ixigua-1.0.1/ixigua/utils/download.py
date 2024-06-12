import time
import random

from pathlib import Path
from typing import Union

from webrequests import WebRequest

from .url import get_video_url


def download_video(vid: Union[str, int], outfile: Path, definition='720p'):
    """Download video from vid
    """
    while True:
        try:
            url = get_video_url(vid, definition=definition)
            if outfile.exists():
                resp = WebRequest.get_response(url, method='HEAD')
                content_length = resp.headers['Content-Length']
                if outfile.stat().st_size == int(content_length):
                    print(f'skip download: {outfile}')
                    break
            print(f'>>> downloading: {outfile}')
            WebRequest.download(url, str(outfile))
            break
        except Exception as e:
            time.sleep(random.randint(1, 5))
