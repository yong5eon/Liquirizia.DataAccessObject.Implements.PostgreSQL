# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Filter
from Liquirizia.DataModel import Model

from .Select import Select

from ..Cursor import Cursor

from typing import Type

__all__ = (
	'Get'
)


class Get(Select):
	def fetch(self, cursor: Cursor, filter: Filter = None, fetch: Type[Model] = None):
		rows = super().fetch(cursor, filter=filter, fetch=fetch)
		if rows:
			return rows[0]
		return None
