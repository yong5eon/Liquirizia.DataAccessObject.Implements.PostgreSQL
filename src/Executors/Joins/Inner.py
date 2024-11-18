# -*- coding: utf-8 -*-

from ..Join import Join

from Liquirizia.DataModel import Model


from typing import Type

__all__ = (
	'Inner'
)


class Inner(Join):
	"""Inner Join Class"""

	def __init__(self, table: Type[Model], *args) -> None:
		super(Inner, self).__init__('INNER', table, *args)
		return
