# -*- coding: utf-8 -*-

from ..Constraint import Constraint

__all__ = (
	'Check'
)


class Check(Constraint):
	def __init__(
		self,
		name: str,
		expr: str
	):
		super().__init__(name)
		self.expr = expr
		return
	