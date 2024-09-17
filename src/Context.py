# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Context as BaseContext

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from psycopg import (
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
	'Context'
)


class Context(BaseContext):
	"""Context Class for PostgreSQL"""

	def __init__(self, cursor):
		self.cursor = cursor
		return

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

	@property
	def query(self):
		return self.cursor.query