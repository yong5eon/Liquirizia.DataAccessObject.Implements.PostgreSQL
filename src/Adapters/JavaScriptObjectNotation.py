# -*- coding: utf-8 -*-

# from psycopg.abc import Dumper, Loader
from psycopg.adapt import Dumper, Loader

from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence, Mapping

from json import dumps, loads

from typing import Any

__all__ = (
	'JavaScriptObjectNotationDumper',
)


class JavaScriptObjectNotationDumper(Dumper):
	def encode(self, o: Any):
		encoder = (
			(set, lambda o: list(o)),
			(datetime, lambda o: o.isoformat()),
			(date, lambda o: o.isoformat()),
			(time, lambda o: o.isoformat()),
			(Decimal, lambda o: str(o)),
			(Sequence, lambda o: list(o)),
			(Mapping, lambda o: dict(o)),
		)
		for T, enc in encoder:
			if isinstance(o, T): return enc(o)
		raise TypeError('{} is not support to encode in {}'.format(o.__class__.__name__, self.__class__.__name__))
	def dump(self, o : Mapping):
		return dumps(o, default=self.encode, ensure_ascii=False).encode('utf-8')
	
class JavaScriptObjectNotationLoader(Loader):
	def load(self, data):
		return loads(data.decode('utf-8'))
	
