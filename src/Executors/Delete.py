# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Executor
from Liquirizia.DataModel import Model

from typing import Type

__all__ = (
	'Update'
)


class Delete(Executor):
	def __init__(self, o: Type[Model]):
		self.obj = o
		self.table = o.__model__
		self.kwargs = {}
		self.cond = None
		return
	
	def set(self, **kwargs):
		for k, v in self.obj.__mapper__.items():
			if k not in kwargs.keys(): continue
			self.kwargs[v.key] = v.validator(kwargs[k])
		return self
	
	def where(self, *args):
		self.conds = args
		return self
	
	@property
	def query(self):
		return 'DELETE FROM {}{}'.format(
			self.table,
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)

	@property	
	def args(self):
		return list(self.kwargs.values())
	