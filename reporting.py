import os
import urllib as url
import re
import numpy as np


_TOKEN = os.environ.get('TRELLO_TOKEN')
_APP_KEY = os.environ.get('TRELLO_APP_KEY');


def _get_from_trello(api, *args):
  args = reduce(lambda x, a: a+'&'+x, args, '')
  f = url.urlopen(r'https://api.trello.com/1/%s?%skey=%s&token=%s' % (api, args, _APP_KEY, _TOKEN))
  return json.load(f)


def _get_lists(board_id):
  return [l['id'] for l in _get_from_trello('boards/%s/lists' % board_id, 'fields=id')]


def _get_cards(board_id):
  return [c['name'] for c in _get_from_trello('boards/%s/cards' % board_id, 'fields=name')]
  
  
def _get_time_data(cards):
  def cutout(card, pattern):
    m = re.search(pattern, card)
    if m is None:
      return ''
    b, e = m.span()
    return card[b:e]
    
  def parse(time):
    if time in ['', '?']:
      return np.nan
    return float(time)
    
  get_est  = lambda card: parse(cutout(card, r'^\(.*?\)')[1:-1])
  get_real = lambda card: parse(cutout(card, r'\[.*?\]$')[1:-1])
  return np.array([[get_est(card), get_real(card)] for card in cards])
