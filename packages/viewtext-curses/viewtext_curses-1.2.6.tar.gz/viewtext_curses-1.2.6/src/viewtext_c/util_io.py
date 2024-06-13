#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

from pathlib                 import Path
from typing                  import Iterable, Optional

def file_available_for_read(files: Iterable[str]) -> Optional[Path]:
	"""Takes a list of paths (strings) and returns the first one that exists and is a file.
	Doesn't check if it is readable or not"""
	for p in (Path(file).expanduser() for file in files):
		if p.exists() and p.is_file():
			return p
	return None

def file_available_for_write(files: Iterable[str]) -> Optional[Path]:
	"""Takes a list of paths (strings) and returns the first one that either exists or can be created.
	Doesn't check if it is writeable"""
	for p in (Path(file).expanduser() for file in files):
		if p.exists() and p.is_file():
			return p
		if p.parent.exists():
			return p
		try:
			p.parent.mkdir(parents = True)
			return p
		except Exception as e:
			pass
	return None
