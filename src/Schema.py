# -*- coding: utf-8 -*-

__all__ = (
	'Schema'
)


class Schema(object):
	def __init__(
		self, 
		name: str,
		username: str = None,
	):
		self.name = name
		self.username = username
		return
	
	def __str__(self):
		return self.name
