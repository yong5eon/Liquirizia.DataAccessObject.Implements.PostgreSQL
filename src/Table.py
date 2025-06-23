# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model, Handler

from .Schema import Schema
from .Constraint import Constraint
from .Index import Index
from .Sequence import Sequence

from typing import Sequence as TSequence

__all__ = (
	'Table'
)


class Table(Model):
	"""Table Model Class"""
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
		name: str = None,
		schema: Schema = None,
		sequences: TSequence[Sequence] = None,
		constraints: TSequence[Constraint] = None,
		indexes: TSequence[Index] = None,
		description: str = None,
		fn: Handler = None,
	):
		if schema:
			if isinstance(schema, str): schema = Schema(schema)
		cls.__schema__ = schema
		cls.__table__ = name if name else cls.__name__
		if sequences:
			if isinstance(sequences, Sequence): sequences = [sequences]
			for sequence in sequences:
				sequence.schema = cls.__schema__
		cls.__sequences__ = sequences
		if constraints:
			if isinstance(constraints, Constraint): constraints = [constraints]
		cls.__constraints__ = constraints
		if indexes:
			if isinstance(indexes, Index): indexes = [indexes]
		cls.__indexes__ = indexes
		return super().__init_subclass__(
			name=None,
			fn=fn,
			description=description,
		)
