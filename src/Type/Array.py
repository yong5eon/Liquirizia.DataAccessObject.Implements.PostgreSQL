# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsListable,
)

from .Object import Object

__all__ = (
	'Array',
)


class Array(Object):
	def __init__(
			self, 
			name: str,
			type: str,
			size: type[int|tuple|list] = None,
			null: bool = False,
			default: str = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsListable(*vaps)))
		else:
			patterns.append(IsListable(*vaps))
		args = None
		if size:
			args = []
			for s in size if isinstance(size, (tuple, list)) else [size]:
				args.append('[{}]'.format(s))
		super().__init__(
			key=name, 
			type='{}{}'.format(
				type,
				''.join(args) if args else []
			),
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return
