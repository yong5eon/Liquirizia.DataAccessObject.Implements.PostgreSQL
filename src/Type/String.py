# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsString,
	IsSizeOf,
	IsSizeIn,
)

from .Object import Object

from typing import Union, Sequence

__all__ = (
	'Char',
	'String',
	'Text',
)

class Char(Object):
	def __init__(
			self, 
			name: str,
			size: int,
			null: bool = False,
			default: str = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsString(IsSizeOf(size), *vaps)))
		else:
			patterns.append(IsString(IsSizeOf(size), *vaps))
		super().__init__(
			key=name, 
			type='CHAR{}'.format(
				'({})'.format(size) if size else ''
			),
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return


class String(Object):
	def __init__(
			self, 
			name: str, 
			size: int = None,
			null: bool = False,
			default: str = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		_ = []
		if size:
			_.append(IsSizeIn(size))
		_.extend(vaps)
		if null:
			patterns.append(IsToNone(IsString(*_)))
		else:
			patterns.append(IsString(*_))
		super().__init__(
			key=name, 
			type='VARCHAR{}'.format(
				'({})'.format(size) if size else ''
			),
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return


class Text(Object):
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
			patterns.append(IsToNone(IsString(*vaps)))
		else:
			patterns.append(IsString(*vaps))
		super().__init__(
			key=name, 
			type='TEXT',
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return
