# -*- coding: utf-8 -*-

from ..Function import Function

from ..Type import Type

from typing import Union

__all__ = (
	'Count',
	'Sum',
	'Average',
	'Min',
	'Max',
	'AggregateToArray',
)


class Count(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		return
	def __str__(self):
		return 'COUNT({})'.format(str(self.col))


class Sum(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		return
	def __str__(self):
		return 'SUM({})'.format(str(self.col))
	

class Average(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		return
	def __str__(self):
		return 'AVG({})'.format(str(self.col))
	

class Min(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		return
	def __str__(self):
		return 'MIN({})'.format(str(self.col))
	

class Max(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		return
	def __str__(self):
		return 'MAX({})'.format(str(self.col))


class AggregateToArray(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		return
	def __str__(self):
		return 'ARRAY_AGG({})'.format(str(self.col))