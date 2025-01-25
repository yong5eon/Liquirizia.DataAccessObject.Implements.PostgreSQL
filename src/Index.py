# -*- coding: utf-8 -*-

from .Expr import Expr

from typing import Sequence

__all__ = (
	'Index',
	'IndexUnique',
)


class Index(object):
	def __init__(
		self, 
		name: str,
		exprs: Sequence[Expr],
		unique: bool = False,
		using: str = 'BTREE',
		notexists: bool = True,
	):
		self.name = name
		self.table = None
		self.exprs = list(exprs) if isinstance(exprs, (tuple, list)) else [exprs]
		self.unique = unique
		self.using = using
		self.notexists = notexists
		self.conds = None
		return

	def where(self, *args: Sequence[Expr]) -> 'Index':
		if not isinstance(args, (tuple, list)):
			args = [args]
		self.conds = args
		return self


class IndexUnique(Index):
	def __init__(self, name, exprs, using = 'BTREE', notexists = True):
		super().__init__(name, exprs, True, using, notexists)
		return
