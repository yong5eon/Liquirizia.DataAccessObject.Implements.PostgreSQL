# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Executors
from Liquirizia.DataModel import Model

from ..Schema import Schema
from ..Table import Table
from ..View import View
from ..Index import Index
from ..Sequence import Sequence
from ..Constraints import (
	PrimaryKey,
	ForeignKey,
	Unique,
	Check,
)

from ..Type import Type

from typing import Type  as T

__all__ = (
	'Create'
)

class ColumnToSQL(object):
	def __call__(self, col: Type) -> str:
		return '"{}" {}{}{}'.format(
			col.key,
			col.type,
			' NOT NULL' if not col.null else '',
			' DEFAULT {}'.format(col.typedefault) if col.typedefault is not None else '',
		)

class PrimaryKeyToSQL(object):
	def __call__(self, key: PrimaryKey) -> str:
		return 'CONSTRAINT "{}" PRIMARY KEY({})'.format(
			key.name,
			', '.join([str(col) for col in key.cols])
		)

class ForeignKeyToSQL(object):
	def __call__(self, key: ForeignKey) -> str:
		referenceSchema = None
		if issubclass(key.reference, Table):
			referenceSchema = key.reference.__schema__
		referenceTable = None
		if issubclass(key.reference, Table):
			referenceTable = key.reference.__table__
		else:
			referenceTable = key.reference
		return 'CONSTRAINT "{}" FOREIGN KEY({}) REFERENCES {}"{}"({})'.format(
			key.name,
			', '.join([str(col) for col in key.cols]),
			'"{}".'.format(str(referenceSchema)) if referenceSchema else '',
			referenceTable,
			', '.join(['"{}"'.format(col.key) if isinstance(col, Type) else str(col) for col in key.referenceCols])
		)
	

class UniqueToSQL(object):
	def __call__(self, key: Unique) -> str:
		return 'CONSTRAINT "{}" UNIQUE{}({})'.format(
			key.name,
			' NULLS NOT DISTINCT' if key.null else '',
			', '.join([str(col) for col in key.cols]),
		)


class CheckToSQL(object):
	def __call__(self, chk: Check) -> str:
		return 'CONSTRAINT "{}" CHECK({})'.format(
			chk.name,
			chk.expr,
		)
	

class SequenceToSQL(object):
	def __call__(self, seq: Sequence, schema: Schema = None) -> str:
		return 'CREATE SEQUENCE {}{}"{}" AS {}{}{}{}'.format(
			'IF NOT EXISTS ' if seq.notexists else '',
			'"{}".'.format(str(schema)) if schema else '',
			seq.name,
			seq.type,
			' INCREMENT BY {}'.format(seq.increment) if seq.increment else '',
			' MINVALUE {}'.format(seq.min) if seq.min else '',
			' MAXVALUE {}'.format(seq.max) if seq.max else '',
		)

class IndexToSQL(object):
	def __call__(self, o: T[Table], index: Index) -> str:
		return 'CREATE INDEX {}"{}" ON {}"{}" USING {} ({})'.format(
			'IF NOT EXISTS ' if index.notexists else '',
			index.name,
			'"{}".'.format(str(o.__schema__)) if o.__schema__ else '',
			o.__table__,
			index.using,
			', '.join(str(expr) for expr in index.exprs),
		)


class TableToSQL(object):
	ColumnToSQL = ColumnToSQL()
	PrimaryKeyToSQL = PrimaryKeyToSQL()
	ForeignKeyToSQL = ForeignKeyToSQL()
	UniqueToSQL = UniqueToSQL()
	CheckToSQL = CheckToSQL()
	SequenceToSQL = SequenceToSQL()
	IndexToSQL = IndexToSQL()

	def __call__(self, o: T[Table], notexist) -> str:
		__ = []
		_ = []
		for k, v in o.__mapper__.items():
			_.append(self.ColumnToSQL(v))
		for constraint in o.__constraints__ if o.__constraints__ else []:
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
		for sequence in o.__sequences__ if o.__sequences__ else []:
			__.append((self.SequenceToSQL(sequence, o.__schema__), ()))
			pass
		__.append(('CREATE TABLE {}{}"{}"({})'.format(
			'IF NOT EXISTS ' if notexist else '',
			'"{}".'.format(str(o.__schema__)) if o.__schema__ else '',
			o.__table__,
			', '.join(_)
		), ()))
		for index in o.__indexes__ if o.__indexes__ else []:
			__.append((self.IndexToSQL(o, index), ()))
		# TODO : CREATE COMMENT
		return __
	

class ViewToSQL(object):
	def __call__(self, o: T[View], notexist) -> str:
		return [('CREATE {}VIEW {}"{}" AS {}'.format(
			'OR REPLACE ' if notexist else '',
			'"{}".'.format(str(o.__schema__)) if o.__schema__ else '',	
			o.__view__,
			o.__executor__.query,
		), ())]


class Create(Executors):

	TableToSQL = TableToSQL()
	ViewToSQL = ViewToSQL()

	def __init__(self, o: T[Model], notexist: bool = True):
		self.model = o
		self.executors = []
		if issubclass(o, Table):
			self.executors = self.TableToSQL(o, notexist)
		if issubclass(o, View):
			self.executors = self.ViewToSQL(o, notexist)
		return
	
	def __iter__(self):
		return self.executors.__iter__()
