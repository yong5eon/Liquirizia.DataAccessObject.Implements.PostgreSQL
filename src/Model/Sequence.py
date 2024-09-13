# -*- coding: utf-8 -*-

__all__ = (
	'Sequence'
)


class Sequence(object):
	def __init__(
		self, 
		name: str,
		type: str = 'BIGINT',
		increment: int = 1,
		min: int = 1,
		max: int = None,
		start: int = 1,
		notexists: bool = True,
	):
		self.name = name
		self.table = None
		self.col = None
		self.type = type
		self.increment = increment
		self.min = min
		self.max = max
		self.start = start
		self.notexists = notexists
		return
	