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
		self.cols = cols if isinstance(cols, (tuple, list)) else [cols]
		self.reference = reference
		self.referenceCols = cols if isinstance(referenceCols, (tuple, list)) else [referenceCols]
		self.onDelete = onDelete
		self.onUpdate = onUpdate
		return
