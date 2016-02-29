import os
import urllib as url


_TOKEN = os.environ.get('TRELLO_TOKEN')
_APP_KEY = os.environ.get('TRELLO_APP_KEY');


def _get_from_trello(api, *args):
  args = reduce(lambda x, a: a+'&'+x, args, '')
  f = url.urlopen(r'https://api.trello.com/1/%s?%skey=%s&token=%s' % (api, args, _APP_KEY, _TOKEN))
  return json.load(f)


def _get_lists(board_id):
  return [l['id'] for l in _get_from_trello('boards/%s/lists' % board_id, 'fields=id')]


