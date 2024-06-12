import click

from ixigua import version_info
from ixigua.core import IXiGuaDown


CONTEXT_SETTINGS = dict(
    help_option_names=['-?', '-h', '--help'],
    max_content_width=200,
)

__epilog__ = click.style('''

\b
examples:
    {prog} SINGLE_URL_OR_ID
    {prog} SERIES_URL_OR_ID --playlist
    {prog} SERIES_URL_OR_ID --playlist --rank-prefix
    {prog} SERIES_URL_OR_ID --playlist --playlist-start 10 --playlist-end 20 -O 10-20 --index-prefix 10
    {prog} SERIES_URL_OR_ID --playlist --prefix-pattern '第\d+课'
                              
\x1b[34mcontact: {author} <{author_email}>
''', fg='yellow').format(**version_info)

@click.command(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
    epilog=__epilog__,
)
@click.argument('url')
@click.option('-O', '--outdir', help='output directory', default='download', show_default=True)
@click.option('--playlist', help='download playlist', is_flag=True)
@click.option('--playlist-start', help='playlist start index', type=int, default=0)
@click.option('--playlist-end', help='playlist end index', type=int)
@click.option('--rank-prefix', help='add prefix with the rank number', is_flag=True)
@click.option('--index-prefix', help='add prefix with the index number', type=int)
@click.option('--prefix-pattern', help='match prefix pattern from video_abstract, eg. "第\d+课"')
@click.option('--definition', help='the video definition', default='720p')
@click.option('--dryrun', help='dryrun mode', is_flag=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
def cli(**kwargs):
    ixigua = IXiGuaDown(
        url=kwargs['url'],
        outdir=kwargs['outdir'],
        rank_prefix=kwargs['rank_prefix'],
        index_prefix=kwargs['index_prefix'],
        playlist=kwargs['playlist'],
        playlist_start=kwargs['playlist_start'],
        playlist_end=kwargs['playlist_end'],
    )

    ixigua.download(
        dryrun=kwargs['dryrun'],
        prefix_pattern=kwargs['prefix_pattern'],
        definition=kwargs['definition'],
    )


def main():
    cli()


if __name__ == '__main__':
    main()
