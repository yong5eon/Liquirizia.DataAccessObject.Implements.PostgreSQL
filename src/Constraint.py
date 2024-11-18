# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

__all__ = (
	'Constraint'
)


class Constraint(metaclass=ABCMeta):
	def __init__(
		self,
		name: str
	):
		self.name = name
		self.table = None
		return
