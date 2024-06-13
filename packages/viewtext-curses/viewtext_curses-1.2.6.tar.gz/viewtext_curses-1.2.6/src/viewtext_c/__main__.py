#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

# A text viewer like less, with scrolling
# Requires: Python 3.10+

# Usage:
# viewtext-curses [OPTIONS] <text file>

# Copyright (C) 2024 Joe Rodrigue <joe.rodrigue at gmail dot com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import curses
import json
import locale
import os
import subprocess
from collections.abc    import Generator
from datetime           import datetime
from time               import sleep
from viewtext_c.color   import Palette
from viewtext_c.globyl  import Global
from viewtext_c.pane    import Pane, init_pane, refresh_status_bar
from viewtext_c.util_io import file_available_for_read, file_available_for_write

HISTORY_FILES = [
	'~/.config/viewtext/.history',
	'~/.viewtext_history',
	'./.viewtext_history'
]

chars_: list[str] = []

def init_curses() -> None:
	curses.curs_set(0)  # make cursor invisible
	(_availmask, _oldmask) = curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
	Palette.init_colors()

def restore_curses() -> None:
	curses.curs_set(1)  # restore normal cursor visibility

def movement(c: int | str, state: str) -> bool:
	"""Return True iff character <c> in state <state> represents a movement command (eg, scroll)"""
	if c in (
			curses.KEY_DOWN,   # Scroll down one line
			curses.KEY_UP,     # Scroll up one line
			curses.KEY_SF,     # Scroll down 10 lines (iTerm only)
			curses.KEY_SR,     # Scroll up 10 lines   (iTerm only)
			curses.KEY_NPAGE,  # Scroll down 1 page
			curses.KEY_PPAGE,  # Scroll up 1 page

			curses.KEY_SRIGHT, # Scroll right 1/3 page
			curses.KEY_SLEFT,  # Scroll left 1/3 page
			curses.KEY_END,    # Jump to end of file
			curses.KEY_HOME,   # Jump to beginning of file
					):
		return True
	if state in (
			'C-f',
			'style-elt',
			'style-elt-ground',
			'style-elt-color',
			'switch-theme',
			'save-theme',
			'delete-theme',
		):
		return False
	return c in [
			curses.KEY_RIGHT,
			curses.KEY_LEFT,
		]

def open_frame(stdscr: curses.window, filename: str, playback: bool) -> None:
	"""Opens the root curses window and implements the main loop, responding to each input character"""
	try:
		init_curses()
		init_pane(stdscr, filename)
		state       = 'normal'
		prev_ctl_l  = False
		input_chars = input_ch_gen(stdscr, playback)
		stdscr.refresh()
		Pane.refresh_all()
		refresh_status_bar(stdscr)
		for c in input_chars:
			state = find_next_state(c, prev_ctl_l, state)
			if state == 'quit':
				break
			Pane.refresh_all()
			refresh_status_bar(stdscr)
			prev_ctl_l = c == '\N{FF}'
			if playback:
				sleep(Global.delay)
	except Exception as e:
		print(e)
	finally:
		if not playback:
			p = file_available_for_write(map(lambda str: f'{str}_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}', HISTORY_FILES))
			if not p:
				raise Exception(f'open_frame: cannot open history file for write')
			with p.open(mode = 'w') as f:
				f.write(json.dumps(chars_))
		restore_curses()

def input_ch_gen(win: curses.window, playback: bool) -> Generator[str, str, str]:  # [yield-type, send-type, return-type]
	global chars_

	if playback:
		p = file_available_for_read(HISTORY_FILES)
		if not p:
			raise Exception(f'input_ch_gen: cannot locate history file for playback')
		with p.open() as f:
			chars = json.loads(f.read())
		for c in chars:
			yield c
	while True:
		c = win.get_wch()
		chars_.append(c)
		yield c

def find_next_state(c: int | str, prev_ctl_l: bool, state: str) -> str:
	if movement(c, state):    return Pane.move(c)
	if c == curses.KEY_MOUSE: return Pane.mouse_event(state)
	match state:
		case 'normal':           return Pane.on_normal          (c)
		case 'search':           return Pane.on_search          (c, prev_ctl_l)
		case 'arg':              return Pane.on_arg             (c)
		case 'C-x':              return Pane.on_ctl_x           (c)
		case 'C-f':              return Pane.on_ctl_f           (c)
		case 'style-elt':        return Pane.on_style_elt       (c)
		case 'style-elt-ground': return Pane.on_style_elt_ground(c)
		case 'style-elt-color':  return Pane.on_style_elt_color (c)
		case 'switch-theme':     return Pane.on_switch_theme    (c)
		case 'save-theme':       return Pane.on_save_theme      (c)
		case 'delete-theme':     return Pane.on_delete_theme    (c)
		case _:                  raise Exception(f'find_next_state: unknown state {state}')


@click.command()
@click.argument('filename',                             type = click.Path(exists = True, readable = True))
@click.option('--debug/--no-debug',       '_debug',     type = bool,  help = 'Turn on debugging',                      default = False)
@click.option('--delay',                  '_delay',     type = float, help = 'Time in seconds for embedded delays',    default = 0.0)
@click.option('--msg-delay',              '_msg_delay', type = float, help = 'Time in seconds for temporary messages', default = 1.0)
@click.option('--playback/--no-playback', '_playback',  type = bool,  help = 'Recreate previous session',              default = False)
@click.option('--tab-width',              '_tab_w',     type = int,   help = 'Convert each tab to tab_width spaces',   default = 2)
@click.option('--theme',                  '_theme',     type = str,   help = 'The color scheme for the display',       default = '')
@click.version_option(package_name = 'viewtext-curses')
def read_cl_arguments(filename: str, _debug: bool, _delay: float, _playback: bool, _msg_delay: float, _tab_w: int, _theme: str) -> None:
	Global.debug          = _debug
	Global.delay          = _delay
	Global.msg_delay      = _msg_delay
	Global.tab_w          = _tab_w
	Palette.current_theme = _theme
	locale.setlocale(locale.LC_ALL, '')
	filetype  = str(subprocess.check_output(['file', filename])).split(': ')[1]
	for type in ('text', 'JSON', 'empty'):
		if type in filetype:
			curses.wrapper(open_frame, os.path.abspath(filename), _playback)
			break
	else:
		if (input(f'{filename} may be a binary file.  See it anyway? ')) == 'y':
			curses.wrapper(open_frame, os.path.abspath(filename), _playback)

if __name__ == '__main__':
	read_cl_arguments()
