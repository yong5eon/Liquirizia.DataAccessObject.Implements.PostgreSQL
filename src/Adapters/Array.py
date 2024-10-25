# -*- coding: utf-8 -*-

from psycopg.types.array import ListDumper

from collections.abc import Sequence

from typing import Any

__all__ = (
	'ArrayDumper',
)


class ArrayDumper(ListDumper):
	def dump(self, o : Sequence):
		return super().dump(list(o))
