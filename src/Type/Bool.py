# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsBool,
)

from .Object import Object

from typing import Union, Sequence

__all__ = (
	'Bool',
)


class Bool(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsBool(*vaps)))
		else:
			patterns.append(IsBool(*vaps))
		super().__init__(
			key=name, 
			type='BOOLEAN',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return
