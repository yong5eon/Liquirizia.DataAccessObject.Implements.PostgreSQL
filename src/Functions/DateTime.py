# -*- coding: utf-8 -*-

from ..Function import Function
from ..Column import Column
from ..Expr import Expr
from enum import Enum
from typing import Union

__all__ = (
	'Now',
	'DatePartType',
	'DatePart',
	'Year',
	'Month',
	'Day',
	'Hour',
	'Minute',
	'Second',
	'MilliSecond',
	'MicroSecond',
	'Quarter',
	'Week',
	'DayOfWeek',
	'DayOfWeekISO',
	'DayOfYear',
	'Timezone',
	'TimezoneHour',
	'TimezoneMinute',
	'TimezoneHourMinute',
	'Millenium',
	'Century',
	'Decade',
	'EPoch',
)


class Now(Function):
	def __init__(self):
		return
	def __str__(self):
		return 'NOW()'


class DatePartType(str, Enum):
	Year = 'YEAR'
	Month = 'MONTH'
	Day = 'DAY'
	Hour = 'HOUR'
	Minute = 'MINUTE'
	Second = 'SECOND'
	MilliSecond = 'MILLISECOND'
	MicroSecond = 'MICROSECOND'
	Quarter = 'QUARTER'
	Week = 'WEEK'
	DayOfWeek = 'DOW'
	DayOfWeekISO = 'ISODOW'
	DayOfYear = 'DOY'
	Timezone = 'TIMEZONE'
	TimezoneHour = 'TIMEZONE_HOUR'
	TimezoneMinute = 'TIMEZONE_MINUTE'
	TimezoneHourMinute = 'TIMEZONE_HOUR_MINUTE'
	Millenium = 'MILLENNIUM'
	Centry = 'CENTURY'
	Decade = 'DECADE'
	EPoch = 'EPOCH'
	def __str__(self): return self.value


class DatePart(Function):
	def __init__(self, part: Union[DatePartType, str], expr: Union[Expr, Column, str]):
		self.part = part
		self.expr = expr
		return
	def __str__(self):
		return 'DATE_PART(\'{}\', {})'.format(str(self.part), str(self.expr))


class Year(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Year, expr)
		return


class Month(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Month, expr)
		return


class Day(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Day, expr)
		return


class Hour(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Hour, expr)
		return


class Minute(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Minute, expr)
		return


class Second(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Second, expr)
		return


class MilliSecond(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.MilliSecond, expr)
		return


class MicroSecond(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.MicroSecond, expr)
		return


class Quarter(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Quarter, expr)
		return


class Week(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Week, expr)
		return


class DayOfWeek(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.DayOfWeek, expr)
		return


class DayOfWeekISO(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.DayOfWeekISO, expr)
		return


class DayOfYear(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.DayOfYear, expr)
		return


class Timezone(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Timezone, expr)
		return


class TimezoneHour(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.TimezoneHour, expr)
		return


class TimezoneMinute(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.TimezoneMinute, expr)
		return


class TimezoneHourMinute(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.TimezoneHourMinute, expr)
		return


class Millenium(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Millenium, expr)
		return


class Century(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Centry, expr)
		return


class Decade(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.Decade, expr)
		return


class EPoch(DatePart):
	def __init__(self, expr: Union[Expr, Column, str]):
		super().__init__(DatePartType.EPoch, expr)
		return
