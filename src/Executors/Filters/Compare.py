# -*- coding: utf-8 -*-

from ..Expr import Expr

from ...Function import Function
from ...Type import Type

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
		col: Union[str, Type, Function],
		other: Union[Any, Type, Function],
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} = {}'.format(
			str(self.col),
			str(self.other) if isinstance(self.other, Type) else self.encode(self.other),
		)
	

class IsNotEqualTo(Expr):
	"""Is Not Equal Filter Class"""

	def __init__(
		self,
		col: Union[str, Type, Function],
		other: Union[Any, Type, Function],
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} != {}'.format(
			str(self.col),
			str(self.other) if isinstance(self.other, Type) else self.encode(self.other),
		)


class IsGreaterThan(Expr):
	"""Is Greater Than Filter Class"""

	def __init__(
		self,
		col: Union[str, Type, Function],
		other: Union[Any, Type, Function],
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} > {}'.format(
			str(self.col),
			str(self.other) if isinstance(self.other, Type) else self.encode(self.other),
		)


class IsGreaterEqualTo(Expr):
	"""Is Greater Equal Filter Class"""

	def __init__(
		self,
		col: Union[str, Type, Function],
		other: Union[Any, Type, Function],
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} >= {}'.format(
			str(self.col),
			str(self.other) if isinstance(self.other, Type) else self.encode(self.other),
		)


class IsLessThan(Expr):
	"""Is Less Than Filter Class"""

	def __init__(
		self,
		col: Union[str, Type, Function],
		other: Union[Any, Type, Function],
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} < {}'.format(
			str(self.col),
			str(self.other) if isinstance(self.other, Type) else self.encode(self.other),
		)


class IsLessEqualTo(Expr):
	"""Is Less Equal Filter Class"""

	def __init__(
		self,
		col: Union[str, Type, Function],
		other: Union[Any, Type, Function],
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} <= {}'.format(
			str(self.col),
			str(self.other) if isinstance(self.other, Type) else self.encode(self.other),
		)
