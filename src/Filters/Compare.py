# -*- coding: utf-8 -*-

from ..Expr import Expr

from ..Function import Function
from ..Type import Type
from ..Column import Column
from ..Value import Value

from typing import Union, Any

__all__ = (
	'IsEqualTo',
	'IsNotEqualTo',
	'IsGreaterThan',
	'IsGreaterEqualtTo',
	'IsLessThan',
	'IsLessEqualtTo',
)


class IsEqualTo(Expr):
	"""Is Equal Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		other: Union[Any, Value, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		if not isinstance(other, (Value, Type, Function, Expr)):
			other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} = {}'.format(
			str(self.col),
			str(self.other),
		)
	

class IsNotEqualTo(Expr):
	"""Is Not Equal Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		other: Union[Any, Value, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		if not isinstance(other, (Value, Type, Function, Expr)):
			other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} != {}'.format(
			str(self.col),
			str(self.other),
		)


class IsGreaterThan(Expr):
	"""Is Greater Than Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		other: Union[Any, Value, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		if not isinstance(other, (Value, Type, Function, Expr)):
			other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} > {}'.format(
			str(self.col),
			str(self.other),
		)


class IsGreaterEqualTo(Expr):
	"""Is Greater Equal Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		other: Union[Any, Value, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		if not isinstance(other, (Value, Type, Function, Expr)):
			other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} >= {}'.format(
			str(self.col),
			str(self.other),
		)


class IsLessThan(Expr):
	"""Is Less Than Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		other: Union[Any, Value, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		if not isinstance(other, (Value, Type, Function, Expr)):
			other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} < {}'.format(
			str(self.col),
			str(self.other),
		)


class IsLessEqualTo(Expr):
	"""Is Less Equal Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		other: Union[Any, Value, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col
		if not isinstance(other, (Value, Type, Function, Expr)):
			other = Value(other)
		self.other = other
		return

	def __str__(self):
		return '{} <= {}'.format(
			str(self.col),
			str(self.other),
		)
