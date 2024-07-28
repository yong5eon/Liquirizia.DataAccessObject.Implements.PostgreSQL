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
				host='YOUR_POSTGRESQL_HOST',  # PostgreSQL Database Host Address
				port=5432,  # PostgreSQL Database Host Port
				database='YOUR_DATABASE',  # Database Name
				username='YOUR_USER',  # Database User
				password='YOUR_PASSWORD',  # Database Password for User
				persistent=True,  # Is Persistent Connection, True/False
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

		con.commit()
	except ExecuteError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except CursorError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except CommitError as e:
		print(str(e), file=sys.stderr)
	except RollBackError as e:
		print(str(e), file=sys.stderr)
	except ConnectionClosedError as e:
		print('Connection is closed, {}'.format(str(e)), file=sys.stderr)
	except Error as e:
		print('Error, {}'.format(str(e)), file=sys.stderr)
	except Exception as e:
		print(str(e), file=sys.stderr)

	try:
		con.execute('SELECT * FROM LOG')

		rows = con.rows()

		for i, row in enumerate(rows):
			print('{} : {}'.format(i, row), file=sys.stdout)

		con.execute('DROP TABLE IF EXISTS LOG')
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
