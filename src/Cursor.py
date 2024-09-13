# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Cursor

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Model import (
	Executors,
	Executor,
	Fetch,
	Run,
)

from .Context import Context

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

__all__ = (
	'Cursor'
)


class Cursor(Cursor, Run):
	"""Cursor Class for PostgreSQL"""
	def __init__(self, cursor):
		self.cursor = cursor
		return

	def execute(self, sql, *args):
		try:
			self.cursor.execute(sql, args)
			return Context(self.cursor)
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
			self.cursor.executemany(sql, args)
			return Context(self.cursor)
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

	def run(self, executor: type[Executor|Executors]):
		cursor = None
		try:
			def execs(execs: Executors):
				__ = []
				for query, args in execs:
					self.cursor.execute(query, args)
					if not isinstance(executor, Fetch): continue
					rows = executor.fetch(Cursor(self.cursor))
					__.extend(rows)
				return __
			def exec(exec: Executor):
				self.cursor.execute(exec.query, exec.args)
				if not isinstance(exec, Fetch): return
				return exec.fetch(Cursor(self.cursor))
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
		
	def rows(self):
		def transform(rows):
			li = []  # the dictionary to be filled with the row data and to be returned
			for i, row in enumerate(rows):  # iterate throw the sqlite3.Row objects
				li.append(dict(row))
			return li
		try:
			return transform(self.cursor.fetchall())
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

	def row(self):
		try:
			return dict(self.cursor.fetchone())
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

	def count(self):
		return self.cursor.rowcount