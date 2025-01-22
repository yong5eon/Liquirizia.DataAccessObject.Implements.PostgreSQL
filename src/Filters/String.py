# -*- coding: utf-8 -*-

from ..Expr import Expr

from ..Type import Type

from typing import Union

__all__ = (
	'IsLike'
)


class IsLike(Expr):
	"""Is Like Filter Class"""

	def __init__(
		self,
		col: Union[str, Type],
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
