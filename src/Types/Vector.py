# -*- coding: utf-8 -*-

from ..Type import Type

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsArray,
	If,
	IsString,
)

from ..Function import Function

from typing import Union, Sequence

__all__ = (
	'Vector',
)


class Vector(Type, typestr='VECTOR'):
	def __init__(
			self, 
			name: str,
			size: Union[int, Sequence[int]],
			null: bool = False,
			default: Union[Sequence[float], Function] = None,
			description: str = None,
			va: Validator = None,
			fn: Handler = None,
		):
		class Eval(Pattern):
			def __call__(self, parameter):
				return eval(parameter)
		if not va:
			if null:
				va = Validator(IsToNone(If(IsString(Eval())), IsArray()))
			else:
				va = Validator(IsNotToNone(If(IsString(Eval())), IsArray()))
		args = None
		if size:
			args = []
			for s in size if isinstance(size, Sequence) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type='{}({})'.format(self.typestr, size),
			null=null,
			default=str(default) if isinstance(default, Function) else default,
			description=description,
			va=va,
			fn=fn,
		)
		return

	def encode(self, o: any): return str(o)
