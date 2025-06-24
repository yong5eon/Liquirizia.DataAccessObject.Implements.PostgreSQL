# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
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
		va: Validator = Validator(IsByteString()),
		fn: Handler = None,
		null: bool = False,
		default: Union[bytes, Value, Function] = None,
		description: str = None,
	):
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
