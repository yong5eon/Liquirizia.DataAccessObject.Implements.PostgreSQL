# -*- coding: utf-8 -*-

from ..Constraint import Constraint
from ..Table import Table
from ..Type import Type

from typing import Union, Sequence, Type as T

__all__ = (
	'ForeignKey'
)


class ForeignKey(Constraint):
	def __init__(
		self,
		name: str,
		cols: Union[str, Sequence[str]],
		reference: Union[str, T[Table]] = None,
		referenceCols: Union[str, Type] = None,
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
	
