import textwrap


def print_item(item):
    print('=' * 80)
    print(textwrap.dedent('''
        rank:         {rank}
        title:        {title}
        vid:          {vid}
        item_id:      {item_id}
        definitions:  {definitions}
        prefix:       {prefix}
    ''').format(**item).strip())
