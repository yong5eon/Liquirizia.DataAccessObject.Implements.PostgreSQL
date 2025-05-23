# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import (
	Executor,
	Fetch,
	Filter,
)
from Liquirizia.DataModel import Model

from ..Cursor import Cursor

from ..Table import Table
from ..View import View
from ..Type import Type
from ..Expr import Expr
from ..Joins import Join

from typing import Type as T, Sequence, Union

__all__ = (
	'Select'
)


class Select(Executor, Fetch):
	def __init__(self, o: Union[T[Table], T[View]]):
		self.obj = o
		self.kwargs = {}
		self.joins = None
		self.conds = None
		self.grps = None
		self.havs = None
		self.ords = None
		self.vals = None
		self.offset = None
		self.size = None
		return

	def join(self, *args: Sequence[Join]):
		self.joins = args
		return self

	def where(self, *args: Sequence[Expr]):
		self.conds = args
		return self

	def group(self, *args: Sequence[Expr]):
		self.grps = args
		return self
	
	def having(self, *args: Sequence[Expr]):
		self.havs = args
		return self

	def order(self, *args: Sequence[Expr]):
		self.ords = args
		return self

	def limit(self, size: int = None, offset: int = 0):
		self.size = size
		self.offset = offset
		return self
	
	def values(self, *args: Sequence[Type]):
		self.vals = args
		return self
	
	@property
	def query(self):
		args = []
		if not self.vals:
			for k, v in self.obj.__mapper__.items():
				args.append(str(v))
		else:
			for v in self.vals:
				args.append(str(v))
		if issubclass(self.obj, Table):
			obj = self.obj.__table__
		if issubclass(self.obj, View):
			obj = self.obj.__view__
		sql = 'SELECT {} FROM {}"{}"{}{}{}{}{}{}'.format(
			', '.join(args),
			'"{}".'.format(self.obj.__schema__) if self.obj.__schema__ else '',
			obj,
			''.join([' {}'.format(str(join)) for join in self.joins]) if self.joins else '',
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
			' GROUP BY {}'.format(', '.join([str(grp) for grp in self.grps])) if self.grps else '',
			' HAVING {}'.format(' AND '.join([str(hav) for hav in self.havs])) if self.havs else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.ords])) if self.ords else '',
			' OFFSET {} LIMIT {}'.format(self.offset, self.size) if self.size else '',
		)
		return sql
	
	@property	
	def args(self):
		return list(self.kwargs.values())

	def fetch(self, cursor: Cursor, filter: Filter = None, fetch: T[Model] = None):
		rows = cursor.rows()
		if not rows: return None
		_ = []
		for i, row in enumerate(rows):
			if filter: row = filter(row)
			if fetch:
				obj = fetch(**row)
				if isinstance(obj, (Table, View)):
					obj.__cursor__ = cursor
				_.append(obj)
			else:
				_.append(row)
		return _
