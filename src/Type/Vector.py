# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsListable,
	If,
	IsString,
)

from .Object import Object

from typing import Union, Sequence

__all__ = (
	'Vector',
)


class Vector(Object):
	def __init__(
			self, 
			name: str,
			size: int,
			null: bool = False,
			default: str = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		class Eval(Pattern):
			def __call__(self, parameter):
				return eval(parameter)
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(
				IsToNone(
					If(IsString(Eval())),
					IsListable(*vaps),
				)
			)
		else:
			patterns.append(If(IsString(Eval())))
			patterns.append(IsListable(*vaps))
		args = None
		if size:
			args = []
			for s in size if isinstance(size, (tuple, list)) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type='VECTOR({})'.format(size),
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return
	
	def encode(self, o: any):
		return str(o)