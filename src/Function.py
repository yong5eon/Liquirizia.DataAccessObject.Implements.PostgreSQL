# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

__all__ = (
	'Function'
)


class Function(metaclass=ABCMeta):
	"""Function Interface"""
	@abstractmethod
	def __str__(self):
		raise NotImplementedError('{} must be implemented __str__'.format(self.__class__.__name__))