# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper

from Liquirizia.DataAccessObject.Implements.PostgreSQL import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Types import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Constraints import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Functions import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Executors import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Filters import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Orders import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Joins import *
from Liquirizia.DataAccessObject.Implements.PostgreSQL.Exprs import *

from Liquirizia.Utils import PrettyPrint

class SampleTable(
	Table,
	name='SAMPLE',
	constraints=(
		PrimaryKey('PK_SAMPLE', cols='ID'),
	),
):
	id: int = INT('ID')
	col: str = VARCHAR('COL', size=256)

Helper.Set(
	'Sample',
	Connection,
	Configuration(
		host='127.0.0.1',  # PostgreSQL Database Host Address
		port=5432,  # PostgreSQL Database Host Port
		database='postgres',  # Database Name
		username='postgres',  # Database User
		password='password',  # Database Password for User
		pool=True,  # Is Use Connection Pool, True/False
		min=1, # Minimum Connections in Pool
		max=1, # Maximum Connections in Pool
	)
)

con = Helper.Get('Sample')

con.begin()

con.run(Drop(SampleTable))
con.run(Create(SampleTable))

_ = con.run(Insert(SampleTable).values(
	id=1,
	col='Hi',
))
PrettyPrint(_)

_ = con.run(Insert(SampleTable).values(
	id=2,
	col='Hello',
))
PrettyPrint(_)

_ = Insert(SampleTable).values(
	id=2,
	col='안녕',
).on(SampleTable.id).set(
	col='안녕하세요',
)
PrettyPrint(_.query)
PrettyPrint(_.args)
_ = con.run(_)
PrettyPrint(_)

con.run(Drop(SampleTable))
con.commit()
