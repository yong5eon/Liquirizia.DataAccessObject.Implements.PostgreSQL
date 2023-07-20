# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import DataAccessObjectConfiguration as DataAccessObjectConfigurationBase

__all__ = (
	'DataAccessObjectConfiguration'
)


class DataAccessObjectConfiguration(DataAccessObjectConfigurationBase):
	"""
	Data Access Configuration Class for PostgreSQL
	"""

	def __init__(self, host, port, database, username=None, password=None, autocommit=False, persistent=False, min=0, max=0):
		self.host = host
		self.port = port
		self.database = database
		self.user = username
		self.password = password
		self.persistent = persistent
		self.min = min
		self.max = max
		self.autocommit = autocommit
		return

