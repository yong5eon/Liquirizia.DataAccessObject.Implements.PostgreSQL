# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	ToByteArray,
	IsByteArray,
	SetDefault,
)

from typing import Union

__all__ = (
	'ByteArray',
)


class ByteArray(Type, typestr='BYTEA'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[bytes, Value, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			vargs = []
			if default:
				if not isinstance(default, Function):
					if isinstance(default, Value):
						vargs.append(SetDefault(default.value))
					else:
						vargs.append(SetDefault(default))
			if null:
				vargs.append(IsToNone(ToByteArray(), IsByteArray()))
			else:
				vargs.append(IsNotToNone(ToByteArray(), IsByteArray()))
			va = Validator(*vargs)
		typedefault = None
		if default is not None:
			if isinstance(default, Value):
				typedefault = str(default)
				default = default.value
			elif isinstance(default, Function):
				typedefault = str(default)
				default = None
			else:
				typedefault = str(Value(default))
		super().__init__(
			key=name, 
			type='BYTEA',
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return
