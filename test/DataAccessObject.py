# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.PostgreSQL import Configuration, Connection
	

class TestDataAccessObject(Case):
	@classmethod
	def setUpClass(cls):
		Helper.Set(
			'Sample',
			Connection,
			Configuration(
				host='127.0.0.1',  # PostgreSQL Database Host Address
				port=5432,  # PostgreSQL Database Host Port
				database='postgres',  # Database Name
				username='postgres',  # Database User
				password='password',  # Database Password for User
				persistent=True,  # Is Persistent Connection, True/False
				min=1,
				max=100,
			)
		)
		return super().setUpClass()

	@Order(1)
	def testConnectClose(self):
		con = Helper.Get('Sample')
		ASSERT_IS_NOT_NONE(con)
		con.connect()
		con.close()
		return
	
	@Order(2)
	def testExecute(self):
		con = Helper.Get('Sample')
		ctx = con.execute('SELECT 1 AS col1')
		ASSERT_IS_NOT_NONE(ctx)
		rows = ctx.rows()
		ASSERT_IS_EQUAL(len(rows), 1)
		row = rows[0]
		ASSERT_IS_EQUAL(len(row), 1)
		ASSERT_IS_EQUAL(row['col1'], 1)
		return

	@Order(3)
	def testCursorExecute(self):
		con = Helper.Get('Sample')
		cur = con.cursor()
		ctx = cur.execute('SELECT 1 AS col1')
		ASSERT_IS_NOT_NONE(ctx)
		rows = ctx.rows()
		ASSERT_IS_EQUAL(len(rows), 1)
		row = rows[0]
		ASSERT_IS_EQUAL(len(row), 1)
		ASSERT_IS_EQUAL(row['col1'], 1)
		return

	@Order(3)
	def testSessionExecute(self):
		con = Helper.Get('Sample')
		ses = con.session()
		ctx = ses.execute('SELECT 1 AS col1')
		ASSERT_IS_NOT_NONE(ctx)
		rows = ctx.rows()
		ASSERT_IS_EQUAL(len(rows), 1)
		row = rows[0]
		ASSERT_IS_EQUAL(len(row), 1)
		ASSERT_IS_EQUAL(row['col1'], 1)
		return

