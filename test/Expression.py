# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraints import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from datetime import datetime


class SampleModel(
	Table,
	name='SAMPLE',
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


class TestExpression(Case):
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
				pool=True,
				min=1,
				max=10,
			)
		)
		con = Helper.Get('Sample')
		con.begin()
		con.run(Drop(SampleModel))
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
		con.commit()
		return super().setUpClass()

	@classmethod
	def tearDownClass(cls):
		con = Helper.Get('Sample')
		con.begin()
		con.run(Drop(SampleModel))
		con.commit()
		return super().tearDownClass()

	@Order(1)
	def testAlias(self):
		con = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			Alias(SampleModel.name, 'NM')
		))
		con.commit()
		for row in rows:
			ASSERT_IS_EQUAL('NM' in row, True)
		return

	@Order(2)
	def testTypeTo(self):
		con = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			TypeTo(SampleModel.id, FLOAT)
		))
		con.commit()
		for row in rows:
			ASSERT_IS_EQUAL(isinstance(row['ID'], float), True)
		return

	@Order(3)
	def testIf(self):
		con = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).values(
			SampleModel.description,
			Alias(
				If(
					IsNotNull(
						SampleModel.description
					)
				).then_(Value('Y')).else_(Value('N')), 'STATUS'
			),
		))
		con.commit()
		for row in rows:
			if row['DESCRIPTION']:
				ASSERT_IS_EQUAL(row['STATUS'], 'Y')
			else:
				ASSERT_IS_EQUAL(row['STATUS'], 'N')
		return

	@Order(4)
	def testIn(self):
		con = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			In(SampleModel.name, (Value('A'), Value('B')))
		))
		con.commit()
		ASSERT_IS_EQUAL(len(rows), 2)
		return

	@Order(5)
	def testIsNull(self):
		con = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			IsNull(SampleModel.description)
		))
		con.commit()
		ASSERT_IS_EQUAL(len(rows), 2)
		return

	@Order(6)
	def testIsNotNull(self):
		con = Helper.Get('Sample')
		con.begin()
		rows = con.run(Select(SampleModel).where(
			IsNotNull(SampleModel.description)
		))
		con.commit()
		ASSERT_IS_EQUAL(len(rows), 1)
		return
