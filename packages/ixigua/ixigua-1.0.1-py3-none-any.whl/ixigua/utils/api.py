from webrequests import WebRequest


def get_series_list(pseries_id, start=0, end=None, limit=30):
    """
    根据合集ID，获取该合集的视频列表

    https://www.ixigua.com/api/videov2/pseries_more_v2?pSeriesId=6988400843246535199&rank=990&tailCount=30
    rank -- skip
    tailCount -- limit

    Refer: https://www.ixigua.com
    """
    url = 'https://www.ixigua.com/api/videov2/pseries_more_v2'

    headers = {'Referer': 'https://www.ixigua.com'}

    for rank in range(start, end, limit):
        payload = {
            'pSeriesId': pseries_id,
            'rank': rank,
            'tailCount': end - start + 1 if limit > (end - start + 1) else limit,
        }

        response = WebRequest.get_response(url, params=payload, headers=headers)
        data = response.json()['data']

        for item in data:
            yield item
