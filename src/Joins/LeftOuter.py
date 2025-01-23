# -*- coding: utf-8 -*-

from .Join import Join
from ..Expr import Expr

from Liquirizia.DataModel import Model

from typing import Type, Sequence

__all__ = (
	'LeftOuter'
)


class LeftOuter(Join):
	"""Left Outer Class"""
	def __init__(self, table: Type[Model], *args: Sequence[Expr]) -> None:
		super(LeftOuter, self).__init__('LEFT OUTER', table, *args)
		return
