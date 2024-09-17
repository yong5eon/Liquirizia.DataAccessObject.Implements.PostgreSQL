# -*- coding: utf-8 -*-

from psycopg.adapt import Dumper, Loader
from psycopg.types import TypeInfo
from psycopg import Connection

from decimal import Decimal
from datetime import datetime, date, time
from json import dumps, loads, dump

__all__ = (
	'JavaScriptObjectNotationDumper',
	'InitAdapterForJavaScriptObjectNotation',
)

	
class JavaScriptObjectNotationDumper(Dumper):
	def encode(self, o):
		encoder = (
			(datetime, lambda o: o.isoformat()),
			(date, lambda o: o.isoformat()),
			(time, lambda o: o.isoformat()),
			(Decimal, lambda o: str(o)),
			# (List, lambda o: o.__value__),
			# (Tuple, lambda o: o.__value__),
			# (Dictionary, lambda o: o.__value__),
			# (Model, lambda o: o.__object__),
		)
		for T, enc in encoder:
			if isinstance(o, T): return enc(o)
		raise TypeError('{} is not support JavaScriptNotationObject encode'.format(o.__class__.__name__))
	def dump(self, o : dict):
		return dumps(o, default=self.encode).encode('utf-8')
	
class JavaScriptObjectNotationLoader(Loader):
	def load(self, data):
		return loads(data.decode('utf-8'))
	

def InitAdapterForJavaScriptObjectNotation(connection: Connection):
	T = TypeInfo.fetch(connection, 'JSON')
	T.register(connection)
	dumper = type('', (JavaScriptObjectNotationDumper,), {'old': T.oid})
	# loader = type('', (JavaScriptObjectNotationLoader,), {'old': T.oid})
	connection.adapters.register_dumper(dict, dumper)
	# connection.adapters.register_loader(T.oid, loader)
	return
