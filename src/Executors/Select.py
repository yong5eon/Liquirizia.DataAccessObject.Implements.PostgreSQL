# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Executor, Fetch
from Liquirizia.DataModel import Model

from ..Cursor import Cursor

from typing import Type

__all__ = (
	'Select'
)


class Select(Executor, Fetch):
	def __init__(self, o: Type[Model]):
		self.obj = o
		self.table = o.__model__
		self.kwargs = {}
		self.joins = None
		self.conds = None
		self.grps = None
		self.havs = None
		self.ords = None
		self.vals = None
		self.offset = None
		self.size = None
		self.o = None
		return

	def join(self, *args):
		self.joins = args
		return self

	def where(self, *args):
		self.conds = args
		return self

	def groupBy(self, *args):
		self.grps = args
		return self
	
	def having(self, *args):
		self.havs = args
		return self

	def orderBy(self, *args):
		self.ords = args
		return self

	def limit(self, size: int = None, offset: int = 0):
		self.size = size
		self.offset = offset
		return self
	
	def values(self, *args):
		self.vals = args
		return self
	
	def to(self, o: Type[Model]):
		self.o = o
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
		sql = 'SELECT {} FROM {}{}{}{}{}{}{}'.format(
			', '.join(args),
			self.table,
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

	def fetch(self, cursor: Cursor):
		_ = []
		for i, row in enumerate(cursor.rows()):
			if self.o:
				obj = self.o(**dict(row))
				obj.__cursor__ = cursor
				_.append(obj)
			else:
				_.append(dict(row))
		return _ if len(_) else None
