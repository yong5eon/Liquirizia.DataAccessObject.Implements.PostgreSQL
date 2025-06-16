# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Column import Column
from ..Value import Value

from typing import Union, Any

__all__ = (
	'Like',
	'LikeStartWith',
	'LikeEndWith',
)


class Like(Expr):
	"""Like Filter Class"""
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: str,
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		self.other = other
		return
	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.col),
			'\'%%{}%%\''.format(self.other),
		)


class LikeStartWith(Expr):
	"""Is Like Filter Class"""
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: str,
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		self.other = other
		return
	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.col),
			'\'{}%%\''.format(self.other),
		)


class LikeEndWith(Expr):
	"""Is Like Filter Class"""
	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: str,
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		self.other = other
		return
	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.col),
			'\'%%{}\''.format(self.other),
		)
