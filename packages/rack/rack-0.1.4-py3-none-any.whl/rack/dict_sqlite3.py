#!/usr/bin/env python
# SPDX-FileCopyrightText: 2024 Jérôme Carretero <cJ-rack@zougloub.eu> & contributors
# SPDX-License-Identifier: MIT

import os
import logging
import marshal
import typing as t

import sqlite3

from .utils import create_new_name


logger = logging.getLogger(__name__)


schema = """
CREATE TABLE IF NOT EXISTS dict (
 k BLOB PRIMARY KEY,
 v BLOB
) WITHOUT ROWID;
"""


class PersistentDict(t.Dict):
	"""
	Persistent dict using SQLite3 database as backend
	"""
	def __init__(self, name=None, serdes=None):
		self._name = name
		self._debug = False
		if serdes is None:
			self._loads = marshal.loads
			self._dumps = marshal.dumps
		else:
			self._loads, self._dumps = serdes

	def __enter__(self):
		self.conn = conn = sqlite3.connect(self._name + ".sqlite3")
		conn.executescript(schema)
		return self

	def __exit__(self, ext_type, exc_value, exc_tb):
		self.conn.close()


	def _set(self, cursor, key, value):
		k = self._dumps(key)
		v = self._dumps(value)
		query = "INSERT OR REPLACE INTO dict (k,v) VALUES (?,?)"
		args = (k,v)
		if self._debug:
			logger.debug("Insert %s=%s", key, value)
		cursor.execute(query, args)

	def __setitem__(self, key, value):
		cursor = self.conn.cursor()
		self._set(cursor, key, value)
		self.conn.commit()

	def __getitem__(self, key):
		cursor = self.conn.cursor()
		query = "SELECT v FROM dict where k = ?;"
		k = self._dumps(key)
		args = (k,)
		cursor.execute(query, args)
		res = cursor.fetchone()
		if res is None:
			raise KeyError(key)
		return self._loads(res[0])

	def __delitem__(self, key):
		k = self._dumps(key)
		cursor = self.conn.cursor()
		query = "SELECT v FROM dict where k = ?;"
		k = self._dumps(key)
		args = (k,)
		cursor.execute(query, args)
		res = cursor.fetchone()
		if res is None:
			raise KeyError(key)
		query = "DELETE FROM dict WHERE k = ?;"
		args = (k,)
		cursor.execute(query, args)
		self.conn.commit()

	def get(self, key, default=None):
		k = self._dumps(key)
		cursor = self.conn.cursor()
		query = "SELECT v FROM dict where k = ?;"
		k = self._dumps(key)
		args = (k,)
		cursor.execute(query, args)
		res = cursor.fetchone()
		if res is None:
			return default

		return self._loads(res[0])

	def clear(self):
		cursor = self.conn.cursor()
		query = "DELETE FROM dict WHERE 1;"
		args = ()
		cursor.execute(query, args)
		self.conn.commit()

	def update(self, other=None, **kw):
		cursor = self.conn.cursor()
		if other:
			for k, v in other.items():
				self._set(cursor, k, v)

		for k, v in kw.items():
			self._set(cursor, k, v)
		self.conn.commit()

	def __contains__(self, key):
		k = self._dumps(key)
		cursor = self.conn.cursor()
		query = "SELECT COUNT(*) FROM dict WHERE k = ?;"
		args = (k,)
		cursor.execute(query, args)
		res = cursor.fetchone()
		#logger.info("res: %s", res)
		return res[0] == 1

	def __len__(self):
		"""
		:return: number of items in dict
		"""
		cursor = self.conn.cursor()
		query = "SELECT COUNT(*) FROM dict WHERE 1;"
		args = ()
		cursor.execute(query, args)
		return cursor.fetchone()[0]

	def keys(self):
		cursor = self.conn.cursor()
		query = "SELECT k FROM dict WHERE 1;"
		args = ()
		for row in cursor.execute(query, args):
			yield self._loads(row[0])

	def values(self):
		cursor = self.conn.cursor()
		query = "SELECT v FROM dict WHERE 1;"
		args = ()
		for row in cursor.execute(query, args):
			yield self._loads(row[0])

	def items(self):
		cursor = self.conn.cursor()
		query = "SELECT k, v FROM dict WHERE 1;"
		args = ()
		for row in cursor.execute(query, args):
			k, v = row
			yield self._loads(k), self._loads(v)

	def __iter__(self):
		yield from self.keys()

	def popitem(self):
		cursor = self.conn.cursor()
		query = "SELECT k, v FROM dict WHERE 1 LIMIT 1;"
		args = ()
		cursor.execute(query, args)
		cnt = cursor.fetchone()
		if cnt is None:
			raise KeyError(key)
		res = self._loads(cnt[0]), self._loads(cnt[1])
		query = "DELETE FROM dict WHERE k = ?;"
		args = (cnt[0],)
		cursor.execute(query, args)
		self.conn.commit()
		return res

	def pop(self, key):
		k = self._dumps(key)
		cursor = self.conn.cursor()
		query = "SELECT v FROM dict WHERE k = ?;"
		args = (k,)
		cursor.execute(query, args)
		cnt = cursor.fetchone()
		if cnt is None:
			raise KeyError(key)
		res = self._loads(cnt[0])
		query = "DELETE FROM dict WHERE k = ?;"
		args = (k,)
		cursor.execute(query, args)
		self.conn.commit()
		return res

	def setdefault(self, key, value=None):
		k = self._dumps(key)
		cursor = self.conn.cursor()
		query = "SELECT v FROM dict WHERE k = ?;"
		args = (k,)
		cursor.execute(query, args)
		cnt = cursor.fetchone()
		if cnt is None:
			self._set(cursor, key, value)
			self.conn.commit()
			return value
		return self._loads(cnt[0])

	def copy(self, name: str=None):
		if name is None:
			name = create_new_name(self._name)
		with PersistentDict(name=name) as new:
			new.update(self)
		return new

	@classmethod
	def fromkeys(cls, keys: t.Iterable, value=None, name: str=None):
		if name is None:
			name = create_new_name()
		with PersistentDict(name=name) as new:
			cursor = new.conn.cursor()
			for key in keys:
				new._set(cursor, key, value)
			new.conn.commit()
		return new
