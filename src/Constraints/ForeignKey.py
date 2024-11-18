# -*- coding: utf-8 -*-

from ..Constraint import Constraint

from typing import Union, Sequence

__all__ = (
	'ForeignKey'
)


class ForeignKey(Constraint):
	def __init__(
		self,
		name: str,
		cols: Union[str, Sequence[str]],
		reference: str = None,
		referenceCols: str = None,
		onDelete: str = None,
		onUpdate: str = None,
	):
		super().__init__(name)
		self.cols = cols if isinstance(cols, (tuple, list)) else [cols]
		self.reference = reference
		self.referenceCols = cols if isinstance(referenceCols, (tuple, list)) else [referenceCols]
		self.onDelete = onDelete
		self.onUpdate = onUpdate
		return
	