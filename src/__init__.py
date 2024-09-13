# -*- coding: utf-8 -*-

from .Configuration import Configuration
from .Connection import Connection
from .Context import Context
from .Cursor import Cursor
from .Session import Session

from Liquirizia.DataModel import Model
from Liquirizia.DataModel.Types import (
	List,
	Tuple,
	Dictionary,
)

from psycopg2.extensions import (
	register_adapter,
	adapt,
)
from decimal import Decimal
from datetime import datetime, date, time
from json import dumps

__all__ = (
	'Configuration',
	'Connection',
	'Context',
	'Cursor',
	'Session',
)

# register adapter

## declare Adaptors
class ListAdaptor(object):
	def __call__(self, o : List):
		return adapt(o.__value__)
	
class TupleAdaptor(object):
	def __call__(self, o : Tuple):
		return adapt(o.__value__)

class DictionaryAdaptor(object):
	def __call__(self, o : Dictionary):
		return adapt(o.__value__)
	
class ModelAdaptor(object):
	def __call__(self, o : Model):
		return adapt(o.__object__)
	
class JavaScriptNotationObjectAdaptor(object):
	def __init__(self, enc=(
		(datetime, lambda o: o.isoformat()),
		(date, lambda o: o.isoformat()),
		(time, lambda o: o.isoformat()),
		(Decimal, lambda o: str(o)),
		(List, lambda o: o.__value__),
		(Tuple, lambda o: o.__value__),
		(Dictionary, lambda o: o.__value__),
		(Model, lambda o: o.__object__),
	)) -> None:
		self.encoder = enc
		return
	def encode(self, o):
		for T, enc in self.encoder:
			if isinstance(o, T): return enc(o)
		raise TypeError('{} is not support JavaScriptNotationObject encode'.format(o.__class__.__name__))
	def __call__(self, o : dict):
		return adapt(dumps(o, default=self.encode))
	
## common
register_adapter(dict, JavaScriptNotationObjectAdaptor())

## DataModel
register_adapter(List, ListAdaptor())
register_adapter(Tuple, TupleAdaptor())
register_adapter(Dictionary, JavaScriptNotationObjectAdaptor())
register_adapter(Model, JavaScriptNotationObjectAdaptor())
