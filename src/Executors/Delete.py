# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Executor

from ..Table import Table
from ..Expr import Expr

from typing import Type, Iterable

__all__ = (
	'Update'
)


class Delete(Executor):
	def __init__(self, o: Type[Table]):
		self.obj = o
		self.kwargs = {}
		self.cond = None
		return
	
	def where(self, *args: Iterable[Expr]):
		self.conds = args
		return self
	
	@property
	def query(self):
		return 'DELETE FROM {}"{}"{}'.format(
			'"{}".'.format(self.obj.__schema__) if self.obj.__schema__ else '',
			self.obj.__table__,
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)

	@property	
	def args(self):
		return list(self.kwargs.values())
	