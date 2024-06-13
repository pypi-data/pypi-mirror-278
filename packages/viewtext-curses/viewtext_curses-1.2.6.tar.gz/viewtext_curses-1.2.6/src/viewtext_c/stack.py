#! /usr/bin/python3.10
# -*- coding: utf-8 -*-

class Stack():
	def __init__(self, *args):
		self._stack = []
		for arg in args:
			self._stack.append(arg)

	def empty(self):
		return self.size() == 0

	def size(self):
		return len(self._stack)

	def top(self):
		return None if self.empty() else self._stack[-1]

	def push(self, elt):
		self._stack.append(elt)
		return None

	def pop(self):
		return None if self.empty() else self._stack.pop()
