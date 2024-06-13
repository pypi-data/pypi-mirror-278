#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

import curses
from viewtext_c.color  import Palette
from viewtext_c.const  import META_BEG, META_END, STYLE_END, LINE_TRUNCATE_CHAR
from viewtext_c.stryng import display_w

def paint_colored_str(
		win:  curses.window,
		y:    int,
		x:    int,
		str:  str,
		attr: int
			) -> None:
	tuples = []
	for pair in str.split(f'{META_BEG}{STYLE_END}{META_END}'):  # split into unstyled-styled pairs
		match pair.split(f'{META_BEG}'):                          # break apart the pair
			case [unstyled] if unstyled != '':                      # if no styling
				tuples.append((attr, unstyled))
			case [unstyled, styled]:
				if unstyled != '':
					tuples.append((attr, unstyled))
				elt, strng = styled.split(f'{META_END}')              # break off the styling
				tuples.append((Palette.elt_attr[elt], strng))
	win_h, win_w = win.getmaxyx()
	canvas_size  = win_h * win_w - (y * win_w + x)
	win.move(y, x)
	for attri, stri in tuples:
		paint_str(win, stri, attri, canvas_size)
		canvas_size -= display_w(stri)

# paint_str() gets around a curses bug that crashes when you write to the lower right corner of a window

def paint_str(
		win:      curses.window,
		str:      str,
		attr:     int,
		canvas_w: int,
			) -> None:
	str_w = display_w(str)
	if str_w == 0 or canvas_w == 0:
		return
	if   str_w <  canvas_w:
		win.addstr(str, attr)
	elif str_w == canvas_w:
		win.scrollok(False)
		try:
			win.addstr(str, attr)
		except curses.error:
			pass
		except Exception as e:
			pass
	else:
		w = 0
		i = -1
		for c in str:
			c_w = display_w(c)
			if (w + c_w) > canvas_w:
				break
			i += 1
			w += c_w
		if i >= 0:
			win.addstr(str[:i], attr)
		while (w < canvas_w):
			win.addstr(' ', attr)
			w += 1
		win.insch (LINE_TRUNCATE_CHAR, attr)

def paint_str_at_x_y(
		win:  curses.window,
		y:    int,
		x:    int,
		str:  str,
		attr: int,
			) -> None:
	win_h, win_w = win.getmaxyx()
	canvas_size  = win_h * win_w - (y * win_w + x)
	win.move(y, x)
	paint_str(win, str, attr, canvas_size)
