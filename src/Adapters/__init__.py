# -*- coding: utf-8 -*-

from .JavaScriptObjectNotation import JavaScriptObjectNotationDumper
from .DataModel import DataModelDumper

from ..Values import Point

from psycopg.adapt import Dumper
from psycopg.types.array import ListDumper

from typing import Sequence

__all__ = (
	'JavaScriptObjectNotationDumper',
	'DataModelDumper',
	'ArrayDumper',
	'PointDumper',
)

class ArrayDumper(ListDumper):
	def dump(self, o : Sequence):
		return super().dump(list(o))


class PointDumper(Dumper):
	def dump(self, o : Point):
		return 'POINT({} {})'.format(o.longitude, o.latitude).encode('utf-8')
