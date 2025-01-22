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


if __name__ == '__main__':
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

	# ALIAS
	rows = con.run(Select(SampleModel).values(
		Alias(SampleModel.name, 'NM')
	))
	for row in rows:
		print(row)

	# CAST
	rows = con.run(Select(SampleModel).values(
		TypeTo(SampleModel.id, FLOAT)
	))
	for row in rows:
		print(row)

	# IF THEN ELSE
	rows = con.run(Select(SampleModel).values(
		SampleModel.description,
		Alias(
			If(
				IsNotNull(
					SampleModel.description
				)
			).then(Value('Y')).els(Value('N')), 'STATUS'
		),
	))
	for row in rows:
		print(row)

	# IN
	rows = con.run(Select(SampleModel).where(
		In(SampleModel.name, ('A', 'B'))
	))
	for row in rows:
		print(row)

	# IS NULL
	rows = con.run(Select(SampleModel).where(
		IsNull(SampleModel.description)
	))
	for row in rows:
		print(row)

	# IS NOT NULL
	rows = con.run(Select(SampleModel).where(
		IsNotNull(SampleModel.description)
	))
	for row in rows:
		print(row)

	con.run(Drop(SampleModel))
