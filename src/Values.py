# -*- coding: utf-8 -*-

from dataclasses import dataclass

__all__ = (
	'Point',
)

@dataclass
class Point(object):
	"""Point Class"""
	longitude: float
	latitude: float
	def __eq__(self, o: 'Point') -> bool:
		if self.longitude == o.longitude and self.latitude == o.latitude:
			return True
		return False
