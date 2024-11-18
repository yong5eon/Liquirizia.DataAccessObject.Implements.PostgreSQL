# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model

from .Expr import Expr

from typing import Type

__all__ = (
	'Join'
)


class Join(Expr):
	"""Join Class"""

	def __init__(self, expr: str, table: Type[Model], *args) -> None:
		self.expr = expr
		self.table = table
		self.args = args
		return

	def __str__(self):
		return '{} JOIN {} ON {}'.format(
			self.expr,
			self.table.__model__,
			' AND '.join([str(arg) for arg in self.args]),
		)
