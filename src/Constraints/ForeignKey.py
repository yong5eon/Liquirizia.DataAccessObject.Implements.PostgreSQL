# -*- coding: utf-8 -*-

from ..Constraint import Constraint
from ..Table import Table
from ..Column	import Column
from ..Type import Type

from typing import Union, Sequence, Type as T

__all__ = (
	'ForeignKey'
)


class ForeignKey(Constraint):
	def __init__(
		self,
		name: str,
		cols: Union[Column, Sequence[Column]],
		reference: Union[T[Table]] = None,
		referenceCols: Union[Column, Sequence[Column], Type, Sequence[Type]] = None,
		onDelete: str = None,
		onUpdate: str = None,
	):
		super().__init__(name)
		self.cols = []
		cols = cols if isinstance(cols, (tuple, list)) else [cols]
		for col in cols:
			if not isinstance(col, Column):
				col = Column(col)
			self.cols.append(col)
		self.reference = reference
		self.referenceCols = []
		referenceCols = referenceCols if isinstance(referenceCols, (tuple, list)) else [referenceCols]
		for col in referenceCols:
			if not isinstance(col, (Column, Type)):
				col = Column(col)
			self.referenceCols.append(col)
		self.onDelete = onDelete
		self.onUpdate = onUpdate
		return
