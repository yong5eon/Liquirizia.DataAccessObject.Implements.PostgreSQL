# -*- coding: utf-8 -*-

from ..Function import Function

from ...Type import Object

__all__ = (
	'Count',
	'Sum',
	'Average',
	'Min',
	'Max',
	'NextVal',
)


class Count(Function):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'COUNT({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)


class Sum(Function):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'SUM({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)
	

class Average(Function):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'AVG({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)
	

class Min(Function):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'MIN({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)
	

class Max(Function):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'MIN({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)
	

class NextVal(Function):
	def __init__(self, name:str):
		self.name = name
		return
	def __str__(self):
		return 'NEXTVAL({})'.format(self.name)
