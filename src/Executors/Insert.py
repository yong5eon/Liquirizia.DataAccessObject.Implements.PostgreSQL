# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import (
	Executor,
	Fetch,
	Filter,
)
from Liquirizia.DataModel import Model

from ..Cursor import Cursor
from ..Table import Table
from ..Column import Column
from ..Type import Type

from typing import Type as T, Dict, Any, Sequence, Union
from uuid import uuid4

__all__ = (
	'Insert'
)


class Insert(Executor, Fetch):
	def __init__(self, o: T[Table]):
		self.obj = o
		self.kwargs = {}
		self.ons = None
		self.onkwargs = None
		return
	
	def values(self, **kwargs: Dict[str, Any]):
		for k, v in self.obj.__mapper__.items():
			if k not in kwargs.keys(): continue
			self.kwargs[v.key] = (uuid4().hex, v.encode(v.validator(kwargs[k])))
		return self
	
	def on(self, *args: Sequence[Union[Column, Type]]):
		self.ons = []
		for arg in args:
			if isinstance(arg, Type):
				self.ons.append(arg.key)
			elif isinstance(arg, Column):
				self.ons.append(str(arg))
			else:
				self.ons.append(arg)
		return self

	def set(self, **kwargs: Dict[str, Any]):
		self.onkwargs = {}
		for k, v in self.obj.__mapper__.items():
			if k not in kwargs.keys(): continue
			self.onkwargs[v.key] = (uuid4().hex, v.encode(v.validator(kwargs[k])))
		return self

	@property
	def query(self):
		on = None
		if self.ons:
			on = 'ON CONFLICT ({}) DO '.format(', '.join(['"{}"'.format(on) for on in self.ons]))
			if self.onkwargs:
				on += 'UPDATE SET {}'.format(', '.join(['"{}"=%({})s'.format(k, idx) for k, (idx, v) in self.onkwargs.items()]))
			else:
				on += 'NOTHING'
		return 'INSERT INTO {}"{}"({}) VALUES({}){} RETURNING *'.format(
			'"{}".'.format(self.obj.__schema__) if self.obj.__schema__ else '',
			self.obj.__table__,
			', '.join(['"{}"'.format(k) for k in self.kwargs.keys()]),
			', '.join(['%({})s'.format(idx) for k, (idx, v) in self.kwargs.items()]),
			' {}'.format(on) if on else ''
		)

	@property	
	def args(self):
		kwargs = {}
		for k, (idx, v) in self.kwargs.items():
			kwargs[idx] = v
		if self.onkwargs:
			for k, (idx, v) in self.onkwargs.items():
				kwargs[idx] = v
		return kwargs

	def fetch(self, cursor: Cursor, filter: Filter = None, fetch: T[Model] = None):
		row = cursor.row()
		if filter: row = filter(row)
		if fetch:
			obj = fetch(**row)
			if isinstance(obj, Table):
				obj.__cursor__ = cursor
			return obj
		else:
			return row
