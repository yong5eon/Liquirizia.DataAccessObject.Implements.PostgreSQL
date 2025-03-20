# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import (
	Cursor as BaseCursor,
	Executors,
	Executor,
	Fetch,
	Run,
	Filter,
)
from Liquirizia.DataModel import Model

from .Context import Context

from typing import Union, Type

__all__ = (
	'Cursor'
)


class Cursor(BaseCursor, Run):
	"""Cursor Class for PostgreSQL"""
	def __init__(self, cursor):
		self.cursor = cursor
		return

	def execute(self, sql, *args):
		self.cursor.execute(sql, args)
		return Context(self.cursor)

	def executes(self, sql, *args):
		self.cursor.executemany(sql, args)
		return Context(self.cursor)

	def run(
		self,
		executor: Union[Executor,Executors],
		filter: Filter = None,
		fetch: Type[Model] = None,
	):
		def execs(execs: Executors):
			__ = []
			for query, args in execs:
				self.cursor.execute(query, args)
				if not isinstance(executor, Fetch): continue
				rows = executor.fetch(Cursor(self.cursor), filter=filter, fetch=fetch)
				__.extend(rows)
			return __
		def exec(exec: Executor):
			self.cursor.execute(exec.query, exec.args)
			if not isinstance(exec, Fetch): return
			return exec.fetch(Cursor(self.cursor), filter=filter, fetch=fetch)
		if isinstance(executor, Executors): return execs(executor)
		if isinstance(executor, Executor): return exec(executor)
		raise RuntimeError('{} must be executor or executors'.format(executor.__class__.__name__))
		
	def rows(self):
		def transform(rows):
			li = []  # the dictionary to be filled with the row data and to be returned
			for i, row in enumerate(rows):  # iterate throw the sqlite3.Row objects
				li.append(dict(row))
			return li
		rows = self.cursor.fetchall()
		if rows is None: return None
		return transform(rows)

	def row(self):
		row = self.cursor.fetchone()
		if row is None: return None
		return dict(row)

	def count(self):
		return self.cursor.rowcount

