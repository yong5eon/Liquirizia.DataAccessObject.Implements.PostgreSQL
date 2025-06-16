# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Function import Function
from ..Column import Column
from ..Value import Value

from typing import Union, Any

__all__ = (
	'EqualTo',
	'NotEqualTo',
	'GreaterThan',
	'GreaterEqualTo',
	'LessThan',
	'LessEqualtTo',
)


class EqualTo(Expr):
	"""Equal Filter Class"""

	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		if not isinstance(other, (Value, Column, Function, Expr)): other = Value(other)
		self.other = other
		return

	def __str__(self):
		if isinstance(self.other, Value) and str(self.other) == 'NULL':
			return '{} IS {}'.format(
				str(self.col),
				str(self.other),
			)
		return '{} = {}'.format(
			str(self.col),
			str(self.other),
		)


class NotEqualTo(Expr):
	"""Not Equal Filter Class"""

	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		if not isinstance(other, (Value, Column, Function, Expr)): other = Value(other)
		self.other = other
		return

	def __str__(self):
		if isinstance(self.other, Value) and str(self.other) == 'NULL':
			return '{} IS NOT {}'.format(
				str(self.col),
				str(self.other),
			)
		return '{} != {}'.format(
			str(self.col),
			str(self.other),
		)


class GreaterThan(Expr):
	"""Greater Than Filter Class"""

	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		if not isinstance(other, (Value, Column, Function, Expr)): other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} > {}'.format(
			str(self.col),
			str(self.other),
		)


class GreaterEqualTo(Expr):
	"""Is Greater Equal Filter Class"""

	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		if not isinstance(other, (Value, Column, Function, Expr)): other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} >= {}'.format(
			str(self.col),
			str(self.other),
		)


class LessThan(Expr):
	"""Less Than Filter Class"""

	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		if not isinstance(other, (Value, Column, Function, Expr)): other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} < {}'.format(
			str(self.col),
			str(self.other),
		)


class LessEqualTo(Expr):
	"""Less Equal Filter Class"""

	def __init__(
		self,
		col: Union[Any, Value, Column, Function, Expr],
		other: Union[Any, Value, Column, Function, Expr],
	):
		if not isinstance(col, (Value, Column, Function, Expr)): col = Value(col)
		self.col = col
		if not isinstance(other, (Value, Column, Function, Expr)): other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} <= {}'.format(
			str(self.col),
			str(self.other),
		)
