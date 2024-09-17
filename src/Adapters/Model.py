# -*- coding: utf-8 -*-

from psycopg.adapt import Dumper, Loader
from psycopg import Connection

from Liquirizia.DataModel import Model
from Liquirizia.DataModel.Types import (
	List,
	Tuple,
	Dictionary,
)

from datetime import datetime, date, time
from decimal import Decimal

from json import dumps

__all__ = (
	'InitAdapterForModel',
	'ListDumper',
	'TupleDumper',
	'DictionaryDumper',
	'ModelDumper',
)


## declare Adaptors
class ListDumper(Dumper):
	def dump(self, o : List):
		return o.__value__


class TupleDumper(Dumper):
	def dump(self, o : Tuple):
		return o.__value__


class DictionaryDumper(Dumper):
	def dump(self, o : Dictionary):
		return o.__value__


class ModelDumper(Dumper):
	def encode(self, o):
		encoder = (
			(datetime, lambda o: o.isoformat()),
			(date, lambda o: o.isoformat()),
			(time, lambda o: o.isoformat()),
			(Decimal, lambda o: str(o)),
			(List, lambda o: o.__value__),
			(Tuple, lambda o: o.__value__),
			(Dictionary, lambda o: o.__value__),
			(Model, lambda o: o.__object__),
		)
		for T, enc in encoder:
			if isinstance(o, T): return enc(o)
		raise TypeError('{} is not support JavaScriptNotationObject encode'.format(o.__class__.__name__))

	def dump(self, o : Model):
		return dumps(o.__object__, default=self.encode).encode('utf-8')
	

def InitAdapterForModel(connection: Connection):
	connection.adapters.register_dumper(Model, ModelDumper)
	connection.adapters.register_dumper(List, ListDumper)
	connection.adapters.register_dumper(Tuple, TupleDumper)
	connection.adapters.register_dumper(Dictionary, DictionaryDumper)
	return
