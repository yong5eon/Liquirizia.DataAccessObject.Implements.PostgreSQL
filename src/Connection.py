# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Connection as BaseConnection
from Liquirizia.DataAccessObject.Properties.Database import (
	Database,
	Executors,
	Executor,
	Fetch,
	Run,
	Filter,
)

from Liquirizia.DataAccessObject.Properties.Database.Cursor import Cursor
from Liquirizia.DataAccessObject.Properties.Database.Session import Session

from Liquirizia.DataModel import Model

from .Configuration import Configuration
from .Pool import Pool
from .Context import Context
from .Cursor import Cursor
from .Session import Session

from psycopg import connect, ClientCursor
from psycopg.rows import dict_row

from typing import Union, Type


__all__ = (
	'Connection'
)


class Connection(BaseConnection, Database, Run):
	"""Connection Class for PostgreSQL"""
	def __init__(self, conf: Configuration):
		self.conf = conf
		self.connection = None
		return

	def __del__(self):
		if not self.connection:
			return
		self.close()
		return

	def connect(self):
		if self.conf.persistent:
			self.connection = Pool.Get(self.conf)
		else:
			dsn = 'postgresql://'
			if self.conf.user:
				dsn += self.conf.user
				if self.conf.password:
					dsn += ':' + self.conf.password
				dsn += '@'
			dsn += '{}:{}/{}'.format(self.conf.host, self.conf.port, self.conf.database)
			self.connection = connect(
				conninfo=dsn,
				autocommit=self.conf.autocommit,
				cursor_factory=ClientCursor,
				row_factory=dict_row,
			)
		for k, v in self.conf.dumpers.items() if self.conf.dumpers else []:
			self.connection.adapters.register_dumper(k, v)
		# TODO : set Loaders
		return

	def close(self):
		if self.conf.autocommit:
			self.commit()
		if self.conf.persistent:
			Pool.Release(self.conf, self.connection)
			del self.connection
			self.connection = None
		else:
			self.connection.close()
			del self.connection
			self.connection = None
		return

	def begin(self):
		self.connection.autocommit = False
		return

	def execute(self, sql, *args):
		cursor = self.connection.cursor()
		cursor.execute(sql, args)
		return Context(cursor)

	def executes(self, sql, *args):
		cursor = self.connection.cursor()
		cursor.executemany(sql, args)
		return Context(cursor)

	def run(
		self,
		executor: Union[Executor,Executors],
		filter: Filter = None,
		fetch: Type[Model] = None,
	):
		cursor = self.connection.cursor()
		def execs(execs: Executors):
			__ = []
			for query, args in execs:
				cursor.execute(query, args)
				if not isinstance(executor, Fetch): continue
				rows = executor.fetch(Cursor(cursor), filter=filter, fetch=fetch)
				__.extend(rows)
			return __
		def exec(exec: Executor):
			cursor.execute(exec.query, exec.args)
			if not isinstance(exec, Fetch): return
			return exec.fetch(Cursor(cursor), filter=filter, fetch=fetch)
		if isinstance(executor, Executors): return execs(executor)
		if isinstance(executor, Executor): return exec(executor)
		raise RuntimeError('{} must be executor or executors'.format(executor.__class__.__name__))
		
	def cursor(self) -> Cursor:
		return Cursor(self.connection.cursor())
		
	def session(self) -> Session:
		return Session(self.connection)

	def commit(self):
		if self.connection and not self.connection.closed:
			self.connection.commit()
			self.connection.autocommit = self.conf.autocommit
		return

	def rollback(self):
		if self.connection and not self.connection.closed:
			self.connection.rollback()
			self.connection.autocommit = self.conf.autocommit
		return

