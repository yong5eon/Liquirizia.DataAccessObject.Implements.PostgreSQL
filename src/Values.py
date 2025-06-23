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
		if self.longitude.__eq__(o.longitude) and self.latitude.__eq__(o.latitude):
			return True
		return False
	def __ne__(self, o: 'Point') -> bool:
		if self.longitude.__ne__(o.longitude) or self.latitude.__ne__(o.latitude):
			return True
		return False

