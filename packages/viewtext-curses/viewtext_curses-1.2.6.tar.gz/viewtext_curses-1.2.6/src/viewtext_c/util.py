#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

from typing import Callable

def compose(g: Callable[[str], str], f: Callable[[str], str]) -> Callable[[str], str]:
	"""Given f(x), g(x), returns g(f(x))"""
	return lambda x: g(f(x))

class Completion:
	chunks: list[str] = []
	i:      int       = -1

	def init(self, chunks: list[str]) -> None:
		self.chunks = chunks
		self.i      = 0

	def this(self) -> str:
		return self.chunks[self.i]

	def next(self) -> str:
		if self.i < len(self.chunks) - 1:
			self.i += 1
		return self.chunks[self.i]
	
	def prev(self) -> str:
		if self.i > 0:
			self.i -= 1
		return self.chunks[self.i]

	def disable(self) -> None:
		self.i = -1

	def enabled(self) -> bool:
		return self.i >= 0
