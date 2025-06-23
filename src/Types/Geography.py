# -*- coding: utf-8 -*-

from ..Type import Type
from ..Patterns import IsPoint, TupleToPoint, StrToPoint

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsTuple,
	IsSizeOf,
)

__all__ = (
	'Geography',
)


class Geography(Type, typestr='GEOGRAPHY'):
	def __init__(
			self, 
			name: str,
			subtype: str = 'POINT',
			srid: int = 4326,
			va: Validator = Validator(IsTuple(IsSizeOf(2), TupleToPoint())),
			fn: Handler = None,
			null: bool = False,
			description: str = None,
		):
		super().__init__(
			key=name, 
			type=tuple,
			typestr='{}({}, {})'.format('GEOGRAPHY', subtype, srid),
			null=null,
			default=None,
			description=description,
			va=va,
			fn=fn,
		)
		return
