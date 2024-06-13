#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

import curses
import os
import tomllib
import tomli_w

from typing                import Optional
from viewtext_c.color_list import Color, color_list
from viewtext_c.util_io    import file_available_for_read, file_available_for_write

CONFIG_FILES = [
	'~/.config/viewtext/config.toml',
	'~/.viewtextrc.toml',
	'./resources/config.toml'
]

N_COLOR_COMPLETIONS_MAX = 15  # Modify theme: max # of color names displayed in status bar
N_COLOR_PAIRS_MAX       = 256 # This depends on the version of curses, which I currently am not checking

class Palette():
	color_id = {
			'ansi_black':     curses.COLOR_BLACK,
			'ansi_red':       curses.COLOR_RED,
			'ansi_yellow':    curses.COLOR_YELLOW,
			'ansi_green':     curses.COLOR_GREEN,
			'ansi_cyan':      curses.COLOR_CYAN,
			'ansi_blue':      curses.COLOR_BLUE,
			'ansi_magenta':   curses.COLOR_MAGENTA,
			'ansi_white':     curses.COLOR_WHITE,
	}

	mod_attr = {
			'blink':          curses.A_BLINK,
			'bold':           curses.A_BOLD,
			'dim':            curses.A_DIM,
			'reverse':        curses.A_REVERSE,
			'standout':       curses.A_STANDOUT,
			'underline':      curses.A_UNDERLINE,
	}

	celt_ID_max   = 0     # Completion elements make up the lower pairIDs, theme elements the higher ones
	celt_prefix   = 'completion'
	current_theme = ''
	n_colors      = 0
	n_pairs       = 0
	n_pairs_max   = 0
	pairID        = 0  # curses internal color pair ID

	celts:       Optional[tuple[str, ...]]   = None  # completion elements
	celt_ID:              dict[str, int]     = dict()
	colors:      Optional[tuple[Color, ...]] = None
	elt_attr:             dict[str, int]     = dict()
	elt_ID:               dict[str, int]     = dict()
	elt_styling:          dict[str, str]     = dict()
	themes:     dict[str, dict[str, str]]    = dict()

	@classmethod
	def init_colors(cls) -> None:
		"""Initialize colors and the celt_ID mapping and load themes"""
		cls.n_pairs_max = min(N_COLOR_PAIRS_MAX, curses.COLOR_PAIRS)  # COLOR_PAIRS is undefined until you initialize curses
		cls.load_colors()
		cls.pairID      = 0  # curses hardwires pairID 0 to 'ansi_white on ansi_black'
		cls.init_celts()
		cls.celt_ID_max = cls.pairID
		cls.load_themes()
		cls.n_pairs     = cls.pairID + 1
		if cls.n_pairs > cls.n_pairs_max:
			raise Exception(f'{os.path.basename(__file__)} init_colors(): can only admit {cls.n_pairs - 1} color pairs')

	@classmethod
	def load_colors(cls) -> None:
		"""Initialize the constants color_id and n_colors"""
		n_predefined_colors = len(cls.color_id)
		# if n_predefined_colors + len(color_list) > curses.COLORS:
		# 	logging.warning(f'This terminal only allows {curses.COLORS} colors; proceeding with limited palette')
		cls.colors = color_list[:curses.COLORS - n_predefined_colors]
		for color_id, color in enumerate(cls.colors, start = n_predefined_colors):
			cls.color_id[color.name] = color_id
			curses.init_color(color_id, *color.rgb)
		cls.n_colors = (color_id + 1) if cls.colors else n_predefined_colors

	@classmethod
	def init_celts(cls) -> None:
		"""Initialize the constant celt_ID, which will be used every time you generate completions"""
		cls.celts          = tuple([f'{cls.celt_prefix}{id:02}' for id in range(N_COLOR_COMPLETIONS_MAX)])
		for elt in cls.celts:
			cls.pairID      += 1
			cls.celt_ID[elt] = cls.pairID

	@classmethod
	def load_themes(cls) -> None:
		"""Read the configuration file and load its themes"""
		path = file_available_for_read(CONFIG_FILES)
		if not path:
			raise Exception(f'load_themes: cannot find config file for read')
		with path.open(mode = 'rb') as f:
			config = tomllib.load(f)
		cls.current_theme = cls.current_theme or config['current_theme']
		cls.themes        = config['themes']
		cls.load_theme(cls.current_theme)

	@classmethod
	def load_theme(cls, theme: str) -> None:
		"""Load theme <theme>, incrementing pairID"""
		cls.elt_styling     = cls.themes[theme]
		cls.pairID          = cls.celt_ID_max  # Reuse the pairIDs for theme elements
		for elt in cls.elt_styling:
			cls.pairID       += 1
			cls.elt_ID[elt]   = cls.pairID    # Assign pairID to elt
			cls.elt_attr[elt] = cls.styling_attr(cls.pairID, cls.elt_styling[elt]) # Redefine pairID to colors(styling)

	@classmethod
	def styling_attr(cls, pairID: int, styling: str) -> int:
		"""Returns attr corresponding to styling string.
		As a side effect, assigns (fg, bg) from the styling string to curses pairID"""
		def cont(tokens, attr):
			match tokens:
				case []:
					return attr
				case [fg, 'on', bg, *rest]:
					attr |= cls.colorpair_attr(pairID, fg, bg)
					return cont(rest, attr)
				case [mod, *rest] if mod in cls.mod_attr:
					attr |= cls.mod_attr[mod]
					return cont(rest, attr)
				case _:
					raise Exception

		return cont(styling.split(), 0)

	@classmethod
	def colorpair_attr(cls, pairID: int, fg: str, bg: str) -> int:
		"""Returns attr corresponding to (fg, bg).
		As a side effect, assigns (fg, bg) to curses pairID"""
		for color in (fg, bg):
			if color not in cls.color_id:
				raise Exception(f'{os.path.basename(__file__)} colorpair_attr(): {color} is not a legal color')
				exit()
		curses.init_pair(pairID, cls.color_id[fg], cls.color_id[bg])  # Assign (fg, bg) to pairID
		return curses.color_pair(pairID)                              # Return the corresponding attr

	@classmethod
	def delete_theme(cls, theme: str) -> str:
		"""Delete theme <theme>.
		Save all the themes and return the path to the configuration file"""
		del cls.themes[theme]
		return cls.save_themes()				

	@classmethod
	def save_theme(cls, theme: str) -> str:
		"""Define the current configuration as <theme>.
		If <theme> is not an existing theme, create it.
		Save all the themes and return the path to the configuration file"""
		cls.themes[theme] = cls.elt_styling
		return cls.save_themes()				

	@classmethod
	def switch_to_theme(cls, theme: str) -> str:
		"""Set the current theme to <theme>.
		Save the new configuration file"""
		cls.current_theme = theme
		cls.load_theme(theme)
		return cls.save_themes()				

	@classmethod
	def save_themes(cls) -> str:
		"""Choose a config file and save all themes and the name of the current theme to it"""
		path = file_available_for_write(CONFIG_FILES)
		if not path:
			raise Exception(f'save_themes: cannot find config file for write')
		config = {
			'themes':        cls.themes,
			'current_theme': cls.current_theme,
		}
		try:
			with path.open(mode = 'wb') as f:
				tomli_w.dump(config, f)
		except IOError as e:
			raise Exception(f'save_themes: error {e}')
		return str(path)

	@classmethod
	def styling_color(cls, elt: str, ground: str) -> str:
		"""Return the foreground or background color in the styling string for element <elt>"""
		tokens = cls.elt_styling[elt].split()
		on_index = tokens.index('on')
		match ground:
			case 'foreground':
				offset = -1
			case 'background':
				offset = 1
			case _:
				raise Exception(f': {ground} must be either foreground or background')
		return tokens[on_index + offset]

	@classmethod
	def styling_modify(cls, elt: str, ground: str, color: str) -> str:
		"""Return the styling string for <elt> with its foreground or background changed to <color>"""
		tokens = cls.elt_styling[elt].split()
		on_index = tokens.index('on')
		match ground:
			case 'foreground':
				offset = -1
			case 'background':
				offset = 1
			case _:
				raise Exception(f': {ground} must be either foreground or background')
		tokens[on_index + offset] = color
		return ' '.join(tokens)
