# -*- coding: utf-8 -*-

from .Type import Type

from typing import Type as T, Union

__all__ = (
	'Column',
)

class Column(object):
	def __init__(
		self,
		name: str,
	):
		self.name = name
		self.typecast = None
		return
	
	def __str__(self):
		return '{}{}'.format(
			self.name,
			'::{}'.format(self.typecast) if self.typecast else '',
		)
	
	def cast(
		self,
		type: Union[str, T[Type]],
	):
		self.typecast = type if isinstance(type, str) else str(type)
		return self
