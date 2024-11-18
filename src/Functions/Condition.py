# -*- coding: utf-8 -*-

from ..Function import Function

from ..Type import Type

from typing import Union, Any

__all__ = (
	'IfNull'
)


class IfNull(Function):
	def __init__(
		self,
		col: Union[str, Type],
		value: Any,
	):
		self.col = col
		self.value = value
		return
	def __str__(self):
		return 'IFNULL({}, {})'.format(
			str(self.col),
			self.value,
		)
