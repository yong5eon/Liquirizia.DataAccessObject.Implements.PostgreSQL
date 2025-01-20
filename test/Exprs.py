# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraints import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Filters import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors.Exprs import *

from datetime import datetime


class SampleModel(
	Table,
	table='SAMPLE',
	sequences=(
		Sequence(name='SEQ_SAMPLE', type=INT),
	),
	constraints=(
		PrimaryKey(name='PK_SAMPLE', cols='ID'),
	),
	indexes=(),
):
	id: int = INT(name='ID', default=NextVal('SEQ_SAMPLE'))
	name: str = VARCHAR(name='NAME')
	description: str = VARCHAR(name='DESCRIPTION', null=True)
  atCreated: datetime = TIMESTAMP(name='AT_CREATED')


class TestExprs(Case):
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
		con = Helper.Get('Sample')
		con.run(Create(SampleModel))
		con.run(Insert(SampleModel).values(
			name='A',
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='B',
			description='This is B',
			atCreated=datetime.now(),
		))
		con.run(Insert(SampleModel).values(
			name='C',
			atCreated=datetime.now(),
		))
		return super().setUpClass()

	@classmethod
	def tearDownClass(cls):
		con = Helper.Get('Sample')
		con.run(Drop(SampleModel))
		return super().tearDownClass()

	@Order(1)
	def testAlias(self):
		con = Helper.Get('Sample')
		rows = con.run(Select(SampleModel).values(
			Alias(SampleModel.name, 'NM')
		))
		for row in rows:
			ASSERT_IS_TRUE('nm' in row)
		return

	@Order(2)
	def testTypeTo(self):
		con = Helper.Get('Sample')
		rows = con.run(Select(SampleModel).values(
			TypeTo(SampleModel.id, FLOAT)
		))
		for row in rows:
			ASSERT_IS_TRUE(isinstance(row['id'], float))
		return

	@Order(3)
	def testIf(self):
		con = Helper.Get('Sample')
		rows = con.run(Select(SampleModel).values(
			SampleModel.description,
			Alias(If(IsNotNull(SampleModel.description)).then('Y').else('N'), 'STATUS'),
		))
		for row in rows:
			if row['description']:
				ASSERT_IS_EQUAL(row['status'], 'Y')
			else:
				ASSERT_IS_EQUAL(row['status'], 'N')
		return

	@Order(4)
	def testIn(self):
		con = Helper.Get('Sample')
		rows = con.run(Select(SampleModel).where(
			In(SampleModel.name, ('A', 'B'))
		))
		ASSERT_IS_EQUAL(len(rows), 2)
		return

	@Order(5)
	def testIsNull(self):
		con = Helper.Get('Sample')
		rows = con.run(Select(SampleModel).where(
			IsNull(SampleModel.description)
		))
		ASSERT_IS_EQUAL(len(rows), 2)
		return

	@Order(6)
	def testIsNotNull(self):
		con = Helper.Get('Sample')
		rows = con.run(Select(SampleModel).where(
			IsNotNull(SampleModel.description)
		))
		ASSERT_IS_EQUAL(len(rows), 1)
		return

