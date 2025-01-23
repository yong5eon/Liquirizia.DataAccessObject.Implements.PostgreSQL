# -*- coding: utf-8 -*-

from ..Type import Type
from ..Function import Function
from ..Value import Value

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsNotToNone,
	IsArray,
	If,
	IsString,
	SetDefault,
)

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
			vargs = []
			if default:
				if not isinstance(default, Function):
					if isinstance(default, Value):
						vargs.append(SetDefault(default.value))
					else:
						vargs.append(SetDefault(default))
			if null:
				vargs.append(IsToNone(If(IsString(Eval())), IsArray()))
			else:
				vargs.append(IsNotToNone(If(IsString(Eval())), IsArray()))
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
		args = None
		if size:
			args = []
			for s in size if isinstance(size, Sequence) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type='{}({})'.format('VECTOR', size),
			typedefault=typedefault,
			null=null,
			default=default,
			description=description,
			va=va,
			fn=fn,
		)
		return

	def encode(self, o: any): return str(o)
