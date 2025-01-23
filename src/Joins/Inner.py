# -*- coding: utf-8 -*-

from .Join import Join
from ..Expr import Expr

from Liquirizia.DataModel import Model

from typing import Type, Sequence

__all__ = (
	'Inner'
)


class Inner(Join):
	"""Inner Join Class"""
	def __init__(self, table: Type[Model], *args: Sequence[Expr]) -> None:
		super(Inner, self).__init__('INNER', table, *args)
		return
