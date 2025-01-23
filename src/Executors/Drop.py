# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Executors

from ..Table import Table
from ..View import View

from typing import Union

__all__ = (
	'Drop'
)


class Drop(Executors):
	def __init__(self, o: Union[Table, View], exist: bool = True, cascade=False):
		self.executors = []
		if issubclass(o, Table):
			for index in o.__indexes__ if o.__indexes__ else []:
				self.executors.append(('DROP INDEX {}{}"{}"{}'.format(
					'IF EXISTS ' if exist else '',
					'"{}".'.format(o.__schema__) if o.__schema__ else '',
					index.name,
					' CASCADE' if cascade else ' RESTRICT'
				), ()))
			for constraint in o.__constraints__ if o.__constraints__ else []:
				self.executors.append(('ALTER TABLE {}{}"{}" DROP CONSTRAINT {}"{}"{}'.format(
					'IF EXISTS ' if exist else '',
					'"{}".'.format(o.__schema__) if o.__schema__ else '',
					o.__table__,
					'IF EXISTS ' if exist else '',
					constraint.name,
					' CASCADE' if cascade else ' RESTRICT'
				), ()))
			self.executors.append(('DROP TABLE {}{}"{}"{}'.format(
				'IF EXISTS ' if exist else '',
				'"{}".'.format(o.__schema__) if o.__schema__ else '',
				o.__table__,
				' CASCADE' if cascade else ' RESTRICT'
			), ()))
			for sequence in o.__sequences__ if o.__sequences__ else []:
				self.executors.append(('DROP SEQUENCE {}{}"{}"{}'.format(
					'IF EXISTS ' if exist else '',
					'"{}".'.format(o.__schema__) if o.__schema__ else '',
					sequence.name,
					' CASCADE' if cascade else ' RESTRICT'
				), ()))
		if issubclass(o, View):
			self.executors.append(('DROP VIEW {}{}"{}"{}'.format(
				'IF EXISTS ' if exist else '',
				'"{}".'.format(o.__schema__) if o.__schema__ else '',
				o.__view__,
				' CASCADE' if cascade else ' RESTRICT'
			), ()))
		return
	
	def __iter__(self):
		return self.executors.__iter__()
