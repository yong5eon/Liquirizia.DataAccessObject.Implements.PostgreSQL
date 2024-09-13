# -*- coding: utf-8 -*-

from .Configuration import Configuration

from Liquirizia.Template import Singleton

from psycopg2.pool import ThreadedConnectionPool


__all__ = (
	'DatabaseAccessObjectPool'
)


class Pool(Singleton):

	def __init__(self):
		self.pool = {}
		return

	def __del__(self):
		for key in self.pool.keys():
			self.pool[key].closeall()

	@classmethod
	def Get(cls, conf: Configuration):
		pool = Pool()
		return pool.get(conf)

	def get(self, conf: Configuration):
		if conf not in self.pool:
			dsn = 'postgresql://'
			if conf.user:
				dsn += conf.user
				if conf.password:
					dsn += ':' + conf.password
				dsn += '@'
			dsn += '{}:{}/{}'.format(conf.host, conf.port, conf.database)
			self.pool[conf] = ThreadedConnectionPool(conf.min, conf.max, dsn)
		return self.pool[conf].getconn()

	@classmethod
	def Release(cls, conf: Configuration, connection):
		pool = Pool()
		return pool.release(conf, connection)

	def release(self, conf: Configuration, connection):
		if conf not in self.pool:
			return
		self.pool[conf].putconn(connection)
		return