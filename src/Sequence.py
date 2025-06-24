# -*- coding: utf-8 -*-

from .Type import Type
from .Types import BIGINT

from typing import Type as T, Union

__all__ = (
	'Sequence'
)


class Sequence(object):
	def __init__(
		self, 
		name: str,
		type: Union[str, T[Type]] = BIGINT,
		increment: int = 1,
		min: int = 1,
		max: int = None,
		start: int = 1,
		notexists: bool = True,
	):
		self.name = name
		self.schema = None
		self.type = type if isinstance(type, str) else type.__typestr__
		self.increment = increment
		self.min = min
		self.max = max
		self.start = start
		self.notexists = notexists
		return
	
	def __str__(self):
		return self.name
