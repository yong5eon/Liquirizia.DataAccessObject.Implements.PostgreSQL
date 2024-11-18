# -*- coding: utf-8 -*-

from psycopg.adapt import Dumper

from decimal import Decimal
from datetime import datetime, date, time
from collections.abc import Sequence, Mapping
from Liquirizia.DataModel import Model

from json import dumps

from typing import Any

__all__ = (
	'DataModelDumper',
)


class DataModelDumper(Dumper):
	def encode(self, o: Any):
		encoder = (
			(set, lambda o: list(o)),
			(datetime, lambda o: o.isoformat()),
			(date, lambda o: o.isoformat()),
			(time, lambda o: o.isoformat()),
			(Decimal, lambda o: str(o)),
			(Sequence, lambda o: list(o)),
			(Mapping, lambda o: dict(o)),
			(Model, lambda o: dict(o.__properties__)),
		)
		for T, enc in encoder:
			if isinstance(o, T): return enc(o)
		raise TypeError('{} is not support to encode in {}'.format(o.__class__.__name__, self.__class__.__name__))
	def dump(self, o : Model):
		return dumps(o.__properties__, default=self.encode, ensure_ascii=False).encode('utf-8')

