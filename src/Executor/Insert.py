# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executor, Fetch

from ..Model import Table
from ..Type import Object
from ..Cursor import Cursor

from typing import Type

__all__ = (
	'Insert'
)


class Insert(Executor, Fetch):
	def __init__(self, o: Type[Table]):
		self.obj = o
		self.table = o.__properties__['name']
		self.kwargs = {}
		return
	
	def values(self, **kwargs):
		for k, v in self.obj.__dict__.items():
			if not isinstance(v, Object): continue
			if k not in kwargs.keys(): continue
			self.kwargs[v.key] = v.encode(v.validator(kwargs[k]))
		return self
	
	@property
	def model(self):
		return self.obj
	
	@property
	def query(self):
		return 'INSERT INTO {}({}) VALUES({}) RETURNING *'.format(
			self.table,
			', '.join(self.kwargs.keys()),
			', '.join(['%({})s'.format(k) for k in self.kwargs.keys()]),
		)

	@property	
	def args(self):
		return self.kwargs.values()

	def fetch(self, cursor: Cursor):
		obj = self.obj(**dict(cursor.row()))
		obj.__cursor__ = cursor
		return obj
