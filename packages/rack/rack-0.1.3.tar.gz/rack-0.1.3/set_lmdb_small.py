#!/usr/bin/env python
# SPDX-FileCopyrightText: 2019,2024 Jérôme Carretero <cJ-rack@zougloub.eu> & contributors
# SPDX-License-Identifier: MIT

import logging
import marshal
import typing as t

import lmdb

from .utils import create_new_name, h


logger = logging.getLogger(__name__)


class PersistentSet(t.Set):
	"""
	Persistent set using LMDB database as backend
	"""
	def __init__(self, name: str=None, hasher=None, serdes=None):
		"""
		:param name: Name of the db
		:param serdes: Pluggable serializer
		"""
		self._name = name
		if hasher is None:
			hasher = h
		self._h = hasher
		if serdes is None:
			self._loads = marshal.loads
			self._dumps = marshal.dumps
		else:
			self._loads, self._dumps = serdes

	def __enter__(self):
		self._env = env = lmdb.open(self._name + ".lmdb",
		 subdir=False,
		 max_dbs=3,
		 sync=False,
		 map_size=(50<<30),
		)

		self.db = env.open_db(
		 key=b"12",
		 dupsort=True,
		 create=True
		)


		return self

	def __exit__(self, exc_type, exc_value, exc_tb):
		self._env.close()

	def __len__(self):
		"""
		:return: number of items in set
		"""
		env = self._env
		with env.begin() as txn:
			s = txn.stat(db=self.db)
			entries = s["entries"]
			return entries

	def __iter__(self):
		with self._env.begin() as txn:
			with txn.cursor(db=self.db) as cur:
				for n, v in cur:
					yield self._loads(v)

	def __contains__(self, value):
		with self._env.begin() as txn:
			return self._contains(value, txn)

	def _contains(self, value, txn):
		v = self._dumps(value)
		k = self._h(v)
		with txn.cursor(db=self.db) as cur:
			return cur.set_key_dup(k, v)

	def _put(self, value, txn):
		v = self._dumps(value)
		k = self._h(v)
		txn.put(k, v, db=self.db)

	def _delete(self, key, value, txn):
		return txn.delete(key, value, db=self.db)

	def add(self, value: t.Any) -> None:
		with self._env.begin(write=True) as txn:
			self._put(value, txn)

	def update(self, other: t.Set) -> None:
		with self._env.begin(write=True) as txn:
			for value in other:
				self._put(value, txn)

	def remove(self, value: t.Any) -> None:
		v = self._dumps(value)
		k = self._h(v)
		with self._env.begin(write=True) as txn:
			res = self._delete(k, v, txn)
			if res:
				return
			raise KeyError()

	def discard(self, value: t.Any) -> None:
		v = self._dumps(value)
		k = self._h(v)
		with self._env.begin(write=True) as txn:
			self._delete(k, v, txn)

	def pop(self) -> t.Any:
		with self._env.begin(write=True) as txn:
			with txn.cursor(db=self.db) as cur:
				if not cur.last():
					return KeyError()
				if not cur.last_dup():
					return KeyError()
				v = cur.value()
				cur.delete()
				return self._loads(v)

	def clear(self) -> None:
		with self._env.begin(write=True) as txn:
			txn.drop(delete=False, db=self.db)

	def union(self, *others: t.Iterable, name: str=None) -> "PersistentSet":
		new_name = name
		if name is None:
			new_name = create_new_name(self._name)
		self._env.copy(path=new_name+".lmdb", compact=True)
		with PersistentSet(new_name) as new:
			for x in others:
				new.update(x)
		return new

	def intersection(self, *others: t.Iterable, name: str=None) -> "PersistentSet":
		"""Returns new set with elements common to the set and all others.

		:param others: Other sets.
		:param name: Optional name of the returned set.
		"""
		new_name = name
		if name is None:
			new_name = create_new_name(self._name)
		with PersistentSet(new_name) as new:
			with new._env.begin(write=True) as new_txn:
				for elem in self:
					for s in others:
						if elem in s:
							new._put(elem, new_txn)
						else:
							break
			return new

	def difference(self, *others: t.Iterable[t.Set], name: str=None) -> "PersistentSet":
		new_name = name
		if name is None:
			new_name = create_new_name(self._name)
		with PersistentSet(new_name) as new:
			with new._env.begin(write=True) as new_txn:
				for elem in self:
					for s in others:
						if elem not in s:
							new._put(elem, new_txn)
		return new

	def symmetric_difference(self, other: t.Set, name: str=None):
		new_name = name
		if name is None:
			new_name = create_new_name(self._name)
		with PersistentSet(name=new_name) as new:
			with new._env.begin(write=True) as txn:
				for x in self:
					if x not in other:
						new._put(x, txn)
				for x in other:
					if x not in self:
						new._put(x, txn)
		return new

	def symmetric_difference_update(self, other: t.Set):
		with self._env.begin(write=True) as txn:
			for x in other:
				if x in self:
					v = self._dumps(x)
					k = self._h(v)
					self._delete(k, v, txn)
				else:
					self._put(x, txn)

	def isdisjoint(self, other: t.Set) -> bool:
		# not sure it's a good idea to create new set just for this,
		# but this is how it works in python
		x = self.intersection(other)
		with x as s:
			return len(s) == 0

	def issuperset(self, other: t.Set) -> bool:
		with self._env.begin() as txn:
			for elem in other:
				res = self._contains(elem, txn)
				if not res:
					return False
		return True

	def issubset(self, other: t.Set) -> bool:
		with self._env.begin() as txn:
			for elem in self:
				res = elem in other
				if not res:
					return False
		return True
