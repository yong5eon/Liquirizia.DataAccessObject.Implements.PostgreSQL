# -*- coding: utf-8 -*-

from ..Expr import Expr

from ..Type import Type
from ..Column import Column

from typing import Union

__all__ = (
	'Descend'
)


class Descend(Expr):
	"""Descend Order Class"""

	def __init__(
		self,
		col: Union[str, Type], 
		null='LAST'
	) -> None:
		self.col = col 
		self.null = null
		return

	def __str__(self):
		return '{} DESC{}'.format(
			str(self.col),
			' NULLS {}'.format(self.null) if self.null else '',
		)
