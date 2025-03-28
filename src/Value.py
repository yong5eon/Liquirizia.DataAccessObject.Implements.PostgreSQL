# -*- coding: utf-8 -*-

from .Values import Point

from typing import Any

__all__ = (
	'Value',
)


class Value(object):
	def __init__(self, value: Any):
		self.value = value
		return
	def __str__(self):
		fn ={
			type(None): lambda x: 'NULL',
			bool: lambda x: 'TRUE' if x else 'FALSE',
			str: lambda x: '\'{}\''.format(x),
			Point: lambda x: 'POINT({} {})'.format(x.longitude, x.latitude),
		}.get(type(self.value), None)
		if fn: return fn(self.value)
		return str(self.value)
