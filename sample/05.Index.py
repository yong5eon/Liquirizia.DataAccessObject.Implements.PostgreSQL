# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from Liquirizia.Utils import PrettyPrint

from datetime import datetime


class SampleTable(
	Table,
	name='SAMPLE',
	sequences=(
		Sequence('SEQ_SAMPLE', type=INT)
	),
	constraints=(
		PrimaryKey('PK_SAMPLE', cols=Column('ID')),
	),
	indexes=(
		Index('IDX_SAMPLE_COL_1', exprs=['COL_1']),
		Index('IDX_SAMPLE_COL_2', exprs=Column('COL_1')),
		# Index('IDX_SAMPLE_DATA', exprs=Column('DATA')),
		Index('IDX_SAMPLE_DATA_TARGET', exprs=Of(Of(Of('DATA', 'target'), 0), 'dest')),
		Index('IDX_SAMPLE_DATA_COL', exprs=Of('DATA', 'col'), using=IndexType.GeneralizedInvertedIndex),
	),
):
	id : int = INT('ID', default=NextVal('SEQ_SAMPLE'))
	col1: str = VARCHAR('COL_1', null=True)
	col2: str = VARCHAR('COL_2', null=True)
	data: str = JSONB('DATA', null=True)
	atCreated: datetime = TIMESTAMP('AT_CREATED', default=Now())


Helper.Set(
	'Sample',
	Connection,
	Configuration(
		host='127.0.0.1',  # PostgreSQL Database Host Address
		port=5432,  # PostgreSQL Database Host Port
		database='postgres',  # Database Name
		username='postgres',  # Database User
		password='password',  # Database Password for User
	)
)

con: Connection = Helper.Get('Sample')
con.begin()
con.run(Drop(SampleTable))
for sql, *args in Create(SampleTable):
	print(sql)
con.run(Create(SampleTable))


con.commit()

