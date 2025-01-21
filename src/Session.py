# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import (
	Session as BaseSession,
	Run,
	Fetch,
	Mapper,
	Filter,
	Executor,
	Executors,
)
from Liquirizia.DataModel import Model

from .Context import Context
from .Cursor import Cursor

from psycopg.rows import dict_row

from typing import Union, Type

__all__ = (
	'Session'
)


class Session(BaseSession, Run):
	"""Session Class for PostgreSQL"""

	def __init__(self, connection):
		self.connection = connection
		self.connection.autocommit = False
		self.cursor  = self.connection.cursor(row_factory=dict_row)
		return

	def __del__(self):
		self.cursor.close()
		self.connection.commit()
		return

	def execute(self, sql, *args):
		self.cursor.execute(sql, args)
		return Context(self.cursor)
		return

	def executes(self, sql, *args):
		self.cursor.executemany(sql, args)
		return Context(self.cursor)
		return

	def run(
		self,
		executor: Union[Executor,Executors],
		mapper: Mapper = None,
		filter: Filter = None,
		fetch: Type[Model] = None,
	):
		def execs(execs: Executors):
			__ = []
			for query, args in execs:
				self.cursor.execute(query, args)
				if not isinstance(executor, Fetch): continue
				rows = executor.fetch(Cursor(self.cursor), mapper=mapper, filter=filter, fetch=fetch)
				__.extend(rows)
			return __
		def exec(exec: Executor):
			self.cursor.execute(exec.query, exec.kwargs)
			if not isinstance(exec, Fetch): return
			return exec.fetch(Cursor(self.cursor), mapper=mapper, filter=filter, fetch=fetch)
		if isinstance(executor, Executors): return execs(executor)
		if isinstance(executor, Executor): return exec(executor)
		raise RuntimeError('{} must be executor or exectors'.format(executor.__class__.__name__))

	def rows(self):
		def transform(rows):
			li = []  # the dictionary to be filled with the row data and to be returned
			for i, row in enumerate(rows):  # iterate throw the sqlite3.Row objects
				li.append(dict(row))
			return li
		return transform(self.cursor.fetchall())

	def row(self):
		return dict(self.cursor.fetchone())

	def count(self):
		return self.cursor.rowcount

