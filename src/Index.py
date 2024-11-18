# -*- coding: utf-8 -*-

from typing import Sequence

__all__ = (
	'Index'
)


class Index(object):
	def __init__(
		self, 
		name: str,
		colexprs: Sequence[str],
		using: str = 'BTREE',
		notexists: bool = True,
	):
		self.name = name
		self.table = None
		self.colexprs = colexprs if isinstance(colexprs, (tuple, list)) else [colexprs]
		self.using = using
		self.notexists = notexists
		return
	