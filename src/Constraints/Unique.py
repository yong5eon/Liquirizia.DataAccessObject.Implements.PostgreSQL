# -*- coding: utf-8 -*-

from ..Constraint import Constraint
from ..Column import Column

from typing import Union, Sequence

__all__ = (
	'Unique'
)


class Unique(Constraint):
	def __init__(
		self, 
		name: str,
		cols: Union[Column, Sequence[Column]],
		null: bool = False
	):
		super().__init__(name)
		self.cols = []
		cols = cols if isinstance(cols, (tuple, list)) else [cols]
		for col in cols:
			if not isinstance(col, Column):
				col = Column(col)
			self.cols.append(col)
		self.null = null
		return
	