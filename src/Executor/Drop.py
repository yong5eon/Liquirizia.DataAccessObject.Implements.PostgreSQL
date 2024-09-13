# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executors
from Liquirizia.DataModel import Model

from ..Model import Type
from ..Type import Short, Integer, Long

__all__ = (
	'Drop'
)


class Drop(Executors):
	def __init__(self, o: type[Model], exist: bool = True, cascade=False):
		self.executors = []
		if o.__properties__['type'] == Type.Table:
			for index in o.__properties__['indexes'] if o.__properties__['indexes'] else []:
				self.executors.append(('DROP INDEX {}{}{}'.format(
					'IF EXISTS ' if exist else '',
					index.name,
					' CASCADE' if cascade else ' RESTRICT'
				), ()))
			for constraint in o.__properties__['constraints'] if o.__properties__['constraints'] else []:
				self.executors.append(('ALTER TABLE {}{} DROP CONSTRAINT {}{}{}'.format(
					'IF EXISTS ' if exist else '',
					constraint.table,
					'IF EXISTS ' if exist else '',
					constraint.name,
					' CASCADE' if cascade else ' RESTRICT'
				), ()))
			self.executors.append(('DROP TABLE {}{}{}'.format(
				'IF EXISTS ' if exist else '',
				o.__properties__['name'],
				' CASCADE' if cascade else ' RESTRICT'
			), ()))
			for k, v in o.__dict__.items():
				if isinstance(v, (Short, Integer, Long)) and v.seq:
					self.executors.append(('DROP SEQUENCE {}{}{}'.format(
						'IF EXISTS ' if exist else '',
						v.seq.name,
						' CASCADE' if cascade else ' RESTRICT'
					), ()))
		if o.__properties__['type'] == Type.View:
			self.executors.append(('DROP VIEW {}{}{}'.format(
				'IF EXISTS ' if exist else '',
				o.__properties__['name'],
				' CASCADE' if cascade else ' RESTRICT'
			), ()))
		return
	
	def __iter__(self):
		return self.executors.__iter__()

