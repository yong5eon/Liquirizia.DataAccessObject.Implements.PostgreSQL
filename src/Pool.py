# -*- coding: utf-8 -*-

from .Configuration import Configuration

from Liquirizia.Template import Singleton

from psycopg_pool import ConnectionPool
from psycopg import (
	Cursor,
	ClientCursor,
	ServerCursor,
)
from psycopg.rows import dict_row


__all__ = (
	'DatabaseAccessObjectPool'
)


class Pool(Singleton):

	def __init__(self):
		self.pool = {}
		return

	def __del__(self):
		for key in self.pool.keys():
			self.pool[key].close()

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
			self.pool[conf] = ConnectionPool(
				conninfo=dsn,
				min_size=conf.min,
				max_size=conf.max,
				kwargs={
					'autocommit': conf.autocommit,
					'cursor_factory': ClientCursor,
					'row_factory': dict_row,
				}
			)
		return self.pool[conf].getconn()

	@classmethod
	def Release(cls, conf: Configuration, connection):
		pool = Pool()
		return pool.release(conf, connection)

	def release(self, conf: Configuration, connection):
		try:
			self.pool[conf].putconn(connection)
		except Exception as e:
			pass
		return
