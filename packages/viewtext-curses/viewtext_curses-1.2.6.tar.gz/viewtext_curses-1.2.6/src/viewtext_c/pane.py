#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

import codecs
import curses
import fnmatch
import os
import subprocess
from functools         import reduce
from time              import sleep
from typing            import Any, Callable, Optional
from unicodedata       import category as unicode_category
from viewtext_c.color  import Palette
from viewtext_c.const  import META_BEG, META_END, STYLE_END, cSTYLE, cDIR, CURSOR_CHAR, CURSOR, LINE_TRUNCATE_CHAR
from viewtext_c.globyl import Global
from viewtext_c.paint  import paint_colored_str, paint_str_at_x_y
from viewtext_c.search import EnvFrame, Posn, SearchFrame
from viewtext_c.stack  import Stack
from viewtext_c.stryng import display_w
from viewtext_c.util   import Completion, compose

DEFAULT_ARG         = 4
DEFAULT_SHIFT_W     = 8
FIND_PREFIX         = 'Find'
MIN_PANE_HEIGHT     = 2
MIN_PANE_WIDTH      = 16
SAVE_THEME_PREFIX   = 'Save current theme as'
SCROLL_H_OVERLAP    = 2   # default is to scroll a screenful with this much overlap
SEARCH_PREFIX       = 'Search'
STYLING_PREFIX      = 'Modify'
SWITCH_THEME_PREFIX = 'Switch to theme'
DELETE_THEME_PREFIX = 'Delete theme'

EDGE_CHAR      = ' ' # u'\174'

color_         = ''
completions_   = Completion()
elt_           = ''
focus_:     Optional['Pane'] = None
from_pane_: Optional['Pane'] = None
from_x_: int        = -1
from_y_: int        = -1
ground_        = ''
msgs_: list[str]    = []
path_          = ''
patt_          = ''
sprefix_       = ''
styled_color_  = ''
styled_elt_    = ''
styled_prefix_ = ''
theme_         = ''

spaces_: Optional[curses.window] = None
stdscr_h_    = 0
stdscr_w_    = 0
v_alignment_ = 'center'

class Pane():
	buffers: dict[str, dict[str, Any]] = dict()
#	panes:   dict[str, set['Pane']]    = dict()  ## maps filenames to panes.  not used
	pane_0:       Optional['Pane']     = None

	def __init__(self,
							filename: str,
							pad_y:    int,
							pad_x:    int,
							pminrow:  int,
							pmaxrow:  int,
							pmincol:  int,
							pmaxcol:  int,
							prev:     Optional['Pane']        = None,
							caption:  Optional[curses.window] = None,
							edge:     bool | curses.window    = False,
							encoding: Optional[str]           = 'utf-8',
								) -> None:
		self.filename = filename
		self.pad_y    = pad_y
		self.pad_x    = pad_x
		self.pminrow  = pminrow
		self.pmaxrow  = pmaxrow
		self.pmincol  = pmincol
		self.pmaxcol  = pmaxcol
		self.next: Optional['Pane'] = prev and prev.next
		if prev is None:
			Pane.pane_0 = self
		else:
			prev.next   = self
		self.edge     = False if edge is False else create_window(pminrow, pmaxrow, pmaxcol, pmaxcol) if edge is True else edge
		_, _, tmincol, tmaxcol = self.pane_text_corners()
		self.caption  = caption or                create_window(pmaxrow, pmaxrow, tmincol, tmaxcol)
		self.envs = Stack(EnvFrame('normal', '', '', None))
		if filename not in self.buffers:
#			self.panes[filename] = set()  ## keep set of panes for this filename.  not used for now
			try:
				with codecs.open(filename, encoding = encoding) as f:
					content = f.read()
			except:
				print('Pane: Unable to open file %s' % filename)
			else:
				lines  = content.expandtabs(Global.tab_w).splitlines()
				maxlen = reduce(lambda x, y: x if x > y else y, [display_w(line) for line in lines], 0)
				pad    = curses.newpad(max(len(lines), 1), max(maxlen, 1))
				self.buffers[filename] = {
					'lines':    lines,
					'pad':      pad,
					'follow':   create_follow(lines),
					'prefixes': singleton_prefixes(lines),
				}
				self.rewrite(lines = lines, pad = pad)
#		self.panes[filename].add(self)  ## not used for now
		self.dirty = True

	def refresh(self) -> None:
		global focus_, spaces_

		tminrow, tmaxrow, tmincol, tmaxcol = self.pane_text_corners()
		path, fn = os.path.split(self.filename)
		dir      = os.path.basename(path)
		lcaption = f'  {os.path.join(dir, fn)}'
		rcaption = f' ({self.pad_y}, {self.pad_x})  '
		llen     = display_w(lcaption)
		rlen     = len(rcaption)
		scr_w    = tmaxcol - tmincol + 1
		clen     = scr_w - llen - rlen
		caption  = lcaption + ' ' * clen + rcaption
		attr     = Palette.elt_attr['caption_focus' if focus_ == self else 'caption_nofocus']
		paint_str_at_x_y(self.caption, 0, 0, caption, attr)
		self.caption.refresh()
		pad      = self.buffers[self.filename]['pad']
		pad_h, pad_w = pad.getmaxyx()
		scr_h    = tmaxrow - tminrow + 1
		txt_h    = min(pad_h - self.pad_y, scr_h)  # display this many lines of text
		txt_w    = min(pad_w - self.pad_x, scr_w)  # display this many columns of text
		xmaxrow  = tminrow + txt_h - 1             # last line of text
		xmaxcol  = tmincol + txt_w - 1             # last column of text
		pad.clearok(True)
		pad.refresh(self.pad_y, self.pad_x, tminrow,     tmincol,     xmaxrow, xmaxcol)
		if txt_h < scr_h:                          # if text doesn't fill the pane
			assert spaces_ is not None
			spaces_.refresh(    0,          0, xmaxrow + 1, tmincol,     tmaxrow, tmaxcol)
		if txt_w < scr_w:
			assert spaces_ is not None
			spaces_.refresh(    0,          0, tminrow,     xmaxcol + 1, xmaxrow, tmaxcol)
		if self.edge:
			attr = Palette.elt_attr['edge_focus' if focus_ == self else 'edge_nofocus']
			self.fill_edge(attr)
			assert type(self.edge) == curses.window
			self.edge.refresh()
		self.dirty = False

	def fill_edge(self, attr: int) -> None:
		pminrow, pmaxrow, _, _ = self.pane_corners()
		edge                   = EDGE_CHAR * (pmaxrow - pminrow + 1)
		assert type(self.edge) == curses.window
		paint_str_at_x_y(self.edge, 0, 0, edge, attr)

	@classmethod
	def refresh_all(cls) -> None:
		def cont(pane):
			if pane:
				if pane.dirty:
					pane.refresh()
				cont(pane.next)

		cont(cls.pane_0)

	def rewrite(self, lines: list[str], pad: curses.window) -> None:
		attr = Palette.elt_attr['text']
		pad.bkgd(' ', attr)
		for l, line in enumerate(lines):
			paint_str_at_x_y(pad, l, 0, line, attr)

	def mv_down(self, delta: int) -> bool:
		pad      = self.buffers[self.filename]['pad']
		pad_h, _ = pad.getmaxyx()
		txt_h    = pad_h - self.pad_y  # remaining lines
		if (delta < txt_h):
			self.pad_y += delta
			self.dirty  = True
		return delta < txt_h

	def scroll_h(self, partial: bool) -> int:
		tminrow, tmaxrow, _, _ = self.pane_text_corners()
		scr_h                  = tmaxrow - tminrow + 1
		return (scr_h // 3) if partial else (scr_h - SCROLL_H_OVERLAP)

	def mv_up(self, delta: int) -> bool:
		if self.pad_y > 0:
			self.pad_y -= min(self.pad_y, delta)
			self.dirty  = True
			return True
		return False

	def mv_right(self, delta: int) -> bool:
		pad                    = self.buffers[self.filename]['pad']
		_, pad_w               = pad.getmaxyx()
		txt_w                  = pad_w - self.pad_x
		_, _, tmincol, tmaxcol = self.pane_text_corners()
		scr_w                  = tmaxcol - tmincol + 1
		rhs_offscreen_txt_w    = txt_w - scr_w
		if (rhs_offscreen_txt_w > 0):
			self.pad_x += min(delta, rhs_offscreen_txt_w)
			self.dirty  = True
		return rhs_offscreen_txt_w > 0

	def mv_left(self, delta: int) -> bool:
		if self.pad_x > 0:
			self.pad_x -= min(self.pad_x, delta)
			self.dirty  = True
			return True
		return False

	def mv_home(self) -> None:
		if (self.pad_y, self.pad_x) == (0, 0):
			return
		self.pad_y, self.pad_x = 0, 0
		self.dirty             = True

	def mv_end(self) -> None:
		pad                    = self.buffers[self.filename]['pad']
		pad_h, _               = pad.getmaxyx()
		tminrow, tmaxrow, _, _ = self.pane_text_corners()
		scr_h                  = tmaxrow - tminrow + 1
		self.pad_y             = pad_h - scr_h + SCROLL_H_OVERLAP
		self.pad_x             = 0
		self.dirty             = True

	def resize(self,
						direction: str,
						edge:      bool | curses.window,
						size:      int = 0,
						delta:     int = 0,
							) -> None:
		pminrow, pmaxrow, pmincol, pmaxcol = self.pane_corners()
		match direction:
			case 'west':
				pmaxcol      = pmincol + size - 1 if size else pmaxcol + delta
				self.pmaxcol = pmaxcol
			case 'north':
				pmaxrow      = pminrow + size - 1 if size else pmaxrow + delta
				self.pmaxrow = pmaxrow
			case 'east':
				pmincol      = pmaxcol - size + 1 if size else pmincol - delta
				self.pmincol = pmincol
			case 'south':
				pminrow      = pmaxrow - size + 1 if size else pminrow - delta
				self.pminrow = pminrow
			case _:
				raise Exception(f'resize: Unknown direction {direction}')
		if direction    != 'east':
			self.edge      = edge and create_window(pminrow, pmaxrow, pmaxcol, pmaxcol)
		if direction    != 'south':
			_, _, tmincol, tmaxcol = self.pane_text_corners()
			self.caption   =          create_window(pmaxrow, pmaxrow, tmincol, tmaxcol)
		self.dirty       = True

	def split_horizontal(self, arg: str) -> None:
		global msgs_

		s_pminrow, s_pmaxrow, s_pmincol, s_pmaxcol = self.pane_corners()
		s_pheight = s_pmaxrow - s_pminrow + 1
		if s_pheight < MIN_PANE_HEIGHT * 2:
			msgs_.append(f'Focused pane {self.filename} is too small to split')
		val       = s_pheight // 2 if arg == '' else int(arg)
		u_pheight = val            if val >= 0  else s_pheight + val
		if             u_pheight < MIN_PANE_HEIGHT:
			msgs_.append(f'The upper pane must have a minimum of {MIN_PANE_HEIGHT} lines')
		if s_pheight - u_pheight < MIN_PANE_HEIGHT:
			msgs_.append(f'The lower pane must have a minimum of {MIN_PANE_HEIGHT} lines')

		l_pminrow = s_pminrow + u_pheight
		l_pmaxrow = s_pmaxrow
		l_pmincol = s_pmincol
		l_pmaxcol = s_pmaxcol
		assert type(self.edge) == bool or type(self.edge) == curses.window
		Pane(self.filename, self.pad_y, self.pad_x, l_pminrow, l_pmaxrow, l_pmincol, l_pmaxcol, prev = self, caption = self.caption, edge = self.edge)
		self.resize('north', bool(self.edge), size = u_pheight)

	def split_vertical(self, arg: str) -> None:
		global msgs_

		s_pminrow, s_pmaxrow, s_pmincol, s_pmaxcol = self.pane_corners()
		s_pwidth  = s_pmaxcol - s_pmincol + 1
		if s_pwidth < MIN_PANE_WIDTH * 2:
			msgs_.append(f'Focused pane {self.filename} is too narrow to split')
		val       = s_pwidth // 2 if arg == '' else int(arg)
		l_pwidth  = val           if val >= 0  else s_pwidth + val
		if            l_pwidth < MIN_PANE_WIDTH:
			msgs_.append(f'The left pane must have a minimum of {MIN_PANE_WIDTH} columns')
		if s_pwidth - l_pwidth < MIN_PANE_WIDTH:
			msgs_.append(f'The right pane must have a minimum of {MIN_PANE_WIDTH} columns')
		r_pminrow = s_pminrow
		r_pmaxrow = s_pmaxrow
		r_pmincol = s_pmincol + l_pwidth
		r_pmaxcol = s_pmaxcol
		assert type(self.edge) == bool or type(self.edge) == curses.window
		Pane(self.filename, self.pad_y, self.pad_x, r_pminrow, r_pmaxrow, r_pmincol, r_pmaxcol, prev = self, edge = self.edge)
		self.resize('west', True, size = l_pwidth)

	def delete_other_panes(self) -> None:
		def cont(pane: 'Pane') -> None:
			if pane != self:
				pane.delete()
				Pane.refresh_all()
				sleep(Global.delay)
				cont(pane.next_pane())

		cont(self.next_pane())

	def delete(self) -> 'Pane':
		global focus_, msgs_

		switch_focus = self == focus_
		next = self.next_pane()
		prev = self.prev_pane()
		if self == next:
			msgs_.append('Cannot delete the last pane')
			return self
		self.unwind_env_stack()
		if   (self.is_west(prev)):
			self.resize_west_panes()
		elif (self.is_north(prev)):
			self.resize_north_panes()
		elif (self.is_east(next)):
			self.resize_east_panes()
		elif (self.is_south(next)):
			self.resize_south_panes()
		else:
			raise Exception('Pane.delete: cannot find panes that share a border')
		if self == Pane.pane_0:
			Pane.pane_0 = self.next
		else:
			prev.next = self.next
		if switch_focus:
			prev.dirty  = True  # dirty because it now has the focus
		return prev

	def shrink_to_buffer_all(self) -> None:
		def cont(pane: 'Pane') -> None:
			pane.shrink_to_buffer(south_only = True)
			Pane.refresh_all()
			sleep(Global.delay)
			if (next := pane.next):
				cont(next)

		assert type(Pane.pane_0) == Pane
		cont(Pane.pane_0)

	def shrink_to_buffer(self, south_only: bool = False) -> None:
		pad                        = self.buffers[self.filename]['pad']
		pad_h, _                   = pad.getmaxyx()
		s_tminrow, s_tmaxrow, _, _ = self.pane_text_corners()
		scr_h                      = s_tmaxrow - s_tminrow + 1
		if scr_h > pad_h:
			delta = scr_h - pad_h
			if   (self.is_south(self.next_pane())):
				for pane in self.find_south_panes():
					pane.resize('south', bool(pane.edge), delta = delta)
				self.pad_y = 0
				self.resize('north', bool(self.edge), size = pad_h + 1)
			elif south_only:
				pass
			elif (self.is_north(self.prev_pane())):
				for pane in self.find_north_panes():
					pane.resize('north', bool(pane.edge), delta = delta)
				self.pad_y = 0
				self.resize('south', bool(self.edge), size = pad_h + 1)

	def p_next(self) -> 'Pane':
		next       = self.next_pane()
		self.dirty = True
		next.dirty = True
		return next

	def p_prev(self) -> 'Pane':
		prev       = self.prev_pane()
		self.dirty = True
		prev.dirty = True
		return prev

	def next_pane(self) -> 'Pane':
		assert type(Pane.pane_0) == Pane
		return (self.next or Pane.pane_0)

	def prev_pane(self) -> 'Pane':
		def cont(pane):
			while (next := pane.next_pane()) != self:
				pane = next
			return pane

		return cont(self)

	def is_west(self, pane: 'Pane') -> bool:
		s_minrow, s_maxrow, s_mincol, _ = self.pane_text_corners()
		p_minrow, p_maxrow, p_mincol, _ = pane.pane_text_corners()
		return ((p_minrow >= s_minrow) and
						(p_maxrow <= s_maxrow) and
						(p_mincol <  s_mincol))

	def is_north(self, pane: 'Pane') -> bool:
		s_minrow, _, s_mincol, s_maxcol = self.pane_text_corners()
		p_minrow, _, p_mincol, p_maxcol = pane.pane_text_corners()
		return ((p_mincol >= s_mincol) and
						(p_maxcol <= s_maxcol) and
						(p_minrow <  s_minrow))

	def is_east(self, pane: 'Pane') -> bool:
		s_minrow, s_maxrow, s_mincol, _ = self.pane_text_corners()
		p_minrow, p_maxrow, p_mincol, _ = pane.pane_text_corners()
		return ((p_minrow >= s_minrow) and
						(p_maxrow <= s_maxrow) and
						(p_mincol >  s_mincol))

	def is_south(self, pane: 'Pane') -> bool:
		s_minrow, _, s_mincol, s_maxcol = self.pane_text_corners()
		p_minrow, _, p_mincol, p_maxcol = pane.pane_text_corners()
		return ((p_mincol >= s_mincol) and
						(p_maxcol <= s_maxcol) and
						(p_minrow >  s_minrow))

	def pane_corners(self) -> tuple[int, int, int, int]:
		return (self.pminrow, self.pmaxrow, self.pmincol, self.pmaxcol)

	def pane_text_corners(self) -> tuple[int, int, int, int]:
		pminrow, pmaxrow, pmincol, pmaxcol = self.pane_corners()
		return (pminrow, pmaxrow - 1, pmincol, pmaxcol - (1 if self.edge else 0))

	def resize_west_panes(self) -> None:
		_, _, s_pmincol, s_pmaxcol = self.pane_corners()
		delta                      = s_pmaxcol - s_pmincol + 1
		for pane in self.find_west_panes():
			pane.resize('west', bool(self.edge), delta = delta)

	def resize_north_panes(self) -> None:
		s_pminrow, s_pmaxrow, _, _ = self.pane_corners()
		delta                      = s_pmaxrow - s_pminrow + 1
		for pane in self.find_north_panes():
			pane.resize('north', bool(pane.edge), delta = delta)

	def resize_east_panes(self) -> None:
		_, _, s_pmincol, s_pmaxcol = self.pane_corners()
		delta                      = s_pmaxcol - s_pmincol + 1
		for pane in self.find_east_panes():
			pane.resize('east', bool(self.edge), delta = delta)

	def resize_south_panes(self) -> None:
		s_pminrow, s_pmaxrow, _, _ = self.pane_corners()
		delta                      = s_pmaxrow - s_pminrow + 1
		for pane in self.find_south_panes():
			pane.resize('south', bool(pane.edge), delta = delta)

	def find_west_panes(self) -> list['Pane']:
		panes                      = []
		s_pminrow, _, s_pmincol, _ = self.pane_corners()
		def cont(pane: 'Pane') -> list['Pane']:
			while True:
				p_pminrow, _, _, p_pmaxcol = pane.pane_corners()
				if p_pmaxcol == s_pmincol - 1:
					panes.append(pane)
					if p_pminrow == s_pminrow:
						return panes
				pane = pane.prev_pane()

		return cont(self.prev_pane())

	def find_north_panes(self) -> list['Pane']:
		panes                      = []
		s_pminrow, _, s_pmincol, _ = self.pane_corners()
		def cont(pane: 'Pane') -> list['Pane']:
			while True:
				_, p_pmaxrow, p_pmincol, _ = pane.pane_corners()
				if p_pmaxrow == s_pminrow - 1:
					panes.append(pane)
					if p_pmincol == s_pmincol:
						return panes
				pane = pane.prev_pane()

		return cont(self.prev_pane())

	def find_east_panes(self) -> list['Pane']:
		panes                      = []
		_, s_pmaxrow, _, s_pmaxcol = self.pane_corners()
		def cont(pane: 'Pane') -> list['Pane']:
			while True:
				_, p_pmaxrow, p_pmincol, _ = pane.pane_corners()
				if p_pmincol == s_pmaxcol + 1:
					panes.append(pane)
					if p_pmaxrow == s_pmaxrow:
						return panes
				pane = pane.next_pane()

		return cont(self.next_pane())

	def find_south_panes(self) -> list['Pane']:
		panes                      = []
		_, s_pmaxrow, _, s_pmaxcol = self.pane_corners()
		def cont(pane: 'Pane') -> list['Pane']:
			while True:
				p_pminrow, _, _, p_pmaxcol = pane.pane_corners()
				if p_pminrow == s_pmaxrow + 1:
					panes.append(pane)
					if p_pmaxcol == s_pmaxcol:
						return panes
				pane = pane.next_pane()

		return cont(self.next_pane())

	def replace(self, filename: str) -> 'Pane':
		self.unwind_env_stack()
		pminrow, pmaxrow, pmincol, pmaxcol = self.pane_corners()
		prev      = None if self == Pane.pane_0 else self.prev_pane()
		pane      = Pane(filename, 0, 0, pminrow, pmaxrow, pmincol, pmaxcol, prev = prev, edge = bool(self.edge))
		pane.next = self.next
		return pane

	def jump_to_ss(self,
									posns:        list[Posn],
									rank:         int           = -1,
									v_alignment_: Optional[str] = None,
										) -> tuple[int, Posn]:
		tminrow, tmaxrow, tmincol, tmaxcol = self.pane_text_corners()
		y, x   = self.pad_y, self.pad_x
		height = tmaxrow - tminrow + 1
		width  = tmaxcol - tmincol + 1
		rank   = next_match_rank(y, posns) if rank < 0 else rank
		posn   = posns[rank]
		match v_alignment_:
			case None:
				if not ((posn.row - y >= 0) and   \
								(posn.row - y <  height)):
					self.pad_y = max(0, posn.row - (height // 2))
				if not ((posn.col - x >= 0) and   \
								(posn.col - x <  width)):
					self.pad_x = max(0, posn.col - (width // 2))
			case 'center':
				self.pad_y = max(0, posn.row - (height // 2))
			case 'top':
				self.pad_y = posn.row
			case 'bottom':
				self.pad_y = posn.row - (height - 1)
			case _:
				raise Exception(f'jump_to_ss: illegal v_alignment: {v_alignment_}')
		return rank, Posn(self.pad_y, self.pad_x)

	@staticmethod
	def move(c: int | str) -> str:
		global focus_, msgs_

		assert focus_ is not None
		if focus_.envs.empty():
			raise Exception(f'move: envs stack is empty')
		(this_state, arg, _, _) = focus_.envs.top()
		if this_state == 'arg':
			focus_.envs.pop()
		msgs_ = []
		match c:
			case curses.KEY_DOWN | curses.KEY_NPAGE | curses.KEY_SF | curses.KEY_UP | curses.KEY_PPAGE | curses.KEY_SR:
				one_line  = (c == curses.KEY_DOWN) or (c == curses.KEY_UP)
				partial   = (c == curses.KEY_SF)   or (c == curses.KEY_SR)
				direction = 'down' if ((c == curses.KEY_DOWN) or (c == curses.KEY_NPAGE) or (c == curses.KEY_SF)) else 'up'
				if this_state == 'arg':
					arg      = arg or DEFAULT_ARG
					modifier = '' if one_line else '1/3 page ' if partial else 'page '
					msgs_.append(f'C-u {arg} {modifier}{direction}')
					delta  = int(arg)
				else:
					delta  = 1
				scroll_h = 1 if one_line else focus_.scroll_h(partial)
				dshift   = (direction == 'down') if (delta >= 0) else (direction == 'up')
				# mv       = lambda : focus_.mv_down(abs(delta) * scroll_h) if dshift else focus_.mv_up(abs(delta) * scroll_h)
				mv       = focus_.mv_down if dshift else focus_.mv_up
				if not mv(abs(delta) * scroll_h):
					curses.beep()
					msgs_.append('End of file' if dshift else 'Beginning of file')
			case curses.KEY_RIGHT | curses.KEY_SRIGHT | curses.KEY_LEFT | curses.KEY_SLEFT:
				one_column = (c == curses.KEY_RIGHT) or (c == curses.KEY_LEFT)
				direction  = 'right' if ((c == curses.KEY_RIGHT) or (c == curses.KEY_SRIGHT)) else 'left'
				if this_state == 'arg':
					arg      = arg or DEFAULT_ARG
					modifier = '' if one_column else 'shift '
					msgs_.append(f'C-u {arg} {modifier}{direction}')
					delta = int(arg)
				else:
					delta = 1
				shift_w = 1 if one_column else DEFAULT_SHIFT_W
				rshift  = (direction == 'right') if (delta >= 0) else (direction == 'left')
				mv      = focus_.mv_right if rshift else focus_.mv_left
				if not mv(abs(delta) * shift_w):
					if rshift:
						msgs_.append('Right edge of file')
			case curses.KEY_HOME:
				focus_.mv_home()
				msgs_.append('Beginning of file')
			case curses.KEY_END:
				focus_.mv_end()
				msgs_.append('End of file')
		if msgs_:
			msgs_.append(focus_.envs.top().msg)
		return focus_.envs.top().state if this_state == 'arg' else this_state

	@staticmethod
	def on_normal(c: int | str) -> str:
		global completions_, focus_, msgs_, patt_, theme_

		assert focus_ is not None
		if focus_.envs.empty():
			raise Exception(f'on_normal: envs stack is empty')
		msgs_ = []
		match c:
			case '\N{ESC}':
				env = focus_.envs.pop()
				if focus_.envs.empty() or (focus_.envs.top().state != 'search'):
					focus_.envs.push(env)
					msgs_.append('No search to resume')
				else:
					focus_.pad_y, focus_.pad_x = focus_.envs.top().searches.top().origin
					msgs_.append('Resuming search')
			case '/':
				search = SearchFrame('', '', [], None, Posn(focus_.pad_y, focus_.pad_x))
				focus_.envs.push(EnvFrame('search', '', f'{SEARCH_PREFIX}: ', Stack(search)))
			case '\N{CAN}':          # control-X on MacOS
				focus_.envs.push(EnvFrame('C-x',    '', 'C-x-',     None))
			case '\N{NAK}':          # control-U on MacOS
				focus_.envs.push(EnvFrame('arg',    '', 'C-u-',     None))
			case '\N{BEL}':          # control-G on MacOS
				msgs_.append('Command aborted')
				curses.beep()
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				return 'normal'
			case '=':
				tminrow, tmaxrow, tmincol, tmaxcol = focus_.pane_text_corners()
				height = tmaxrow - tminrow + 1
				width  = tmaxcol - tmincol + 1
				msgs_.append(f'  Height: {height} rows; Width: {width} columns')
			case 'c':
				focus_.envs.push(EnvFrame('style-elt', '', 'Element to modify [TAB to list]: ', None))
				completions_.disable()
				patt_ = ''
			case 'd':
				focus_.envs.push(EnvFrame('delete-theme', '', f'{DELETE_THEME_PREFIX} [TAB to list]: ', None))
				completions_.disable()
			case 'q':
				return 'quit'
			case 's':
				path = Palette.save_themes()
				msgs_.append(f'  Saved current configuration to {path}')
			case 't':
				msgs_.append(f'Theme: {Palette.current_theme}, '
										 f'{Palette.n_colors}/{curses.COLORS} colors, '
										 f'{Palette.n_pairs}/{Palette.n_pairs_max} color pairs '
										 f'{focus_.buffers[focus_.filename]["pad"].encoding}'
									 )
			case 'w':
				focus_.envs.push(EnvFrame('switch-theme', '', f'{SWITCH_THEME_PREFIX} [TAB to list]: ', None))
				theme_ = ''
				completions_.disable()
			case 'x':
				focus_.envs.push(EnvFrame('save-theme', '', f'{SAVE_THEME_PREFIX} [{Palette.current_theme}] [TAB to list]: ', None))
				theme_ = ''
				completions_.disable()
			case _:
				curses.beep()
				if type(c) == str:
					msgs_.append(f'{my_repr(c)} is undefined')
				else:
					msgs_.append(f'Integer code {c} is undefined')
		msgs_.append(focus_.envs.top().msg)
		return focus_.envs.top().state

	@staticmethod
	def on_search(c: int | str, prev_ctl_l: bool) -> str:
		global focus_, msgs_, v_alignment_

		msgs_    = []
		assert focus_ is not None
		pad      = focus_.buffers[focus_.filename]['pad']
		searches = focus_.envs.top().searches
		if type(c) == int:
			curses.beep()
			msgs_.append(f'{SEARCH_PREFIX}: Integer code {c} is not a legal search character')
			msgs_.append(focus_.envs.top().msg)
			return focus_.envs.top().state

		assert type(c) == str
		match c:
			case '\n' | '\N{TAB}' | curses.KEY_BTAB | curses.KEY_ENTER:
				if searches.empty() or (not searches.top().matches):
					return 'search'
				ss, ss_repr, matches, rank, _ = searches.pop()
				color_strs([matches[rank]], ss, pad, Palette.elt_attr['search'])
				rank = (rank + (1 if (c == '\n' or c == '\N{TAB}') else -1)) % len(matches)
				color_strs([matches[rank]], ss, pad, Palette.elt_attr['search_current'])
				rank, origin = focus_.jump_to_ss(      matches, rank)
				searches.push(SearchFrame(ss, ss_repr, matches, rank, origin))
				msg = f'{SEARCH_PREFIX}: {ss_repr} [{rank + 1}/{len(matches)}]'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame('search', '', msg, searches))
				Pane.mark_filename_buffers(focus_.filename)
			case '\N{FF}':                      # Ctl-L on MacOS
				if searches.empty() or (not searches.top().matches):
					return 'search'
				if prev_ctl_l:
					alignments   = ['center', 'top', 'bottom']
					i            = alignments.index(v_alignment_)
					v_alignment_ = alignments[(i + 1) % len(alignments)]
				else:
					v_alignment_ = 'center'
				ss, ss_repr, matches, rank, _ = searches.pop()
				rank, origin   = focus_.jump_to_ss(     matches, rank, v_alignment_)
				searches.push(SearchFrame(ss, ss_repr, matches, rank, origin))
				focus_.dirty   = True
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				if searches.size() <= 1:          # first frame on searches is the empty string
					return 'search'
				ssx, _, matchesx, _, _ = searches.pop()
				if matchesx:
					color_strs( matchesx,       ssx, pad, Palette.elt_attr['text'], last_ch = True)
				ss, ss_repr, matches, rank, origin = searches.top()
				if matches:
					color_strs( matches,        ss,  pad, Palette.elt_attr['search'])
					color_strs([matches[rank]], ss,  pad, Palette.elt_attr['search_current'])
				focus_.pad_y, focus_.pad_x = origin
				msg = f'{SEARCH_PREFIX}: {ss_repr}' + (f' [{rank + 1}/{len(matches)}]' if matches else '')
				focus_.envs.pop()
				focus_.envs.push(EnvFrame('search', '', msg, searches))
				Pane.mark_filename_buffers(focus_.filename)
			case '\N{ESC}':
				msgs_.append('Suspended search')
				focus_.envs.push(EnvFrame('normal', '', '',     None))
			case '\N{CAN}':          # control-X on MacOS
				focus_.envs.push(EnvFrame('C-x',    '', 'C-x-', None))
			case '\N{NAK}':          # control-U on MacOS
				focus_.envs.push(EnvFrame('arg',    '', 'C-u-', None))
			case '\N{EOT}':          # control-D on MacOS
				ss, _, matches, _, _ = focus_.envs.pop().searches.pop()
				if matches:
					color_strs(matches, ss, pad, Palette.elt_attr['text'])
				msgs_.append('Search terminated')
				Pane.mark_filename_buffers(focus_.filename)
			case '\N{BEL}':          # control-G on MacOS
				ss, _, matches, _, _ = focus_.envs.pop().searches.pop()
				if matches:
					color_strs(matches, ss, pad, Palette.elt_attr['text'])
				curses.beep()
				msgs_.append('Search aborted')
				Pane.mark_filename_buffers(focus_.filename)
			case _:
				if unicode_category(c) in searchable_categories:
					prefixes = focus_.buffers[focus_.filename]['prefixes']
					follow   = focus_.buffers[focus_.filename]['follow']
					ss, ss_repr, matches, _, origin = searches.top()
					ssx      = ss + c
					matchesx = []
					if ssx in prefixes:                   # memoized, found
						matchesx = prefixes[ssx]
						if ss:                              # if there are existing matches, erase them
							color_strs(matches,  ss,  pad, Palette.elt_attr['text'])
						color_strs  (matchesx, ssx, pad, Palette.elt_attr['search'])
					elif display_w(ss) == 0:              # ssx failed, singleton
						curses.beep()
					elif ss in prefixes:                  # ss found; ssx = ?  Erase existing matches
						color_strs  (matches,  ss,  pad, Palette.elt_attr['text'])
						if (matchesx := search(ss, c, prefixes, follow)):  # ssx found; search() side-effects prefixes
							color_strs(matchesx, ssx, pad, Palette.elt_attr['search'])
						else:                               # ss found, ssx failed
							curses.beep()
					else:                                 # ss failed, ssx failed
						pass
					if matchesx:
						rankx, originx = focus_.jump_to_ss(matchesx)
						color_strs([matchesx[rankx]], ssx, pad, Palette.elt_attr['search_current'])
					else:
						rankx, originx = -1, origin
					ssx_repr   = ss_repr + ch_repr(c, bool(matchesx))
					searches.push(SearchFrame(ssx, ssx_repr, matchesx, rankx, originx))
					msg = f'{SEARCH_PREFIX}: {ssx_repr}' + (f' [{rankx + 1}/{len(matchesx)}]' if matchesx else '')
					focus_.envs.pop()
					focus_.envs.push(EnvFrame('search', '', msg, searches))
					Pane.mark_filename_buffers(focus_.filename)
				else:
					curses.beep()
					msgs_.append(f'{SEARCH_PREFIX}: {my_repr(c)}, unicode category {unicode_category(c)} is not a legal search character')
		msgs_.append(focus_.envs.top().msg)
		return focus_.envs.top().state

	@staticmethod
	def on_arg(c: int | str) -> str:
		global focus_, msgs_

		msgs_ = []
		assert focus_ is not None
		arg   = focus_.envs.pop().arg
		match c:
			case '-' if not arg:
				arg = '-'
				focus_.envs.push(EnvFrame('arg', arg, f'C-u {arg}-', None))
			case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
				arg += c
				focus_.envs.push(EnvFrame('arg', arg, f'C-u {arg}-', None))
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				if not arg:
					return 'arg'
				arg = focus_.envs.pop().arg[:-1]
				focus_.envs.push(EnvFrame('arg', arg, f'C-u {arg}-', None))
			case '\N{CAN}':          # control-X on MacOS
				arg = arg or DEFAULT_ARG
				focus_.envs.push(EnvFrame('C-x', arg, f'C-u {arg} C-x-', None))
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				curses.beep()
			case _:
				if type(c) == int:
					msg = f'C-u {arg} integer code {c} is not a legal character in an argument'
				else:
					assert type(c) == str
					msg = f'C-u {arg} {my_repr(c)} is undefined'
				msgs_.append(msg)
				curses.beep()
		msgs_.append(focus_.envs.top().msg)
		return focus_.envs.top().state

	@staticmethod
	def on_ctl_x(c: int | str) -> str:
		global focus_, msgs_, path_

		msgs_ = []
		assert focus_ is not None
		arg  = focus_.envs.pop().arg
		match c:
			case '0':  # must uncolor any search matches
				msgs_.append('C-x 0')
				focus_ = focus_.delete()
			case '1':
				msgs_.append('C-x 1')
				focus_.delete_other_panes()
			case '2' | 'h' | '3' | 'v':
				msgs_.append(f'C-u {arg} C-x {c}' if arg else f'C-x {c}')
				focus_.split_horizontal(arg) if (c == '2' or c == 'h') else focus_.split_vertical(arg)
			case 'o':
				msgs_.append(f'C-x {c}')
				focus_ = focus_.p_next()
			case 'O':
				msgs_.append(f'C-x {c}')
				focus_ = focus_.p_prev()
			case '-':
				msgs_.append(f'C-x {c}')
				focus_.shrink_to_buffer()
			case '+':
				msgs_.append(f'C-x {c}')
				focus_.shrink_to_buffer_all()
			case '\N{ACK}':          # control-F on MacOS
				msgs_.append('C-x C-f-')
				path_ = os.path.dirname(focus_.filename) + '/'
				focus_.envs.push(EnvFrame('C-f', '', f'Find: {path_}{CURSOR}', None))
			case '\N{BEL}':          # control-G on MacOS
				msgs_.append('Command aborted')
				curses.beep()
			case _:
				if type(c) == int:
					msg = f'C-x integer code {c} is not a legal character in an argument'
				else:
					assert type(c) == str
					msg = f'C-x {my_repr(c)} is undefined'
				msgs_.append(msg)
				curses.beep()
		msgs_.append(focus_.envs.top().msg)
		return focus_.envs.top().state

	@staticmethod
	def on_ctl_f(c: int | str) -> str:
		global completions_, focus_, msgs_, path_, sprefix_, stdscr_w_

		msgs_ = []
		assert focus_ is not None
		match c:
			case \
					'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | \
					'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | \
					'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | \
					'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | \
					'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | \
					'-' | '_' | '.' | '/' | '~' | '#' | '*' :
				completions_.disable()
				path_  += c
				spath  = shortpath(path_)
				msg    = f'{FIND_PREFIX}: {spath}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame('C-f', '', msg, None))
				msgs_.append(msg)
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				completions_.disable()
				if path_:
					path_ = path_[:-1]
					msg   = f'{FIND_PREFIX}: {path_}{CURSOR}'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame('C-f', '', msg, None))
					msgs_.append(msg)
			case '\N{TAB}':
				completions_.disable()
				dir, _  = os.path.split(path_)
				entries = os.scandir(dir)
				f_paths = sorted(fnmatch.filter([entry.path for entry in entries], path_ + '*'))
				match len(f_paths):
					case 0:
						msgs_.append(f'{FIND_PREFIX}: {path_}{CURSOR} [No match]')
					case 1:
						path_ = f_paths[0]
						if os.path.isdir(path_):
							path_ += '/'
							msg    = f'{FIND_PREFIX}: {path_}{CURSOR}'
							focus_.envs.pop()
							focus_.envs.push(EnvFrame('C-f', '', msg, None))
							msgs_.append(msg)
						else:
							msg = f'{FIND_PREFIX}: {path_}{CURSOR}'
							focus_.envs.pop()
							focus_.envs.push(EnvFrame('C-f', '', msg, None))
							msgs_.append(msg + ' [Sole completion]')
					case 2 if f_paths[1] == f_paths[0] + '~':
						path_ = f_paths[0]
						msg   = f'{FIND_PREFIX}: {path_}{CURSOR}'
						focus_.envs.pop()
						focus_.envs.push(  EnvFrame('C-f', '', msg, None))
						msgs_.append(msg + ' [Sole completion]')
					case _:
						f_files        = ordered_files(f_paths)
						path_          = os.path.commonprefix(f_paths)
						spath          = shortpath(path_)
						sdir, cprefix  = os.path.split(spath)
						msg_template   = f'{FIND_PREFIX}: {spath}{CURSOR} []'
						styled_cprefix = cprefix and f'{META_BEG}pattern{META_END}{cprefix}{META_BEG}{STYLE_END}{META_END}'
						sprefix_       = f'{FIND_PREFIX}: {sdir}/{styled_cprefix}{CURSOR}'
						chunks         = chunk_line(' '.join([f'{len(f_files)} completions:'] + f_files), stdscr_w_ - display_w(unstyle(msg_template)))
						colorize       = compose(lambda chunk: colorize_prefixes(chunk, cprefix), colorize_dictionaries) if cprefix else colorize_dictionaries
						completions_.init(color_chunks(chunks, colorize))
						msg = f'{sprefix_} [{completions_.this()}]'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame('C-f', '', msg, None))
						msgs_.append(msg)
			case curses.KEY_RIGHT | curses.KEY_LEFT:
				if completions_.enabled():
					chunk = completions_.next() if c == curses.KEY_RIGHT else completions_.prev()
					msg = f'{sprefix_} [{chunk}]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame('C-f', '', msg, None))
					msgs_.append(msg)
			case '\n':
				if os.path.exists(path_):
					if os.path.isdir(path_):
						msgs_.append(f'File {path_} is a directory')
						msgs_.append(focus_.envs.top().msg)
					else:
						filetype = str(subprocess.check_output(['file', path_])).split(': ')[1]
						if 'text' in filetype or 'JSON' in filetype:
							focus_.envs.pop()
							focus_ = focus_.replace(path_)  # document this.  what does replace do?
							msgs_.append(focus_.envs.top().msg)
						elif 'empty' in filetype:
							focus_.envs.pop()
							focus_ = focus_.replace(path_)
							msgs_.append(focus_.envs.top().msg)
						else:
							msgs_.append(f'File {path_} is not a text file')
							msgs_.append(focus_.envs.top().msg)
				else:
					msgs_.append(f"File {path_} doesn't exist")
					msgs_.append(focus_.envs.top().msg)
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
			case _:
				if type(c) == int:
					msg = f'Integer code {c} is not a legal character in a filename'
				else:
					assert type(c) == str
					msg = f'Illegal character: {my_repr(c)}'
				msgs_.append(msg)
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
		return focus_.envs.top().state

	@staticmethod
	def on_style_elt(c: int | str) -> str:
		global completions_, elt_, focus_, ground_, msgs_, patt_, styled_elt_, styled_prefix_

		this_state = 'style-elt'
		next_state = 'style-elt-ground'
		msgs_      = []
		assert focus_ is not None
		match c:
			case \
					'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | \
					'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | \
					'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | \
					'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | \
					'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | \
					'-' | '_' | '.' | '/' | '~' | '#' | '*' :
				completions_.disable()
				patt_ += c
				msg    = f'{STYLING_PREFIX}: {patt_}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame(this_state, '', msg, None))
				msgs_.append(msg)
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				if patt_:
					completions_.disable()
					patt_ = patt_[:-1]
					msg   = f'{STYLING_PREFIX}: {patt_}{CURSOR}'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\N{TAB}':
				completions_.disable()
				matches = sorted(filter(lambda elt: elt.startswith(patt_), Palette.elt_styling))
				match len(matches):
					case 0:
						msgs_.append(f'{STYLING_PREFIX}: {patt_}{CURSOR} [No match]')
					case 1:
						patt_ = matches[0]
						msg   = f'{STYLING_PREFIX}: {patt_}{CURSOR}'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg + ' [Sole completion]')
					case _:
						patt_          = os.path.commonprefix(matches)
						msg_template   = f'{STYLING_PREFIX}: {patt_}{CURSOR} []'
						styled_patt    = f'{META_BEG}pattern{META_END}{patt_}{META_BEG}{STYLE_END}{META_END}'
						styled_prefix_ = f'{STYLING_PREFIX}: {styled_patt}{CURSOR}'
						chunks         = chunk_line(' '.join([f'{len(matches)} completions:'] + matches), stdscr_w_ - display_w(msg_template))
						colorize       = compose(lambda chunk: colorize_prefixes(chunk, patt_), colorize_dictionaries) if patt_ else colorize_dictionaries
						completions_.init(color_chunks(chunks, colorize))
						msg            = f'{styled_prefix_} [{completions_.this()}]'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg)
			case curses.KEY_RIGHT | curses.KEY_LEFT:
				if completions_.enabled():
					chunk = completions_.next() if c == curses.KEY_RIGHT else completions_.prev()
					msg   = f'{STYLING_PREFIX}: [{chunk}]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\n' | '\r':
				if is_elt(patt_):
					ground_     = ''
					elt_        = patt_
					styled_elt_ = f'{META_BEG}{elt_}{META_END}{elt_}{META_BEG}{STYLE_END}{META_END}'
					msg         = f'{STYLING_PREFIX} {styled_elt_} [TAB to list]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(next_state, '', msg, None))
					msgs_.append(msg)
					return next_state
				elif patt_:
					msgs_.append(f'{patt_} is not a legal element')
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
				return focus_.envs.top().state
			case _:
				if type(c) == int:
					msg = f'Integer code {c} is not a legal character in an element name'
				else:
					assert type(c) == str
					msg = f'Illegal character: {my_repr(c)}'
				msgs_.append(msg)
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
		return this_state

	@staticmethod
	def on_style_elt_ground(c: int | str) -> str:
		global color_, completions_, elt_, ground_, msgs_, stdscr_w_, styled_elt_, styled_prefix_

		this_state = 'style-elt-ground'
		next_state = 'style-elt-color'
		msgs_      = []
		assert focus_ is not None
		match c:
			case \
					'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | \
					'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | \
					'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | \
					'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | \
					'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | \
					'-' | '_' | '.' | '/' | '~' | '#' | '*' :
				completions_.disable()
				ground_ += c
				msg      = f'{STYLING_PREFIX} {styled_elt_}: {ground_}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame(this_state, '', msg, None))
				msgs_.append(msg)
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				if ground_:
					completions_.disable()
					ground_ = ground_[:-1]
					msg     = f'{STYLING_PREFIX} {styled_elt_}: {ground_}{CURSOR}'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\N{TAB}':
				completions_.disable()
				matches = sorted(filter(lambda elt: elt.startswith(ground_), ('foreground', 'background')))
				match len(matches):
					case 0:
						msgs_.append(f'{STYLING_PREFIX} {styled_elt_}: {ground_}{CURSOR} [No match]')
					case 1:
						ground_ = matches[0]
						msg     = f'{STYLING_PREFIX} {styled_elt_}: {ground_}{CURSOR}'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg + ' [Sole completion]')
					case _:
						ground_        = os.path.commonprefix(matches)
						msg_template   = f'{STYLING_PREFIX} {elt_}: {ground_}{CURSOR_CHAR} []'
						styled_ground_ = f'{META_BEG}pattern{META_END}{ground_}{META_BEG}{STYLE_END}{META_END}'
						styled_prefix_ = f'{STYLING_PREFIX} {styled_elt_}: {styled_ground_}{CURSOR}'
						chunks         = chunk_line(' '.join([f'{len(matches)} completions:'] + matches), stdscr_w_ - display_w(msg_template))
						colorize       = compose(lambda chunk: colorize_prefixes(chunk, ground_), colorize_dictionaries) if ground_ else colorize_dictionaries
						completions_.init(color_chunks(chunks, colorize))
						msg            = f'{styled_prefix_} [{completions_.this()}]'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg)
			case curses.KEY_RIGHT | curses.KEY_LEFT:
				if completions_.enabled():
					chunk = completions_.next() if c == curses.KEY_RIGHT else completions_.prev()
					msg   = f'{STYLING_PREFIX} {styled_elt_}: [{chunk}]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\n' | '\r':
				if ground_ in ('foreground', 'background'):
					current_color = Palette.styling_color(elt_, ground_)
					msg = f'{STYLING_PREFIX} {styled_elt_} {ground_} [{current_color}] [TAB to list]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(next_state, '', msg, None))
					msgs_.append(msg)
					color_ = ''
					return next_state
				else:
					msgs_.append(f'{ground_} must be either foreground or background')
					msgs_.append(focus_.envs.top().msg)
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
				return focus_.envs.top().state
			case _:
				if type(c) == int:
					msg = f'Integer code {c} is not a legal character in an element name'
				else:
					assert type(c) == str
					msg = f'Illegal character: {my_repr(c)}'
				msgs_.append(msg)
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
		return this_state

	@staticmethod
	def on_style_elt_color(c: int | str) -> str:
		global color_, completions_, elt_, ground_, msgs_, stdscr_w_, styled_color_, styled_elt_, styled_prefix_

		this_state = 'style-elt-color'
		msgs_      = []
		assert focus_ is not None
		match c:
			case \
					'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | \
					'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | \
					'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | \
					'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | \
					'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | \
					'-' | '_' | '.' | '/' | '~' | '#' | '*' :
				completions_.disable()
				color_ += c
				msg     = f'{STYLING_PREFIX} {styled_elt_} {ground_}: {color_}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame(this_state, '', msg, None))
				msgs_.append(msg)
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				if color_:
					color_ = color_[:-1]
				if color_:
					completions_.disable()
					styled_prefix_ = f'{STYLING_PREFIX} {styled_elt_} {ground_}'
				else:
					current_color  = Palette.styling_color(elt_, ground_)
					styled_prefix_ = f'{STYLING_PREFIX} {styled_elt_} {ground_} [{current_color}]'
				msg = f'{styled_prefix_}: {color_}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame(this_state, '', msg, None))
				msgs_.append(msg)
			case '\N{TAB}':
				completions_.disable()
				assert Palette.colors is not None
				matches: list[str] = sorted(filter(lambda color: color.startswith(color_), [color.name for color in Palette.colors]))
				match len(matches):
					case 0:
						msgs_.append(f'{STYLING_PREFIX} {styled_elt_} {ground_}: {color_}{CURSOR} [No match]')
					case 1:
						color_ = matches[0]
						msg    = f'{STYLING_PREFIX} {styled_elt_} {ground_}: {color_}{CURSOR}'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg + ' [Sole completion]')
					case _:
						if color_ := os.path.commonprefix(matches):
							msg_template   = f'{STYLING_PREFIX} {elt_} {ground_}: {color_}{CURSOR_CHAR} []'
							styled_prefix_ = f'{STYLING_PREFIX} {styled_elt_} {ground_}'
							styled_color_  = f'{META_BEG}pattern{META_END}{color_}{META_BEG}{STYLE_END}{META_END}'
						else:
							current_color  = Palette.styling_color(elt_, ground_)
							msg_template   = f'{STYLING_PREFIX} {elt_} {ground_} [{current_color}]: {CURSOR_CHAR} []'
							styled_prefix_ = f'{STYLING_PREFIX} {styled_elt_} {ground_} [{current_color}]'
							styled_color_  = f''
						completions_.init(chunk_line(' '.join([f'{len(matches)} completions:'] + matches), stdscr_w_ - display_w(msg_template)))
						msg = f'{styled_prefix_}: {styled_color_}{CURSOR} [{colorize_colors(completions_.this(), elt_, ground_)}]'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg)
			case curses.KEY_RIGHT | curses.KEY_LEFT:
				if completions_.enabled():
					chunk = completions_.next() if c == curses.KEY_RIGHT else completions_.prev()
					msg   = f'{styled_prefix_}: {styled_color_}{CURSOR} [{colorize_colors(chunk, elt_, ground_)}]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\n' | '\r':
				assert Palette.colors is not None
				if not color_:
					current_color = Palette.styling_color(elt_, ground_)
					msgs_.append(f'No change')
					msgs_.append(f'No change')
					focus_.envs.pop()
					msgs_.append(focus_.envs.top().msg)
				elif color_ in [color.name for color in Palette.colors]:
					styling = Palette.styling_modify(elt_, ground_, color_)
					Palette.elt_styling[elt_] = styling
					Palette.elt_attr   [elt_] = Palette.styling_attr(Palette.elt_ID[elt_], styling)
					focus_.envs.pop()
					msgs_.append(f'{elt_} {ground_} set to {color_}')
					msgs_.append(f'{elt_} {ground_} set to {color_}')
					msgs_.append(focus_.envs.top().msg)
				else:
					msgs_.append(f'{color_} is not a legal color')
					msgs_.append(focus_.envs.top().msg)
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
			case _:
				if type(c) == int:
					msg = f'Integer code {c} is undefined'
				else:
					assert type(c) == str
					msg = f'{my_repr(c)} is undefined'
				msgs_.append(msg)
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
		return focus_.envs.top().state

	@staticmethod
	def on_switch_theme(c: int | str) -> str:
		global completions_, msgs_, stdscr_w_, theme_

		this_state = 'switch-theme'
		msgs_      = []
		assert focus_ is not None
		match c:
			case \
					'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | \
					'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | \
					'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | \
					'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | \
					'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | \
					'-' | '_' | '.' | '/' | '~' | '#' | '*' :
				completions_.disable()
				theme_ += c
				msg     = f'{SWITCH_THEME_PREFIX}: {theme_}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame(this_state, '', msg, None))
				msgs_.append(msg)
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				completions_.disable()
				if theme_:
					theme_ = theme_[:-1]
					msg    = f'{SWITCH_THEME_PREFIX}: {theme_}{CURSOR}'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\N{TAB}':
				completions_.disable()
				matches = sorted(filter(lambda theme: theme.startswith(theme_) and theme != Palette.current_theme, Palette.themes))
				match len(matches):
					case 0:
						msgs_.append(f'{SWITCH_THEME_PREFIX}: {theme_}{CURSOR} [No match]')
					case 1:
						theme_ = matches[0]
						msg    = f'{SWITCH_THEME_PREFIX}: {theme_}{CURSOR}'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg + ' [Sole completion]')
					case _:
						theme_         = os.path.commonprefix(matches)
						msg_template   = f'{SWITCH_THEME_PREFIX}: {theme_}{CURSOR} []'
						styled_theme_  = f'{META_BEG}pattern{META_END}{theme_}{META_BEG}{STYLE_END}{META_END}'
						styled_prefix_ = f'{SWITCH_THEME_PREFIX}: {styled_theme_}{CURSOR}'
						chunks         = chunk_line(' '.join([f'{len(matches)} completions:'] + matches), stdscr_w_ - display_w(msg_template))
						completions_.init(color_chunks(chunks, lambda chunk: colorize_prefixes(chunk, theme_)) if theme_ else chunks)
						msg = f'{styled_prefix_} [{completions_.this()}]'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg)
			case curses.KEY_RIGHT | curses.KEY_LEFT:
				if completions_.enabled():
					chunk = completions_.next() if c == curses.KEY_RIGHT else completions_.prev()
					msg = f'{SWITCH_THEME_PREFIX}: [{chunk}]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\n' | '\r':
				if not theme_ or (theme_ == Palette.current_theme):
					focus_.envs.pop()
					msgs_.append(f"Theme remains '{Palette.current_theme}'")
				elif theme_ in Palette.themes:
					focus_.envs.pop()
					Palette.switch_to_theme(theme_)
					msgs_.append(f"Theme is now '{theme_}'")
				else:
					msgs_.append(f'{theme_} is not the name of a theme')
				msgs_.append(focus_.envs.top().msg)
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
			case _:
				if type(c) == int:
					msg = f'Integer code {c} is undefined'
				else:
					assert type(c) == str
					msg = f'{my_repr(c)} is undefined'
				msgs_.append(msg)
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
		return focus_.envs.top().state

	@staticmethod
	def on_save_theme(c: int | str) -> str:
		global completions_, msgs_, theme_
	
		this_state = 'save-theme'
		assert focus_ is not None
		msgs_      = []
		match c:
			case \
					'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | \
					'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | \
					'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | \
					'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | \
					'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | \
					'-' | '_' | '.' | '/' | '~' | '#' | '*' :
				completions_.disable()
				theme_ += c
				msg     = f'{SAVE_THEME_PREFIX}: {theme_}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame(this_state, '', msg, None))
				msgs_.append(msg)
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				completions_.disable()
				if theme_:
					theme_ = theme_[:-1]
					msg    = f'{SAVE_THEME_PREFIX}: {theme_}{CURSOR}' if theme_ else f'{SAVE_THEME_PREFIX} [{Palette.current_theme}]: {CURSOR}'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\N{TAB}':
				completions_.disable()
				matches = sorted(filter(lambda theme: theme.startswith(theme_), Palette.themes))
				match len(matches):
					case 0:
						msgs_.append(f'{SAVE_THEME_PREFIX}: {theme_}{CURSOR} [No match]')
					case 1:
						theme_ = matches[0]
						msg    = f'{SAVE_THEME_PREFIX}: {theme_}{CURSOR}'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg + ' [Sole completion]')
					case _:
						theme_         = os.path.commonprefix(matches)
						msg_template   = f'{SAVE_THEME_PREFIX}: {theme_}{CURSOR} []'
						styled_value   = f'{META_BEG}pattern{META_END}{theme_}{META_BEG}{STYLE_END}{META_END}'
						styled_prefix_ = f'{SAVE_THEME_PREFIX}: {styled_value}{CURSOR}'
						chunks         = chunk_line(' '.join([f'{len(matches)} completions:'] + matches), stdscr_w_ - display_w(msg_template))
						completions_.init(color_chunks(chunks, lambda chunk: colorize_prefixes(chunk, theme_)) if theme_ else chunks)
						msg = f'{styled_prefix_} [{completions_.this()}]'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg)
			case curses.KEY_RIGHT | curses.KEY_LEFT:
				if completions_.enabled():
					chunk = completions_.next() if c == curses.KEY_RIGHT else completions_.prev()
					msg   = f'{SAVE_THEME_PREFIX}: [{chunk}]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\n' | '\r':
				if theme_:
					Palette.current_theme = theme_
				else:
					theme_ = Palette.current_theme
				path = Palette.save_theme(theme_)
				focus_.envs.pop()
				msgs_.append(f"Saved current configuration to {path} as theme '{theme_}'")
				msgs_.append(focus_.envs.top().msg)
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
			case _:
				if type(c) == int:
					msg = f'Integer code {c} is undefined'
				else:
					assert type(c) == str
					msg = f'{my_repr(c)} is undefined'
				msgs_.append(msg)
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
		return focus_.envs.top().state

	@staticmethod
	def on_delete_theme(c: int | str) -> str:
		global completions_, msgs_, theme_
	
		this_state = 'delete-theme'
		assert focus_ is not None
		msgs_      = []
		match c:
			case \
					'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | \
					'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | \
					'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | \
					'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | \
					'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | \
					'-' | '_' | '.' | '/' | '~' | '#' | '*' :
				completions_.disable()
				theme_ += c
				msg     = f'{DELETE_THEME_PREFIX}: {theme_}{CURSOR}'
				focus_.envs.pop()
				focus_.envs.push(EnvFrame(this_state, '', msg, None))
				msgs_.append(msg)
			case '\N{DEL}' | '\N{BS}' | curses.KEY_BACKSPACE: # \N{DEL} is delete on MacOS; \N{BS} is delete on Linux
				completions_.disable()
				if theme_:
					theme_ = theme_[:-1]
					msg    = f'{DELETE_THEME_PREFIX}: {theme_}{CURSOR}'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\N{TAB}':
				completions_.disable()
				matches = sorted(filter(lambda theme: theme.startswith(theme_) and theme != Palette.current_theme, Palette.themes))
				match len(matches):
					case 0:
						msgs_.append(f'{DELETE_THEME_PREFIX}: {theme_}{CURSOR} [No match]')
					case 1:
						theme_ = matches[0]
						msg = f'{DELETE_THEME_PREFIX}: {theme_}{CURSOR}'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg + ' [Sole completion]')
					case _:
						theme_         = os.path.commonprefix(matches)
						msg_template   = f'{DELETE_THEME_PREFIX}: {theme_}{CURSOR} []'
						styled_theme   = f'{META_BEG}pattern{META_END}{theme_}{META_BEG}{STYLE_END}{META_END}'
						styled_prefix_ = f'{DELETE_THEME_PREFIX}: {styled_theme}{CURSOR}'
						chunks         = chunk_line(' '.join([f'{len(matches)} completions:'] + matches), stdscr_w_ - display_w(msg_template))
						completions_.init(color_chunks(chunks, lambda chunk: colorize_prefixes(chunk, theme_)) if theme_ else chunks)
						msg = f'{styled_prefix_} [{completions_.this()}]'
						focus_.envs.pop()
						focus_.envs.push(EnvFrame(this_state, '', msg, None))
						msgs_.append(msg)
			case curses.KEY_RIGHT | curses.KEY_LEFT:
				if completions_.enabled():
					chunk = completions_.next() if c == curses.KEY_RIGHT else completions_.prev()
					msg = f'{DELETE_THEME_PREFIX}: [{chunk}]'
					focus_.envs.pop()
					focus_.envs.push(EnvFrame(this_state, '', msg, None))
					msgs_.append(msg)
			case '\n' | '\r':
				if theme_ == Palette.current_theme:
					msgs_.append('Cannot delete current theme')
					curses.beep()
				elif theme_ in Palette.themes:
					Palette.delete_theme(theme_)
					focus_.envs.pop()
					msgs_.append(f"Deleted theme '{theme_}'")
				else:
					msgs_.append(f"There is no theme called '{theme_}'")
				msgs_.append(focus_.envs.top().msg)
			case '\N{BEL}':          # control-G on MacOS
				focus_.envs.pop()
				msgs_.append('Command aborted')
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
			case _:
				if type(c) == int:
					msg = f'Integer code {c} is undefined'
				else:
					assert type(c) == str
					msg = f'{my_repr(c)} is undefined'
				msgs_.append(msg)
				msgs_.append(focus_.envs.top().msg)
				curses.beep()
		return focus_.envs.top().state

	def unwind_env_stack(self) -> None:
		pad = self.buffers[self.filename]['pad']

		while not self.envs.empty():
			env = self.envs.pop()
			if env.state == 'search':
				if env.searches.size() > 1:  # first frame of searches is the empty string
					ss, _, matches, _, _ = env.searches.top()
					color_strs(matches, ss, pad, Palette.elt_attr['text'])
		Pane.mark_filename_buffers(self.filename)

	@staticmethod
	def mark_filename_buffers(filename: str) -> None:
		"""Marks all the panes displaying file <filename>"""
		def cont(pane: Optional['Pane']) -> None:
			if pane:
				if pane.filename == filename:
					pane.dirty = True
				cont(pane.next)

		cont(Pane.pane_0)

	@staticmethod
	def mouse_event(state: str) -> str:
		global elt_, focus_, from_pane_, from_x_, from_y_, ground_, msgs_, styled_elt_

		msgs_ = []
		assert focus_ is not None
		_, x, y, _, bstate = curses.getmouse()
		pane, elt_ = Pane.clicked_pane_elt(y, x)
		match bstate:
			case curses.BUTTON1_DOUBLE_CLICKED:
				next_state  = 'style-elt-ground'
				ground_     = ''
				styled_elt_ = f'{META_BEG}{elt_}{META_END}{elt_}{META_BEG}{STYLE_END}{META_END}'
				msg         = f'{STYLING_PREFIX} {styled_elt_} [TAB to list]'
				focus_.envs.push(EnvFrame(next_state, '', msg, None))
				msgs_.append(msg)
				return next_state
			case curses.BUTTON1_CLICKED:
				if pane != focus_:
					Pane.change_focus(pane)
					msgs_.append(focus_.envs.top().msg)
			case curses.BUTTON1_PRESSED:
				from_x_    = x
				from_y_    = y
				from_pane_ = pane
				msgs_.append('Hold and drag to scroll')
			case curses.BUTTON1_RELEASED:
				assert from_pane_ is not None
				x_delta = x - from_x_
				y_delta = y - from_y_
				if y_delta:
					from_pane_.mv_up  (y_delta) if (y_delta > 0) else from_pane_.mv_down (- y_delta)
				if x_delta:
					from_pane_.mv_left(x_delta) if (x_delta > 0) else from_pane_.mv_right(- x_delta)
				msgs_.append(focus_.envs.top().msg)
			case curses.BUTTON4_PRESSED:        # returned on 'scroll up'
				pane.mv_up(DEFAULT_ARG)
			case curses.REPORT_MOUSE_POSITION:  # returned on 'scroll down'
				pane.mv_down(DEFAULT_ARG)
			case _:
				binary = '{0:b}'.format(bstate)
				str    = decode_bstate(bstate)
				msgs_.append(f'{y=}, {x=}, {binary}, {bstate}, {str}')
				msgs_.append(focus_.envs.top().msg)
		return state

	@staticmethod
	def clicked_pane_elt(
				y:       int,
				x:       int,
			) -> tuple['Pane', str]:
		"""Returns the pane and display element at (<y>, <x>).
		If (<y>, <x>) is in the status bar, returns (focus, 'status')"""
		global focus_, stdscr_h_, stdscr_w_

		assert focus_ is not None
		def cont(pane: Optional['Pane']) -> tuple['Pane', str]:
			if not pane:
				raise ValueError(f'Cannot locate ({y}, {x})')
			pminrow, pmaxrow, pmincol, pmaxcol = pane.pane_corners()
			if (y < pminrow) or \
				 (y > pmaxrow) or \
				 (x < pmincol) or \
				 (x > pmaxcol):
				return cont(pane.next)
			if (y == pmaxrow):
				return pane, 'caption_' + ('focus' if pane == focus_ else 'nofocus')
			if (x == pmaxcol) and pane.edge:
				return pane, 'edge_'    + ('focus' if pane == focus_ else 'nofocus')
			return pane, 'text'

		if (y < 0) or (y > stdscr_h_ - 1) or \
			 (x < 0) or (x > stdscr_w_ - 1):
			raise ValueError(f'({y}, {x}) is off the screen')
		if (y == stdscr_h_ - 1):
			return focus_, 'status'
		return cont(Pane.pane_0)

	@staticmethod
	def change_focus(pane: 'Pane') -> None:
		"""Switches focus to <pane>"""
		global focus_

		assert focus_ is not None
		focus_.dirty = True
		pane.dirty   = True
		focus_       = pane

def is_elt(str: str) -> bool:
	return str in Palette.elt_styling

def init_pane(stdscr: curses.window, filename: str) -> None:
	"""Creates the initial pane and gives it the focus"""
	global focus_, msgs_, spaces_, stdscr_h_, stdscr_w_

	stdscr_h_, stdscr_w_ = stdscr.getmaxyx()
	spaces_ = curses.newpad(stdscr_h_, stdscr_w_)
	spaces_.bkgd(' ', Palette.elt_attr['text'])
	stdscr.bkgd(' ', Palette.elt_attr['status'])
	focus_ = Pane(filename, pad_y = 0, pad_x = 0, pminrow = 0, pmaxrow = stdscr_h_ - 2, pmincol = 0, pmaxcol = stdscr_w_ - 1)
	msgs_  = [u'q: Quit, C-g: Abort command, Fn-Down arrow: Scroll down'.center(stdscr_w_)]
	stdscr.refresh()

def refresh_status_bar(stdscr: curses.window) -> None:
	"""Paints msgs_ one by one to the status bar, with a delay between each pair"""
	global msgs_, stdscr_h_

	def cont(messages: list[str]) -> None:
		match messages:
			case [message]:
				message = ('C ' + message) if (Global.debug and completions_.enabled()) else message
				paint_colored_str(stdscr, stdscr_h_ - 1, 0, message, Palette.elt_attr['status'])
				stdscr.clrtoeol()
				stdscr.refresh()
			case [message, *rest]:
				cont([message])
				sleep(Global.msg_delay)
				cont(rest)
			case []:
				return

	cont(msgs_)


def create_window(
		minrow: int,
		maxrow: int,
		mincol: int,
		maxcol: int,
			) -> curses.window:
	height = maxrow - minrow + 1
	width  = maxcol - mincol + 1
	return curses.newwin(height, width, minrow, mincol)

def singleton_prefixes(lines: list[str]) -> dict[str, list[Posn]]:
	prefixes: dict[str, list[Posn]] = dict()
	for row, line in enumerate(lines):
		col = 0
		for c in line:
			if c not in prefixes:
				prefixes[c] = []
			prefixes[c].append(Posn(row, col))
			col += display_w(c)
	return prefixes

def create_follow(lines: list[str]) -> dict[str, list[Posn]]:
	follow: dict[str, list[Posn]] = dict()
	for row, line in enumerate(lines):
		col = 0
		for c, d in zip(line, (line + '\n')[1:]):
			pair = f'{c}{d}'
			if pair not in follow:
				follow[pair] = []
			follow[pair].append(Posn(row, col))
			col += display_w(c)
	return follow

def next_match_rank(y: int, posns: list[Posn]) -> int:
	"""Return the rank of the first match in the rest of the file; if there is no such match, return 0"""
	for rank, posn in enumerate(posns):
		if posn.row >= y:
			return rank
	return 0

def my_repr(c: str) -> str:
	match c:
		case '\N{SOH}':
			str = 'C-a'
		case '\N{STX}':
			str = 'C-b'
		case '\N{ETX}':
			str = 'C-c'
		case '\N{EOT}':
			str = 'C-d'
		case '\N{ENQ}':
			str = 'C-e'
		case '\N{ACK}':
			str = 'C-f'
		case '\N{BEL}':
			str = 'C-g'
		case '\N{BS}':
			str = 'C-h'
		case '\N{TAB}':  # '\N{HT}', '\t'
			str = 'TAB'
		case '\N{LF}':
			str = 'ENTER'
		case '\N{VT}':
			str = 'C-k'
		case '\N{FF}':
			str = 'C-l'
		case '\N{CR}':
			str = 'C-m'
		case '\N{SO}':
			str = 'C-n'
		case '\N{SI}':
			str = 'C-o'
		case '\N{DLE}':
			str = 'C-p'
		case '\N{DC1}':
			str = 'C-q'
		case '\N{DC2}':
			str = 'C-r'
		case '\N{DC3}':
			str = 'C-s'
		case '\N{DC4}':
			str = 'C-t'
		case '\N{NAK}':
			str = 'C-u'
		case '\N{SYN}':
			str = 'C-v'
		case '\N{ETB}':
			str = 'C-w'
		case '\N{CAN}':
			str = 'C-x'
		case '\0x19':
			str = 'C-y'
		case '\N{SUB}':
			str = 'C-z'
		case '\N{ESC}':
			str = 'ESC'
		case '\N{FS}':
			str = 'C-\\'
		case '\N{GS}':
			str = 'C-]'
		case '\N{RS}':
			str = 'C-^'
		case '\N{US}':
			str = 'C-_'
		case '\N{SP}':
			str = 'space'
		case '\N{DEL}':
			str = 'DEL'
		case _:
			str = c
	return str

def color_strs(
		posns:   list[Posn],
		str:     str,
		pad:     curses.window,
		attr:    int,
		last_ch: bool = False,
			) -> None:
	"""Apply attribute <attr> to the string <str> at all positions in <posns>.
	If <last_ch> is truthy, only apply <attr> to the last character of <str>"""
	str_w     = display_w(str)
	last_ch_w = display_w(str[-1])
	offset    = (str_w - last_ch_w) if last_ch else 0
	n_cols    =          last_ch_w  if last_ch else str_w
	for row, col in posns:
		pad.chgat(row, col + offset, n_cols, attr)

## The following are taken from the table of General_Category values from the Unicode Standard Annex #44
## https://www.unicode.org/reports/tr44/
searchable_categories = (
	'Ll',  # Lowercase letter
	'Lo',  # Other letters, including syllables and ideographs
	'Lu',  # Uppercase letter
	'Nd',  # Decimal digit
	'Pc',  # Connecting punctuation mark, like a tie
	'Pd',  # Dash or hyphen punctuation mark
	'Pe',  # Closing punctuation mark (of a pair)
	'Po',  # Other punctuation mark
	'Ps',  # Opening punctuation mark (of a pair)
	'Sc',  # Currency symbol
	'Sk',  # Non-letterlike modifier symbol (?)
	'Sm',  # Math symbol
	'Zs',  # Space separator (of non-zero width)
	)

def search(ss: str, c: str, prefixes: dict[str, list[Posn]], follow: dict[str, list[Posn]]) -> list[Posn]:
	"""Finds the position of all occurrences of ss + c in the file and adds them to <prefixes>; returns those positions.
	Side-effects <prefixes>"""
	b           = ss[-1]
	b_offset    = display_w(ss) - display_w(b)
	pair        = f'{b}{c}'
	ss_matches  = prefixes[ss]
	ssc_matches = []
	if pair in follow:
		pair_matches = follow[pair]
		for row, col in ss_matches:
			if Posn(row, col + b_offset) in pair_matches:
				ssc_matches.append(Posn(row, col))
		if ssc_matches:
			prefixes[ss + c] = ssc_matches
	return ssc_matches

def ch_repr(c: str, matched: bool) -> str:
	elt = 'match' if matched else 'nomatch'
	return f'{META_BEG}{elt}{META_END}{c}{META_BEG}{STYLE_END}{META_END}'

def shortpath(path):
	dirpath, filename = os.path.split(path)
	dir               = os.path.basename(dirpath)
	return '...' + os.path.join(dir, filename)

def ordered_files(f_paths: list[str]) -> list[str]:  # Order directories first
	dirs, files = [], []
	for f_path in f_paths:
		if os.path.isdir(f_path):
			dirs.append(os.path.basename(f_path) + '/')
		else:
			files.append(os.path.basename(f_path))
	return dirs + files

def chunk_line(line: str, screen_w: int) -> list[str]:
	"""Split <line> into strings of length at most <screen_w>, adding continuation dots"""
	dots   = '...'
	dots_w = len(dots)

	def cont(tail: str, chunks: list[str]) -> list[str]:
		if display_w(tail) <= screen_w:
			return chunks + [tail]
		i, prev_i = 0, 0
		while (i >= 0) and (i <= screen_w - (dots_w + 1)):  # i == -1 if ' ' not found
			i = tail.find(' ', (prev_i := i) + 1)
		if prev_i == dots_w:  # next token runs off the screen
			if i == -1:         # this is the last token
				chunk = f'{tail[:screen_w - 1]}{LINE_TRUNCATE_CHAR}'  # truncate the token
				return chunks + [chunk]
			chunk = f'{tail[:screen_w - (dots_w + 2)]}{LINE_TRUNCATE_CHAR}'  # truncate the token and add dots
			rest = tail[i + 1:]
		else:
			chunk = tail[:prev_i]
			rest  = tail[ prev_i + 1:]
		return cont(f'{dots} {rest}', chunks + [f'{chunk} {dots}'])

	return cont(line, [])

def unstyle(str: str) -> str:
	return cSTYLE.sub(r'\g<unstyled_string>', str)

keys = {
  'KEY_A1': curses.KEY_A1,
  'KEY_A3': curses.KEY_A3,
  'KEY_B2': curses.KEY_B2,
  'KEY_BACKSPACE': curses.KEY_BACKSPACE,
  'KEY_BEG': curses.KEY_BEG,
  'KEY_BREAK': curses.KEY_BREAK,
  'KEY_BTAB': curses.KEY_BTAB,
  'KEY_C1': curses.KEY_C1,
  'KEY_C3': curses.KEY_C3,
  'KEY_CANCEL': curses.KEY_CANCEL,
  'KEY_CATAB': curses.KEY_CATAB,
  'KEY_CLEAR': curses.KEY_CLEAR,
  'KEY_CLOSE': curses.KEY_CLOSE,
  'KEY_COMMAND': curses.KEY_COMMAND,
  'KEY_COPY': curses.KEY_COPY,
  'KEY_CREATE': curses.KEY_CREATE,
  'KEY_CTAB': curses.KEY_CTAB,
  'KEY_DC': curses.KEY_DC,
  'KEY_DL': curses.KEY_DL,
  'KEY_DOWN': curses.KEY_DOWN,
  'KEY_EIC': curses.KEY_EIC,
  'KEY_END': curses.KEY_END,
  'KEY_ENTER': curses.KEY_ENTER,
  'KEY_EOL': curses.KEY_EOL,
  'KEY_EOS': curses.KEY_EOS,
  'KEY_EXIT': curses.KEY_EXIT,
  'KEY_F0': curses.KEY_F0,
  'KEY_F1': curses.KEY_F1,
  'KEY_F10': curses.KEY_F10,
  'KEY_F11': curses.KEY_F11,
  'KEY_F12': curses.KEY_F12,
  'KEY_F13': curses.KEY_F13,
  'KEY_F14': curses.KEY_F14,
  'KEY_F15': curses.KEY_F15,
  'KEY_F16': curses.KEY_F16,
  'KEY_F17': curses.KEY_F17,
  'KEY_F18': curses.KEY_F18,
  'KEY_F19': curses.KEY_F19,
  'KEY_F2': curses.KEY_F2,
  'KEY_F20': curses.KEY_F20,
  'KEY_F21': curses.KEY_F21,
  'KEY_F22': curses.KEY_F22,
  'KEY_F23': curses.KEY_F23,
  'KEY_F24': curses.KEY_F24,
  'KEY_F25': curses.KEY_F25,
  'KEY_F26': curses.KEY_F26,
  'KEY_F27': curses.KEY_F27,
  'KEY_F28': curses.KEY_F28,
  'KEY_F29': curses.KEY_F29,
  'KEY_F3': curses.KEY_F3,
  'KEY_F30': curses.KEY_F30,
  'KEY_F31': curses.KEY_F31,
  'KEY_F32': curses.KEY_F32,
  'KEY_F33': curses.KEY_F33,
  'KEY_F34': curses.KEY_F34,
  'KEY_F35': curses.KEY_F35,
  'KEY_F36': curses.KEY_F36,
  'KEY_F37': curses.KEY_F37,
  'KEY_F38': curses.KEY_F38,
  'KEY_F39': curses.KEY_F39,
  'KEY_F4': curses.KEY_F4,
  'KEY_F40': curses.KEY_F40,
  'KEY_F41': curses.KEY_F41,
  'KEY_F42': curses.KEY_F42,
  'KEY_F43': curses.KEY_F43,
  'KEY_F44': curses.KEY_F44,
  'KEY_F45': curses.KEY_F45,
  'KEY_F46': curses.KEY_F46,
  'KEY_F47': curses.KEY_F47,
  'KEY_F48': curses.KEY_F48,
  'KEY_F49': curses.KEY_F49,
  'KEY_F5': curses.KEY_F5,
  'KEY_F50': curses.KEY_F50,
  'KEY_F51': curses.KEY_F51,
  'KEY_F52': curses.KEY_F52,
  'KEY_F53': curses.KEY_F53,
  'KEY_F54': curses.KEY_F54,
  'KEY_F55': curses.KEY_F55,
  'KEY_F56': curses.KEY_F56,
  'KEY_F57': curses.KEY_F57,
  'KEY_F58': curses.KEY_F58,
  'KEY_F59': curses.KEY_F59,
  'KEY_F6': curses.KEY_F6,
  'KEY_F60': curses.KEY_F60,
  'KEY_F61': curses.KEY_F61,
  'KEY_F62': curses.KEY_F62,
  'KEY_F63': curses.KEY_F63,
  'KEY_F7': curses.KEY_F7,
  'KEY_F8': curses.KEY_F8,
  'KEY_F9': curses.KEY_F9,
  'KEY_FIND': curses.KEY_FIND,
  'KEY_HELP': curses.KEY_HELP,
  'KEY_HOME': curses.KEY_HOME,
  'KEY_IC': curses.KEY_IC,
  'KEY_IL': curses.KEY_IL,
  'KEY_LEFT': curses.KEY_LEFT,
  'KEY_LL': curses.KEY_LL,
  'KEY_MARK': curses.KEY_MARK,
  'KEY_MAX': curses.KEY_MAX,
  'KEY_MESSAGE': curses.KEY_MESSAGE,
  'KEY_MIN': curses.KEY_MIN,
  'KEY_MOUSE': curses.KEY_MOUSE,
  'KEY_MOVE': curses.KEY_MOVE,
  'KEY_NEXT': curses.KEY_NEXT,
  'KEY_NPAGE': curses.KEY_NPAGE,
  'KEY_OPEN': curses.KEY_OPEN,
  'KEY_OPTIONS': curses.KEY_OPTIONS,
  'KEY_PPAGE': curses.KEY_PPAGE,
  'KEY_PREVIOUS': curses.KEY_PREVIOUS,
  'KEY_PRINT': curses.KEY_PRINT,
  'KEY_REDO': curses.KEY_REDO,
  'KEY_REFERENCE': curses.KEY_REFERENCE,
  'KEY_REFRESH': curses.KEY_REFRESH,
  'KEY_REPLACE': curses.KEY_REPLACE,
  'KEY_RESET': curses.KEY_RESET,
  'KEY_RESIZE': curses.KEY_RESIZE,
  'KEY_RESTART': curses.KEY_RESTART,
  'KEY_RESUME': curses.KEY_RESUME,
  'KEY_RIGHT': curses.KEY_RIGHT,
  'KEY_SAVE': curses.KEY_SAVE,
  'KEY_SBEG': curses.KEY_SBEG,
  'KEY_SCANCEL': curses.KEY_SCANCEL,
  'KEY_SCOMMAND': curses.KEY_SCOMMAND,
  'KEY_SCOPY': curses.KEY_SCOPY,
  'KEY_SCREATE': curses.KEY_SCREATE,
  'KEY_SDC': curses.KEY_SDC,
  'KEY_SDL': curses.KEY_SDL,
  'KEY_SELECT': curses.KEY_SELECT,
  'KEY_SEND': curses.KEY_SEND,
  'KEY_SEOL': curses.KEY_SEOL,
  'KEY_SEXIT': curses.KEY_SEXIT,
  'KEY_SF': curses.KEY_SF,
  'KEY_SFIND': curses.KEY_SFIND,
  'KEY_SHELP': curses.KEY_SHELP,
  'KEY_SHOME': curses.KEY_SHOME,
  'KEY_SIC': curses.KEY_SIC,
  'KEY_SLEFT': curses.KEY_SLEFT,
  'KEY_SMESSAGE': curses.KEY_SMESSAGE,
  'KEY_SMOVE': curses.KEY_SMOVE,
  'KEY_SNEXT': curses.KEY_SNEXT,
  'KEY_SOPTIONS': curses.KEY_SOPTIONS,
  'KEY_SPREVIOUS': curses.KEY_SPREVIOUS,
  'KEY_SPRINT': curses.KEY_SPRINT,
  'KEY_SR': curses.KEY_SR,
  'KEY_SREDO': curses.KEY_SREDO,
  'KEY_SREPLACE': curses.KEY_SREPLACE,
  'KEY_SRESET': curses.KEY_SRESET,
  'KEY_SRIGHT': curses.KEY_SRIGHT,
  'KEY_SRSUME': curses.KEY_SRSUME,
  'KEY_SSAVE': curses.KEY_SSAVE,
  'KEY_SSUSPEND': curses.KEY_SSUSPEND,
  'KEY_STAB': curses.KEY_STAB,
  'KEY_SUNDO': curses.KEY_SUNDO,
  'KEY_SUSPEND': curses.KEY_SUSPEND,
  'KEY_UNDO': curses.KEY_UNDO,
  'KEY_UP': curses.KEY_UP,
  'OK':   curses.OK,
  'REPORT_MOUSE_POSITION': curses.REPORT_MOUSE_POSITION,
}

def identify(code: int) -> str:
	for key, value in keys.items():
		if value == code:
			return key
	return f'unknown code {code}'

def colorize_prefixes(chunk: str, prefix: str) -> str:
	"""Encodes the 'prefix' colorization of occurrences of <prefix> in <chunk> (including directory names)"""
	string = ' ' + chunk.replace( f'{META_BEG}directory{META_END}{prefix}',
																f'{META_BEG}prefix{META_END}{prefix}{META_BEG}{STYLE_END}{META_END}{META_BEG}directory{META_END}')
	return  string.replace(                                f' {prefix}',
															 f' {META_BEG}prefix{META_END}{prefix}{META_BEG}{STYLE_END}{META_END}')[1:]

def colorize_dictionaries(chunk: str) -> str:
	"""Encodes the 'directory' colorization of directory names in <chunk>"""
	return cDIR.sub(f'{META_BEG}directory{META_END}\g<directory>{META_BEG}{STYLE_END}{META_END}', chunk)

def colorize_colors(chunk: str, elt: str, ground: str) -> str:
	id = -1
	def colorize_color(word: str) -> str:
		nonlocal id

		assert Palette.colors is not None
		if word in [color.name for color in Palette.colors]:
			id     += 1
			celt    = f'{Palette.celt_prefix}{id:02}'
			styling = Palette.styling_modify(elt, ground, word)
			Palette.elt_attr[celt] = Palette.styling_attr(Palette.celt_ID[celt], styling)
			return f'{META_BEG}{celt}{META_END}{word}{META_BEG}{STYLE_END}{META_END}'
		else:
			return word

	return ' '.join([colorize_color(word) for word in chunk.split()])

def color_chunks(
		chunks:   list[str],
		colorize: Callable,
			) -> list[str]:
	prefix, chunk = chunks[0].split(': ')
	return [f'{prefix}: {colorize(chunk)}'] + [colorize(chunk) for chunk in chunks[1:]]

def decode_bstate(bstate: int) -> str:
	repr = {
		curses.BUTTON1_CLICKED:        '1c',
		curses.BUTTON1_DOUBLE_CLICKED: '1cc',
		curses.BUTTON1_TRIPLE_CLICKED: '1ccc',
		curses.BUTTON1_PRESSED:        '1p',
		curses.BUTTON1_RELEASED:       '1r',
		curses.BUTTON2_CLICKED:        '2c',
		curses.BUTTON2_DOUBLE_CLICKED: '2cc',
		curses.BUTTON2_TRIPLE_CLICKED: '2ccc',
		curses.BUTTON2_PRESSED:        '2p',
		curses.BUTTON2_RELEASED:       '2r',
		curses.BUTTON3_CLICKED:        '3c',
		curses.BUTTON3_DOUBLE_CLICKED: '3cc',
		curses.BUTTON3_TRIPLE_CLICKED: '3ccc',
		curses.BUTTON3_PRESSED:        '3p',
		curses.BUTTON3_RELEASED:       '3r',
		curses.BUTTON4_CLICKED:        '4c',
		curses.BUTTON4_DOUBLE_CLICKED: '4cc',
		curses.BUTTON4_TRIPLE_CLICKED: '4ccc',
		curses.BUTTON4_PRESSED:        '4p',
		curses.BUTTON4_RELEASED:       '4r',
		# curses.BUTTON5_CLICKED:        '5c',
		# curses.BUTTON5_DOUBLE_CLICKED: '5cc',
		# curses.BUTTON5_TRIPLE_CLICKED: '5ccc',
		# curses.BUTTON5_PRESSED:        '5p',
		# curses.BUTTON5_RELEASED:       '5r',
		curses.BUTTON_ALT:             'ba',
		curses.BUTTON_CTRL:            'bc',
		curses.BUTTON_SHIFT:           'bs',
	}
	result = ['|']
	for elt in repr:
		if elt & bstate:
			result.append(repr[elt])
	return ' '.join(result)

