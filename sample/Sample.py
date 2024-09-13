# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper, Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.PostgreSQL import Connection,Configuration 

import sys

if __name__ == '__main__':

	con = None

	try:
		# Set connection
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
				max=1,
			)
		)

		# Get Connection
		con = Helper.Get('Sample')
	except ConnectionError as e:
		print(str(e), file=sys.stderr)
		exit(-1)
	except Exception as e:
		print(str(e), file=sys.stderr)
		exit(-1)

	try:
		con.begin()

		con.execute('DROP TABLE IF EXISTS LOG')
		con.execute(
			'''
			CREATE TABLE IF NOT EXISTS LOG (
				ID SERIAL NOT NULL,
				TEXT TEXT NOT NULL,
				CREATED TIMESTAMP NOT NULL DEFAULT NOW(),
				CONSTRAINT PK_LOG PRIMARY KEY(ID)
			)
			'''
		)
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST1')")
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST2')")
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST3')")

		ctx = con.execute('SELECT * FROM LOG')
		rows = ctx.rows()

		for i, row in enumerate(rows):
			print('{} : {}'.format(i, row), file=sys.stdout)

		con.execute('DROP TABLE IF EXISTS LOG')
		con.commit()
	except ExecuteError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except CursorError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except ConnectionClosedError as e:
		print('Connection is closed, {}'.format(str(e)), file=sys.stderr)
	except Error as e:
		print('Error, {}'.format(str(e)), file=sys.stderr)
	except Exception as e:
		print(str(e), file=sys.stderr)
