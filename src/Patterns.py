# -*- coding: utf-8 -*-

from Liquirizia.Validator import Pattern

from .Values import Point

from typing import Tuple

__all__ = (
	'IsPoint',
	'TupleToPoint',
	'StrToPoint',
)


class IsPoint(Pattern):
	def __init__(self, *args, error: BaseException = None):
		self.args = args
		self.error = error
		return
	def __call__(self, parameter):
		if not isinstance(parameter, Point):
			if self.error:
				raise self.error
			raise TypeError('{} is not a Point'.format(parameter))
		for pattern in self.args:
			parameter = pattern(parameter)
		return parameter
	

class StrToPoint(Pattern):
	def __init__(self, error: BaseException = None):
		self.error = error
		return
	def __call__(self, parameter):
		try:
			point = wkb.loads(bytes.fromhex(parameter))
			return Point(point.x, point.y)
		except Exception as e:
			if self.error:
				raise self.error
			raise ValueError('{} is not a Point'.format(parameter))


class TupleToPoint(Pattern):
	def __init__(self, error: BaseException = None):
		self.error = error
		return
	def __call__(self, parameter):
		if not isinstance(parameter, Tuple):
			if self.error:
				raise self.error
			raise TypeError('{} is not a tuple'.format(parameter))
		if len(parameter) != 2:
			if self.error:
				raise self.error
			raise ValueError('Tuple {} must have 2 elements'.format(parameter))
		return Point(parameter[0], parameter[1])
