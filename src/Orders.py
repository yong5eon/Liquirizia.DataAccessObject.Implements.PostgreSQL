# -*- coding: utf-8 -*-

from .Expr import Expr
from .Type import Type
from .Column import Column
from .Function import Function

from typing import Union

__all__ = (
	'Ascend',
	'Descend',
	'Random',
)


class Ascend(Expr):
	"""Ascend Order Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		null='LAST'
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		self.null = null
		return

	def __str__(self):
		return '{} ASC{}'.format(
			str(self.col),
			' NULLS {}'.format(self.null) if self.null else '',
		)


class Descend(Expr):
	"""Descend Order Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr], 
		null='LAST'
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col 
		self.null = null
		return

	def __str__(self):
		return '{} DESC{}'.format(
			str(self.col),
			' NULLS {}'.format(self.null) if self.null else '',
		)


class Random(Expr):
	"""Random Order Class"""

	def __init__(self):
		return

	def __str__(self):
		return 'RANDOM()'
