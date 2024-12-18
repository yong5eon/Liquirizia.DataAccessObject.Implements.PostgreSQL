# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import (
	Executor,
	Fetch,
	Mapper,
	Filter,
)
from Liquirizia.DataModel import Model

from ..Cursor import Cursor

from typing import Type

__all__ = (
	'Update'
)


class Update(Executor, Fetch):
	def __init__(self, o: Type[Model]):
		self.obj = o
		self.table = o.__model__
		self.kwargs = {}
		self.cond = None
		return
	
	def set(self, **kwargs):
		for k, v in self.obj.__mapper__.items():
			if k not in kwargs.keys(): continue
			self.kwargs[v.key] = v.encode(v.validator(kwargs[k]))
		return self
	
	def where(self, *args):
		self.conds = args
		return self
	
	@property
	def query(self):
		return 'UPDATE {} SET {}{} RETURNING *'.format(
			self.table,
			', '.join(["{}=%({})s".format(k, k) for k in self.kwargs.keys()]),
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)

	@property	
	def args(self):
		return self.kwargs

	def fetch(self, cursor: Cursor, mapper: Mapper = None, filter: Filter = None):
		row = cursor.row()
		if mapper: row = {mapper(k): v for k, v in row.items()}
		if filter: row = filter(row)
		obj = self.obj(**row)
		obj.__cursor__ = cursor
		return obj
