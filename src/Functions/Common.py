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
	'RowNumber',
	'Rank',
	'DenseRank',
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


class RowNumber(Function):
	def __init__(self, *args):
		self.orders = args
		self.partitions = None
		return
	def orderBy(self, *args):
		self.orders = args
		return
	def partitionBy(self, *args):
		self.partitions = args
		return
	def __str__(self):
		return 'ROW_NUMBER() OVER({}{})'.format(
			' PARTITION BY {} '.format(', '.join([str(partition) for partition in self.partitionBy])) if self.partitions else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.orders])),
		)


class Rank(Function):
	def __init__(self, *args):
		self.orders = args
		self.partitions = None
		return
	def orderBy(self, *args):
		self.orders = args
		return
	def partitionBy(self, *args):
		self.partitions = args
		return
	def __str__(self):
		return 'RANK() OVER({}{})'.format(
			' PARTITION BY {} '.format(', '.join([str(partition) for partition in self.partitionBy])) if self.partitions else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.orders])),
		)


class DenseRank(Function):
	def __init__(self, *args):
		self.orders = args
		self.partitions = None
		return
	def orderBy(self, *args):
		self.orders = args
		return
	def partitionBy(self, *args):
		self.partitions = args
		return
	def __str__(self):
		return 'DENSE_RANK() OVER({}{})'.format(
			' PARTITION BY {} '.format(', '.join([str(partition) for partition in self.partitionBy])) if self.partitions else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.orders])),
		)
