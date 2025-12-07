# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	Optional,
	IsByteString,
)

from typing import Union

__all__ = (
	'Binary',
)


class Binary(Type, typestr='BYTEA'):
	def __init__(
		self, 
		name: str, 
		va: Validator = None,
		fn: Handler = None,
		null: bool = False,
		default: Union[bytes, Value, Function] = None,
		description: str = None,
	):
		if va is None:
			if null:
				va = Validator(Optional(IsByteString()))
			else:
				va = Validator(IsByteString())
		super().__init__(
			key=name, 
			type=bytes,
			typestr='BYTEA',
			va=va,
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return
