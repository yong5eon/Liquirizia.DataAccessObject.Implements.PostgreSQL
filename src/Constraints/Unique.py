# -*- coding: utf-8 -*-

from ..Constraint import Constraint

from typing import Union, Sequence

__all__ = (
	'Unique'
)


class Unique(Constraint):
	def __init__(
		self, 
		name: str,
		cols: Union[str, Sequence[str]],
		null: bool = False
	):
		super().__init__(name)
		self.cols = cols if isinstance(cols, (tuple, list)) else [cols]
		self.null = null
		return
	