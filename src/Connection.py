# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Connection as BaseConnection
from Liquirizia.DataAccessObject.Properties.Database import Database

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from .Configuration import Configuration
from .Formatter import Formatter
from .Pool import Pool

from psycopg2 import connect
from psycopg2 import DatabaseError, IntegrityError, ProgrammingError, OperationalError, NotSupportedError, DataError, InternalError
from psycopg2.extras import DictCursor


__all__ = (
	'DatabaseAccessObject'
)


class Connection(BaseConnection, Database):
	"""Connection Class for PostgreSQL"""

	def __init__(self, conf: Configuration):
		self.conf = conf
		self.connection = None
		self.cursor = None
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
			self.connection.cursor_factory = DictCursor
			self.connection.autocommit = self.conf.autocommit
			self.cursor = self.connection.cursor()
		except OperationalError as e:
			raise ConnectionError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def close(self):
		try:
			if self.conf.autocommit:
				self.commit()

			if not self.cursor:
				self.cursor.close()
				del self.cursor
				self.cursor = None

			if self.conf.persistent:
				Pool.Release(self.conf, self.connection)
				del self.connection
				self.connection = None
			else:
				self.connection.close()
				del self.connection
				self.connection = None
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError, DataError, InternalError) as e:
			raise ExecuteError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def begin(self):
		self.connection.autocommit = False
		return

	def execute(self, sql, *args, **kwargs):
		try:
			query = str(Formatter(sql, *args, **kwargs))
			self.cursor.execute(query)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError, DataError, InternalError) as e:
			raise ExecuteError(str(e), sql=str(Formatter(sql, *args, **kwargs)), code=e.pgcode, error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def affected(self):
		return self.cursor.rowcount

	def rows(self):
		def transform(rows):
			li = []  # the dictionary to be filled with the row data and to be returned
			for i, row in enumerate(rows):  # iterate throw the sqlite3.Row objects
				li.append(dict(row))
			return li
		try:
			return transform(self.cursor.fetchall())
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError, DataError, InternalError) as e:
			raise CursorError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)

	def commit(self):
		try:
			if self.connection and not self.connection.closed:
				self.connection.commit()
				self.connection.autocommit = self.conf.autocommit
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError, DataError, InternalError) as e:
			raise CommitError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def rollback(self):
		try:
			if self.connection and not self.connection.closed:
				self.connection.rollback()
				self.connection.autocommit = self.conf.autocommit
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError, DataError, InternalError) as e:
			raise RollBackError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return
