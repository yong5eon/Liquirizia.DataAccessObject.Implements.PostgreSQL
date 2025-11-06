# -*- coding: utf-8 -*-

from .Expr import Expr
from .Column import Column
from enum import Enum
from typing import Sequence, Union

__all__ = (
	'IndexType',
	'Index',
	'IndexUnique',
)

class IndexType(str, Enum):
	BTree = 'BTREE'
	Hash = 'HASH'
	GeneralizedSearchTree = 'GIST'
	SpacePartitionedGeneralizedSearchTree = 'SPGIST'
	GeneralizedInvertedIndex = 'GIN'
	BlockRangeIndex = 'BRIN'
	Bloom = 'BLOOM'
	ReverseUnorderedMatching = 'RUM'
	def __str__(self): return self.value


class Index(object):
	def __init__(
		self, 
		name: str,
		exprs: Union[
			str,
			Sequence[str],
			Column,
			Sequence[Column],
			Expr,
			Sequence[Expr],
		],
		unique: bool = False,
		using: IndexType = None,
		operator: str = None,
		notexists: bool = True,
	):
		self.name = name
		self.table = None
		self.exprs = []
		for expr in exprs if isinstance(exprs, Sequence) else [exprs]:
			if isinstance(expr, str):
				self.exprs.append(Column(expr))
			else:
				self.exprs.append(expr)
		self.unique = unique
		self.using = using
		self.operator = operator
		self.notexists = notexists
		self.conds = None
		return

	def where(self, *args: Sequence[Expr]) -> 'Index':
		if not isinstance(args, (tuple, list)):
			args = [args]
		self.conds = args
		return self


class IndexUnique(Index):
	def __init__(
		self,
		name: str, 
		exprs: Union[Expr, Sequence[Expr]],
		using: IndexType = None,
		operator: str = None,
		notexists: bool = True,
	):
		super().__init__(
			name=name,
			exprs=exprs,
			unique=True,
			using=using,
			operator=operator,
			notexists=notexists
		)
		return
