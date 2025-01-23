# -*- coding: utf-8 -*-

from ..Expr import Expr
from ..Table import Table
from ..View import View

from typing import Type, Sequence, Union

__all__ = (
	'Join'
)


class Join(Expr):
	"""Join Class"""

	def __init__(self, expr: str, obj: Union[Type[Table], Type[View]], *args: Sequence[Expr]) -> None:
		self.expr = expr
		self.obj = obj 
		self.args = list(args) if isinstance(args, (tuple, list)) else [args]
		return

	def __str__(self):
		if issubclass(self.obj, Table):
			return '{} JOIN {}"{}" ON {}'.format(
				self.expr,
				'"{}".'.format(self.obj.__schema__) if self.obj.__schema__ else '',
				self.obj.__table__,
				' AND '.join([str(arg) for arg in self.args]),
			)
		if issubclass(self.obj, View):
			return '{} JOIN {}"{}" ON {}'.format(
				self.expr,
				'"{}".'.format(self.obj.__schema__) if self.obj.__schema__ else '',
				self.obj.__view__,
				' AND '.join([str(arg) for arg in self.args]),
			)
	
	def on(self, *args: Sequence[Expr]):
		self.args = args
		return self
	
	def where(self, expr: Expr):
		self.args.append(expr)
		return self
