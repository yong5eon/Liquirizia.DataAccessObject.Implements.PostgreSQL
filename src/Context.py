# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Context as BaseContext

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
		return transform(self.cursor.fetchall())

	def row(self):
		return dict(self.cursor.fetchone())

	def count(self):
		return self.cursor.rowcount

	@property
	def query(self):
		return self.cursor.query