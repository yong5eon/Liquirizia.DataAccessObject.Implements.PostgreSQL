# -*- coding: utf-8 -*-

from .Join import Join

from Liquirizia.DataModel import Model


from typing import Type

__all__ = (
	'LeftOuter'
)


class LeftOuter(Join):
	"""Left Outer Class"""

	def __init__(self, table: Type[Model], *args) -> None:
		super(LeftOuter, self).__init__('LEFT OUTER', table, *args)
		return
