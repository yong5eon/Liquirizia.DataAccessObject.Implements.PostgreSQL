# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	ToByteArray,
	IsByteArray,
)

from ..Function import Function

from typing import Union

__all__ = (
	'ByteArray',
)


class ByteArray(Type, typestr='BYTEA'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[bytes, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(ToByteArray(), IsByteArray()))
			else:
				va = Validator(IsNotToNone(ToByteArray(), IsByteArray()))
		super().__init__(
			key=name, 
			type='BYTEA',
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return
