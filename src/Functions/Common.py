# -*- coding: utf-8 -*-

from ..Function import Function

from ..Type import Type
from ..Executors import Expr

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
		self.conds = None
		return
	def where(self, *args):
		self.conds = args
		return self
	def __str__(self):
		return 'COUNT({}){}'.format(
			str(self.col),
			' FILTER (WHERE {})'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)


class Sum(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		self.conds = None
		return
	def where(self, *args):
		self.conds = args
		return self
	def __str__(self):
		return 'SUM({}){}'.format(
			str(self.col),
			' FILTER (WHERE {})'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)
	

class Average(Function):
	def __init__(
		self,
		col: Union[str, Type],
	):
		self.col = col 
		self.conds = None
		return
	def where(self, *args):
		self.conds = args
		return self
	def __str__(self):
		return 'AVG({}){}'.format(
			str(self.col),
			' FILTER (WHERE {})'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)
	

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