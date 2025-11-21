# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import (
	Executor,
	Fetch,
	Filter,
)
from Liquirizia.DataModel import Model

from ..Cursor import Cursor
from ..Table import Table
from ..Expr import Expr

from typing import Type, Dict, Any, Sequence
from uuid import uuid4

__all__ = (
	'Update'
)


class Update(Executor, Fetch):
	def __init__(self, o: Type[Table]):
		self.obj = o
		self.kwargs = {}
		self.conds = None
		return
	
	def set(self, **kwargs: Dict[str, Any]):
		for k, v in self.obj.__mapper__.items():
			if k not in kwargs.keys(): continue
			o = v.validator(kwargs[k])
			self.kwargs[v.key] = (uuid4().hex, v.encoder(o) if v.encoder else o)
		return self
	
	def where(self, *args: Sequence[Expr]):
		self.conds = args
		return self
	
	@property
	def query(self):
		return 'UPDATE {}"{}" SET {}{} RETURNING *'.format(
			'"{}".'.format(self.obj.__schema__) if self.obj.__schema__ else '',
			self.obj.__table__,
			', '.join(['"{}"=%({})s'.format(k, idx) for k, (idx, v) in self.kwargs.items()]),
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)

	@property	
	def args(self):
		kwargs = {}
		for k, (idx, v) in self.kwargs.items():
			kwargs[idx] = v
		return kwargs

	def fetch(self, cursor: Cursor, filter: Filter = None, fetch: Type[Model] = None):
		row = cursor.row()
		if not row: return None
		if filter: row = filter(row)
		if fetch:
			obj = fetch(**row)
			if isinstance(obj, Table):
				obj.__cursor__ = cursor
			return obj
		else:
			return row
