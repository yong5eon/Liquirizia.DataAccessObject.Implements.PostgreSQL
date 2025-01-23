# -*- coding: utf-8 -*-

from .Join import Join
from ..Expr import Expr

from Liquirizia.DataModel import Model

from typing import Type, Sequence

__all__ = (
	'RightOuter'
)


class RightOuter(Join):
	"""Right Outer Join Class"""
	def __init__(self, table: Type[Model], *args: Sequence[Expr]) -> None:
		super(RightOuter, self).__init__('RIGHT OUTER', table, *args)
		return
