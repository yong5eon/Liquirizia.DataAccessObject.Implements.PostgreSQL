# -*- coding: utf-8 -*-

from typing import Union, Type as T, Any

__all__ = (
	'Value',
)


class Value(object):
	def __init__(self, value: Any):
		self.value = value
		return
	def __str__(self):
		fn ={
			str: lambda x: "'{}'".format(x),
			bool: lambda x: 'TRUE' if x else 'FALSE',
		}.get(type(self.value), None)
		if fn: return fn(self.value)
		return str(self.value)
