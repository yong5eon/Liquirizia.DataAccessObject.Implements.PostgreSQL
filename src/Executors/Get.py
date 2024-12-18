# -*- coding: utf-8 -*-

from .Select import Select

from ..Cursor import Cursor

from Liquirizia.DataAccessObject.Properties.Database import Mapper, Filter

__all__ = (
	'Get'
)


class Get(Select):
	def fetch(self, cursor: Cursor, mapper: Mapper = None, filter: Filter = None):
		rows = super().fetch(cursor, mapper=mapper, filter=filter)
		if rows:
			return rows[0]
		return None
