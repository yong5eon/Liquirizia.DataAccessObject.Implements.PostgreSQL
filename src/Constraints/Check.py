# -*- coding: utf-8 -*-

from ..Constraint import Constraint
from ..Expr import Expr

__all__ = (
	'Check'
)


class Check(Constraint):
	def __init__(
		self,
		name: str,
		expr: Expr,
	):
		super().__init__(name)
		self.expr = expr
		return
	