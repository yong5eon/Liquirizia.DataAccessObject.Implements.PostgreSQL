# -*- coding: utf-8 -*-

from ..Type import Type
from ..Values import Point
from ..Patterns import IsPoint, TupleToPoint, StrToPoint

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	Optional,
)

__all__ = (
	'Geography',
)


class IfStrOrTupleToPoint(IsPoint):
	def __call__(self, parameter):
		if isinstance(parameter, str):
			parameter = StrToPoint()(parameter)
		if isinstance(parameter, tuple):
			parameter = TupleToPoint()(parameter)
		return super().__call__(parameter)


class Geography(Type, typestr='GEOGRAPHY'):
	def __init__(
			self, 
			name: str,
			subtype: str = 'POINT',
			srid: int = 4326,
			va: Validator = None,
			fn: Handler = None,
			null: bool = False,
			description: str = None,
		):
		if va is None:
			if null:
				va = Validator(Optional(IfStrOrTupleToPoint()))
			else:
				va = Validator(IfStrOrTupleToPoint())
		super().__init__(
			key=name, 
			type=Point,
			typestr='{}({}, {})'.format('GEOGRAPHY', subtype, srid),
			null=null,
			default=None,
			description=description,
			va=va,
			fn=fn,
		)
		return
