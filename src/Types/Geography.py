# -*- coding: utf-8 -*-

from ..Type import Type
from ..Patterns import IsPoint, TupleToPoint, StrToPoint

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	Any,
	IsTuple,
	IsSizeOf,
	IsString,
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
			null: bool = False,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			vargs = []
			if null:
				vargs.append(IsToNone(Any(IsPoint(), IsTuple(IsSizeOf(2), TupleToPoint()), IsString(StrToPoint()))))
			else:
				vargs.append(IsNotToNone(Any(IsPoint(), IsTuple(IsSizeOf(2), TupleToPoint()), IsString(StrToPoint()))))
			va = Validator(*vargs)
		super().__init__(
			key=name, 
			type='{}({}, {})'.format('GEOGRAPHY', subtype, srid),
			typedefault=None,
			null=null,
			default=None,
			description=description,
			va=va,
			fn=fn,
		)
		return
