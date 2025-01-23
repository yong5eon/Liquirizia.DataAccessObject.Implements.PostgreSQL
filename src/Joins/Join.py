# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model

from ..Expr import Expr

from typing import Type, Sequence

__all__ = (
	'Join'
)


class Join(Expr):
	"""Join Class"""

	def __init__(self, expr: str, table: Type[Model], *args: Sequence[Expr]) -> None:
		self.expr = expr
		self.table = table
		self.args = list(args) if isinstance(args, (tuple, list)) else [args]
		return

	def __str__(self):
		return '{} JOIN {} ON {}'.format(
			self.expr,
			self.table.__model__,
			' AND '.join([str(arg) for arg in self.args]),
		)
	
	def on(self, *args: Sequence[Expr]):
		self.args = args
		return self
	
	def where(self, expr: Expr):
		self.args.append(expr)
		return self
