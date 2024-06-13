#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

import re

META_BEG     = '\N{STX}'
META_END     = '\N{ETX}'

STYLE_END    = r'/'

pWORD        = r'[a-z]+'
pSPACE       = r'\s'
pSTYLE_BEG   = f'{META_BEG} {pWORD} ({pSPACE}+{pWORD})* {META_END}'
pSTYLE_END   = f'{META_BEG} /                           {META_END}'
pSTYLE       = f'{pSTYLE_BEG} (?P<unstyled_string> .)*? {pSTYLE_END}'
pDIR         = r'(?P<directory> [^\s/]+/)'     # Picks up directories in completions list
cSTYLE       = re.compile(pSTYLE, re.VERBOSE)
cDIR         = re.compile(pDIR,   re.VERBOSE)

CURSOR_CHAR        = '_'
CURSOR             = f'{META_BEG}cursor{META_END}{CURSOR_CHAR}{META_BEG}{STYLE_END}{META_END}'
LINE_TRUNCATE_CHAR = '\\'
