# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model, Handler
from Liquirizia.DataAccessObject.Properties.Database import Executor

from .Schema import Schema

__all__ = (
	'View'
)


class View(Model):
	"""View Model Class"""
	def __new__(cls, **kwargs):
		o = super().__new__(cls, **kwargs)
		o.__cursor__ = None
		return o

	def __init__(self, **kwargs):
		_ = {}
		for k, v in kwargs.items():
			for c, t in self.__mapper__.items():
				if k == t.key:
					k = c
			_[k] = v
		return super().__init__(**_)

	def __setattr__(self, name, value):
		if name in ('__cursor__'): return super(Model, self).__setattr__(name, value)
		return super().__setattr__(name, value)

	def __init_subclass__(
		cls,
		executor: Executor,
		name: str = None,
		schema: Schema = None,
		fn: Handler = None,
		description: str = None,
	):
		cls.__executor__ = executor
		if schema:
			if isinstance(schema, str): schema = Schema(schema)
		cls.__schema__ = schema
		cls.__view__ = name if name else cls.__name__
		return super().__init_subclass__(
			name=None,
			fn=fn,
			description=description,
		)
