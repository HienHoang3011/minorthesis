#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
from contextlib import contextmanager
from typing import List

class SQLiteTransactionManager(object):
	def __init__(self, db_path: str = 'northfield.db'):
		self._db_path = db_path

	@contextmanager
	def transaction(self):
		conn = sqlite3.connect(self._db_path)
		conn.row_factory = sqlite3.Row
		conn.execute('PRAGMA foreign_keys = ON')
		try:
			yield conn
			conn.commit()
		except Exception:
			conn.rollback()
			raise
		finally:
			conn.close()

	def connection(self):
		conn = sqlite3.connect(self._db_path)
		conn.row_factory = sqlite3.Row
		conn.execute('PRAGMA foreign_keys = ON')
		return conn
