# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsDateTime,
	IsDate,
	IsTime,
)

from .Object import Object

from datetime import date, time, datetime

__all__ = (
	'Timestamp',
	'Date',
	'Time',
)


class Timestamp(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			timezone: bool = False,
			default: datetime = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsDateTime(*vaps)))
		else:
			patterns.append(IsDateTime(*vaps))
		super().__init__(
			name,
			type='TIMESTAMP{}'.format(' WITH TIME ZONE' if timezone else ''),
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return


class Date(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: date = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsDate(*vaps)))
		else:
			patterns.append(IsDate(*vaps))
		super().__init__(
			key=name, 
			type='DATE',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return


class Time(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			timezone: bool = False,
			default: time = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsTime(*vaps)))
		else:
			patterns.append(IsTime(*vaps))
		super().__init__(
			key=name, 
			type='TIME{}'.format(' WITH TIME ZONE' if timezone else ''),
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return
