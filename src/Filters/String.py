# -*- coding: utf-8 -*-

from ..Expr import Expr

from ..Type import Type
from ..Column import Column

from typing import Union

__all__ = (
	'IsLike',
	'IsLikeStartWith',
	'IsLikeEndWith',
)


class IsLike(Expr):
	"""Is Like Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type],
		other,
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.col),
			self.encode('%%{}%%'.format(self.other)),
		)


class IsLikeStartWith(Expr):
	"""Is Like Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type],
		other,
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.col),
			self.encode('{}%%'.format(self.other)),
		)


class IsLikeEndWith(Expr):
	"""Is Like Filter Class"""

	def __init__(
		self,
		col: Union[Column, Type],
		other,
	):
		self.col = col
		self.other = other
		return

	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.col),
			self.encode('%%{}'.format(self.other)),
		)
