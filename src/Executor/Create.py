# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model
from Liquirizia.DataAccessObject.Model import Executors

from ..Model import Type as ModelType, Index, Sequence
from ..Type import Object, Short, Integer, Long
from ..Constraint import PrimaryKey, ForeignKey, Unique, Check

from typing import Type

__all__ = (
	'Create'
)

class TypeToSQL(object):

	def encode(self, o: any):
		try:
			if isinstance(o, str): return '\'{}\''.format(o)
			return o
		except Exception as e:
			return o

	def __call__(self, attr: Object) -> str:
		return '{} {}{}{}'.format(
			attr.key,
			attr.type,
			' NOT NULL' if not attr.null else '',
			' DEFAULT {}'.format(self.encode(attr.default)) if attr.default is not None else '',
		)

class PrimaryKeyToSQL(object):
	def __call__(self, key: PrimaryKey) -> str:
		return 'CONSTRAINT {} PRIMARY KEY({})'.format(
			key.name,
			', '.join(key.cols)
		)

class ForeignKeyToSQL(object):
	def __call__(self, key: ForeignKey) -> str:
		return 'CONSTRAINT {} FOREIGN KEY({}) REFERENCES {}({})'.format(
			key.name,
			', '.join(key.cols),
			key.reference,
			', '.join(key.referenceCols)
		)
	

class UniqueToSQL(object):
	def __call__(self, key: Unique) -> str:
		return 'CONSTRAINT {} UNIQUE{}({})'.format(
			key.name,
			' NULLS NOT DISTINCT' if key.null else '',
			', '.join(key.cols),
		)


class CheckToSQL(object):
	def __call__(self, chk: Check) -> str:
		return 'CONSTRAINT {} CHECK({})'.format(
			chk.name,
			chk.expr,
		)
	

class SequenceToSQL(object):
	def __call__(self, seq: Sequence):
		return 'CREATE SEQUENCE {}{} AS {}{}{}{}'.format(
			'IF NOT EXISTS ' if seq.notexists else '',
			seq.name,
			seq.type,
			' INCREMENT BY {}'.format(seq.increment) if seq.increment else '',
			' MINVALUE {}'.format(seq.min) if seq.min else '',
			' MAXVALUE {}'.format(seq.max) if seq.max else '',
		)

class IndexToSQL(object):
	def __call__(self, index: Index) -> str:
		return 'CREATE INDEX {}{} ON {}({})'.format(
			'IF NOT EXISTS ' if index.notexists else '',
			index.name,
			index.table,
			', '.join(index.colexprs),
		)


class TableToSQL(object):

	TypeToSQL = TypeToSQL()
	PrimaryKeyToSQL = PrimaryKeyToSQL()
	ForeignKeyToSQL = ForeignKeyToSQL()
	UniqueToSQL = UniqueToSQL()
	CheckToSQL = CheckToSQL()
	SequenceToSQL = SequenceToSQL()
	IndexToSQL = IndexToSQL()

	def __call__(self, o: Type[Model], notexist) -> str:
		__ = []
		_ = []
		for k, v in o.__dict__.items():
			if isinstance(v, Object):
				_.append(self.TypeToSQL(v))
			if isinstance(v, (Short, Integer, Long)) and v.seq:
				__.append((self.SequenceToSQL(v.seq), ()))
		for constraint in o.__properties__['constraints'] if o.__properties__['constraints'] else []:
			if isinstance(constraint, PrimaryKey):
				_.append(self.PrimaryKeyToSQL(constraint))
				continue
			if isinstance(constraint, ForeignKey):
				_.append(self.ForeignKeyToSQL(constraint))
				continue
			if isinstance(constraint, Unique):
				_.append(self.UniqueToSQL(constraint))
				continue
			if isinstance(constraint, Check):
				_.append(self.CheckToSQL(constraint))
				continue
		__.append(('CREATE TABLE {}{}({})'.format(
			'IF NOT EXISTS ' if notexist else '',
			o.__properties__['name'],
			', '.join(_)
		), ()))
		for index in o.__properties__['indexes'] if o.__properties__['indexes'] else []:
			__.append((self.IndexToSQL(index), ()))
		return __
	

class ViewToSQL(object):
	def __call__(self, o: Type[Model], notexist) -> str:
		return [('CREATE {}VIEW {} AS {}'.format(
			'OR REPLACE ' if notexist else '',
			o.__properties__['name'],
			o.__properties__['executor'].query,
		), ())]


class Create(Executors):

	TableToSQL = TableToSQL()
	ViewToSQL = ViewToSQL()

	def __init__(self, o: Type[Model], notexist: bool = True):
		self.model = o
		self.executors = []
		fn = {
			ModelType.Table : Create.TableToSQL,
			ModelType.View  : Create.ViewToSQL,
		}.get(o.__properties__['type'], None)
		if fn:
			self.executors = fn(o, notexist)
		return
	
	def __iter__(self):
		return self.executors.__iter__()
	

