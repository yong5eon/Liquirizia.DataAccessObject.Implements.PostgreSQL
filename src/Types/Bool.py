# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsBool,
)

from ..Function import Function

from typing import Union

__all__ = (
	'Bool',
)


class Bool(Type, typestr='BOOLEAN'):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: Union[bool, Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		if not va:
			if null:
				va = Validator(IsToNone(IsBool()))
			else:
				va = Validator(IsNotToNone(IsBool()))
		super().__init__(
			key=name, 
			type=self.typestr,
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va, 
			fn=fn,
		)
		return

