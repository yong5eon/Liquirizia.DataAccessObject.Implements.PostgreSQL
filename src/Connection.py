# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Connection as BaseConnection
from Liquirizia.DataAccessObject.Properties.Database import Database

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Cursor import Cursor
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Model import (
	Executors,
	Executor,
	Fetch,
	Run,
)
from Liquirizia.DataAccessObject.Properties.Database.Session import Session

from .Configuration import Configuration
from .Pool import Pool
from .Context import Context
from .Cursor import Cursor
from .Session import Session

from psycopg2 import connect
from psycopg2 import (
	# Execute Error
	DatabaseError,
	NotSupportedError as DatabaseNotSupportedError,
	ProgrammingError as DatabaseProgrammingError,
	DataError as DatabaseDataError,
	IntegrityError as DatabaseIntegrityError,
	# Connection Error
	OperationalError as DatabaseOperationError,
	InternalError as DatabaseInternalError,
)
from psycopg2.extras import RealDictCursor

from typing import Union


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
		try:
			if self.conf.persistent:
				self.connection = Pool.Get(self.conf)
			else:
				self.connection = connect(
					host=self.conf.host,
					port=str(self.conf.port),
					database=self.conf.database,
					user=self.conf.user,
					password=self.conf.password
				)
			self.connection.cursor_factory = RealDictCursor
			self.connection.autocommit = self.conf.autocommit
		except (DatabaseInternalError, DatabaseOperationError) as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def close(self):
		try:
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
		except (DatabaseInternalError, DatabaseOperationError) as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def begin(self):
		self.connection.autocommit = False
		return

	def execute(self, sql, *args):
		try:
			cursor = self.connection.cursor()
			cursor.execute(sql, args)
			return Context(cursor)
		except (
			DatabaseError, 
			DatabaseDataError, 
			DatabaseNotSupportedError, 
			DatabaseIntegrityError, 
			DatabaseProgrammingError
		) as e:
			raise ExecuteError(str(e))
		except (DatabaseInternalError, DatabaseOperationError) as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def executes(self, sql, *args):
		try:
			cursor = self.connection.cursor()
			cursor.executemany(sql, args)
			return Context(cursor)
		except (
			DatabaseError, 
			DatabaseDataError, 
			DatabaseNotSupportedError, 
			DatabaseIntegrityError, 
			DatabaseProgrammingError
		) as e:
			raise ExecuteError(str(e))
		except (DatabaseInternalError, DatabaseOperationError) as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def run(self, executor: Union[Executor,Executors]):
		cursor = None
		try:
			cursor = self.connection.cursor()
			def execs(execs: Executors):
				__ = []
				for query, args in execs:
					cursor.execute(query, args)
					if not isinstance(executor, Fetch): continue
					rows = executor.fetch(Cursor(cursor))
					__.extend(rows)
				return __
			def exec(exec: Executor):
				cursor.execute(exec.query, exec.args)
				if not isinstance(exec, Fetch): return
				return exec.fetch(Cursor(cursor))
			if isinstance(executor, Executors): return execs(executor)
			if isinstance(executor, Executor): return exec(executor)
		except (
			DatabaseError, 
			DatabaseDataError, 
			DatabaseNotSupportedError, 
			DatabaseIntegrityError, 
			DatabaseProgrammingError
		) as e:
			raise ExecuteError(str(e))
		except (DatabaseInternalError, DatabaseOperationError) as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		
	def cursor(self) -> Cursor:
		return Cursor(self.connection.cursor())
		
	def session(self) -> Session:
		return Session(self.connection)

	def commit(self):
		try:
			if self.connection and not self.connection.closed:
				self.connection.commit()
				self.connection.autocommit = self.conf.autocommit
		except (
			DatabaseError, 
			DatabaseDataError, 
			DatabaseNotSupportedError, 
			DatabaseIntegrityError, 
			DatabaseProgrammingError
		) as e:
			raise CommitError(str(e), error=e)
			raise ExecuteError(str(e))
		except (DatabaseInternalError, DatabaseOperationError) as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def rollback(self):
		try:
			if self.connection and not self.connection.closed:
				self.connection.rollback()
				self.connection.autocommit = self.conf.autocommit
		except (
			DatabaseError, 
			DatabaseDataError, 
			DatabaseNotSupportedError, 
			DatabaseIntegrityError, 
			DatabaseProgrammingError
		) as e:
			raise RollBackError(str(e), error=e)
		except (DatabaseInternalError, DatabaseOperationError) as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return
