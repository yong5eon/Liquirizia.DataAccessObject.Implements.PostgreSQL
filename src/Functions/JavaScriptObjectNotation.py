# -*- coding: utf-8 -*-

from ..Function import Function

from ..Type import Type

from typing import Union

__all__ = (
	'AggregateToJSON',
	'AggregateToJSONB',
)


class AggregateToJSON(Function):
	def __init__(
		self,
		**kwargs,
	):
		self.kwargs = kwargs
		return
	def __str__(self):
		args = []
		for k, v in self.kwargs.items():
			args.append('\'{}\''.format(k))
			args.append(str(v))
		return 'JSON_AGG(JSON_BUILD_OBJECT({}))'.format(', '.join(args))


class AggregateToJSONB(Function):
	def __init__(
		self,
		**kwargs,
	):
		self.kwargs = kwargs
		return
	def __str__(self):
		args = []
		for k, v in self.kwargs.items():
			args.append('\'{}\''.format(k))
			args.append(str(v))
		return 'JSONB_AGG(JSONB_BUILD_OBJECT({}))'.format(', '.join(args))
