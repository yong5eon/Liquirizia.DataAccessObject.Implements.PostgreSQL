# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsDictionary,
)

from .Object import Object

__all__ = (
	'JavaScriptObjectNotation',
	'JavaScriptObjectNotationByteArray',
)


class JavaScriptObjectNotation(Object):
	def __init__(
			self, 
			name: str, 
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
			patterns.append(IsToNone(IsDictionary(*vaps)))
		else:
			patterns.append(IsDictionary(*vaps))
		super().__init__(
			key=name, 
			type='JSON',
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return


class JavaScriptObjectNotationByteArray(Object):
	def __init__(
			self, 
			name: str, 
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
			patterns.append(IsToNone(IsDictionary(*vaps)))
		else:
			patterns.append(IsDictionary(*vaps))
		super().__init__(
			key=name, 
			type='JSONB',
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return
