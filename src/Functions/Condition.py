# -*- coding: utf-8 -*-

from ..Function import Function

from ..Type import Type
from ..Column import Column
from ..Value import Value

from typing import Union, Any

__all__ = (
	'IfNull'
)


class IfNull(Function):
	def __init__(
		self,
		col: Union[Column, Type, Function],
		value: Union[Any, Value, Type, Function],
	):
		self.col = col
		if not isinstance(value, (Value, Type, Function)):
			value = Value(value)
		self.value = value
		return
	def __str__(self):
		return 'COALESCE({}, {})'.format(
			str(self.col),
			str(self.value),
		)
