# -*- coding: utf-8 -*-

from .Expr import Expr

from typing import Sequence

__all__ = (
	'Index'
)


class Index(object):
	def __init__(
		self, 
		name: str,
		exprs: Sequence[Expr],
		using: str = 'BTREE',
		notexists: bool = True,
	):
		self.name = name
		self.table = None
		self.exprs = list(exprs) if isinstance(exprs, (tuple, list)) else [exprs]
		self.using = using
		self.notexists = notexists
		return
	