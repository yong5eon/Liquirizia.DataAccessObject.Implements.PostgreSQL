# -*- coding: utf-8 -*-

from ..Join import Join

from Liquirizia.DataModel import Model

from typing import Type

__all__ = (
	'FullOuter'
)


class FullOuter(Join):
	"""Full Outer Join Class"""

	def __init__(self, table: Type[Model], *args) -> None:
		super(FullOuter, self).__init__('FULL OUTER', table, *args)
		return
