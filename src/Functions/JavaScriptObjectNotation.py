# -*- coding: utf-8 -*-

from ..Function import Function
from ..Expr import Expr
from ..Type import Type
from ..Column import Column

from typing import Union, Dict

__all__ = (
	'AggregateToJSON',
	'AggregateToJSONB',
)


class AggregateToJSON(Function):
	def __init__(
		self,
		**kwargs: Dict[str, Union[Column, Type, Function, Expr]],
	):
		for k, v in kwargs.items():
			if not isinstance(v, (Column, Type, Function, Expr)):
				kwargs[k] = Column(v)
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
		**kwargs: Dict[str, Union[Column, Type, Function, Expr]],
	):
		for k, v in kwargs.items():
			if not isinstance(v, (Column, Type, Function, Expr)):
				kwargs[k] = Column(v)
		self.kwargs = kwargs
		return
	def __str__(self):
		args = []
		for k, v in self.kwargs.items():
			args.append('\'{}\''.format(k))
			args.append(str(v))
		return 'JSONB_AGG(JSONB_BUILD_OBJECT({}))'.format(', '.join(args))
