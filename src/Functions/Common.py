# -*- coding: utf-8 -*-

from ..Function import Function

from ..Type import Type
from ..Column import Column
from ..Expr import Expr
from ..Function import Function

from typing import Union, Sequence

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
		col: Union[Expr, Function, Column, Type],
		distinct: bool = False,
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col 
		self.conds = None
		self.distinct = distinct
		return
	def where(self, *args):
		self.conds = args
		return self
	def __str__(self):
		return 'COUNT({}{}){}'.format(
			'DISTINCT ' if self.distinct else '',
			str(self.col),
			' FILTER (WHERE {})'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)


class Sum(Function):
	def __init__(
		self,
		col: Union[Expr, Function, Column, Type],
		distinct: bool = False,
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col 
		self.conds = None
		self.distinct = distinct
		return
	def where(self, *args: Sequence[Expr]):
		self.conds = args
		return self
	def __str__(self):
		return 'SUM({}{}){}'.format(
			'DISTINCT ' if self.distinct else '',
			str(self.col),
			' FILTER (WHERE {})'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)
	

class Average(Function):
	def __init__(
		self,
		col: Union[Expr, Function, Column, Type],
		distinct: bool = False,
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col 
		self.conds = None
		self.distinct = distinct
		return
	def where(self, *args: Sequence[Expr]):
		self.conds = args
		return self
	def __str__(self):
		return 'AVG({}{}){}'.format(
			'DISTINCT ' if self.distinct else '',
			str(self.col),
			' FILTER (WHERE {})'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)
	

class Min(Function):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col 
		return
	def __str__(self):
		return 'MIN({})'.format(str(self.col))
	

class Max(Function):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col 
		return
	def __str__(self):
		return 'MAX({})'.format(str(self.col))


class AggregateToArray(Function):
	def __init__(
		self,
		col: Union[Column, Type, Function, Expr],
		distinct: bool = False,
	):
		if not isinstance(col, (Column, Type, Function, Expr)): col = Column(col)
		self.col = col 
		self.distinct = distinct
		return
	def __str__(self):
		return 'ARRAY_AGG({}{})'.format(
			'DISTINCT ' if self.distinct else '',
			str(self.col),
		)


class RowNumber(Function):
	def __init__(self, *args: Sequence[Expr]):
		self.orders = args
		self.partitions = None
		return
	def order(self, *args: Sequence[Expr]):
		self.orders = args
		return
	def partition(self, *args: Sequence[Expr]):
		self.partitions = args
		return
	def __str__(self):
		return 'ROW_NUMBER() OVER({}{})'.format(
			' PARTITION BY {} '.format(', '.join([str(partition) for partition in self.partitions])) if self.partitions else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.orders])) if self.orders else '',
		)


class Rank(Function):
	def __init__(self, *args: Sequence[Expr]):
		self.orders = args
		self.partitions = None
		return
	def order(self, *args: Sequence[Expr]):
		self.orders = args
		return
	def partition(self, *args: Sequence[Expr]):
		self.partitions = args
		return
	def __str__(self):
		return 'RANK() OVER({}{})'.format(
			' PARTITION BY {} '.format(', '.join([str(partition) for partition in self.partitionBy])) if self.partitions else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.orders])) if self.orders else '',
		)


class DenseRank(Function):
	def __init__(self, *args: Sequence[Expr]):
		self.orders = args
		self.partitions = None
		return
	def order(self, *args: Sequence[Expr]):
		self.orders = args
		return
	def partition(self, *args: Sequence[Expr]):
		self.partitions = args
		return
	def __str__(self):
		return 'DENSE_RANK() OVER({}{})'.format(
			' PARTITION BY {} '.format(', '.join([str(partition) for partition in self.partitionBy])) if self.partitions else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.orders])) if self.orders else '',
		)
