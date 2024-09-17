# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsInteger,
	IsFloat,
	IsDecimal,
)

from .Object import Object

from ..Model import Sequence

from typing import Union, Sequence

__all__ = (
	'Short',
	'Integer',
	'Long',
	'Float',
	'Double',
	'Decimal',
)


class Short(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			seq: Sequence = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsInteger(*vaps)))
		else:
			patterns.append(IsInteger(*vaps))
		super().__init__(
			key=name, 
			type='SMALLINT',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		self.seq = seq
		return


class Integer(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			seq: Sequence = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsInteger(*vaps)))
		else:
			patterns.append(IsInteger(*vaps))
		super().__init__(
			key=name, 
			type='INTEGER',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		self.seq = seq
		return


class Long(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			seq: Sequence = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsInteger(*vaps)))
		else:
			patterns.append(IsInteger(*vaps))
		super().__init__(
			key=name, 
			type='BIGINT',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		self.seq = seq
		return
	

class Float(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: float = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsFloat(*vaps)))
		else:
			patterns.append(IsFloat(*vaps))
		super().__init__(
			key=name, 
			type='REAL',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return
	

class Double(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: float = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsFloat(*vaps)))
		else:
			patterns.append(IsFloat(*vaps))
		super().__init__(
			key=name, 
			type='DOUBLE PRECISION',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return


class Decimal(Object):
	def __init__(
			self, 
			name: str, 
			scale: int,
			precision: int,
			null: bool = False,
			default: float = None,
			vaps: Union[Pattern,Sequence[Pattern]] = (),
			fn: Handler = None,
		):
		if not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsDecimal(*vaps)))
		else:
			patterns.append(IsDecimal(*vaps))
		super().__init__(
			key=name, 
			type='NUMERIC({},{})'.format(scale, precision),
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return
