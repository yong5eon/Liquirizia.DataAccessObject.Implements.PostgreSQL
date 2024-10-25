# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Configuration as BaseConfiguration

from .Adapters import (
	JavaScriptObjectNotationDumper,
	ArrayDumper,
)

from collections.abc import Sequence, Mapping
from psycopg.adapt import Dumper, Loader
from typing import Type, Mapping as Map

__all__ = (
	'Configuration'
)


class Configuration(BaseConfiguration):
	"""Configuration Class for PostgreSQL"""

	def __init__(
		self,
		host: str,
		port: int,
		database: str,
		username: str = None,
		password: str = None,
		autocommit: bool = False,
		persistent: bool = False,
		min: int = 0,
		max: int = 0,
		dumpers: Map[Type, Dumper] = None,
		loaders: Map[Type, Loader] = None,
	):
		self.host = host
		self.port = port
		self.database = database
		self.user = username
		self.password = password
		self.persistent = persistent
		self.min = min
		self.max = max
		self.autocommit = autocommit
		self.dumpers = {
			dict: JavaScriptObjectNotationDumper,
			Sequence: ArrayDumper,
			Mapping: JavaScriptObjectNotationDumper,
		}
		if dumpers: self.dumpers.update(dumpers)
		# TODO : set Loaders
		return
	
