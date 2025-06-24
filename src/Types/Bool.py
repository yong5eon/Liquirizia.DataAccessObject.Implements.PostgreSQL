# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler
from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import (
	IsBool,
)

from typing import Union

__all__ = (
	'Bool',
)


class Bool(Type, typestr='BOOLEAN'):
	def __init__(
		self, 
		name: str, 
		va: Validator = Validator(IsBool()),
		fn: Handler = None,
		null: bool = False,
		default: Union[bool, Value, Function] = None,
		description: str = None,
	):
		super().__init__(
			key=name, 
			type=bool,
			typestr='BOOLEAN',
			va=va, 
			fn=fn,
			null=null,
			default=default,
			description=description,
		)
		return
