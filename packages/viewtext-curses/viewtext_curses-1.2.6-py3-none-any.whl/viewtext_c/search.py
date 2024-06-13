#! /usr/bin/python3.10
# -*- coding: utf-8 -*-

from collections      import namedtuple
from viewtext_c.stack import Stack

Posn        = namedtuple('Posn',
	[
		'row',
		'col',
	])

SearchFrame = namedtuple('SearchFrame',
	[
		'ss',        # search string
		'ss_repr',   # search string representation in status bar
		'matches',   # search string match locations
		'rank',      # index of the current match: match == matches[rank]
		'origin',    # pad coordinates (displaying matches[rank])
	])

EnvFrame = namedtuple('EnvFrame',
	[
		'state',     # in ['normal', 'search', 'arg', 'C-x', 'C-f']
		'arg',       # if state == 'arg', the value of arg (as a string)
		'msg',       # status bar message
		'searches',  # if state == 'search', stack of SearchFrames
	])

class EnvsFrame:
	state:    str
	arg:      str
	searches: Stack

	def __init__(self, state: str, arg = '', searches = None) -> None:
		self.state    = state
		self.arg      = arg
		self.searches = searches

	def __repr__(self) -> str:
		match self.state:
			case 'normal':
				return ''
			case 'search':
				_, ss_repr, matches, rank, _ = self.searches.top()
				return f'Search: {ss_repr}' + (f' [{rank + 1}/{len(matches)}]' if matches else '')
			case 'arg':
				return f'C-u {self.arg}-' if self.arg else 'C-u-'
			case 'C-x':
				return 'C-x-'
			case 'C-f':
				return 'C-f-'
			case _:
				raise Exception(f'Unknown state: {self.state}')
