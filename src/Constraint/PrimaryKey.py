# -*- coding: utf-8 -*-

from .Constraint import Constraint

__all__ = (
	'PrimaryKey'
)


class PrimaryKey(Constraint):
	def __init__(
		self,
		name: str,
		cols
	):
		super().__init__(name)
		self.cols = cols if isinstance(cols, (tuple, list)) else [cols]
		return
	